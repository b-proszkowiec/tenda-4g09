"""Models for Tenda 4G09 connected clients."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class OnlineClient:
    """Connected network client."""

    device_id: str
    ip: str
    name: str
    line: int
    upload_speed: float
    download_speed: float
    link_type: str
    blocked: bool
    guest: bool

    @classmethod
    def from_dict(cls, data: dict) -> OnlineClient:
        """Create online client from router response."""

        return cls(
            device_id=data["deviceId"],
            ip=data["ip"],
            name=data["devName"],
            line=int(data["line"]),
            upload_speed=float(data["uploadSpeed"]),
            download_speed=float(data["downloadSpeed"]),
            link_type=data["linkType"],
            blocked=bool(data["black"]),
            guest=data["isGuestClient"] == "true",
        )

    def __str__(self) -> str:
        return (
            f"Client: {self.name} ({self.ip})\n"
            f"  Device ID: {self.device_id}\n"
            f"  Upload: {self.upload_speed:.2f} kB/s\n"
            f"  Download: {self.download_speed:.2f} kB/s\n"
            f"  Blocked: {'Yes' if self.blocked else 'No'}\n"
            f"  Guest: {'Yes' if self.guest else 'No'}"
        )
