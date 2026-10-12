import telnetlib3
import asyncio
import re

SPEED = 115200
DEVICE = "/dev/ttyUSB2"

_at_lock = asyncio.Lock()

_AT_ECHO_RE = re.compile(r"^AT(?:\+|&|\\)?[A-Z0-9]+", re.I)
_AT_PREFIX_RE = re.compile(r"^AT(\+[A-Z0-9]+)", re.I)


def normalize_line(line: str) -> str:
    return line.strip().replace("\r", "")


def expected_prefix(command: str) -> str | None:
    match = _AT_PREFIX_RE.match(command.strip())
    return f"{match.group(1).upper()}:" if match else None


async def execute_telnet(
    host: str, login: str, password: str, command: str,
    port: int=23, timeout: int=5
):
    reader, writer = await telnetlib3.open_connection(
        host=host,
        port=port,
        connect_minwait=0.1,
        connect_maxwait=1.0,
    )

    async def execute_at(at_command: str, at_timeout: float = 5) -> str:
        command = at_command.strip()
        prefix = expected_prefix(command)
        response_lines = []

        async with _at_lock:
            writer.write(f"microcom -s {SPEED} {DEVICE}\n")
            await writer.drain()

            await asyncio.sleep(0.3)

            writer.write(command + "\r")
            await writer.drain()

            started = False
            foreign_transaction = False

            try:
                async with asyncio.timeout(at_timeout):
                    while True:
                        raw_line = await reader.readline()

                        if not raw_line:
                            break

                        if isinstance(raw_line, bytes):
                            raw_line = raw_line.decode(
                                "utf-8", errors="replace"
                            )

                        line = normalize_line(raw_line)
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
                            if upper in ("OK", "ERROR") or upper.startswith(
                                "+CME ERROR:"
                            ) or upper.startswith("+CMS ERROR:"):
                                foreign_transaction = False
                            continue

                        if not started:
                            if prefix and upper.startswith(prefix):
                                started = True
                            elif upper in ("OK", "ERROR"):
                                started = True
                            else:
                                continue

                        response_lines.append(line)

                        if (
                            upper in ("OK", "ERROR")
                            or upper.startswith("+CME ERROR:")
                            or upper.startswith("+CMS ERROR:")
                        ):
                            break

            except TimeoutError:
                response_lines.append("[TIMEOUT]")

            finally:
                writer.write("\x18")
                await writer.drain()
                await asyncio.sleep(0.2)

            return "\n".join(response_lines).strip()

    try:
        await asyncio.wait_for(
            reader.readuntil(b"login: "),
            timeout=timeout,
        )
        writer.write(login + "\n")
        await writer.drain()

        await asyncio.wait_for(
            reader.readuntil(b"Password: "),
            timeout=timeout,
        )
        writer.write(password + "\n")
        await writer.drain()

        separator = b"~ #"
        try:
            data = await asyncio.wait_for(
                reader.readuntil(separator),
                timeout=timeout,
            )
        except asyncio.IncompleteReadError as exc:
            partial = exc.partial

            if isinstance(partial, bytes):
                partial = partial.decode("utf-8", errors="replace")

            raise ConnectionError(
                f"Telnet closed the tunnel before the separator was displayed"
                f"Parial data: {partial!r}"
            ) from exc
        except TimeoutError as exc:
            raise TimeoutError(
                f"Timeout occurred while waiting for the response"
                f"(separator={separator!r})"
            ) from exc

        result = await execute_at(command)
        return result

    finally:
        writer.close()
        await writer.wait_closed()
