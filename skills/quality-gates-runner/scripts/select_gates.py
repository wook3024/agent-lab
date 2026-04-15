#!/usr/bin/env python3
"""Select deterministic gates from a benchmark task JSON file."""

import json
import sys
from pathlib import Path


BASE_GATES = ["tests_pass", "lint_pass", "typecheck_pass"]


AXIS_TO_GATES = {
    "docs-sync": ["docs_sync_check"],
    "security": ["security_scan_pass"],
    "migration-safety": ["migration_safety_check"],
    "retry-semantics": ["retry_behavior_check"],
    "performance-risk": ["performance_smoke_check"],
    "concurrency": ["concurrency_behavior_check"],
    "api-contract": ["external_contract_check"],
    "async-behavior": ["flaky_test_repeat_check"],
    "shared-protocol": ["protocol_compatibility_check"],
    "operational-safety": ["operational_fallback_check"],
}


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: select_gates.py <task-json>", file=sys.stderr)
        return 1

    path = Path(sys.argv[1])
    data = json.loads(path.read_text())
    axes = data.get("complexity_axes", [])
    gates = list(BASE_GATES)
    for axis in axes:
        gates.extend(AXIS_TO_GATES.get(axis, []))

    seen = set()
    ordered = []
    for gate in gates:
        if gate not in seen:
            ordered.append(gate)
            seen.add(gate)

    print(json.dumps({"task_id": data.get("id"), "selected_gates": ordered}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
