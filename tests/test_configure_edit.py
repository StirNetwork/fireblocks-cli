# SPDX-FileCopyrightText: 2025 Ethersecurity Inc.
#
# SPDX-License-Identifier: MPL-2.0
# Author: Shohei KAMON <cameong@stir.network>

import os
import pytest
from typer.testing import CliRunner
from fireblocks_cli.main import app
from fireblocks_cli.utils.profile import get_config_file
from pathlib import Path

runner = CliRunner()


@pytest.fixture
def mock_home(tmp_path, monkeypatch):
    """
    Redirect HOME to a temporary directory to isolate test artifacts.

    Creates:
    - ~/.config/fireblocks-cli/config.toml with dummy valid content
    """
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    config_path = tmp_path / ".config" / "fireblocks-cli" / "config.toml"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        '[default]\napi_id = "test"\napi_secret_key = { type = "file", value = "xxx" }\n'
    )
    return tmp_path


def test_edit_invokes_editor_and_validates(mock_home, monkeypatch):
    """
    Test that `configure edit`:
    - Launches the configured editor via subprocess.run
    - Validates config.toml after editing
    """

    # Flags to confirm mock functions are called
    called = {"editor": False, "validate": False}

    # Mock subprocess.run (simulate editor launch)
    def mock_run(cmd, *args, **kwargs):
        assert get_config_file().name in cmd[-1]
        called["editor"] = True

    # Mock validate() call
    def mock_validate():
        called["validate"] = True

    monkeypatch.setenv("EDITOR", "dummy-editor")
    monkeypatch.setattr("subprocess.run", mock_run)
    monkeypatch.setattr("fireblocks_cli.commands.configure.validate", mock_validate)

    result = runner.invoke(app, ["configure", "edit"])
    assert result.exit_code == 0
    assert called["editor"] is True
    assert called["validate"] is True
