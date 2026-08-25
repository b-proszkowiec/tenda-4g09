from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import TYPE_CHECKING

from .exceptions import *

if TYPE_CHECKING:
    import requests


@dataclass(frozen=True)
class Credentials:

    username: str = "admin"
    password: str = ""


class Auth:

    def __init__(
        self,
        session: requests.Session,
        base_url: str,
        credentials: Credentials,
    ) -> None:
        self._session = session
        self._base_url = base_url.rstrip("/")
        self._credentials = credentials
        self._logged_in = False

    @property
    def logged_in(self) -> bool:
        return self._logged_in

    @staticmethod
    def _hash_password(password: str) -> str:
        return hashlib.md5(
            password.encode("utf-8")
        ).hexdigest()

    def login(self) -> None:

        self.logout()

        url = f"{self._base_url}/login/Auth"

        data = {
            "username": self._credentials.username,
            "password": self._hash_password(
                self._credentials.password
            ),
        }

        headers = {
            "Connection": "keep-alive",
            "Origin": self._base_url,
        }

        try:
            response = self._session.post(
                url,
                data=data,
                headers=headers,
                allow_redirects=False,
                timeout=10,
            )
        except ConnectionError:
            raise TendaConnectionError(
                "Failed to connect to the target device."
            )

        location = response.headers.get("Location", "")
        password_cookie = self._session.cookies.get("password")

        authenticated = (
            response.status_code == 302
            and location == f"{self._base_url}/main.html"
            and password_cookie is not None
        )

        if not authenticated:
            self._logged_in = False
            raise TendaAuthenticationError(
                "Authentication with target router failed."
            )

        self._logged_in = True

    def logout(self) -> None:
        if not self._logged_in:
            return

        url = f"{self._base_url}/goform/exit"

        try:
            self._session.get(
                url,
                timeout=10,
            )
        finally:
            self._session.cookies.clear()
            self._logged_in = False
