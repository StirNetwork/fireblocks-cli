# SPDX-FileCopyrightText: 2025 Ethersecurity Inc.
#
# SPDX-License-Identifier: MPL-2.0

# Author: Shohei KAMON <cameong@stir.network>

import random
import string
from pathlib import Path
import subprocess
import typer
from fireblocks_cli.utils.profile import (
    get_api_key_dir,
)


def generate_unique_basename(base_dir: Path) -> tuple[str, Path, Path]:
    while True:
        basename = "".join(random.choices(string.ascii_lowercase + string.digits, k=12))
        key_path = base_dir / f"{basename}.key"
        csr_path = base_dir / f"{basename}.csr"
        if not key_path.exists() and not csr_path.exists():
            return basename, key_path, csr_path


def generate_key_and_csr(
    org_name: str, key_type: str = "rsa:4096"
) -> tuple[Path, Path]:
    api_key_dir = get_api_key_dir()
    api_key_dir.mkdir(parents=True, exist_ok=True)

    basename, key_path, csr_path = generate_unique_basename(api_key_dir)
    subj = f"/O={org_name}"

    # key_type: "rsa:2048", "rsa:4096", "ed25519"
    if key_type.startswith("rsa:"):
        bits = key_type.split(":")[1]
        key_alg = "rsa"
        key_args = ["-newkey", f"rsa:{bits}"]
    elif key_type == "ed25519":
        key_alg = "ed25519"
        key_args = ["-newkey", "ed25519"]
    else:
        typer.secho(f"❌ Unsupported key type: {key_type}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    result = subprocess.run(
        [
            "openssl",
            "req",
            "-new",
            *key_args,
            "-nodes",
            "-keyout",
            str(key_path),
            "-out",
            str(csr_path),
            "-subj",
            subj,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    if result.returncode != 0:
        typer.secho("❌ OpenSSL error:", fg=typer.colors.RED)
        typer.echo(result.stderr)
        raise typer.Exit(code=1)

    key_path.chmod(0o600)
    csr_path.chmod(0o600)
    return key_path, csr_path
