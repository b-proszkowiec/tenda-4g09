"""Models for Tenda 4G09 SIM WAN configuration."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SimProfile:
    """SIM connection profile."""

    profile_name: str
    pdp_type: str
    apn: str
    username: str
    password: str
    auth_type: str
    system: bool

    @classmethod
    def from_dict(cls, data: dict) -> SimProfile:
        """Create SIM profile from router response."""

        return cls(
            profile_name=data["profileName"],
            pdp_type=data["pdpType"],
            apn=data["apn"],
            username=data["simUser"],
            password=data["simPwd"],
            auth_type=data["authType"],
            system=data["isSys"] == "1",
        )


@dataclass(frozen=True)
class SimWanInfo:
    """SIM WAN configuration."""

    internet_status: str
    mobile_data: bool
    data_roaming: bool
    data_options: int
    profile_index: int
    sim_status: int
    profiles: list[SimProfile]

    @classmethod
    def from_dict(cls, data: dict) -> SimWanInfo:
        """Create SIM WAN information from router response."""

        return cls(
            internet_status=data["internetStatus"],
            mobile_data=data["mobileData"] == "1",
            data_roaming=data["dataRoaming"] == "1",
            data_options=int(data["dataOptions"]),
            profile_index=int(data["profileIndex"]),
            sim_status=int(data["simStatus"]),
            profiles=[
                SimProfile.from_dict(item)
                for item in data["simInfo"]
            ],
        )

    @property
    def active_profile(self) -> SimProfile | None:
        """Return currently selected SIM profile."""

        index = self.profile_index

        if 0 <= index < len(self.profiles):
            return self.profiles[index]

        return None
