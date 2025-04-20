# SPDX-FileCopyrightText: 2025 Ethersecurity Inc.
#
# SPDX-License-Identifier: MPL-2.0
# Author: Shohei KAMON <cameong@stir.network>

from abc import ABC, abstractmethod
from typing import Dict


class BaseAuthProvider(ABC):
    @abstractmethod
    def get_jwt(self) -> str:
        """Get JWT token"""
        pass

    @abstractmethod
    def get_api_id(self) -> str:
        """Return the API ID"""
        pass

    @abstractmethod
    def get_secret_key(self) -> str:
        """
        Return secret info api_secret_key value (raw string )
        """
        pass
