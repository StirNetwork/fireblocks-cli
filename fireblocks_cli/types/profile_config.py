# SPDX-FileCopyrightText: 2025 Ethersecurity Inc.
#
# SPDX-License-Identifier: MPL-2.0
# Author: Shohei KAMON <cameong@stir.network>

from dataclasses import dataclass
from typing import Literal, Dict


@dataclass
class SecretKeyConfig:
    type: Literal["file", "env", "vault"]
    value: str


@dataclass
class ApiProfile:
    profile_name: str
    api_id: str
    api_secret_key: SecretKeyConfig
