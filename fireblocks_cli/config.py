# SPDX-FileCopyrightText: 2025 Ethersecurity Inc.
#
# SPDX-License-Identifier: MPL-2.0

# Author: Shohei KAMON <cameong@stir.network>

from pathlib import Path

CONFIG_DIR = Path("~/.config/fireblocks-cli").expanduser()
CONFIG_FILE = CONFIG_DIR / "config.toml"
CREDENTIALS_FILE = Path("~/.fireblocks/credentials").expanduser()

DEFAULT_CONFIG = {"default": {"api_id": "", "api_secret_key": ""}}
