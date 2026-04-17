---
name: release-gate
description: Decide whether a complex engineering change is truly ready to release by combining gate results, review findings, approval state, rollback readiness, and operator guidance. Use when passing tests is not enough and a deployment decision requires explicit blocker handling.
---

# Release Gate

Judge release readiness explicitly. Do not confuse "tests passed" with "safe to release."

## Workflow

1. Read the task brief, execution report, gate results, review findings, and approval decision.
2. Identify unresolved blockers from requirements, gates, review, policy, or owner signoff.
3. Check rollback readiness, migration safety, and operator guidance.
4. Decide one of:
   - `release-ready`
   - `hold`
   - `escalate`
5. List the exact blocker or missing condition behind the decision.

## Rules

- Any unresolved `High` finding is a blocker unless explicitly superseded by a human decision.
- A skipped or unavailable gate is never equivalent to a pass.
- Missing owner approval on risky or irreversible changes is a blocker.
- If production behavior changed and rollback guidance is missing, prefer `escalate`.
- Keep the decision readable for operators, not just implementers.

## Output Contract

Mirror `../../docs/templates/RELEASE_GATE_DECISION_TEMPLATE.md`.

## Failure Modes To Avoid

- Marking a release ready because tests passed while governance gaps remain
- Hiding blockers inside "residual risks"
- Treating missing rollback notes as optional for risky changes
- Omitting operator follow-up actions
