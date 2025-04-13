#!/usr/bin/env bash

# SPDX-FileCopyrightText: 2025 Ethersecurity Inc.
#
# SPDX-License-Identifier: MPL-2.0

# Author: Shohei KAMON <cameong@stir.network>

set -euo pipefail

COMMIT_MSG_FILE="$1"

if ! grep -qi '^Signed-off-by: ' "$COMMIT_MSG_FILE"; then
  echo "❌ Commit message is missing a 'Signed-off-by' line."
  echo "💡 Please use: git commit -sm \"your message\""
  exit 1
fi
