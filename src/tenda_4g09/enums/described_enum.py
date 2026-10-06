from enum import IntEnum


class DescribedIntEnum(IntEnum):
    def __new__(cls, value, description):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.description = description
        return obj

    def __str__(self) -> str:
        return self.description
