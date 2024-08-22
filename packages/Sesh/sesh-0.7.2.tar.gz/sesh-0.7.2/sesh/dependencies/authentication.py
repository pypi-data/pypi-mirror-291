
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


from fastapi import Depends, HTTPException, Request, Response

from sesh.session.base import Session


def get_request(request: Request):
    return request


def get_response(response: Response):
    return response


def get_state(session_factory: Session):
    async def get_session_data(request=Depends(get_request), response=Depends(get_response)):
        state_data = await session_factory(request, response)

        return state_data
    return get_session_data


def login_check(session_factory: Session):
    async def check_auth(request=Depends(get_request), response=Depends(get_response)):
        state_data: dict = await session_factory(request, response, auth_only=True, login_route=True)

        return state_data
    return check_auth


def user_auth(session_factory: Session):
    async def get_auth(request=Depends(get_request), response=Depends(get_response)):
        await session_factory(request, response, auth_only=True)

    return get_auth
