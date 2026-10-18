import telnetlib3
import asyncio
import re

SPEED = 115200
DEVICE = "/dev/ttyUSB2"

_AT_ECHO_RE = re.compile(r"^AT(?:\+|&|\\)?[A-Z0-9]+", re.I)
_AT_PREFIX_RE = re.compile(r"^AT(\+[A-Z0-9]+)", re.I)


def normalize_line(line: str) -> str:
    return line.strip().replace("\r", "")


def expected_prefix(command: str) -> str | None:
    match = _AT_PREFIX_RE.match(command.strip())
    return f"{match.group(1).upper()}:" if match else None

TIMEOUT = 10

class TelnetATClient:
    def __init__(self, host: str, port: int = 23):
        self.host = host
        self.port = port
        self._at_lock = asyncio.Lock()
        self.reader = None
        self.writer = None

    async def connect_and_login(self, login: str, password: str, timeout: int = TIMEOUT):
        self.reader, self.writer = await telnetlib3.open_connection(
            host=self.host,
            port=self.port,
            connect_minwait=0.1,
            connect_maxwait=TIMEOUT,
        )

        try:
            await asyncio.wait_for(self.reader.readuntil(b"login: "), timeout=TIMEOUT)
            self.writer.write(login + "\n")
            await self.writer.drain()

            await asyncio.wait_for(self.reader.readuntil(b"Password: "), timeout=TIMEOUT)
            self.writer.write(password + "\n")
            await self.writer.drain()

            separator = b"~ #"
            await asyncio.wait_for(self.reader.readuntil(separator), timeout=TIMEOUT)
        except Exception as e:
            await self.close()
            raise ConnectionError(f"Failed to login or reach shell: {e}") from e

    async def execute_at(self, command: str, at_timeout: float = TIMEOUT) -> str:
        if not self.reader or not self.writer:
            raise RuntimeError("Not connected. Call connect_and_login first.")

        command = command.strip()
        prefix = expected_prefix(command)
        response_lines = []

        self.writer.write(f"microcom -s {SPEED} {DEVICE}\n")
        await self.writer.drain()

        await asyncio.sleep(0.5)

        self.writer.write(command + "\r")
        await self.writer.drain()

        started = False
        foreign_transaction = False

        try:
            async with asyncio.timeout(at_timeout):
                while True:
                    line = await self.reader.readline()
                    if not line:
                        break

                    line = normalize_line(line)
                    if not line:
                        continue

                    upper = line.upper()

                    if _AT_ECHO_RE.match(upper):
                        if upper == command.upper():
                            started = True
                            foreign_transaction = False
                            continue
                        foreign_transaction = True
                        continue

                    if foreign_transaction:
                        if upper in ("OK", "ERROR") or upper.startswith(("+CME ERROR:", "+CMS ERROR:")):
                            foreign_transaction = False
                        continue

                    if not started:
                        if (prefix and upper.startswith(prefix)) or upper in ("OK", "ERROR"):
                            started = True
                        else:
                            started = True 

                    response_lines.append(line)

                    if upper in ("OK", "ERROR") or upper.startswith(("+CME ERROR:", "+CMS ERROR:")):
                        break

        except TimeoutError:
            response_lines.append("[TIMEOUT]")

        finally:
            self.writer.write("\x18")
            await self.writer.drain()
            await asyncio.sleep(0.5)

        return "\n".join(response_lines).strip()

    async def close(self):
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()

