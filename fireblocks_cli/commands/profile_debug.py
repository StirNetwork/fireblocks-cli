# SPDX-FileCopyrightText: 2025 Ethersecurity Inc.
#
# SPDX-License-Identifier: MPL-2.0
# Author: Shohei KAMON <cameong@stir.network>

import typer
from fireblocks_cli.utils.profile import load_profile
from fireblocks_sdk import FireblocksSDK
from fireblocks_cli.auth.file_provider import FileAuthProvider
from fireblocks_cli.types.profile_config import ApiProfile, SecretKeyConfig


app = typer.Typer()


@app.command("debug")
def profile_debug(profile_name: str = typer.Option("default", "--profile", "-p")):
    """Check if the selected profile works with Fireblocks SDK."""

    raw_profile = load_profile(profile_name)
    profile_obj = ApiProfile(
        profile_name=profile_name,
        api_id=raw_profile["api_id"],
        api_secret_key=SecretKeyConfig(**raw_profile["api_secret_key"]),
    )
    provider = FileAuthProvider(profile_obj)

    api_id = provider.get_api_id()
    secret_key = provider.get_secret_key()

    fireblocks = FireblocksSDK(secret_key, api_id)

    try:
        accounts = fireblocks.get_vault_account(vault_account_id=1)

        typer.secho(
            f"✅ Successfully accessed Fireblocks API with profile '{profile_name}'",
            fg=typer.colors.GREEN,
        )
        typer.echo(f"Vault info: {accounts}")
    except Exception as e:
        typer.secho(f"❌ Error accessing Fireblocks API: {e}", fg=typer.colors.RED)
