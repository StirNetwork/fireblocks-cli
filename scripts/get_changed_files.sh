#!/bin/bash

# SPDX-FileCopyrightText: 2025 Ethersecurity Inc.
#
# SPDX-License-Identifier: MPL-2.0

# Author: Shohei KAMON <cameong@stir.network>

# exclude removed file: grep -v "^D"
git status --porcelain | grep -v "^??" | grep -v "^D " | cut -c4- | grep -v "\.txt$"
