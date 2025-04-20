# SPDX-FileCopyrightText: 2025 Ethersecurity Inc.
#
# SPDX-License-Identifier: MPL-2.0
# Author: Shohei KAMON <cameong@stir.network>

import typer
from fireblocks_cli.utils.profile import load_profile
from fireblocks_sdk import FireblocksSDK

app = typer.Typer()


@app.command("debug")
def profile_debug(profile: str = typer.Option("default", "--profile", "-p")):
    """Check if the selected profile works with Fireblocks SDK."""
    config = load_profile(profile)

    api_key_path = config["api_key_file"]
    secret_key_path = config["secret_key_file"]

    with open(api_key_path, "r") as f:
        api_key = f.read().strip()
    with open(secret_key_path, "r") as f:
        secret_key = f.read().strip()

    sdk = FireblocksSDK(secret_key, api_key)

    try:
        vaults = sdk.get_vault_accounts(limit=1)
        typer.secho(
            f"✅ Successfully accessed Fireblocks API with profile '{profile}'",
            fg=typer.colors.GREEN,
        )
        typer.echo(f"Vault example: {vaults[0]['name']}")
    except Exception as e:
        typer.secho(f"❌ Error accessing Fireblocks API: {e}", fg=typer.colors.RED)
