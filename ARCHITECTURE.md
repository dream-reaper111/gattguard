# Architecture

The optional Bleak adapter enumerates service, characteristic, and descriptor UUIDs and characteristic properties. Offline snapshots have the same bounded structure. The assessment engine validates and normalizes this metadata, identifies selected standard UUIDs including Device Information Service, flags writable configuration surfaces for review, and emits JSON plus an optional Mermaid relationship diagram. No database or server is required for this read-only utility.

Host GATT enumeration exposes characteristic properties, but generally does not expose the peripheral's server-side authentication or encryption policy. GATTGuard records these requirements as unobservable, and its finding severity reflects review priority rather than confirmed weakness. OWASP style review topics include access control of writable state and validation of commands; implementation is limited to metadata evidence.
