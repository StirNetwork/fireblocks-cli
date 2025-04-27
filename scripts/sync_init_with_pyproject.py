#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025 Ethersecurity Inc.
#
# SPDX-License-Identifier: MPL-2.0
# Author: Shohei KAMON <cameong@stir.network>

import toml
import re


def update_version(
    init_path: str = "fireblocks_cli/__init__.py",
    pyproject_path: str = "pyproject.toml",
) -> None:
    """pyproject.tomlのversionと__init__.pyのversionを同期する"""

    # 1. pyproject.toml を読み込む
    with open(pyproject_path, "r") as f:
        pyproject = toml.load(f)
    pyproject_version = pyproject["project"]["version"]

    # 2. __init__.py を読み込む
    with open(init_path, "r") as f:
        lines = f.readlines()

    # 3. __init__.pyの中の__version__を探す
    current_version = None
    for line in lines:
        match = re.match(r'^__version__\s*=\s*[\'"]([^\'"]+)[\'"]', line.strip())
        if match:
            current_version = match.group(1)
            break

    # 4. バージョンが同じなら何もしない
    if current_version == pyproject_version:
        print(
            f"No update needed: {init_path} version {current_version} matches pyproject.toml version {pyproject_version}"
        )
        return

    # 5. SPDXヘッダーのみ残して、後続を書き直す
    header = []
    for line in lines:
        if line.strip().startswith("#") or not line.strip():
            header.append(line)
        else:
            break

    # 6. ファイルを書き直す
    with open(init_path, "w") as f:
        f.writelines(header)
        f.write("\n")
        f.write(f'__version__ = "{pyproject_version}"\n')

    print(f"Updated {init_path}: {current_version} → {pyproject_version}")


if __name__ == "__main__":
    update_version()
