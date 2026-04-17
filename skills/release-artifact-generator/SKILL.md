---
name: release-artifact-generator
description: Generate a release-ready handoff package including release notes, operator checklist deltas, and rollback notes. Use when a code change is moving toward release and operators or approvers need a concise but actionable artifact package.
---

# Release Artifact Generator

Turn implementation output into an operator-usable release package.

## Workflow

1. Read the task brief, execution report, release gate decision, approval state, and docs/runbook changes.
2. Separate user-visible impact from operator-visible impact.
3. Draft the release note summary.
4. Record operator checklist changes.
5. Write rollback notes and known release risks.

## Rules

- Keep the package concise but operationally actionable.
- Do not claim release readiness if the release gate is `hold` or `escalate`.
- Rollback notes should reflect actual caveats, not generic reassurance.
- If no operator checklist changed, say so explicitly.

## Output Contract

Mirror `../../docs/templates/RELEASE_ARTIFACT_PACKAGE_TEMPLATE.md`.

## Failure Modes To Avoid

- Leaving operators to infer changed procedures from raw diff context
- Omitting rollback caveats
- Mixing release-note language with approval or blocker state
