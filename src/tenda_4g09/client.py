"""Client for Tenda 4G09 router."""

from __future__ import annotations

from typing import Any

import requests

from .auth import Auth, Credentials
from .models import (
    OnlineClient,
    RouterStatus,
    SimMessage,
    SimWanInfo,
    SystemLog,
    SystemStatus,
)


class Tenda4G09:
    """Client for Tenda 4G09 router."""

    def __init__(
        self,
        host: str,        
        password: str,
        username: str = "admin",
    ) -> None:
        """Initialize the client."""

        self.host = host.rstrip("/")
        self._session = requests.Session()
        self._base_url = f"http://{host.rstrip('/')}"
        self.username = username
        self.password = password
        

        self.auth = Auth(
            session=self._session,
            base_url=self._base_url,
            credentials=Credentials(
                username=username,
                password=password,
            ),
        )

    def login(self) -> None:
        """Authenticate with the router."""

        self.auth.login()

    def logout(self) -> None:
        """Log out from the router."""

        self.auth.logout()

    @property
    def logged_in(self) -> bool:
        """Return whether the client is authenticated."""

        return self.auth.logged_in


    def _request(
        self,
        method: str,
        path: str,
        **kwargs: Any,
    ) -> Any:
        """Send a request to the router."""

        if not self.logged_in:
            self.login()

        response = self._session.request(
            method,
            f"http://{self.host}{path}",
            timeout=10,
            **kwargs,
        )
        response.raise_for_status()

        return response.json()

    def get_status(self) -> RouterStatus:
        """Get router status."""

        data = self._request(
            "GET",
            "/goform/GetRouterStatus",
        )

        return RouterStatus.from_dict(data)

    def get_sim_wan_info(self) -> SimWanInfo:
        """Get SIM WAN configuration."""

        data = self._request(
            "GET",
            "/goform/getSimWanInfo",
        )

        return SimWanInfo.from_dict(data)

    def get_system_status(self) -> SystemStatus:
        """Get detailed system status."""

        data = self._request(
            "GET",
            "/goform/GetSystemStatus",
        )

        return SystemStatus.from_dict(data)

    def get_online_clients(self) -> list[OnlineClient]:
        """Get currently connected clients."""

        data = self._request(
            "GET",
            "/goform/getOnlineList",
        )

        return [
            OnlineClient.from_dict(item)
            for item in data
            if "deviceId" in item
        ]

    def get_sim_messages(self) -> list[SimMessage]:
        """Get SIM messages."""

        data = self._request(
            "GET",
            "/goform/getSimList",
        )

        return [
            SimMessage.from_dict(item)
            for item in data
            if "index" in item
        ]

    def get_system_logs(self) -> list[SystemLog]:
        """Get system logs."""

        data = self._request(
            "GET",
            "/goform/GetSySLogCfg",
        )

        return [
            SystemLog.from_dict(item)
            for item in data
        ]

    def is_mobile_data_connected(self, status: RouterStatus | None = None) -> bool:
        """Whether the mobile WAN connection is active."""

        if status is None:
            status = self.get_status()

        return status.sim_info.internet_status == 1

    def mobile_data_connect(self) -> None:
        """Reconnect the mobile WAN connection."""

        self._request(
            "POST",
            "/goform/setSimWanInfo",
            data={
                "action": "1",
            },
        )

    def __enter__(self) -> Tenda4G09:
        """Log in when entering a context manager."""

        self.login()

        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ) -> bool:
        """Log out when leaving a context manager."""

        self.logout()

        return False
