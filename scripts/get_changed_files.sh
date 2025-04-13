#!/bin/bash

# SPDX-FileCopyrightText: 2025 Ethersecurity Inc.
#
# SPDX-License-Identifier: MPL-2.0

# Author: Shohei KAMON <cameong@stir.network>

git status --porcelain | grep -v "^??" | cut -c4- | grep -e "\.sh$" -e "\.py$"
