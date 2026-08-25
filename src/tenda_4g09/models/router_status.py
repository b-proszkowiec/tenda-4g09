from __future__ import annotations

from dataclasses import dataclass

from .sim_info import SimInfo
from .wan_info import WanInfo

@dataclass(frozen=True)
class RouterStatus:
    double_band: bool
    wl24g_enabled: bool
    wl24g_name: str
    wl5g_enabled: bool
    wl5g_name: str
    lineup: str
    client_num: int
    black_num: int
    list_num: int
    device_name: str
    lan_ip: str
    lan_mac: str
    work_mode: str
    ap_status: str
    wan_info: list[WanInfo]
    country_code: str
    sim_info: SimInfo

    @classmethod
    def from_dict(cls, data: dict) -> RouterStatus:
        return cls(
            double_band=data["doubleBand"] == "1",
            wl24g_enabled=data["wl24gEn"] == "1",
            wl24g_name=data["wl24gName"],
            wl5g_enabled=data["wl5gEn"] == "1",
            wl5g_name=data["wl5gName"],
            lineup=data["lineup"],
            client_num=int(data["clientNum"]),
            black_num=int(data["blackNum"]),
            list_num=int(data["listNum"]),
            device_name=data["deviceName"],
            lan_ip=data["lanIP"],
            lan_mac=data["lanMAC"],
            work_mode=data["workMode"],
            ap_status=data["apStatus"],
            wan_info=[
                WanInfo.from_dict(item)
                for item in data["wanInfo"]
            ],
            country_code=data["countryCode"],
            sim_info=SimInfo.from_dict(data["simInfo"]),
        )
