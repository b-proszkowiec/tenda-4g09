import asyncio

from .executor import TelnetATClient
from .response_parser import extract_response

DEFAULT_LOGIN = "root"
DEFAULT_PASSWD = "Fireitup"


def run_telnet_cmd(cmd: str, host: str, port: int=23, login: str=DEFAULT_LOGIN, password: str=DEFAULT_PASSWD):
    async def do_execute():
        client = TelnetATClient(host, port)
        try:
            await client.connect_and_login(login, password)
            return await client.execute_at(cmd)

        finally:
            await client.close()

    result = asyncio.run(do_execute())
    return extract_response(result, cmd)
