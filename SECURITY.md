# Security

Live connections are allowed only to peripherals owned by or explicitly authorized for the operator; `--authorized` records that assertion at the CLI boundary. Default operation is offline. No characteristic read/write, pairing attempt, key extraction, notification capture, or device configuration change is implemented. Report metadata can reveal device configuration; retain it only as long as the assessment requires. The utility has no persistent database. It does not claim that readable or writable GATT properties imply unauthenticated access.
