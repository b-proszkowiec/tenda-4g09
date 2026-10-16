LTE_BANDWIDTHS = {
    0: 1.4,
    1: 3,
    2: 5,
    3: 10,
    4: 15,
    5: 20,
}

def get_bandwidth(bandwidth: int) -> float | None:
    return LTE_BANDWIDTHS.get(bandwidth)
