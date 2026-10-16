from typing import Any
from collections.abc import Awaitable, Callable

from .provider import *
from .cell_location import CellLocation

CellDataProvider = Callable[..., Awaitable[dict[str, Any]]]

COUNTRY_CODE_IMPLEMENTATIONS: dict[str, CellDataProvider] = {
    "260": get_bts_search_data,
}

def get_cell_data(mcc: str, cid: int, pci: int) -> CellLocation:
    provider = COUNTRY_CODE_IMPLEMENTATIONS.get(mcc)
    if provider is None:
        raise NotImplementedError(
            f"Retriving cell data information not implemented for your coountry (MCC={mcc})"
            )

    return provider(cid, pci)
