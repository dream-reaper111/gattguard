# Hardware support

`hardware` lists local HCI sysfs entries conservatively. Sysfs presence does not verify BlueZ D-Bus permission or a successful connection. Live enumeration needs an accessible Linux Bluetooth adapter and Bleak/BlueZ. No adapter was usable in the current environment. Dedicated BLE sniffers and SDR receivers are unsupported; this is GATT host connection metadata, not over-the-air capture. No sample rate applies. Offline JSON assessment requires no radio.
