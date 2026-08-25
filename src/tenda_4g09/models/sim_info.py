from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class SimInfo:
    sim_status: str
    internet_status: str
    rssi: str
    connection_type: str
    upload_speed: float
    download_speed: float
    wan_ip: str
    limit_data: str

    @classmethod
    def from_dict(cls, data: dict) -> SimInfo:
        return cls(
            sim_status=data["simStatus"],
            internet_status=data["internetStatus"],
            rssi=data["rssi"],
            connection_type=data["connectionType"],
            upload_speed=float(data["uploadSpeed"]),
            download_speed=float(data["downloadSpeed"]),
            wan_ip=data["wanIp"],
            limit_data=data["limitData"],
        )
