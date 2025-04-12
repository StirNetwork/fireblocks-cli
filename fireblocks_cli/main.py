#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025 Ethersecurity
#
# SPDX-License-Identifier: MPL-2.0

# Author: Shohei KAMON <cameong@stir.network>

from fireblocks_cli.commands.configure import configure_app
import typer

app = typer.Typer()
app.add_typer(configure_app, name="configure")

if __name__ == "__main__":
    app()
