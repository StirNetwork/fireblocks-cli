# SPDX-FileCopyrightText: 2025 Ethersecurity Inc.
#
# SPDX-License-Identifier: MPL-2.0

# Author: Shohei KAMON <cameong@stir.network>

import os
from typer.testing import CliRunner
from fireblocks_cli.main import app
from pathlib import Path
import pytest

runner = CliRunner()


@pytest.fixture
def mock_home(tmp_path, monkeypatch):
    """
    Redirect the HOME environment to a temporary path to isolate file system side effects.
    """
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    return tmp_path


def test_gen_keys_creates_key_and_csr(mock_home):
    """
    Test that `configure gen-keys` generates a .key and .csr file under ~/.config/fireblocks-cli/keys
    with correct permissions and PEM format.
    """
    key_dir = mock_home / ".config/fireblocks-cli/keys"
    input_text = "TestCompany\n"

    result = runner.invoke(app, ["configure", "gen-keys"], input=input_text)

    assert result.exit_code == 0
    assert key_dir.exists()

    key_files = list(key_dir.glob("*.key"))
    csr_files = list(key_dir.glob("*.csr"))

    assert len(key_files) == 1
    assert len(csr_files) == 1

    key_file = key_files[0]
    csr_file = csr_files[0]

    # 内容チェック（PEM形式）
    key_text = key_file.read_text()
    csr_text = csr_file.read_text()

    assert "BEGIN PRIVATE KEY" in key_text
    assert "BEGIN CERTIFICATE REQUEST" in csr_text

    # パーミッションチェック（600）
    assert key_file.stat().st_mode & 0o777 == 0o600
    assert csr_file.stat().st_mode & 0o777 == 0o600
