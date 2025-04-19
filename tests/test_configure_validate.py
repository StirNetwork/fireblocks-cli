# SPDX-FileCopyrightText: 2025 Ethersecurity Inc.
#
# SPDX-License-Identifier: MPL-2.0
# Author: Shohei KAMON <cameong@stir.network>

import pytest
from pathlib import Path
from typer.testing import CliRunner
from fireblocks_cli.main import app

runner = CliRunner()


@pytest.fixture
def mock_home(tmp_path, monkeypatch):
    """
    Set HOME to tmp path, and pre-create config dir.
    """
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    config_dir = tmp_path / ".config" / "fireblocks-cli"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def test_validate_with_valid_files(mock_home):
    """
    Validate returns success (exit_code 0) when both config files are valid.
    """
    config = mock_home / "config.toml"
    credentials = mock_home / "credentials"

    config.write_text(
        """
[default]
api_id = "abc"
api_secret_key = { type = "file", value = "secret.key" }
"""
    )

    credentials.write_text(
        """
[creds]
api_id = "def"
api_secret_key = { type = "vault", value = "vaultpath" }
"""
    )

    result = runner.invoke(app, ["configure", "validate"])
    assert result.exit_code == 0
    assert "✅" in result.stdout


def test_validate_fails_on_invalid_config(mock_home):
    """
    Should fail if config.toml is malformed.
    """
    config = mock_home / "config.toml"
    config.write_text("this is not toml")

    result = runner.invoke(app, ["configure", "validate"])
    assert result.exit_code == 1
    assert "❌" in result.stdout


def test_validate_fails_on_missing_keys(mock_home):
    """
    Should fail if required keys are missing from profile.
    """
    config = mock_home / "config.toml"
    config.write_text(
        """
[default]
api_id = "only-id"
"""
    )

    result = runner.invoke(app, ["configure", "validate"])
    assert result.exit_code == 1
    assert "missing required keys" in result.stdout


def test_validate_skips_when_files_missing(tmp_path, monkeypatch):
    """
    Should exit normally and skip when no config files exist.
    """
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    result = runner.invoke(app, ["configure", "validate"])
    assert result.exit_code == 0
    assert "not found. Skipping." in result.stdout
