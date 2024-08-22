
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


from typing import Any, Optional, Type

from pydantic import RedisDsn
import redis.asyncio as redis
from redis.exceptions import ConnectionError

from sesh.backend.base import SessionStore
from sesh.exceptions import SessionError
from sesh.models.key import KeyBase


class RedisStore(SessionStore):
    def __init__(self: SessionStore, redis_dsn: RedisDsn):
        self._client: redis.Redis = redis.from_url(str(redis_dsn))

    @property
    def client(self) -> redis.Redis:
        return self._client

    async def create_entry(self, state_data: KeyBase) -> None:
        """Create a new key/value pair in Redis."""
        json_serial = state_data.model_dump_json(exclude_unset=True)
        key_id = state_data.key_id
        key_ttl = state_data.key_ttl

        if not all((json_serial, key_id, key_ttl)):
            raise SessionError('redis', "Missing values needed to set in Redis.")

        try:
            await self.client.set(key_id, json_serial, ex=key_ttl)
        except ConnectionError as e:
            raise SessionError('redis', str(e))

    async def read(self, key_id: str, state_data: Type[KeyBase]) -> Optional[KeyBase]:
        """Read a key/value pair from Redis."""
        try:
            session_data_json: Any = await self.client.get(key_id)
        except ConnectionError as e:
            raise SessionError('redis', str(e))

        if session_data_json:
            session_data: Any = state_data.model_validate_json(session_data_json)
            await self.client.expire(session_data.key_id, session_data.key_ttl)
        else:
            return None

        return session_data

    async def update(self, state_data: KeyBase) -> None:
        """Update a key/value pair in Redis"""
        try:
            await self.client.set(
                state_data.key_id,
                state_data.model_dump_json(exclude_none=True),
                ex=state_data.key_ttl
            )
            await self.client.expire(state_data.key_id, state_data.key_ttl)
        except ConnectionError as e:
            raise SessionError('redis', str(e))

    async def delete(self, key_id: str) -> None:
        """Remove a key/value pair from Redis."""
        if key_id is None:
            raise TypeError("key_id cannot be null")
        await self.client.delete(key_id)

    async def check_for_key(self, key_id: str) -> bool:
        """Get count of instances of key_id in Redis.
                If the count == 0, bool() will be False
                If the count >= 1, bool() will be True
        """
        try:
            key_count = await self.client.exists(key_id)
        except ConnectionError as e:
            raise SessionError('redis', str(e))

        return bool(key_count)

    async def refresh_key_ttl(self, key_id: str, key_ttl: int) -> None:
        await self.client.expire(key_id, key_ttl)
