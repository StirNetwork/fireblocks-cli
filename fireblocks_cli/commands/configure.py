# SPDX-FileCopyrightText: 2025 Ethersecurity Inc.
#
# SPDX-License-Identifier: MPL-2.0

# Author: Shohei KAMON <cameong@stir.network>

import typer
from pathlib import Path
from fireblocks_cli.crypto import generate_key_and_csr
from fireblocks_cli.utils.profile import (
    get_config_dir,
    get_config_file,
    get_api_key_dir,
    get_credentials_file,
    DEFAULT_CONFIG,
    get_profiles,
    ProfileLoadError,
)
from fireblocks_cli.utils.toml import save_toml
from tomlkit import document, table, inline_table, dumps


configure_app = typer.Typer()


@configure_app.command("init")
def init():
    """Initialize configuration files and key directories."""
    typer.secho("🛠 Starting Fireblocks CLI initialization...", fg=typer.colors.CYAN)

    # Create the config directory if it doesn't exist
    config_dir = get_config_dir()
    config_dir.mkdir(parents=True, exist_ok=True)
    typer.secho(f"✅ Config directory ensured: {config_dir}", fg=typer.colors.GREEN)

    # Create config.toml if it does not exist
    config_file = get_config_file()
    if not config_file.exists():
        doc = document()

        # [default]
        default_section = table()
        default_section.add("api_id", "get-api_id-from-fireblocks-dashboard")

        secret_table = inline_table()
        secret_table.add("type", "file")
        secret_table.add("value", "~/.config/fireblocks-cli/keys/abcd.key")
        secret_table.trailing_comma = True  # ← インライン整形のオプション（任意）
        default_section.add("api_secret_key", secret_table)

        doc.add("default", default_section)
        with config_file.open("w", encoding="utf-8") as f:
            f.write(dumps(doc))
    else:
        typer.secho(
            f"✅ config.toml already exists: {config_file}", fg=typer.colors.YELLOW
        )

    # Ensure ~/.config/fireblocks-cli/keys directory exists
    api_key_dir = get_api_key_dir()
    api_key_dir.mkdir(parents=True, exist_ok=True)
    typer.secho(f"✅ Keys directory ensured: {api_key_dir}", fg=typer.colors.GREEN)

    typer.secho("🎉 Initialization complete!", fg=typer.colors.CYAN)


@configure_app.command("gen-keys")
def gen_keys():
    """秘密鍵とCSRを api_key_dir に生成します"""
    org = typer.prompt("🔐 組織名を入力してください（例: MyCompany）").strip()
    if not org:
        typer.secho("❌ 組織名は必須です。処理を中止します。", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    key_path, csr_path = generate_key_and_csr(org)
    typer.secho(f"✅ 秘密鍵: {key_path}", fg=typer.colors.GREEN)
    typer.secho(f"✅ CSR   : {csr_path}", fg=typer.colors.GREEN)


@configure_app.command("validate")
def validate():
    """
    Validate the format of config.toml and credentials files.
    """
    from fireblocks_cli.utils.profile import get_config_file, get_credentials_file
    import toml
    from pathlib import Path

    profiles_by_file = {}

    def validate_file(path: Path):
        if not path.exists():
            typer.echo(f"⚠️ {path} not found. Skipping.")
            return {}

        try:
            data = toml.load(path)
        except Exception as e:
            typer.secho(f"❌ Failed to parse {path}: {e}", fg=typer.colors.RED)
            raise typer.Exit(code=1)

        for profile, values in data.items():
            if not isinstance(values, dict):
                typer.secho(f"❌ [{profile}] is not a table", fg=typer.colors.RED)
                raise typer.Exit(code=1)

            if "api_id" not in values or "api_secret_key" not in values:
                typer.secho(
                    f"❌ [{profile}] missing required keys", fg=typer.colors.RED
                )
                raise typer.Exit(code=1)

            secret = values["api_secret_key"]
            if (
                not isinstance(secret, dict)
                or "type" not in secret
                or "value" not in secret
            ):
                typer.secho(
                    f"❌ [{profile}] api_secret_key must be a dict with 'type' and 'value'",
                    fg=typer.colors.RED,
                )
                raise typer.Exit(code=1)

            if secret["type"] not in ("file", "vault"):
                typer.secho(
                    f"❌ [{profile}] api_secret_key.type must be either 'file' or 'vault' (got '{secret['type']}')",
                    fg=typer.colors.RED,
                )
                raise typer.Exit(code=1)

        typer.secho(f"✅ {path} is valid.", fg=typer.colors.GREEN)
        return set(data.keys())

    config_profiles = validate_file(get_config_file())
    credentials_profiles = validate_file(get_credentials_file())

    if "default" in config_profiles and "default" in credentials_profiles:
        typer.secho(
            "⚠️ Both config.toml and credentials contain [default] profile. "
            "This may cause unexpected behavior.",
            fg=typer.colors.YELLOW,
        )


@configure_app.command("edit")
def edit():
    """
    Open the config.toml file in your default editor ($EDITOR).
    """
    import os
    import subprocess
    from fireblocks_cli.utils.profile import get_config_file

    config_path = get_config_file()

    if not config_path.exists():
        typer.secho(f"❌ Config file not found: {config_path}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    editor = os.environ.get("EDITOR")

    if not editor:
        # Fallbacks
        for fallback in ["code", "nano", "vi"]:
            if shutil.which(fallback):
                editor = fallback
                break

    if not editor:
        typer.secho(
            "❌ No editor found. Please set the $EDITOR environment variable.",
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=1)

    try:
        subprocess.run([editor, str(config_path)])
    except Exception as e:
        typer.secho(f"❌ Failed to open editor: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)
        # Validate after editing
    typer.echo("\n🔍 Validating config.toml after editing...\n")
    try:
        from fireblocks_cli.commands.configure import validate

        validate()
    except Exception as e:
        typer.secho(f"❌ Validation failed: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)


@configure_app.command("list")
def list_profiles():
    """
    List available profiles from config.toml and credentials (if present).
    Profiles in credentials override those in config.toml.
    """

    profiles = {}

    try:
        profiles = get_profiles()
    except ProfileLoadError as e:
        typer.secho(f"❌ {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    if not profiles:
        typer.echo("⚠️ No profiles found in config.toml or credentials.")
        return

    typer.echo("📜 Available Profiles:\n")
    for name, values in profiles.items():
        api_id = values.get("api_id", "<missing>")
        secret_type = values.get("api_secret_key", {}).get("type", "<unknown>")
        typer.echo(
            f"🔹 [{name}]\n    api_id: {api_id}\n    secret_type: {secret_type}\n"
        )
