"""Models for Tenda 4G09 router status."""

from __future__ import annotations

from dataclasses import dataclass

from ..enums import SignalQuality

@dataclass(frozen=True)
class RouterWanInfo:
    """WAN information from router status."""

    status: str
    ip: str
    upload_speed: float
    download_speed: float

    @classmethod
    def from_dict(cls, data: dict) -> RouterWanInfo:
        """Create WAN information from router response."""

        return cls(
            status=data["wanStatus"],
            ip=data["wanIp"],
            upload_speed=float(data["wanUploadSpeed"]),
            download_speed=float(data["wanDownloadSpeed"]),
        )


@dataclass(frozen=True)
class RouterSimInfo:
    """Current cellular connection information."""

    sim_status: int
    internet_status: int
    rssi: SignalQuality
    connection_type: str
    upload_speed: float
    download_speed: float
    wan_ip: str
    limit_data: int

    @classmethod
    def from_dict(cls, data: dict) -> RouterSimInfo:
        """Create SIM information from router response."""

        return cls(
            sim_status=int(data["simStatus"]),
            internet_status=int(data["internetStatus"]),
            rssi=SignalQuality(int(data["rssi"])),
            connection_type=data["connectionType"],
            upload_speed=float(data["uploadSpeed"]),
            download_speed=float(data["downloadSpeed"]),
            wan_ip=data["wanIp"],
            limit_data=int(data["limitData"]),
        )


@dataclass(frozen=True)
class OnlineUpgradeInfo:
    """Firmware upgrade information."""

    new_version_exists: bool
    new_version: str
    current_version: str

    @classmethod
    def from_dict(cls, data: dict) -> OnlineUpgradeInfo:
        """Create upgrade information from router response."""

        return cls(
            new_version_exists=data["newVersionExist"] == "1",
            new_version=data["newVersion"],
            current_version=data["curVersion"],
        )


@dataclass(frozen=True)
class RouterStatus:
    """Current router status."""

    double_band: bool
    wifi_24g_enabled: bool
    wifi_24g_name: str
    wifi_5g_enabled: bool
    wifi_5g_name: str
    lineup: str
    client_count: int
    black_count: int
    list_count: int
    device_name: str
    lan_ip: str
    lan_mac: str
    work_mode: str
    ap_status: str
    wan_info: list[RouterWanInfo]
    country_code: str
    online_upgrade: OnlineUpgradeInfo
    sim_info: RouterSimInfo

    @classmethod
    def from_dict(cls, data: dict) -> RouterStatus:
        """Create router status from router response."""

        return cls(
            double_band=data["doubleBand"] == "1",
            wifi_24g_enabled=data["wl24gEn"] == "1",
            wifi_24g_name=data["wl24gName"],
            wifi_5g_enabled=data["wl5gEn"] == "1",
            wifi_5g_name=data["wl5gName"],
            lineup=data["lineup"],
            client_count=int(data["clientNum"]),
            black_count=int(data["blackNum"]),
            list_count=int(data["listNum"]),
            device_name=data["deviceName"],
            lan_ip=data["lanIP"],
            lan_mac=data["lanMAC"],
            work_mode=data["workMode"],
            ap_status=data["apStatus"],
            wan_info=[
                RouterWanInfo.from_dict(item)
                for item in data["wanInfo"]
            ],
            country_code=data["countryCode"],
            online_upgrade=OnlineUpgradeInfo.from_dict(
                data["onlineUpgradeInfo"]
            ),
            sim_info=RouterSimInfo.from_dict(
                data["simInfo"]
            ),
        )
