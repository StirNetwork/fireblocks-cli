#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025 Ethersecurity Inc.
#
# SPDX-License-Identifier: MPL-2.0

# Author: Shohei KAMON <cameong@stir.network>

"""
add_author.py

This script automatically inserts an Author line into source files based on the current git user's configuration,
using SPDX and REUSE best practices.

Supports comment style switching (e.g., `#` vs `<!-- -->`) based on file extension.
"""

import sys
import os
import subprocess
from pathlib import Path

# コメントスタイル設定
COMMENT_STYLES = {
    ".md": ("<!-- ", " -->"),
    ".html": ("<!-- ", " -->"),
    ".xml": ("<!-- ", " -->"),
    ".py": ("# ", ""),
    ".sh": ("# ", ""),
    ".toml": ("# ", ""),
    ".yml": ("# ", ""),
    ".yaml": ("# ", ""),
    ".ini": ("# ", ""),
    ".txt": ("# ", ""),
    "default": ("# ", ""),
}

# コメントスタイルに応じたSPDX行後のオフセット行数
COMMENT_INSERT_OFFSETS = {"<!--": 2, "#": 1, "//": 1, "default": 1}


def get_comment_wrapper(file_path: Path) -> tuple[str, str]:
    ext = file_path.suffix.lower()
    return COMMENT_STYLES.get(ext, COMMENT_STYLES["default"])


def get_git_author(comment_start: str, comment_end: str) -> str | None:
    try:
        name = subprocess.check_output(
            ["git", "config", "user.name"], text=True
        ).strip()
        email = subprocess.check_output(
            ["git", "config", "user.email"], text=True
        ).strip()
        if not name or not email:
            raise ValueError("Git user.name or user.email is not set")
        return f"{comment_start}Author: {name} <{email}>{comment_end}"
    except (subprocess.CalledProcessError, ValueError):
        return None


def insert_or_append_author(filepath: str, append=False):
    path = Path(filepath)
    if not path.is_file():
        return

    comment_start, comment_end = get_comment_wrapper(path)
    stripped_comment_start = comment_start.strip()
    author_line = get_git_author(comment_start, comment_end)
    if not author_line:
        return

    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if any(author_line.strip() == line.strip() for line in lines):
        return  # already present

    has_author_line = any("Author:" in line for line in lines)

    if append and has_author_line:
        last_author_index = max(i for i, line in enumerate(lines) if "Author:" in line)
        lines.insert(last_author_index + 1, author_line + "\n")
    else:
        inserted = False
        for i, line in enumerate(lines):
            if "SPDX-License-Identifier:" in line:
                insert_offset = COMMENT_INSERT_OFFSETS.get(stripped_comment_start, 1)
                insert_index = i + insert_offset
                lines.insert(insert_index, author_line + "\n")
                inserted = True
                break

        if not inserted:
            if lines and lines[0].startswith("#!"):
                lines.insert(1, "\n" + author_line + "\n")
            else:
                lines.insert(0, author_line + "\n\n")

    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(lines)


if __name__ == "__main__":
    append_mode = "--append" in sys.argv
    files = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not files:
        print("Usage: add_author.py [--append] file1.py file2.md ...")
        sys.exit(1)

    for path in files:
        insert_or_append_author(path, append=append_mode)
