---
name: cost-governance-trace
description: Extend benchmark traces with cost, latency, ownership, approval, and intervention signals so quality decisions can be compared against operational cost. Use when CTO- or org-level routing policy needs more than pass/fail evidence.
---

# Cost Governance Trace

Record cost in context, not in isolation.

## Workflow

1. Capture role-to-model and role-to-effort mappings.
2. Record role-level token usage, elapsed time, and intervention signals.
3. Record owner team, service criticality, approval state, and release state.
4. Aggregate runs by task type, route, and team.
5. Produce a report that compares quality and cost together.

## Rules

- Do not present low cost as success if quality degraded.
- Missing role-level data should stay missing, not be fabricated.
- Distinguish run cost from operator or human intervention cost.
- Keep quality-first and cost-optimized routes directly comparable.

## Output Contract

Mirror `../../docs/templates/TRACE_RECORD_TEMPLATE.json` and `../../docs/templates/COST_GOVERNANCE_REPORT_TEMPLATE.md`.

## Failure Modes To Avoid

- Cost-only optimization
- Missing intervention accounting
- Hiding governance overhead inside generic elapsed time
