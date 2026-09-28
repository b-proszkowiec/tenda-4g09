"""Models for Tenda 4G09 system status."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SystemWanInfo:
    """Detailed WAN information."""

    connect_status: int
    connect_time: int
    ip: str
    mask: str
    gateway: str
    upload_speed: float
    download_speed: float
    dns1: str
    dns2: str
    connect_type: str
    mac: str

    @classmethod
    def from_dict(cls, data: dict) -> SystemWanInfo:
        """Create WAN information from router response."""

        return cls(
            connect_status=int(data["adv_connect_status"]),
            connect_time=int(data["adv_connect_time"]),
            ip=data["adv_ip"],
            mask=data["adv_mask"],
            gateway=data["adv_gateway"],
            upload_speed=float(data["wanUploadSpeed"]),
            download_speed=float(data["wanDownloadSpeed"]),
            dns1=data["adv_dns1"],
            dns2=data["adv_dns2"],
            connect_type=data["adv_connect_type"],
            mac=data["adv_mac"],
        )


@dataclass(frozen=True)
class SystemSimInfo:
    """Detailed cellular connection information."""

    sim_status: int
    connection_status: int
    signal_strength: int
    carrier: str
    mobile_network: str
    statistics: float
    upload_speed: float
    download_speed: float
    ip: str
    mask: str
    gateway: str
    dns1: str
    dns2: str
    mac: str

    @classmethod
    def from_dict(cls, data: dict) -> SystemSimInfo:
        """Create cellular information from router response."""

        return cls(
            sim_status=int(data["adv_sim_status"]),
            connection_status=int(data["adv_sim_connsta"]),
            signal_strength=int(data["adv_signal_strength"]),
            carrier=data["adv_carrier"],
            mobile_network=data["adv_mob_net"],
            statistics=float(data["adv_statistics"]),
            upload_speed=float(data["adv_up_speed"]),
            download_speed=float(data["adv_down_speed"]),
            ip=data["adv_ip"],
            mask=data["adv_mask"],
            gateway=data["adv_gateway"],
            dns1=data["adv_dns1"],
            dns2=data["adv_dns2"],
            mac=data["adv_mac"],
        )


@dataclass(frozen=True)
class SystemStatus:
    """Detailed router system status."""

    system_time: str
    uptime: int
    firmware_version: str
    hardware_version: str
    wan_info: list[SystemWanInfo]
    lan_ip: str
    lan_mask: str
    lan_mac: str
    wifi_5g_enabled: bool
    wifi_5g_enabled_config: bool
    wifi_5g_ssid: str
    wifi_5g_security: str
    wifi_5g_channel: int
    wifi_5g_band: int
    wifi_5g_mac: str
    wifi_enabled: bool
    wifi_enabled_config: bool
    wifi_ssid: str
    wifi_security: str
    wifi_channel: int
    wifi_band: int
    wifi_mac: str
    ipv6_enabled: bool
    connection_type: str
    wan_addresses: list[str]
    lan_addresses: list[str]
    gateway: str
    wan_primary_dns: str
    wan_secondary_dns: str
    sim_info: SystemSimInfo

    @classmethod
    def from_dict(cls, data: dict) -> SystemStatus:
        """Create system status from router response."""

        return cls(
            system_time=data["adv_sys_time"],
            uptime=int(data["adv_run_time"]),
            firmware_version=data["adv_firm_ver"],
            hardware_version=data["adv_hard_ver"],
            wan_info=[
                SystemWanInfo.from_dict(item)
                for item in data["wanInfo"]
            ],
            lan_ip=data["adv_lan_ip"],
            lan_mask=data["adv_lan_mask"],
            lan_mac=data["adv_lan_mac"],
            wifi_5g_enabled=data["wifi_enable_5g"] == "1",
            wifi_5g_enabled_config=data["adv_wrl_en_5g"] == "1",
            wifi_5g_ssid=data["adv_wrl_ssid_5g"],
            wifi_5g_security=data["adv_wrl_sec_5g"],
            wifi_5g_channel=int(data["adv_wrl_channel_5g"]),
            wifi_5g_band=int(data["adv_wrl_band_5g"]),
            wifi_5g_mac=data["adv_wrl_mac_5g"],
            wifi_enabled=data["wifi_enable"] == "1",
            wifi_enabled_config=data["adv_wrl_en"] == "1",
            wifi_ssid=data["adv_wrl_ssid"],
            wifi_security=data["adv_wrl_sec"],
            wifi_channel=int(data["adv_wrl_channel"]),
            wifi_band=int(data["adv_wrl_band"]),
            wifi_mac=data["adv_wrl_mac"],
            ipv6_enabled=data["ipv6En"] == "1",
            connection_type=data["conType"],
            wan_addresses=data["wanAddr"],
            lan_addresses=data["lanAddr"],
            gateway=data["gateway"],
            wan_primary_dns=data["wanPreDNS"],
            wan_secondary_dns=data["wanAltDNS"],
            sim_info=SystemSimInfo.from_dict(
                data["simInfo"]
            ),
        )
