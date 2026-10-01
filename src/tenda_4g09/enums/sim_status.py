from enum import IntEnum


class SimStatus(IntEnum):
    READY = (0, "Ready")
    NO_SIM_CARD = (1, "No SIM card")
    BLOCKED = (2, "Blocked")
    PIN_REQUIRED = (3, "PIN required")
    PUK_REQUIRED = (4, "PUK required")
    PIN_UNLOCKED = (5, "PIN unlocked")

    def __new__(cls, value, description):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.description = description
        return obj

    def __str__(self) -> str:
        return self.description
