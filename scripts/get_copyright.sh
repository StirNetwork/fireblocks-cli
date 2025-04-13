#!/usr/bin/env bash

# SPDX-FileCopyrightText: 2025 Ethersecurity Inc.
#
# SPDX-License-Identifier: MPL-2.0

# Author: Shohei KAMON <cameong@stir.network>

if [ ! -s COPYRIGHT_HOLDER ]; then
  echo "Ethersecurity Inc."
  exit 0
fi

val=$(cat COPYRIGHT_HOLDER)

if [ ${#val} -le 50 ]; then
  echo "$val"
else
  echo "ERROR: COPYRIGHT_HOLDER is too long (>50 chars)" >&2
  exit 1
fi
