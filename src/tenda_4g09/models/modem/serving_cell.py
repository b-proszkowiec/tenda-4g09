import re

from dataclasses import dataclass

from .bandwidth import get_bandwidth

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
    ul_bandwidth: float
    dl_bandwidth: float
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
            r'\+QENG:\s*"servingcell",([^\r\n]*)',
            response,
            re.IGNORECASE,
        )

        if not match:
            raise ValueError(
                f"Invalid AT+QENG response: {response}"
            )

        fields = [
            value.strip().strip('"')
            for value in match.group(1).strip().split(",")
        ]

        if len(fields) != 19:
            raise ValueError(
                f"Expected 19 fields, received {len(fields)}"
            )

        try:
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
                ul_bandwidth=get_bandwidth(int(fields[9])),
                dl_bandwidth=get_bandwidth(int(fields[10])),
                tac=int(fields[11],16),
                rsrp=int(fields[12]),
                rsrq=int(fields[13]),
                rssi=int(fields[14]),
                sinr=float(fields[15]),
                cqi=int(fields[16]),
                tx_power=int(fields[17]),
                srxlev=fields[18],
            )
        except (ValueError, IndexError) as error:
            raise ValueError(
                f"Invalid field in AT+QENG response: {response}"
            ) from error

    @property
    def cell_id_hex(self) -> str:
        """Cell ID provided in hexadecimal format"""
        return hex(self.cell_id)

    @property
    def tac_hex(self) -> str:
        """TAC provided in hexadecimal format"""
        return hex(self.tac)

    def __str__(self) -> str:
        return (
            "========== LTE SERVING CELL ==========\n"
            f"Connection state : {self.state}\n"
            f"Technology       : {self.rat} ({self.duplex})\n"
            f"MCC / MNC        : {self.mcc} / {self.mnc}\n"
            f"Cell ID          : {self.cell_id_hex} (HEX), "
            f"{self.cell_id} (DEC)\n"
            f"PCI              : {self.pci}\n"
            f"TAC              : {self.tac_hex} (HEX), "
            f"{self.tac} (DEC)\n"
            f"LTE band         : B{self.band}\n"
            f"EARFCN           : {self.earfcn}\n"
            f"UL bandwidth     : {self.ul_bandwidth} MHz\n"
            f"DL bandwidth     : {self.dl_bandwidth} MHz\n"
            "--------------------------------------\n"
            f"RSRP             : {self.rsrp:4d} dBm\n"
            f"RSRQ             : {self.rsrq:4d} dB\n"
            f"RSSI             : {self.rssi:4d} dBm\n"
            f"SINR             : {self.sinr:4.1f} dB\n"
            f"CQI              : {self.cqi}\n"
            f"TX power         : {self.tx_power} (raw value)\n"
            f"SRXLEV           : {self.srxlev}\n"
            "======================================"
        )
