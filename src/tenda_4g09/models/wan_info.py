from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class WanInfo:
    wan_status: str
    wan_ip: str
    wan_upload_speed: float
    wan_download_speed: float

    @classmethod
    def from_dict(cls, data: dict) -> WanInfo:
        return cls(
            wan_status=data["wanStatus"],
            wan_ip=data["wanIp"],
            wan_upload_speed=float(data["wanUploadSpeed"]),
            wan_download_speed=float(data["wanDownloadSpeed"]),
        )
