from .described_enum import DescribedIntEnum


class SignalQuality(DescribedIntEnum):
    NO_SIGNAL = 0, "No signal"
    FAIR = 1, "Fair"
    GOOD = 2, "Good"
    EXCELLENT = 3, "Excellent"
