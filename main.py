# main.py
import typer
import os
import random
import string
from pathlib import Path
import subprocess

app = typer.Typer()
configure_app = typer.Typer()

@configure_app.command("gen-keys")
def gen_keys():
    """秘密鍵とCSRを ~/.fireblocks/keys に生成します"""
    base_dir = Path.home() / ".fireblocks" / "keys"
    base_dir.mkdir(parents=True, exist_ok=True)

    def generate_unique_basename():
        while True:
            basename = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
            key_path = base_dir / f"{basename}.key"
            csr_path = base_dir / f"{basename}.csr"
            if not key_path.exists() and not csr_path.exists():
                return basename, key_path, csr_path

    basename, key_path, csr_path = generate_unique_basename()

    org = typer.prompt("🔐 組織名を入力してください（例: MyCompany）").strip()
    if not org:
        typer.secho("❌ 組織名は必須です。処理を中止します。", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    subj = f"/O={org}"
    typer.echo(f"🔧 鍵とCSRを生成中... → {basename}.key / {basename}.csr")

    result = subprocess.run([
        "openssl", "req", "-new", "-newkey", "ed25519",
        "-nodes", "-keyout", str(key_path),
        "-out", str(csr_path),
        "-subj", subj
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode != 0:
        typer.secho("❌ OpenSSLエラー:", fg=typer.colors.RED)
        typer.echo(result.stderr)
        raise typer.Exit(code=1)

    typer.secho(f"✅ 秘密鍵: {key_path}", fg=typer.colors.GREEN)
    typer.secho(f"✅ CSR   : {csr_path}", fg=typer.colors.GREEN)

# configure サブコマンドに登録
app.add_typer(configure_app, name="configure")

if __name__ == "__main__":
    app()
