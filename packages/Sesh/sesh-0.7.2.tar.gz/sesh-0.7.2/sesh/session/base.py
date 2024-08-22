
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
from typing import Optional, Union

from fastapi import HTTPException, Request, Response

from sesh.backend.base import SessionStore
from sesh.models.key import KeyBase


class Session(ABC):
    @abstractmethod
    def __init__(self) -> None:
        raise NotImplementedError()

    @property
    @abstractmethod
    def auto_error(self) -> bool:
        raise NotImplementedError()

    @property
    @abstractmethod
    def auth_http_exception(self) -> HTTPException:
        raise NotImplementedError()

    @property
    @abstractmethod
    def backend(self) -> SessionStore:
        raise NotImplementedError()

    @property
    @abstractmethod
    def created_date(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def created_by(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def data_model(self):
        raise NotImplementedError()

    @property
    def key(self):
        raise NotImplementedError()

    @property
    def value(self):
        raise NotImplementedError()

    @value.setter
    def value(self, new_value):
        raise NotImplementedError()

    @abstractmethod
    async def get_state_data(
            self,
            request: Request,
            response: Response,
    ) -> Optional[dict[str, KeyBase]]:
        raise NotImplementedError()

    @abstractmethod
    async def verify_session(
            self,
            request: Request,
            response: Response,
            login_route: bool
    ) -> bool:
        raise NotImplementedError()

    @abstractmethod
    async def __call__(
        self,
        request: Request,
        response: Response,
        login_route: bool = False
    ) -> Optional[Union[bool, dict[str, KeyBase]]]:
        raise NotImplementedError()
