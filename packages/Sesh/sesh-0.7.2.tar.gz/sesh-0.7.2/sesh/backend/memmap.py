
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


from typing import Dict, Optional

from sesh.backend.base import SessionStore
from sesh.exceptions import SessionError
from sesh.models.key import KeyBase


class InMemoryStore(SessionStore):
    """Stores session data in a dictionary."""

    def __init__(self) -> None:
        """Initialize a new in-memory database."""
        self._data: Dict[str, KeyBase] = {}

    @property
    def data(self):
        return self._data

    async def create_entry(self, state_data: KeyBase) -> None:
        """Create a new session entry."""
        if self.data.get(str(state_data.key_id)):
            raise SessionError("InMemoryStore", "create can't overwrite an existing session")

        self.data[str(state_data.key_id)] = state_data

    async def read(self, key_id: str, data_model: KeyBase) -> Optional[KeyBase]:
        """Read an existing session data."""
        state_data = self.data.get(key_id)

        return state_data

    async def update(self, state_data: KeyBase) -> None:
        """Update an existing session."""
        if self.data.get(str(state_data.key_id)):
            self.data[str(state_data.key_id)] = state_data
        else:
            raise SessionError("InMemoryStore", "session does not exist, cannot update")

    async def delete(self, key_id: str) -> None:
        """Remove session data from the storage."""
        if key_id is None:
            raise TypeError("key_id cannot be null")
        del self.data[str(key_id)]

    async def check_for_key(self, key_id: str) -> bool:
        key_in_data = self.data.get(str(key_id))

        if key_in_data:
            return True
        else:
            return False

    async def refresh_key_ttl(self, key_id: str, key_ttl: int) -> None:
        """Refresh the ttl for the key in the storage.

        We don't implement ttl for keys in the memmap store, but need to define
        this function here to maintain the contract with the ABC, so just 'pass'.
        """
        pass
