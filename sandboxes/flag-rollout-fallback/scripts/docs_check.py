#!/usr/bin/env python3

from pathlib import Path


def main():
    docs_text = Path("docs/feature_flags.md").read_text().lower()
    ops_text = Path("ops/feature_rollout.md").read_text().lower()
    if "fail closed" not in docs_text:
        raise SystemExit("docs/feature_flags.md must mention fail closed")
    if "rollback" not in ops_text:
        raise SystemExit("ops/feature_rollout.md must mention rollback")


if __name__ == "__main__":
    main()
