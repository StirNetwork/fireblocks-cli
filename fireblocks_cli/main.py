#!/usr/bin/env python3

from fireblocks_cli.commands.configure import configure_app
import typer

app = typer.Typer()
app.add_typer(configure_app, name="configure")

if __name__ == "__main__":
    app()
