---
name: docs-sync
description: Keep design docs, ADRs, runbooks, and operator guidance aligned with complex code changes. Use when a task changes behavior, operations, migrations, integrations, or risk posture and documentation drift would create future defects.
---

# Docs Sync

Determine which docs must change and update them deliberately.

## Workflow

1. Inspect the change surface.
2. Ask whether user behavior, operator behavior, or architectural truth changed.
3. Map changed code to the docs that govern that behavior.
4. Mark required doc updates as blocking when drift would be harmful.

## Rules

- Prefer a short precise update over a long generic rewrite.
- Update runbooks when operators would act differently after the change.
- Update ADRs when the architectural decision itself changed.
- If no docs must change, say why.

## Read These References

- `references/doc-sync-rules.md`

## Failure Modes To Avoid

- Assuming tests make docs updates unnecessary
- Forgetting operational runbooks
- Updating marketing-style docs while leaving technical docs stale
