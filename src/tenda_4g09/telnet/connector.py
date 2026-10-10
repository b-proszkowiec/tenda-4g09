import asyncio

from .executor import execute_telnet
from .response_parser import extract_response

DEFAULT_LOGIN = "root"
DEFAULT_PASSWD = "Fireitup"

def run_telnet(cmd: str, host: str, port: int = 23):
    result = asyncio.run(
        execute_telnet(
            host=host,
            port=port,
            login=DEFAULT_LOGIN,
            password=DEFAULT_PASSWD,
            command=cmd
        )
    )

    response = extract_response(result, cmd)
    return response
