#!/bin/bash

# SPDX-FileCopyrightText: 2025 Ethersecurity
#
# SPDX-License-Identifier: MPL-2.0

# Author: Shohei KAMON <cameong@stir.network>

echo '# Contributors' > CONTRIBUTORS.md
echo "" >> CONTRIBUTORS.md
echo "This project is developed with contributions from the following individuals:" >> CONTRIBUTORS.md
echo "" >> CONTRIBUTORS.md
echo "<!-- The list below is automatically generated. Do not edit manually. -->" >> CONTRIBUTORS.md
echo "" >> CONTRIBUTORS.md

# Get unique contributors in the format: Name <email>
git log --format='%aN <%aE>' | sort -u >> CONTRIBUTORS.md
