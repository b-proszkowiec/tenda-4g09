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

    print("\nOnline clients:")
    for client in router.get_online_clients():
        print(
            f"  Name: {client.name}\n"
            f"  IP: {client.ip}\n"
            f"  Upload: {client.upload_speed}\n"
            f"  Download: {client.download_speed}\n"
        )

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
