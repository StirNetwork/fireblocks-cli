# SPDX-FileCopyrightText: 2025 Ethersecurity Inc.
#
# SPDX-License-Identifier: MPL-2.0

# Author: Shohei KAMON <cameong@stir.network>

import os
from typer.testing import CliRunner
from fireblocks_cli.main import app
from pathlib import Path
import toml
import pytest

runner = CliRunner()


@pytest.fixture
def mock_home(tmp_path, monkeypatch):
    """
    Redirect the HOME environment to a temporary path to isolate file system side effects.

    Ensures that the following paths are created under a clean test directory:
    - ~/.config/fireblocks-cli/config.toml
    - ~/.config/fireblocks-cli/keys/
    """
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    return tmp_path


def test_init_creates_config_and_keys_dir(mock_home):
    """
    Test that `configure init` creates the expected configuration file and keys directory.

    Verifies:
    - ~/.config/fireblocks-cli/config.toml is created
    - ~/.config/fireblocks-cli/keys directory is created
    - config file contains default (empty) API values
    """
    config_dir = mock_home / ".config/fireblocks-cli"
    config_file = config_dir / "config.toml"
    keys_dir = config_dir / "keys"

    result = runner.invoke(app, ["configure", "init"])
    assert result.exit_code == 0

    assert config_file.exists()
    assert keys_dir.exists()

    config_data = toml.load(config_file)
    assert isinstance(config_data, dict)
    assert "default" in config_data
    default_section = config_data["default"]
    assert isinstance(default_section, dict)

    # api_id: str
    assert isinstance(default_section["api_id"], str)

    # api_secret_key: dict with {"type": str, "value": str}
    secret_key = default_section["api_secret_key"]
    assert isinstance(secret_key, dict)
    assert isinstance(secret_key.get("type"), str)
    assert isinstance(secret_key.get("value"), str)

    assert secret_key["type"] in {"file", "text", "vault"}  # 必要なら


def test_init_when_config_already_exists(mock_home):
    """
    Test that `configure init` does not fail when config.toml already exists.

    Verifies:
    - config.toml is not overwritten
    - CLI exits successfully (exit_code == 0)
    - The message indicates the config already exists
    """
    config_dir = mock_home / ".config/fireblocks-cli"
    config_file = config_dir / "config.toml"
    config_dir.mkdir(parents=True, exist_ok=True)

    # Pre-create config file
    original_config = {
        "default": {"api_id": "existing_id", "api_secret_key": "existing_secret"}
    }
    config_file.write_text(toml.dumps(original_config), encoding="utf-8")

    result = runner.invoke(app, ["configure", "init"])
    assert result.exit_code == 0
    assert "already exists" in result.stdout

    config_data = toml.load(config_file)
    assert config_data["default"]["api_id"] == "existing_id"
    assert config_data["default"]["api_secret_key"] == "existing_secret"
