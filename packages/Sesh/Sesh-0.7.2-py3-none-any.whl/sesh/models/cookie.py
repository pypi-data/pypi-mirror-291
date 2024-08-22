
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


from datetime import datetime
from typing import Optional, Union

from aenum import UniqueEnum
from pydantic import BaseModel


class SameSiteEnum(UniqueEnum):
    LAX = "lax"
    STRICT = "strict"
    NONE = "none"


class Cookie(BaseModel):
    domain: Optional[str] = None
    expires: Optional[Union[int, datetime]] = None
    httponly: bool = True
    max_age: Optional[int] = None
    key: str
    path: str = "/"
    samesite: str = SameSiteEnum.LAX.value  # noqa
    secure: bool = True
    value: str


class CookiePayload(BaseModel):
    key_id: str
    key_ttl: int
    data_model: str
    remainder: Optional[list[str]] = []


class CookieType(UniqueEnum):
    """An enumeration of the types of cookies available and their associated data model

    Sesh does not impose any limit on the number of cookies that it can handle,
    limited only by system resource availability. Each cookie represents a
    particular slice of state that is represented by a Pydantic model. Sesh
    stores a string identifier inside the cookie of the name of the model that
    is to be hydrated by the data in the cookie or the data returned from the
    cache or other database when referenced by a UUID stored in the cookie. Each
    cookie references one model and each model should only be used by one cookie,
    unless it is reused as a result of composition in another model.

    This enum is a subclass of the UniqueEnum class from the aenum library. This
    allows us to store additional attributes with the value of the enum members.
    It also allows the enum to be extended ad hoc by the end user. An example of
    this is provided in the `cookies.py` module of the example application.

    The CookieBase referenced here is to be used for cookies that store all
    state internally and do not have a UUID that references records or keys in
    an external database.

    See Also:
        https://stackoverflow.com/a/19300424

        https://github.com/ethanfurman/aenum/blob/master/aenum/doc/aenum.rst#allowed-members-and-attributes-of-enumerations

        https://github.com/ethanfurman/aenum/blob/master/aenum/doc/aenum.rst#extend_enum

    Attributes:
        model_class (:obj: `KeyBase`): Subclass of KeyBase used as data model for cookie.
        model (str): Name of model subclass.
    """
    _init_ = 'model_class model'
    COOKIE = CookiePayload, 'CookiePayload'
