"""Models for Tenda 4G09 system logs."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SystemLog:
    """Router system log entry."""

    index: int
    time: str
    type: str
    message: str

    @classmethod
    def from_dict(cls, data: dict) -> SystemLog:
        """Create system log from router response."""

        return cls(
            index=int(data["index"]),
            time=data["time"],
            type=data["type"],
            message=data["log"],
        )
