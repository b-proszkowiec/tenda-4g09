"""Models for Tenda 4G09 SIM messages."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SimMessage:
    """SMS message stored on SIM."""

    index: int
    status: int
    sender: str
    date: str
    message: str

    @classmethod
    def from_dict(cls, data: dict) -> SimMessage:
        """Create SIM message from router response."""

        return cls(
            index=int(data["index"]),
            status=int(data["status"]),
            sender=data["phone"],
            date=data["date"],
            message=data["msg"],
        )
