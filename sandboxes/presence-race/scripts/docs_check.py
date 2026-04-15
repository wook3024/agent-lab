#!/usr/bin/env python3

from pathlib import Path


def main():
    text = Path("docs/realtime_presence.md").read_text().lower()
    if "epoch" not in text:
        raise SystemExit("docs/realtime_presence.md must mention epoch ordering")
    if "stale" not in text:
        raise SystemExit("docs/realtime_presence.md must mention stale events")


if __name__ == "__main__":
    main()
