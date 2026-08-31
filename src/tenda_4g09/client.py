from __future__ import annotations

import requests
import logging

from time import sleep, perf_counter

from .auth import Auth, Credentials
from .models.router_status import RouterStatus
from .models.sim_wan_info import SimWanInfo
from .exceptions import *


logger = logging.getLogger(__name__)

class Tenda4G09:

    def __init__(
        self,
        host: str,
        username: str = "admin",
        password: str = "",
    ) -> None:
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
        self.auth.login()

    def logout(self) -> None:
        self.auth.logout()

    @property
    def logged_in(self) -> bool:
        return self.auth.logged_in

    def get_status(self) -> RouterStatus:
        if not self.logged_in:
            raise TendaAuthenticationError("Client is not authenticated.")

        response = self._session.get(
            f"{self._base_url}/goform/GetRouterStatus",
            timeout=10,
        )
        response.raise_for_status()

        return RouterStatus.from_dict(response.json())

    def get_sim_wan_info(self) -> SimWanInfo:
        if not self.logged_in:
            raise TendaAuthenticationError("Client is not authenticated.")

        response = self._session.get(
            f"{self._base_url}/goform/getSimWanInfo",
            timeout=10,
        )
        response.raise_for_status()

        return SimWanInfo.from_dict(response.json())

    def is_mobile_data_connected(self) -> bool:
        info: SimWanInfo = self.get_sim_wan_info()

        return info.internet_status == "Connected"

    def connect_mobile_data(self, timeout: int = 6) -> bool:
        if not self.logged_in:
            raise TendaAuthenticationError("Client is not authenticated.")

        TARGET_ACTION = 1
        info: SimWanInfo = self.get_sim_wan_info()

        is_connected = info.internet_status == "Connected"
        if is_connected == TARGET_ACTION:
            logger.info("Required state is already fulfilled. Skipping.")
            return True

        start = perf_counter()
        while(True):
            self._send_connection_request(info, TARGET_ACTION)
            if self.is_mobile_data_connected():
                return True

            sleep(0.5)
            if (perf_counter() - start) >= timeout:
                break

        return False

    def _send_connection_request(self, info: SimWanInfo, required_status: int):
        simInfo = info.sim_info[info.profile_index]
        data = {
            "mobileData": info.mobile_data,
            "dataRoaming": info.data_roaming,
            "dataOptions": info.data_options,
            "profileIndex": info.profile_index,
            "pdpType": simInfo.pdp_type, 
            "apn": simInfo.apn,
            "simUser": simInfo.sim_user,
            "simPwd": simInfo.sim_pwd,
            "authType": simInfo.auth_type,
            "action": required_status
        }
        response = self._session.post(
            f"{self._base_url}/goform/setSimWanInfo",
            data=data,
            timeout=3,
        )
        response.raise_for_status()
        return response.json()

    def __enter__(self):
        self.auth.login()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.auth.logout()
        return True
