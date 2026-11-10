# GATTGuard

GATTGuard inventories GATT services, characteristics, descriptors, and advertised operation properties for owned or explicitly authorized BLE peripherals. It can assess a bounded offline JSON snapshot without hardware. Live enumeration requires Bleak, working BlueZ, and `--authorized`. It does not read characteristic values, subscribe to notifications, write, pair, or fuzz.

```sh
python3 -m gattguard.cli hardware
python3 -m gattguard.cli analyze authorized-snapshot.json --output report.json --diagram graph.mmd
python3 -m gattguard.cli inspect AA:BB:CC:DD:EE:FF --authorized --output report.json
```

Snapshot format: `{"services":[{"uuid":"180a","characteristics":[{"uuid":"2a29","properties":["read"],"descriptors":["2901"]}]}]}`. The limit is 2 MB, 256 services, 512 characteristics per service, and 128 descriptors per characteristic. Findings are review prompts based on advertised properties. They are not proof of exploitable access. Mermaid diagrams can be rendered separately. See [ARCHITECTURE.md](ARCHITECTURE.md), [SECURITY.md](SECURITY.md), [HARDWARE.md](HARDWARE.md), [DEPENDENCIES.md](DEPENDENCIES.md), and [VALIDATION_REPORT.md](VALIDATION_REPORT.md).
