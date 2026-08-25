from src.tenda_4g09 import Tenda4G09

URL = "192.168.0.1"


router = Tenda4G09(
    host=URL,
    password="admin",
)

router.login()

status = router.get_status()
print(status)

router.logout()
