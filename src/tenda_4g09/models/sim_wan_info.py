from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class SimWanInfo:
    internet_status: str
    mobile_data: int
    data_roaming: int
    data_options: int
    profile_index: int
    sim_status:int
    sim_info: list[SimInfo]

    @classmethod
    def from_dict(cls, data: dict) -> SimWanInfo:
        return cls(
            internet_status=data["internetStatus"],
            mobile_data=int(data["mobileData"]),
            data_roaming=int(data["dataRoaming"]),
            data_options=int(data["dataOptions"]),
            profile_index=int(data["profileIndex"]),
            sim_status=int(data["simStatus"]),
            sim_info=[
                SimInfo.from_dict(item)
                for item in data["simInfo"]
            ]
        )


@dataclass(frozen=True)
class SimInfo:
    profile_name: str
    pdp_type: str
    apn: str
    sim_user: str
    sim_pwd: str
    auth_type: str
    is_sys: int

    @classmethod
    def from_dict(cls, data: dict) -> SimInfo:
        return cls(
            profile_name=data["profileName"],
            pdp_type=data["pdpType"],
            apn=data["apn"],
            sim_user=data["simUser"],
            sim_pwd=data["simPwd"],
            auth_type=data["authType"],
            is_sys=int(data["isSys"])
        )
