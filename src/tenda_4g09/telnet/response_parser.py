def extract_response(raw: str, command: str):
    lines = [
        line.strip()
        for line in raw.replace("\r", "").split("\n")
        if line.strip()
    ]

    lines = [
        line for line in lines
        if line != command
        and not line.startswith("microcom ")
    ]

    lines = [
        line for line in lines
        if line not in ("OK", "ERROR")
    ]

    return "\n".join(lines)
