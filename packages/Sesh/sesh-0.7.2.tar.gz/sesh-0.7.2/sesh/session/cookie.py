
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
from types import MethodType
from typing import Callable, Optional, Type, Union

from fastapi import HTTPException, Request, Response
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from loguru import logger

from sesh.backend.base import SessionStore
from sesh.exceptions import SessionError
from sesh.models.cookie import Cookie, CookiePayload, CookieType, SameSiteEnum
from sesh.models.key import KeyBase
from sesh.session.base import Session


class CookieSession(Session):

    def __init__(
        self,
        *,
        cookie_type: CookieType,
        created_by: Union[int, str],
        domain: Optional[str],
        max_age: Optional[int],
        auth_http_exception: HTTPException = HTTPException(status_code=401, detail="Unauthorized"),
        auto_error: bool = True,
        backend: Optional[SessionStore] = None,
        cookie_packer: Optional[Callable] = None,
        cookie_parser: Optional[Callable] = None,
        cookie_processor: Optional[Callable] = None,
        created_date: str = datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        expires: Optional[Union[int, datetime]] = None,
        httponly: bool = True,
        path: str = "/",
        salt: Optional[str] = None,
        samesite: SameSiteEnum = SameSiteEnum.LAX,
        secret_key: Optional[str] = None,
        secure: bool = True,
        signer: Optional[Type[URLSafeTimedSerializer]] = URLSafeTimedSerializer,
        value: str = '',
    ):
        self._auto_error = auto_error
        self._auth_http_exception = auth_http_exception
        self._backend = backend
        self._cookie_type = cookie_type
        self._created_date = created_date
        self._created_by = created_by
        self._data_model = cookie_type.model_class

        if not backend and (not cookie_packer or not cookie_parser or not cookie_processor):
            raise SessionError(
                'cookie_session', "Must provide either a backend or a cookie packer, parser, and processor."
            )

        if cookie_packer or cookie_parser or cookie_processor:
            msg = "Cannot provide cookie_packer or cookie_parser or cookie_processor without providing all three."
            assert cookie_packer and cookie_parser and cookie_processor, msg
            self._cookie_packer = MethodType(cookie_packer, self)
            self._cookie_parser = MethodType(cookie_parser, self)
            self._cookie_processor = MethodType(cookie_processor, self)
        else:
            self._cookie_packer = self.default_packer
            self._cookie_parser = self.default_parser
            # NOTE: There is never a default cookie processor as these are only used for cookies that
            # do not have an associated KeyModel
            self._cookie_processor = None

        if salt or secret_key or signer:
            msg = "If providing salt, secret_key, or signer, must provide all three."
            assert salt and secret_key and signer, msg

        self._salt = salt
        self._secret_key = secret_key
        self._signer = signer

        self._domain = domain
        self._expires = expires
        self._httponly = httponly
        self._max_age = max_age
        self._key = cookie_type.name.lower()
        self._path = path
        self._samesite = samesite
        self._secure = secure
        self._value = value

        self._cookie_model = Cookie

    @property
    def auto_error(self) -> bool:
        return self._auto_error

    @property
    def auth_http_exception(self) -> HTTPException:
        return self._auth_http_exception

    @property
    def backend(self) -> SessionStore:
        return self._backend

    @property
    def created_date(self):
        return self._created_date

    @property
    def created_by(self):
        return self._created_by

    @property
    def cookie_packer(self):
        return self._cookie_packer

    @property
    def cookie_parser(self):
        return self._cookie_parser

    @property
    def cookie_processor(self):
        return self._cookie_processor

    @property
    def data_model(self):
        return self._data_model

    @property
    def salt(self):
        return self._salt

    @property
    def secret_key(self):
        return self._secret_key

    @property
    def signer(self):
        if self._signer:
            return self._signer(self.secret_key, self.salt)
        else:
            return None

    @property
    def cookie_type(self):
        return self._cookie_type

    @property
    def domain(self):
        return self._domain

    @property
    def expires(self):
        return self._expires

    @property
    def httponly(self):
        return self._httponly

    @property
    def max_age(self):
        return self._max_age

    @property
    def key(self):
        return self._key

    @property
    def path(self):
        return self._path

    @property
    def samesite(self):
        return self._samesite

    @property
    def secure(self):
        return self._secure

    @property
    def cookie_model(self):
        return self._cookie_model

    def make_cookie(self) -> Cookie:
        cookie = Cookie(
            domain=self.domain,
            expires=self.expires,
            httponly=self.httponly,
            max_age=self.max_age,
            key=self.key,
            path=self.path,
            samesite=self.samesite.value,
            secure=self.secure,
            value=''
        )
        logger.debug(f"Newly Made Cookie: {cookie}")

        return cookie

    def get_cookie_payload(self, signed_payload: Union[str, bytes]) -> str:
        if self.signer and signed_payload:
            try:
                payload = self.signer.loads(
                        signed_payload,
                        max_age=self.max_age,
                        return_timestamp=False,
                )
            except (SignatureExpired, BadSignature):
                raise HTTPException(status_code=401, detail="Unauthorized")
        else:
            payload = signed_payload
            logger.error(f"PAYLOAD GOT: {payload}")
        return payload

    @staticmethod
    def default_packer(payload: CookiePayload):
        payload_string = '.'.join(
            [payload.key_id, str(payload.key_ttl), payload.data_model, *payload.remainder]
        )
        return payload_string

    def default_parser(self, signed_payload: Union[str, bytes]) -> CookiePayload:
        decrypted_payload: str = self.get_cookie_payload(signed_payload)
        parts: list = decrypted_payload.split('.')
        payload: CookiePayload = CookiePayload(
            key_id=parts[0],
            key_ttl=int(parts[1]),
            data_model=parts[2],
            remainder=parts[3:]
        )

        return payload

    def pack_payload(self, payload: CookiePayload):
        logger.debug(f"CookiePayload: {payload}")
        packed_payload = self.cookie_packer(payload)  # type: ignore

        return packed_payload

    def parse_cookie(self, signed_payload: Union[str, bytes]) -> Optional[CookiePayload]:
        if signed_payload:
            payload = self.cookie_parser(signed_payload)  # type: ignore
        else:
            payload = None

        return payload

    def process_cookie(self, request: Request, response: Response, payload: CookiePayload):
        logger.debug(f"PAYLOAD TO PROCESS: {payload}")
        self.cookie_processor(request, response, payload)

        return

    def attach_to_response(self, payload: str, response: Response) -> None:
        cookie = self.make_cookie()
        if self.signer:
            cookie.value = str(self.signer.dumps(payload))
        else:
            cookie.value = payload
        logger.debug(f"COOKIE VALUE: {cookie.value}")
        response.set_cookie(
            **cookie.model_dump()
        )

        return

    @staticmethod
    def delete_from_response(response: Response, cookie: Cookie) -> None:
        response.delete_cookie(
            key=cookie.key,
            path=cookie.path,
            domain=cookie.domain,
        )

        return

    async def get_state_data(
            self,
            request: Request,
            response: Response,
    ) -> Optional[dict[str, KeyBase]]:
        state_data = None

        if str(request.url).endswith(self.path):
            logger.debug(f"Getting state data for path: {str(request.url)}")
            signed_payload: str = request.cookies.get(self.key)
            payload: CookiePayload = self.parse_cookie(signed_payload)
            if issubclass(self.data_model, CookiePayload) and signed_payload:
                # Cookie is a container cookie
                logger.debug(f"Processing cookie: {payload.data_model}")
                self.process_cookie(request, response, payload)
            elif signed_payload:
                # Cookie is used to look up a session id in storage backend and return a data_model to the route
                logger.debug(f"Hydrating model: {payload.data_model}")
                state_data = await self.backend.read(payload.key_id, self.data_model)
                logger.debug(f"AWAITED DATA: {state_data}")

        return state_data

    async def verify_session(
            self,
            request: Request,
            response: Response,
            login_route: bool
    ) -> Optional[Union[bool, dict[str, KeyBase]]]:
        """If the session exists, it is valid"""
        # TODO: Process other potential parts of AuthModel, like RBAC
        signed_payload: str = request.cookies.get(self.key)
        validated: bool
        result = None
        if signed_payload:
            # If there is no signed_payload, then the auth cookie was not present in the request
            payload: CookiePayload = self.parse_cookie(signed_payload)
            validated = bool(await self.backend.check_for_key(payload.key_id))
            if validated:
                await self.backend.refresh_key_ttl(payload.key_id, payload.key_ttl)
                if login_route:
                    result = await self.get_state_data(request, response)
                else:
                    result = validated
        else:
            if login_route:
                return False
            if self.auto_error:
                raise HTTPException(status_code=401, detail="Unauthorized")
            else:
                raise SessionError('validator', 'Unauthorized')

        return result

    async def __call__(
        self,
        request: Request,
        response: Response,
        auth_only: bool = False,
        login_route: bool = False
    ) -> Optional[Union[bool, dict[str, KeyBase]]]:
        # Get any cookies needed for this call
        logger.info(f"URL: {str(request.url)}")
        validated = await self.verify_session(request, response, login_route)

        if auth_only:
            return validated

        state_data = None

        if validated or login_route:
            try:
                state_data = await self.get_state_data(request, response)
            except SessionError as error:
                if self.auto_error:
                    raise HTTPException(
                        status_code=503,
                        detail="There is a problem with the session validation service."
                    )
                raise error
        return state_data
