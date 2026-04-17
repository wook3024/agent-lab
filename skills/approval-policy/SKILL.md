---
name: approval-policy
description: Classify engineering changes by approval tier and identify which actions must stop for explicit human approval. Use when a change may touch destructive, privileged, production-affecting, or policy-sensitive surfaces and the system must distinguish what can proceed automatically from what cannot.
---

# Approval Policy

Classify first, then decide what is allowed now.

## Workflow

1. Read the task brief, change scope, and known constraints.
2. Classify the work as one of:
   - `read-only`
   - `safe write`
   - `moderate`
   - `risky`
   - `irreversible`
3. Identify which actions are auto-allowable now and which must stop for approval.
4. Record required approvers and escalation reasons.
5. Make the approval boundary explicit for downstream execution and release steps.

## Rules

- If classification is ambiguous, choose the more conservative tier.
- Destructive, privileged, production-affecting, payment-related, permission-related, and data-migration changes should never silently fall into a lower tier.
- Separate "code can be prepared" from "code can be deployed" when needed.
- Approval classification must name the trigger, not just the tier label.
- Do not assume a task is safe because the diff is small.

## Classification Hints

- `read-only`: inspection, search, log review, docs lookup
- `safe write`: tests, comments, local docs with no behavior change
- `moderate`: normal feature fixes or refactors within approved scope
- `risky`: schema, auth, external config, privilege, large rename, migration
- `irreversible`: deploy, production shell, live-data delete, billing or permission changes in production

## Output Contract

Mirror `../../docs/templates/APPROVAL_DECISION_TEMPLATE.md`.

## Failure Modes To Avoid

- Under-classifying a risky change because it "looks small"
- Mixing allowed-now actions with blocked actions
- Missing the approval owner
- Treating irreversible steps as ordinary execution
