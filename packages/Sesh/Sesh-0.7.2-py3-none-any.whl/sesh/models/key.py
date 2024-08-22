
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


from typing import Optional

from pydantic import BaseModel


class KeyBase(BaseModel):
    """Mixin for key_id and key_ttl for models stored in key/value storage

    These two attributes are absolutely necessary when passing a model to
    a key/value store like Redis, but they will not be present when received
    in a request, so we make them Optional here.
    """
    key_id: Optional[str] = None
    key_ttl: Optional[int] = None
