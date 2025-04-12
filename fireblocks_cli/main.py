#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025 Ethersecurity
#
# SPDX-License-Identifier: MPL-2.0

# Author: Shohei KAMON <cameong@stir.network>

from fireblocks_cli.commands.configure import configure_app
import typer
from fireblocks_cli import __version__

app = typer.Typer()
app.add_typer(configure_app, name="configure")


@app.callback()
def main(
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the version and exit.",
        is_eager=True,
        callback=lambda v: (
            (print(f"fireblocks-cli version {__version__}") or raise_exit())
            if v
            else None
        ),
    )
):
    pass


def raise_exit():
    raise typer.Exit()


@app.command()
def version():
    """Show CLI version"""
    typer.echo(f"fireblocks-cli version {__version__}")


if __name__ == "__main__":
    app()
