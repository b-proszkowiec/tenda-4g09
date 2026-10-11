import asyncio

from .executor import execute_telnet
from .response_parser import extract_response

DEFAULT_LOGIN = "root"
DEFAULT_PASSWD = "Fireitup"

def run_telnet_cmd(cmd: str, host: str, port: int=23, login: str=DEFAULT_LOGIN, password: str=DEFAULT_PASSWD
                   ):
    result = asyncio.run(
        execute_telnet(
            host=host,
            port=port,
            login=login,
            password=password,
            command=cmd
        )
    )

    response = extract_response(result, cmd)
    return response
