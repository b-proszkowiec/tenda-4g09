# Tenda 4G09 Python Client

A lightweight Python library for interacting with the Tenda 4G09 LTE router through its web interface.

## Features

- Router authentication and session management
- Retrieving router status and Wi-Fi information
- Reading SIM and WAN configuration
- Detecting whether the mobile WAN connection is active
- Requesting a mobile WAN reconnection
- Retrieving serving cell information from the modem

## Requirements

- Python 3.10+
- Tenda 4G09 router accessible over the local network

## Installation

Install:

```bash
pip install tenda-4g09-client
```

## Quick start

Collecting basic information.

```python
from tenda_4g09 import Tenda4G09


URL = "192.168.0.1"

with Tenda4G09(URL, password="your-password") as router:
    status = router.get_status()

    print(f"Router IP:          {status.lan_ip}")
    print(f"Connected clients:  {status.client_count}")
    print(f"Work mode:          {status.work_mode}")
    print(f"Device name:        {status.device_name}\n")

    [print(f"{client}\n") for client in router.get_online_clients()]

```

#### output:

```
Router IP:          192.168.0.1
Connected clients:  3
Work mode:          3G/4G
Device name:        4G09

Client: RE605X (192.168.0.2)
  Device ID: ee:d3:##:##:##:29
  Upload: 8.05 kB/s
  Download: 30.63 kB/s
  Blocked: No
  Guest: No

Client: homeassistant (192.168.0.4)
  Device ID: b8:27:##:##:##:0a
  Upload: 0.00 kB/s
  Download: 0.00 kB/s
  Blocked: No
  Guest: No

Client: DESKTOP-AT2M0OR (192.168.0.49)
  Device ID: 34:6f:##:##:##:ef
  Upload: 27.26 kB/s
  Download: 403.56 kB/s
  Blocked: No
  Guest: No
```

Replace the IP address and password with your router's settings.

## The mobile WAN reconnect

Check whether the router has lost its mobile WAN connection and try to reconnect.

```python
with Tenda4G09(URL, password) as router:

    print(f"Before:\n\tMobile data connected: {router.is_mobile_data_connected()}\n")

    if not router.is_mobile_data_connected():
        router.mobile_data_connect()

    time.sleep(2)

    print(f"After:\n\tMobile data connected: {router.is_mobile_data_connected()}")
```

#### output:

```
Before:
        Mobile data connected: False

After:
        Mobile data connected: True
```

## Getting the signal information from the modem

Retrieve the parameters of the serving cell connection (equivalent AT command: AT+QENG="servingcell").

```python
with Tenda4G09(URL, password) as router:
    client = router.get_telnet_client(router.host_ip)
    print(client.get_signal_info())
```

#### output:

```
========== LTE SERVING CELL ==========
Connection state : NOCONN
Technology       : LTE (FDD)
MCC / MNC        : 260 / 02
Cell ID          : 0x###2512 (HEX), ###67602 (DEC)
PCI              : 334
TAC              : 0x##af (HEX), ##911 (DEC)
LTE band         : B20
EARFCN           : 6375
UL bandwidth     : 15 MHz
DL bandwidth     : 15 MHz
--------------------------------------
RSRP             : -105 dBm
RSRQ             :  -13 dB
RSSI             :  -72 dBm
SINR             : 11.0 dB
CQI              : 255
TX power         : 170 (raw value)
SRXLEV           : -
======================================
```

## Compatibility

Designed for the Tenda 4G09 router. Compatibility with other models and firmware versions has not been verified.

## Security

Use the library only on trusted networks. Do not commit router credentials to your repository.

## License

MIT — see the [LICENSE](LICENSE) file.
