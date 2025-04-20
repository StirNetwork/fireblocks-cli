# SPDX-FileCopyrightText: 2025 Ethersecurity Inc.
#
# SPDX-License-Identifier: MPL-2.0
# Author: Shohei KAMON <cameong@stir.network>

from typing import List, Dict
import toml
from fireblocks_cli.types.profile_config import ApiProfile, SecretKeyConfig


DEFAULT_PROFILE = "default"


from pathlib import Path

DEFAULT_PROFILE = "default"
DEFAULT_CONFIG = {
    "default": {
        "api_id": "get-api_id-from-fireblocks-dashboard",
        "api_secret_key": {
            "type": "file",
            "value": "~/.config/fireblocks-cli/keys/abcd.key",
        },
    }
}


def get_config_dir() -> Path:
    return Path.home() / ".config" / "fireblocks-cli"


def get_config_file() -> Path:
    return get_config_dir() / "config.toml"


def get_api_key_dir() -> Path:
    return get_config_dir() / "keys"


def get_credentials_file() -> Path:
    return get_config_dir() / "credentials"


class ProfileLoadError(Exception):
    pass


def get_profiles() -> dict:
    """
    Load and merge profile configurations from config.toml and credentials.

    Returns:
        dict: A dictionary where keys are profile names and values are their respective configurations.

    Raises:
        ProfileLoadError: If either config.toml or credentials.toml fails to parse.

    Notes:
        - config.toml is loaded first.
        - credentials (if present) will override any conflicting keys from config.toml.
    """
    config_path = get_config_file()
    credentials_path = get_credentials_file()
    combined_data = {}

    # Step 1: load config.toml
    if config_path.exists():
        try:
            config_data = toml.load(config_path)
            combined_data.update(config_data)
        except Exception as e:
            raise ProfileLoadError(f"Failed to parse config.toml: {e}")

    # Step 2: override with credentials if it exists
    if credentials_path.exists():
        try:
            credentials_data = toml.load(credentials_path)
            combined_data.update(credentials_data)  # override same keys
        except Exception as e:
            raise ProfileLoadError(f"Failed to parse credentials: {e}")
    return combined_data


def load_profile(profile: str = DEFAULT_PROFILE) -> dict:
    profiles = get_profiles()
    if profile not in profiles:
        raise ValueError(f"No such profile :'{profile}' is defined.")
    return profiles[profile]
