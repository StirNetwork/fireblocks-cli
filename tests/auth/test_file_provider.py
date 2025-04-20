# SPDX-FileCopyrightText: 2025 Ethersecurity Inc.
#
# SPDX-License-Identifier: MPL-2.0
# Author: Shohei KAMON <cameong@stir.network>

import pytest
from fireblocks_cli.auth.file_provider import FileAuthProvider
from fireblocks_cli.types.profile_config import ApiProfile, SecretKeyConfig


def test_get_api_id():
    profile = ApiProfile(
        profile_name="test",
        api_id="test-api-id",
        api_secret_key=SecretKeyConfig(
            type="file", value="/dummy/path"
        ),  # 使わないのでダミーでOK
    )
    provider = FileAuthProvider(profile)
    assert provider.get_api_id() == "test-api-id"


def test_get_secret_key(tmp_path):
    # 仮の秘密鍵ファイルを作成
    secret_file = tmp_path / "test_secret.key"
    secret_file.write_text("my-secret-key\n")

    profile = ApiProfile(
        profile_name="test",
        api_id="dummy",
        api_secret_key=SecretKeyConfig(type="file", value=str(secret_file)),
    )
    provider = FileAuthProvider(profile)
    secret = provider.get_secret_key()

    assert secret.strip() == "my-secret-key"
