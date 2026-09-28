"""Client for communicating with a Tenda 4G09 router."""

from __future__ import annotations

import requests

from .auth import Auth, Credentials
from .exceptions import TendaAuthenticationError
from .models.router_status import RouterStatus
from .models.sim_wan import SimWanInfo

class Tenda4G09:
    """Client for the Tenda 4G09 router."""

    def __init__(
        self,
        host: str,
        username: str = "admin",
        password: str = "",
    ) -> None:
        """Initialize the client."""

        self._base_url = f"http://{host.rstrip('/')}"

        self._session = requests.Session()

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

    def get_status(self) -> RouterStatus:
        """Get the current router status."""

        if not self.logged_in:
            raise TendaAuthenticationError(
                "Client is not authenticated."
            )

        response = self._session.get(
            f"{self._base_url}/goform/GetRouterStatus",
            timeout=10,
        )
        response.raise_for_status()

        return RouterStatus.from_dict(response.json())

    def get_sim_wan_info(self) -> SimWanInfo:
        """Get SIM/WAN information."""

        if not self.logged_in:
            raise TendaAuthenticationError(
                "Client is not authenticated."
            )

        response = self._session.get(
            f"{self._base_url}/goform/getSimWanInfo",
            timeout=10,
        )
        response.raise_for_status()

        return SimWanInfo.from_dict(response.json())

    def is_lte_connected(self) -> bool:
        """Return whether LTE WAN is connected."""

        info = self.get_sim_wan_info()

        return info.internet_status == "Connected"

    def lte_connect(self) -> dict:
        """Reconnect the LTE WAN connection."""

        if not self.logged_in:
            raise TendaAuthenticationError(
                "Client is not authenticated."
            )

        target_action = 1

        info = self.get_sim_wan_info()
        sim_info = info.sim_info[info.profile_index]

        data = {
            "mobileData": info.mobile_data,
            "dataRoaming": info.data_roaming,
            "dataOptions": info.data_options,
            "profileIndex": info.profile_index,
            "pdpType": sim_info.pdp_type,
            "apn": sim_info.apn,
            "simUser": sim_info.sim_user,
            "simPwd": sim_info.sim_pwd,
            "authType": sim_info.auth_type,
            "action": target_action,
        }

        response = self._session.post(
            f"{self._base_url}/goform/setSimWanInfo",
            data=data,
            timeout=5,
        )
        response.raise_for_status()

        return response.json()

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
