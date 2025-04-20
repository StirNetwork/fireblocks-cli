# SPDX-FileCopyrightText: 2025 Ethersecurity Inc.
#
# SPDX-License-Identifier: MPL-2.0
# Author: Shohei KAMON <cameong@stir.network>

import toml
from fireblocks_cli.auth.file_provider import FileAuthProvider
from fireblocks_cli.types.profile_config import ApiProfile, SecretKeyConfig
from fireblocks_cli.utils.profile import load_profile


def get_auth_provider(profile_name: str = "default"):
    config = load_profile(profile_name)
    provider_type = config["api_secret_key"]["type"]

    if provider_type == "file":
        profile = ApiProfile(
            profile_name=profile_name,
            api_id=config["api_id"],
            api_secret_key=SecretKeyConfig(**config["api_secret_key"]),
        )
        return FileAuthProvider(profile)
    elif provider_type == "vault":
        raise NotImplementedError("Vault provider is not yet implemented")
    else:
        raise ValueError(f"Unknown provider type: {provider_type}")
