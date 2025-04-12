# SPDX-FileCopyrightText: 2025 Ethersecurity
#
# SPDX-License-Identifier: MPL-2.0

# Author: Shohei KAMON <cameong@stir.network>

import typer
from fireblocks_cli.crypto import generate_key_and_csr

configure_app = typer.Typer()


@configure_app.command("gen-keys")
def gen_keys():
    """秘密鍵とCSRを ~/.fireblocks/keys に生成します"""
    org = typer.prompt("🔐 組織名を入力してください（例: MyCompany）").strip()
    if not org:
        typer.secho("❌ 組織名は必須です。処理を中止します。", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    key_path, csr_path = generate_key_and_csr(org)
    typer.secho(f"✅ 秘密鍵: {key_path}", fg=typer.colors.GREEN)
    typer.secho(f"✅ CSR   : {csr_path}", fg=typer.colors.GREEN)
