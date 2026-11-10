"""Optional Bleak service enumeration. No characteristic reads or writes."""

import re

ADDRESS = re.compile(r"^(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$")


async def inventory(address: str) -> dict:
    if not ADDRESS.fullmatch(address):
        raise ValueError("invalid authorized address")
    try:
        from bleak import BleakClient
    except ImportError as exc:
        raise RuntimeError("live inspection requires bleak") from exc
    services = []
    try:
        async with BleakClient(address, timeout=15) as client:
            for service in client.services:
                chars = []
                for char in service.characteristics:
                    chars.append({"uuid": char.uuid, "properties": list(char.properties),
                                  "descriptors": [descriptor.uuid for descriptor in char.descriptors]})
                services.append({"uuid": service.uuid, "characteristics": chars})
    except Exception as exc:
        raise RuntimeError(f"authorized GATT enumeration failed: {exc}") from exc
    return {"source": "Bleak/BlueZ authorized connection", "services": services}
