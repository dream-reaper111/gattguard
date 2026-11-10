from pathlib import Path


def capabilities() -> list[dict]:
    adapters = sorted(p.name for p in Path("/sys/class/bluetooth").glob("hci*"))
    result = [
        {"kind": "local_ble_adapter", "device": a, "available": False, "detail": "sysfs presence only; connection requires BlueZ and permission verification", "frequency_range_hz": [2400000000, 2483500000], "sample_rate_limits": None, "operations": ["authorized GATT connection"], "required_permissions": ["BlueZ D-Bus access", "peripheral owner authorization"], "driver_dependencies": ["BlueZ", "Bleak"]} for a in adapters
    ]
    if not adapters:
        result.append({"kind": "local_ble_adapter", "device": None, "available": False, "detail": "no adapter found", "frequency_range_hz": None, "sample_rate_limits": None, "operations": [], "required_permissions": ["BlueZ D-Bus access"], "driver_dependencies": ["BlueZ", "Bleak"]})
    return result + [
        {"kind": "offline_capture_import", "device": "GATT JSON", "available": True, "frequency_range_hz": None, "sample_rate_limits": None, "operations": ["analyze"], "required_permissions": ["file read"], "driver_dependencies": []},
        {"kind": "dedicated_ble_sniffer", "device": None, "available": False, "frequency_range_hz": None, "sample_rate_limits": None, "operations": [], "required_permissions": [], "driver_dependencies": [], "detail": "unsupported"},
        {"kind": "receive_only_sdr", "device": None, "available": False, "frequency_range_hz": None, "sample_rate_limits": None, "operations": [], "required_permissions": [], "driver_dependencies": [], "detail": "unsupported"},
    ]
