from dataclasses import dataclass
from typing import Any


@dataclass
class DataLimitSetting:
    total_used_mb: str
    data_limit: str
    monthly_allowance: str
    unit: str
    usage_alert: str
    sms_usage: str
    monthly_statistics: str
    start_date: str
    time_up: str
    limit_data: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DataLimitSetting:
        return cls(
            total_used_mb=data["totalUsed"],
            data_limit=data["dataLimit"],
            monthly_allowance=data["monthlyAllowance"],
            unit=data["unit"],
            usage_alert=data["usageAlert"],
            sms_usage=data["smsUsage"],
            monthly_statistics=data["monthlyStatistics"],
            start_date=data["startDate"],
            time_up=data["timeUp"],
            limit_data=data["limitData"],
        )
