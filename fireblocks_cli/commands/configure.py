# SPDX-FileCopyrightText: 2025 Ethersecurity Inc.
#
# SPDX-License-Identifier: MPL-2.0

# Author: Shohei KAMON <cameong@stir.network>

import typer
from pathlib import Path
from fireblocks_cli.crypto import generate_key_and_csr
from fireblocks_cli.config import (
    CONFIG_DIR,
    CONFIG_FILE,
    CREDENTIALS_FILE,
    DEFAULT_CONFIG,
)
from fireblocks_cli.utils.toml import save_toml

configure_app = typer.Typer()


@configure_app.command("init")
def init():
    """Initialize configuration files and key directories."""
    typer.secho("🛠 Starting Fireblocks CLI initialization...", fg=typer.colors.CYAN)

    # Create the config directory if it doesn't exist
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    typer.secho(f"✅ Config directory ensured: {CONFIG_DIR}", fg=typer.colors.GREEN)

    # Create config.toml if it does not exist
    if not CONFIG_FILE.exists():
        config = DEFAULT_CONFIG.copy()

        # If credentials file exists, use its values to populate config
        if CREDENTIALS_FILE.exists():
            lines = CREDENTIALS_FILE.read_text().splitlines()
            for line in lines:
                if "api_id" in line:
                    config["default"]["api_id"] = line.split("=")[-1].strip()
                elif "api_secret_key" in line:
                    config["default"]["api_secret_key"] = line.split("=")[-1].strip()
            typer.secho(
                f"✅ Loaded credentials from: {CREDENTIALS_FILE}",
                fg=typer.colors.YELLOW,
            )

        # Save the populated config to file
        save_toml(config, CONFIG_FILE)
        typer.secho(f"✅ Created config.toml: {CONFIG_FILE}", fg=typer.colors.GREEN)
    else:
        typer.secho(
            f"⚠ config.toml already exists: {CONFIG_FILE}", fg=typer.colors.YELLOW
        )

    # Ensure ~/.fireblocks/keys directory exists
    keys_dir = Path("~/.fireblocks/keys").expanduser()
    keys_dir.mkdir(parents=True, exist_ok=True)
    typer.secho(f"📁 Keys directory ensured: {keys_dir}", fg=typer.colors.GREEN)

    typer.secho("🎉 Initialization complete!", fg=typer.colors.CYAN)


@configure_app.command("gen-keys")
def gen_keys():
    """秘密鍵とCSRを ~/.fireblocks/keys に生成します"""
    org = typer.prompt("🔐 組織名を入力してください（例: MyCompany）").strip()
    if not org:
        typer.secho("❌ 組織名は必須です。処理を中止します。", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    key_path, csr_path = generate_key_and_csr(org)
    typer.secho(f"✅ 秘密鍵: {key_path}", fg=typer.colors.GREEN)
    typer.secho(f"✅ CSR   : {csr_path}", fg=typer.colors.GREEN)
