import requests

from .cell_location import CellLocation

def get_bts_search_data(cell_id: int, pci: int) -> CellLocation:
    """Retrieve cell location data from BTSearch."""

    url = "https://btsearch.pl/api/v2/search"
    params = {
        "q": f"ecid:{cell_id} lte_pci:{pci}",
        "statuses": "active",
        "include": "operator,location.region",
    }

    response = requests.get(url, params=params, timeout=5)
    response.raise_for_status()

    data = response.json()["data"]
    if not data:
        raise LookupError(
            f"No BTS found for cell_id={cell_id}, pci={pci}"
        )

    location = data[0]["location"]

    address = " ".join(
        part
        for part in (
            location.get("address") + ',',
            location.get("city") + ' -',
            (location.get("region") or {}).get("name"),
        )
        if part
    )

    return CellLocation(
        address,
        location.get("latitude"),
        location.get("longitude"),
    )
