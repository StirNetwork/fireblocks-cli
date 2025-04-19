# SPDX-FileCopyrightText: 2025 Ethersecurity Inc.
#
# SPDX-License-Identifier: MPL-2.0

# Author: Shohei KAMON <cameong@stir.network>

import toml
from pathlib import Path


def save_toml(data: dict, path: Path):
    path.write_text(toml.dumps(data), encoding="utf-8")
