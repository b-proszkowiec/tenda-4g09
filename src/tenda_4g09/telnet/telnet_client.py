from functools import wraps

from ..models import (
    LTEServingCell
)
from .connector import run_telnet_cmd


def requires_connection(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._check_connected()
        return method(self, *args, **kwargs)
    return wrapper


class TelnetClient:
    def __init__(self, ip, port, init_telnet_fn):
        self.ip = ip
        self.port = port
        self.telnet_enabled = init_telnet_fn()

    def _check_connected(self):
        if not self.telnet_enabled:
            raise ConnectionError("Telnet hasn't been enabled")

    @requires_connection
    def get_signal_info(self) -> LTEServingCell:

        sc_rsp = run_telnet_cmd('AT+QENG="servingcell"', self.ip, self.port)
        serving_cell = LTEServingCell.from_qeng(sc_rsp)
        return serving_cell
