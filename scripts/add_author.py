#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025 Ethersecurity
#
# SPDX-License-Identifier: MPL-2.0

# Author: Shohei KAMON <cameong@stir.network>

"""
add_author.py

This script automatically inserts an Author line into source files based on the current git user's configuration.

Usage:
  python add_author.py file1.py file2.sh ...         # Inserts Author line if missing
  python add_author.py --append file1.py             # Appends your Author line after existing Author(s)

Behavior:
- Extracts user.name and user.email from git config.
- Inserts `# Author: Name <email>` after the SPDX-License-Identifier line.
- If no SPDX line exists, and a shebang is present, inserts Author line after shebang.
- Otherwise inserts Author line at the top.
- Adds a blank line above the inserted Author line when newly added.
- In append mode, adds Author line directly below existing Author lines.
- Avoids duplicate Author lines.
- Skips processing if git config is missing or incomplete.

Intended for use in compliance with REUSE and SPDX standards, especially for projects requiring traceable authorship (e.g. financial institutions).
"""

import sys
import os
import subprocess


def get_git_author():
    try:
        name = subprocess.check_output(
            ["git", "config", "user.name"], text=True
        ).strip()
        email = subprocess.check_output(
            ["git", "config", "user.email"], text=True
        ).strip()
        if not name or not email:
            raise ValueError("Git user.name or user.email is not set")
        return f"# Author: {name} <{email}>"
    except (subprocess.CalledProcessError, ValueError):
        return None


AUTHOR_LINE = get_git_author()


def insert_or_append_author(filepath, append=False):
    if not os.path.isfile(filepath) or AUTHOR_LINE is None:
        return

    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if any(AUTHOR_LINE.strip() == line.strip() for line in lines):
        return  # already present

    has_author_line = any(line.startswith("# Author:") for line in lines)

    if append and has_author_line:
        last_author_index = max(
            i for i, line in enumerate(lines) if line.startswith("# Author:")
        )
        lines.insert(last_author_index + 1, AUTHOR_LINE + "\n")
    else:
        inserted = False
        for i, line in enumerate(lines):
            if line.startswith("# SPDX-License-Identifier:"):
                lines.insert(i + 1, "\n" + AUTHOR_LINE + "\n")
                inserted = True
                break
        if not inserted:
            if lines and lines[0].startswith("#!"):
                lines.insert(1, "\n" + AUTHOR_LINE + "\n")
            else:
                lines.insert(0, AUTHOR_LINE + "\n\n")

    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(lines)


if __name__ == "__main__":
    if AUTHOR_LINE is None:
        print("❌ Skipping: Git user.name and user.email are not set.")
        sys.exit(1)

    append_mode = "--append" in sys.argv
    files = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    for path in files:
        insert_or_append_author(path, append=append_mode)
