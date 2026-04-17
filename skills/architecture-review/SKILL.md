---
name: architecture-review
description: Review complex changes for boundary erosion, coupling growth, migration sequencing mistakes, and unjustified abstractions. Use when code can pass tests yet still leave the system harder to evolve, operate, or safely migrate.
---

# Architecture Review

Review the long-term structural cost of the change, not just whether it currently works.

## Workflow

1. Read the task brief, context pack, diff, execution report, and general review findings.
2. Check whether the change preserves module boundaries and ownership clarity.
3. Look for new shared state, hidden coupling, or convenience abstractions that spread concerns across domains.
4. Evaluate migration sequencing and operability impact.
5. Report findings by architecture severity and record residual structural risks.

## Rules

- Prefer maintainability and safe change boundaries over clever local optimizations.
- Do not reject a change merely because it is unfamiliar; reject it when it makes future changes or operations meaningfully riskier.
- If a task-scoped fix is better than a reusable abstraction, say so explicitly.
- Treat migration sequencing mistakes as architecture findings even if today’s tests pass.

## Output Contract

Mirror `../../docs/templates/ARCHITECTURE_REVIEW_TEMPLATE.md`.

## Failure Modes To Avoid

- Missing boundary erosion because the current task passes
- Accepting incidental abstractions without questioning future cost
- Ignoring ownership confusion introduced by shared modules
