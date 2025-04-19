#!/bin/bash

# SPDX-FileCopyrightText: 2025 Ethersecurity Inc.
#
# SPDX-License-Identifier: MPL-2.0

# Author: Shohei KAMON <cameong@stir.network>

set -x

cat <<'EOS'> CONTRIBUTORS.md
<!--
SPDX-FileCopyrightText: 2025 Ethersecurity Inc.

SPDX-License-Identifier: MPL-2.0
-->

<!-- Author: Shohei KAMON <cameong@stir.network> -->


# Contributors
EOS
echo "" >> CONTRIBUTORS.md
echo "This project is developed with contributions from the following individuals:" >> CONTRIBUTORS.md
echo "" >> CONTRIBUTORS.md
echo "<!-- The list below is automatically generated. Do not edit manually. -->" >> CONTRIBUTORS.md
echo "" >> CONTRIBUTORS.md

# Sorted in chronological order (oldest first)
# With duplicates removed
# Each entry formatted as "- Name <email>"
git log --format='%aN <%aE>' | tac | awk '!seen[$0]++ { print "- " $0 }' >> CONTRIBUTORS.md
