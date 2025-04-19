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
    Redirect HOME to a temporary directory to isolate config paths.
    Creates both config.toml and credentials.
    """
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    config_dir = tmp_path / ".config" / "fireblocks-cli"
    config_dir.mkdir(parents=True, exist_ok=True)

    config_toml = config_dir / "config.toml"
    credentials = config_dir / "credentials"

    # Write config.toml with default profile (should be overridden)
    config_toml.write_text(
        """
[default]
api_id = "from-config"
api_secret_key = { type = "file", value = "config.key" }

[only_in_config]
api_id = "config-only"
api_secret_key = { type = "file", value = "config.key" }
"""
    )

    # Write credentials with default profile (should override) and another unique one
    credentials.write_text(
        """
[default]
api_id = "from-credentials"
api_secret_key = { type = "vault", value = "vault.key" }

[only_in_credentials]
api_id = "credentials-only"
api_secret_key = { type = "vault", value = "vault.key" }
"""
    )

    return config_toml, credentials


def test_configure_list_merges_profiles(mock_home):
    """
    Test that `configure list` merges config.toml and credentials,
    and credentials override config values when profile names match.
    """
    result = runner.invoke(app, ["configure", "list"])
    output = result.stdout

    assert result.exit_code == 0

    # default should come from credentials (vault)
    assert "[default]" in output
    assert "api_id: from-credentials" in output
    assert "secret_type: vault" in output

    # config-only profile should still appear
    assert "[only_in_config]" in output
    assert "api_id: config-only" in output

    # credentials-only profile should also appear
    assert "[only_in_credentials]" in output
    assert "api_id: credentials-only" in output
