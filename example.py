from src.tenda_4g09 import Tenda4G09

URL = "192.168.0.1"


with Tenda4G09(URL, password="admin") as router:
    status = router.get_status()
    print(status)
