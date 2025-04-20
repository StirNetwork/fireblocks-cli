# SPDX-FileCopyrightText: 2025 Ethersecurity Inc.
#
# SPDX-License-Identifier: MPL-2.0
# Author: Shohei KAMON <cameong@stir.network>

# fireblocks_cli/auth/vault_provider.py

from fireblocks_cli.auth.base import BaseAuthProvider


class VaultAuthProvider(BaseAuthProvider):
    def __init__(self, vault_path: str):
        # Planning: HashiCorp Vault,  AWS Secrets Manager
        self.vault_path = vault_path

    def get_api_key(self) -> str:
        raise NotImplementedError

    def get_secret_key(self) -> str:
        raise NotImplementedError

    def get_jwt(self) -> str:
        raise NotImplementedError
