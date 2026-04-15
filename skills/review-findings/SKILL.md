---
name: review-findings
description: Perform an independent review pass focused on regressions, missing requirements, test gaps, security risks, and operational hazards. Use after complex implementations where a separate reviewer must report concrete findings instead of re-implementing the change.
---

# Review Findings

Review independently and report only concrete findings.

## Workflow

1. Read the task brief and context pack first.
2. Read the diff and verification results.
3. Look for requirement misses, regression risks, test gaps, and operational hazards.
4. Report findings by severity.
5. Record residual risks that still need validation.

## Rules

- Prefer defects over stylistic suggestions.
- Do not rewrite the implementation during review.
- If there are no findings, state that explicitly and still list residual risks.
- Tie each finding to a file, behavior, or reproduction path.

## Output Contract

Mirror `../../docs/templates/REVIEW_FINDINGS_TEMPLATE.md`.

## Read These References

- `references/severity-rubric.md` for severity calibration

## Failure Modes To Avoid

- Generic praise with no defects
- Weak severity calibration
- Missing a test gap because the code "looks fine"
- Mixing design preferences into High severity findings
