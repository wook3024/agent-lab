---
name: owner-aware-context-builder
description: Build a narrow context pack that includes owner team, service criticality, runbooks, recent incidents, and approval hints. Use when a change touches services where review, release, and escalation quality depend on ownership-aware context rather than code context alone.
---

# Owner-Aware Context Builder

Build the smallest context pack that still reflects who owns the service and what operational reality surrounds it.

## Workflow

1. Start from the task brief and the relevant or changed files.
2. Use owner mapping and service criticality to identify which operational context matters.
3. Add only the owner-relevant docs, runbooks, recent incidents, and approval hints that will materially improve execution, review, or release decisions.
4. Keep the pack narrow; ownership context should sharpen the handoff, not widen it.
5. Produce a handoff package that execution, review, and governance steps can share.

## Rules

- Do not dump every on-call or runbook link for a service; include only what matters to this task.
- If ownership is missing, mark it explicitly as a gap.
- Critical services should carry stronger release and review context than non-critical services.
- Prefer deterministic metadata from owner maps over vague guesses.

## Output Contract

Mirror `../../docs/templates/OWNER_AWARE_CONTEXT_PACK_TEMPLATE.md`.

## Failure Modes To Avoid

- Treating critical services like ordinary services
- Omitting runbook or incident context for risky changes
- Expanding the pack with noisy ownership information
