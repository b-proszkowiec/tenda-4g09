from .described_enum import DescribedIntEnum


class SimStatus(DescribedIntEnum):
    READY = 0, "Ready"
    NO_SIM_CARD = 1, "No SIM card"
    BLOCKED = 2, "Blocked"
    PIN_REQUIRED = 3, "PIN required"
    PUK_REQUIRED = 4, "PUK required"
    PIN_UNLOCKED = 5, "PIN unlocked"


class ConnectionState(DescribedIntEnum):
    DISCONNECTED = 0, "Disconnected"
    CONNECTED = 1, "Connected"


class EnableState(DescribedIntEnum):
    DISABLED = 0, "Disabled"
    ENABLED = 1, "Enabled"
