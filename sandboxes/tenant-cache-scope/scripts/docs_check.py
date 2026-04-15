#!/usr/bin/env python3

from pathlib import Path


def main():
    caching = Path("docs/caching.md").read_text().lower()
    architecture = Path("docs/multi-tenant-architecture.md").read_text().lower()
    if "tenant_id" not in caching:
        raise SystemExit("docs/caching.md must mention tenant_id")
    if "cache key" not in architecture:
        raise SystemExit("docs/multi-tenant-architecture.md must mention cache key")


if __name__ == "__main__":
    main()
