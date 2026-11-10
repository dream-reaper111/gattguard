import asyncio
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from gattguard.core import inspect, mermaid
from gattguard.cli import main
from gattguard.live import inventory


SNAPSHOT = {"services": [{"uuid": "180a", "characteristics": [
    {"uuid": "2a29", "properties": ["read"], "descriptors": ["2901"]},
    {"uuid": "abcd", "properties": ["write-without-response"], "descriptors": []},
]}]}


class Tests(unittest.TestCase):
    def test_inventory(self):
        report = inspect(SNAPSHOT)
        self.assertEqual(report["service_count"], 1)
        self.assertEqual(report["findings"][0]["severity"], "review")
        self.assertIn("not observable", report["services"][0]["characteristics"][0]["encryption_requirement"])
        self.assertIn("s0 --> c0_0", mermaid(report))

    def test_malformed(self):
        for snapshot in ({"services": "wrong"}, {"services": [{"uuid": "bad"}]},
                         {"services": [{"uuid": "180a", "characteristics": [{"uuid": "2a29", "properties": ["secret"]}]}]}):
            with self.subTest(snapshot=snapshot), self.assertRaises(ValueError):
                inspect(snapshot)

    def test_cli_offline_and_auth_gate(self):
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory)
            source = p / "snapshot.json"
            source.write_text(json.dumps(SNAPSHOT))
            self.assertEqual(main(["analyze", str(source), "--output", str(p / "report.json"), "--diagram", str(p / "graph.mmd")]), 0)
            self.assertTrue((p / "report.json").exists())
            self.assertEqual(main(["inspect", "AA:BB:CC:DD:EE:FF"]), 2)

    def test_unavailable_bleak(self):
        with patch.dict("sys.modules", {"bleak": None}):
            with self.assertRaisesRegex(RuntimeError, "requires bleak"):
                asyncio.run(inventory("AA:BB:CC:DD:EE:FF"))


if __name__ == "__main__":
    unittest.main()
