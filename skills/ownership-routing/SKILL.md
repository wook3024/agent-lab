---
name: ownership-routing
description: Route complex changes to the correct owner teams, reviewers, and approval paths based on changed files and service criticality. Use when the system must decide who is accountable for a change and which stricter gates or escalations should apply.
---

# Ownership Routing

Figure out who owns the change before assuming the default path is safe.

## Workflow

1. Read changed files or relevant files for the task.
2. Match them against the owner map and criticality metadata.
3. Produce:
   - primary owner team
   - secondary or dependent teams
   - required reviewers
   - release approvers
   - stricter gates or escalations
4. Mark unmapped paths explicitly.
5. Pass the routing decision into review, approval, and release steps.

## Rules

- Unmapped critical paths are not acceptable defaults; surface them as routing gaps.
- Shared platform or critical service paths should trigger stricter routing, not generic routing.
- Separate "who should review the code" from "who must approve release."
- Prefer deterministic path-based routing first; add heuristics only as a secondary layer.

## Output Contract

Mirror `../../docs/templates/OWNER_ROUTING_DECISION_TEMPLATE.md`.

## Failure Modes To Avoid

- Routing a critical change to only the local implementation team
- Ignoring shared-platform ownership
- Treating missing owner metadata as harmless
