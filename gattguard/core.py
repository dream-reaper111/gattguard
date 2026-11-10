"""Validate and assess GATT metadata without asserting unobservable permissions."""

import json
import re

UUID = re.compile(r"^[0-9a-fA-F]{4}$|^[0-9a-fA-F]{8}$|^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")
PROPERTIES = {"broadcast", "read", "write-without-response", "write", "notify", "indicate", "authenticated-signed-writes", "extended-properties"}
KNOWN = {"180a": "Device Information", "1800": "Generic Access", "1801": "Generic Attribute", "2a29": "Manufacturer Name", "2a24": "Model Number", "2a26": "Firmware Revision"}


def inspect(snapshot: dict) -> dict:
    if not isinstance(snapshot, dict) or not isinstance(snapshot.get("services"), list) or len(snapshot["services"]) > 256:
        raise ValueError("invalid service inventory")
    if len(json.dumps(snapshot)) > 2_000_000:
        raise ValueError("snapshot exceeds 2 MB")
    findings = []
    services = []
    char_count = 0
    for service in snapshot["services"]:
        uuid = service.get("uuid")
        if not isinstance(uuid, str) or not UUID.fullmatch(uuid):
            raise ValueError("invalid service UUID")
        chars = service.get("characteristics", [])
        if not isinstance(chars, list) or len(chars) > 512:
            raise ValueError("invalid characteristic list")
        normalized_chars = []
        for char in chars:
            char_count += 1
            cuuid = char.get("uuid")
            props = char.get("properties")
            if not isinstance(cuuid, str) or not UUID.fullmatch(cuuid) or not isinstance(props, list) or not set(props) <= PROPERTIES:
                raise ValueError("invalid characteristic metadata")
            descriptors = char.get("descriptors", [])
            if not isinstance(descriptors, list) or len(descriptors) > 128 or any(not isinstance(d, str) or not UUID.fullmatch(d) for d in descriptors):
                raise ValueError("invalid descriptors")
            props = sorted(set(props))
            if "write-without-response" in props:
                findings.append({"uuid": cuuid.lower(), "severity": "review", "confidence": "high", "title": "Writable without response", "evidence": "GATT property advertised by host", "recommendation": "Review access controls and command validation on the peripheral; property alone is not a vulnerability."})
            elif "write" in props:
                findings.append({"uuid": cuuid.lower(), "severity": "info", "confidence": "high", "title": "Writable characteristic", "evidence": "GATT property advertised by host", "recommendation": "Confirm authorization and encryption requirements through approved device documentation or a separate approved test."})
            normalized_chars.append({"uuid": cuuid.lower(), "name": KNOWN.get(cuuid.lower()), "properties": props,
                                     "descriptors": sorted(set(d.lower() for d in descriptors)),
                                     "authentication_requirement": "not observable from GATT enumeration",
                                     "encryption_requirement": "not observable from GATT enumeration"})
        services.append({"uuid": uuid.lower(), "name": KNOWN.get(uuid.lower()), "characteristics": normalized_chars})
    return {"source": snapshot.get("source", "offline snapshot"), "services": services,
            "service_count": len(services), "characteristic_count": char_count,
            "findings": findings, "permission_evidence": "GATT properties expose nominal operations; BlueZ/Bleak enumeration does not reveal server-side authentication or encryption permissions."}


def mermaid(report: dict) -> str:
    lines = ["flowchart LR"]
    for si, service in enumerate(report["services"]):
        lines.append(f'  s{si}["Service {service["uuid"]}"]')
        for ci, char in enumerate(service["characteristics"]):
            lines.append(f'  c{si}_{ci}["Characteristic {char["uuid"]}"]')
            lines.append(f"  s{si} --> c{si}_{ci}")
            for di, descriptor in enumerate(char["descriptors"]):
                lines.append(f'  d{si}_{ci}_{di}["Descriptor {descriptor}"]')
                lines.append(f"  c{si}_{ci} --> d{si}_{ci}_{di}")
    return "\n".join(lines) + "\n"
