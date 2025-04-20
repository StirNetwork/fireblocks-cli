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


def generate_key_and_csr(org_name: str) -> tuple[Path, Path]:
    api_key_dir = get_api_key_dir()
    api_key_dir.mkdir(parents=True, exist_ok=True)

    basename, key_path, csr_path = generate_unique_basename(api_key_dir)
    subj = f"/O={org_name}"

    result = subprocess.run(
        [
            "openssl",
            "req",
            "-new",
            "-newkey",
            "ed25519",
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
        typer.secho("❌ OpenSSLエラー:", fg=typer.colors.RED)
        typer.echo(result.stderr)
        raise typer.Exit(code=1)
    key_path.chmod(0o600)
    csr_path.chmod(0o600)

    return key_path, csr_path
