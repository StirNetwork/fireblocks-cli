# SPDX-FileCopyrightText: 2025 Ethersecurity Inc.
#
# SPDX-License-Identifier: MPL-2.0

# Author: Shohei KAMON <cameong@stir.network>

try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version  # Python <3.8 fallback

__version__ = version(__name__)
