import argparse
import asyncio
import json
from pathlib import Path
import sys

from .core import inspect, mermaid
from .hardware import capabilities
from .live import inventory


def main(argv=None):
    parser = argparse.ArgumentParser(prog="gattguard")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("hardware")
    analyze = sub.add_parser("analyze")
    analyze.add_argument("input", type=Path)
    analyze.add_argument("--output", type=Path)
    analyze.add_argument("--diagram", type=Path)
    live = sub.add_parser("inspect")
    live.add_argument("address")
    live.add_argument("--authorized", action="store_true", help="affirm ownership or explicit peripheral authorization")
    live.add_argument("--output", type=Path)
    live.add_argument("--diagram", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.cmd == "hardware":
            print(json.dumps(capabilities(), indent=2))
            return 0
        if args.cmd == "inspect":
            if not args.authorized:
                raise ValueError("live connection requires --authorized")
            snapshot = asyncio.run(inventory(args.address))
        else:
            if args.input.stat().st_size > 2_000_000:
                raise ValueError("snapshot exceeds 2 MB")
            snapshot = json.loads(args.input.read_text())
        report = inspect(snapshot)
        result = json.dumps(report, indent=2) + "\n"
        if args.output:
            args.output.write_text(result)
        else:
            print(result, end="")
        if args.diagram:
            args.diagram.write_text(mermaid(report))
        return 0
    except (OSError, ValueError, RuntimeError, TypeError) as exc:
        print(f"gattguard: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
