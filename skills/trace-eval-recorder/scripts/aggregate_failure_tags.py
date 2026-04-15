#!/usr/bin/env python3
"""Aggregate failure taxonomy counts from trace JSON files."""

import json
import sys
from collections import Counter
from pathlib import Path


def iter_trace_files(root: Path):
    for path in sorted(root.rglob("*.json")):
        yield path


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: aggregate_failure_tags.py <trace-dir>", file=sys.stderr)
        return 1

    root = Path(sys.argv[1])
    counts = Counter()
    for path in iter_trace_files(root):
        try:
            data = json.loads(path.read_text())
        except Exception:
            continue
        for tag in data.get("failure_taxonomy", []):
            counts[tag] += 1

    print(json.dumps({"failure_counts": counts}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
