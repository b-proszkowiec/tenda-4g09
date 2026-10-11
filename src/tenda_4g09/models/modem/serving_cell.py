
from dataclasses import dataclass
import re


@dataclass
class LTEServingCell:
    state: str
    rat: str
    duplex: str
    mcc: str
    mnc: str
    cell_id: int
    pci: int
    earfcn: int
    band: int
    ul_bandwidth: int
    dl_bandwidth: int
    tac: int
    rsrp: int
    rsrq: int
    rssi: int
    sinr: float
    cqi: int
    tx_power: int
    srxlev: str

    @classmethod
    def from_qeng(cls, response: str) -> "LTEServingCell":
        match = re.search(
            r'\+QENG:\s*"servingcell",(.+)',
            response
        )

        if not match:
            raise ValueError(
                f"Invalid response AT+QENG: {response}"
            )

        fields = [
            value.strip().strip('"')
            for value in match.group(1).strip().split(",")
        ]

        if len(fields) != 19:
            raise ValueError(
                f"Invalid length, expected 19 but received {len(fields)}"
            )

        return cls(
            state=fields[0],
            rat=fields[1],
            duplex=fields[2],
            mcc=fields[3],
            mnc=fields[4],
            cell_id=int(fields[5],16),
            pci=int(fields[6]),
            earfcn=int(fields[7]),
            band=int(fields[8]),
            ul_bandwidth=int(fields[9]),
            dl_bandwidth=int(fields[10]),
            tac=int(fields[11],16),
            rsrp=int(fields[12]),
            rsrq=int(fields[13]),
            rssi=int(fields[14]),
            sinr=float(fields[15]),
            cqi=int(fields[16]),
            tx_power=int(fields[17]),
            srxlev=fields[18],
        )

    @property
    def cell_id_hex(self) -> str:
        """Cell ID provided in hexadecimal format"""
        return hex(self.cell_id)

    @property
    def tac_hex(self) -> str:
        """TAC provided in hexadecimal format"""
        return hex(self.tac)
