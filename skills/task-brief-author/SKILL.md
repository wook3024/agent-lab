---
name: task-brief-author
description: Turn ambiguous or broad product-development requests into strict complex-case task briefs with explicit goal, done conditions, non-goals, risks, approvals, and verification scope. Use when a coding task is multi-file, regression-prone, policy-constrained, or likely to sprawl without a tight execution contract.
---

# Task Brief Author

Write a strict task brief before implementation starts.

## Workflow

1. Extract the change goal in one sentence.
2. List explicit done conditions that can be verified.
3. State non-goals to prevent scope creep.
4. Spell out the key invariants and the counterexamples that would break them.
5. Record risks, approvals, and required verification.
6. Mark what the reviewer must inspect closely.

## Rules

- Optimize for complex cases, not simple chores.
- Prefer narrower scope when the request is ambiguous.
- Surface hidden approvals instead of assuming they are allowed.
- Treat tests and docs as first-class outputs when the change affects behavior.
- When the task touches keys, ids, ordering, reconnects, caching, or telemetry, call out collision, idempotency, stale-event, and tie-case risks explicitly.
- If the task cannot be made precise, escalate instead of inventing requirements.

## Output Contract

Mirror `../../docs/templates/TASK_BRIEF_TEMPLATE.md`.

## Read These References

- `references/complex-brief-checklist.md` for must-have brief fields

## Failure Modes To Avoid

- Leaving success conditions vague
- Leaving invariants and edge cases implicit
- Forgetting regression risk
- Mixing implementation ideas into the brief
- Omitting approvals for risky work
