# SPDX-FileCopyrightText: 2025 Ethersecurity Inc.
#
# SPDX-License-Identifier: MPL-2.0

# Author: Shohei KAMON <cameong@stir.network>
from pathlib import Path


def get_config_dir() -> Path:
    return Path.home() / ".config" / "fireblocks-cli"


def get_config_file() -> Path:
    return get_config_dir() / "config.toml"


def get_api_key_dir() -> Path:
    return get_config_dir() / "keys"


def get_credentials_file() -> Path:
    return get_config_dir() / "credentials"


DEFAULT_CONFIG = {
    "default": {
        "api_id": "get-api_id-from-fireblocks-dashboard",
        "api_secret_key": {
            "type": "file",
            "value": "~/.config/fireblocks-cli/keys/abcd.key",
        },
    }
}
