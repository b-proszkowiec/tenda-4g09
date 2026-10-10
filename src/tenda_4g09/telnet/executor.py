import telnetlib3
import asyncio
import re

SPEED = 115200
DEVICE = "/dev/ttyUSB2"

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

    async def execute_at(at_command: str, at_timeout: int = 5):
        
        if "AT+" in at_command:
            match = re.match(r"AT(\+\w+)", at_command)
            at_rsp_prefix = f"{match.group(1)}:"
        
        writer.write(f"microcom -s {SPEED} {DEVICE}\n")
        await writer.drain()

        await asyncio.sleep(0.3)

        writer.write(at_command + "\r")
        await writer.drain()

        response = ""

        try:
            async with asyncio.timeout(at_timeout):
                while True:
                    chunk = await reader.read(256)

                    if not chunk:
                        break

                    response += chunk

                    lines = response.replace("\r", "").split("\n")
                    if any(
                        at_rsp_prefix in line.strip() or "ERROR" in line.strip()
                        for line in lines
                    ):
                        break

        except TimeoutError:
            pass

        finally:
            writer.write("\x18")
            await writer.drain()
            await asyncio.sleep(0.2)

        return response.strip()

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

        await asyncio.wait_for(
            reader.readuntil(b"~ #"),
            timeout=timeout,
        )

        result = await execute_at(command)
        return result

    finally:
        writer.close()
        await writer.wait_closed()
