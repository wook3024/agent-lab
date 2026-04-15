---
name: quality-gates-runner
description: Select and run deterministic quality gates for complex engineering tasks, including tests, lint, typecheck, security checks, docs sync, and task-specific gates such as migration, retry, or performance checks. Use when a task must be judged by repeatable verification rather than narrative confidence.
---

# Quality Gates Runner

Choose the right gates and run them consistently.

## Workflow

1. Read the task's complexity axes and verification requirements.
2. Select the base gates.
3. Add conditional gates driven by task risk.
4. Run the gates in a stable order.
5. Return pass/fail per gate and identify the first blocking failure.

## Base Gates

- tests
- lint
- typecheck
- docs sync

## Conditional Gates

- security scan
- migration safety
- API contract check
- retry semantics
- performance smoke
- concurrency behavior
- flaky repeat check

## Rules

- Do not omit a needed gate to make the run pass.
- Prefer deterministic checks over subjective ones.
- If a gate is unavailable, mark it explicitly as missing rather than silently skipping it.

## Read These References

- `references/gate-selection.md`
- `scripts/select_gates.py`

## Failure Modes To Avoid

- Missing a required gate
- Running gates in an inconsistent order
- Treating a skipped gate as a pass
