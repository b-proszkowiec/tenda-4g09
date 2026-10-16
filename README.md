# Tenda 4G09 Python Client

A lightweight Python library for interacting with the Tenda 4G09 LTE router through its web interface.

## Features

- Router authentication and session management
- Retrieving router status and Wi-Fi information
- Reading SIM and WAN configuration
- Checking LTE connectivity
- Initiating an LTE connection

## Requirements

- Python 3.10+
- Tenda 4G09 router accessible over the local network

## Installation

Install:

```bash
pip install tenda-4g09-client
```

## Quick start

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

## LTE connection

```python
with Tenda4G09("192.168.0.1", password="your-password") as router:

    if not router.is_mobile_data_connected():
        router.mobile_data_connect()
```

## Compatibility

Designed for the Tenda 4G09 router. Compatibility with other models and firmware versions has not been verified.

## Security

Use the library only on trusted networks. Do not commit router credentials to your repository.

## License

MIT — see the [LICENSE](LICENSE) file.
