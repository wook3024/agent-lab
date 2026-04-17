---
name: incident-mode-policy
description: Apply stricter decision rules for hotfixes and incidents, including freeze handling, required communications, approval compression, and rollback obligations. Use when production impact or degraded service requires a temporary mode switch without losing auditability.
---

# Incident Mode Policy

Move faster in incidents without pretending governance no longer matters.

## Workflow

1. Confirm whether the work is in normal mode, incident mode, or hotfix mode.
2. State why the mode switch is justified.
3. List what shortcuts are allowed and what controls remain mandatory.
4. Record required approvers, communications, and rollback expectations.
5. Require post-incident cleanup and documentation obligations before closing the loop.

## Rules

- Incident mode can compress approval paths, but it must never remove accountability.
- Freeze override must be recorded explicitly.
- Auth, data exposure, and irreversible actions still require named approvers.
- If rollback is impossible, escalate rather than silently proceeding.
- Temporary mitigations must carry follow-up obligations.

## Output Contract

Mirror `../../docs/templates/INCIDENT_MODE_DECISION_TEMPLATE.md`.

## Failure Modes To Avoid

- Using incident mode as a blanket excuse to skip governance
- Forgetting required communications
- Leaving hotfix debt with no owner
