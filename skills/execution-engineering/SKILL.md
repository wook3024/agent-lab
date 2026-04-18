---
name: execution-engineering
description: Execute complex product-development changes with strong scope control, explicit verification, test updates, and documentation sync. Use when implementing multi-file fixes or features where shallow solutions, unrelated edits, and missing regression coverage are major risks.
---

# Execution Engineering

Implement only what the task brief authorizes, then prove it.

## Workflow

1. Re-read goal, done conditions, non-goals, and reviewer focus.
2. Write down the exact invariant the fix must preserve, plus 1-3 counterexamples that would violate it.
3. Make the smallest coherent change that satisfies the behavior change.
4. Add or update tests before declaring success.
5. Update docs or runbooks when behavior or operations changed.
6. If the change affects rollout, operator behavior, release notes, approvals, or other governance surfaces, write the required governance artifacts before handoff.
7. Run local verification before handing off to the review step.
8. Ensure the execution report and governance artifacts match the commands and outcomes you actually observed.

## Rules

- Do not widen scope to "clean up" nearby code.
- Prefer explicit behavior-preserving changes over clever rewrites.
- Prefer task-scoped fixes over new abstractions unless the task explicitly requires a reusable abstraction.
- When composing keys, ids, cache entries, or ordering logic, check delimiter collision, canonicalization, equality/tie cases, idempotency, and stale-event behavior.
- If the first fix is shallow, keep iterating before presenting it.
- Keep a short list of residual risks for review.
- If a command passed, do not describe it as blocked or conditional in the report.
- If production or rollout behavior changed, include:
  - `approval_decision.md`
  - `release_gate_decision.md`
  - `release_artifact_package.md`
- Governance artifacts must stay consistent with actual gate outcomes and reviewer-visible blockers.

## Output Contract

- Change summary
- Changed files
- Verification results
- Residual risks
- Reviewer focus points
- When required, approval / release gate / release artifact documents that mirror the templates in `docs/templates/`

## Read These References

- `references/complex-case-loop.md` for the execution loop

## Failure Modes To Avoid

- Over-editing unrelated modules
- Over-generalizing beyond the task invariant
- Skipping regression coverage
- Forgetting docs sync
- Missing collision / stale / tie-case regressions
- Reporting verification results inaccurately
- Stopping after the first plausible fix
- Forgetting approval or release artifacts on rollout-sensitive changes
