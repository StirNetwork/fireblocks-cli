# SPDX-FileCopyrightText: 2025 Ethersecurity Inc.
#
# SPDX-License-Identifier: MPL-2.0
# Author: Shohei KAMON <cameong@stir.network>

from fireblocks_cli.auth.base import BaseAuthProvider
from fireblocks_cli.types.profile_config import ApiProfile, SecretKeyConfig
from pathlib import Path


class FileAuthProvider(BaseAuthProvider):
    def __init__(self, profile: ApiProfile):
        self.profile = profile

    def get_api_id(self) -> str:
        return self.profile.api_id

    def get_secret_key(self) -> str:
        secret_path = Path(self.profile.api_secret_key.value).expanduser()
        with open(secret_path, "r") as f:
            secret_key = f.read()
        return secret_key

    def get_api_secret_info(self) -> dict[str, str]:
        return {
            "profile": self.profile.profile_name,
            "api_id": self.profile.api_id,
            "api_secret_key": self.get_secret_key(),
        }

    def get_jwt(self) -> str:
        print(f"Using profile: {self.profile.profile_name}")

        import time, jwt

        payload = {
            "uri": "/v1/*",
            "nonce": int(time.time() * 1000),
            "iat": int(time.time()),
            "exp": int(time.time()) + 300,
            "sub": self.get_api_id(),
        }
        return jwt.encode(payload, self.get_api_id(), algorithm="HS256")
