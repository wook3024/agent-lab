---
name: research-grounded
description: Use primary sources to de-risk complex implementation choices involving external SDKs, platform rules, protocols, or policies. Use when a coding decision cannot be made safely from local repository context alone and unsupported assumptions would create costly rework.
---

# Research Grounded

Research only what is needed, and ground claims in primary sources.

## Workflow

1. Narrow the question to one implementation decision.
2. Prefer official docs, specs, or primary references.
3. Map each important claim to a source.
4. Separate known facts, inferred guidance, and unresolved uncertainty.
5. Return a recommendation that implementation can act on.

## Rules

- Do not browse aimlessly.
- Avoid speculative conclusions.
- Use secondary sources only when the primary source is missing or incomplete.
- Call out when a recommendation is an inference, not a quoted fact.

## Read These References

- `references/source-hierarchy.md`

## Failure Modes To Avoid

- Hallucinated policy interpretations
- Missing version-specific behavior
- Treating blog posts as authoritative
