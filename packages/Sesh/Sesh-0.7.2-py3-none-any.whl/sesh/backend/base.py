
"""
sesh is a session management library for FastAPI

Copyright (C) 2024  Brian Farrell

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Contact: brian.farrell@me.com
"""


from abc import ABC, abstractmethod
from typing import Optional, Type

from sesh.models.key import KeyBase


class SessionStore(ABC):
    """Abstract Class - This class provides the interface for CRUD operations with session data.
    """
    @abstractmethod
    async def create_entry(self, state_data: KeyBase) -> None:
        """Create a new session."""
        raise NotImplementedError()

    @abstractmethod
    async def read(self, key_id: str, state_data: Type[KeyBase]) -> Optional[KeyBase]:
        """Read session data from the storage."""
        raise NotImplementedError()

    @abstractmethod
    async def update(self, state_data: KeyBase) -> None:
        """Update session data to the storage"""
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, key_id: str) -> None:
        """Remove session data from the storage."""
        raise NotImplementedError()

    @abstractmethod
    async def check_for_key(self, key_id: str) -> bool:
        """Remove session data from the storage."""
        raise NotImplementedError()

    @abstractmethod
    async def refresh_key_ttl(self, key_id: str, key_ttl: int) -> None:
        """Refresh the ttl for the key in the storage."""
        raise NotImplementedError()
