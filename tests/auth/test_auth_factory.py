# SPDX-FileCopyrightText: 2025 Ethersecurity Inc.
#
# SPDX-License-Identifier: MPL-2.0
# Author: Shohei KAMON <cameong@stir.network>

import pytest
from fireblocks_cli.auth.factory import get_auth_provider, FileAuthProvider
from fireblocks_cli.types.profile_config import ApiProfile, SecretKeyConfig


def test_get_auth_provider_returns_file_provider(monkeypatch, tmp_path):
    # 仮の秘密鍵ファイルを作成
    secret_file = tmp_path / "mock_secret.key"
    secret_file.write_text("mock-super-secret")

    # monkeypatch: load_profile() をモックして返す値を差し替える
    monkeypatch.setattr(
        "fireblocks_cli.auth.factory.load_profile",
        lambda profile_name: {
            "api_id": "mock-api-id",
            "api_secret_key": {
                "type": "file",
                "value": str(secret_file),
            },
        },
    )

    # 呼び出し
    provider = get_auth_provider("mock")

    # 検証
    assert isinstance(provider, FileAuthProvider)
    assert provider.get_api_id() == "mock-api-id"
    assert provider.get_secret_key() == "mock-super-secret"
