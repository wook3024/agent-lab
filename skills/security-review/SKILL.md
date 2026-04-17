---
name: security-review
description: Perform a focused security review on auth, permission, data exposure, secret handling, auditability, and trust-boundary changes. Use when a code change touches security-sensitive surfaces and a separate security lane should evaluate exploitability rather than general code quality alone.
---

# Security Review

Review from an attacker or policy-break perspective, not just a correctness perspective.

## Workflow

1. Read the task brief, context pack, diff, execution report, and general review findings.
2. Confirm whether security-sensitive surfaces were touched.
3. Inspect:
   - auth / RBAC / permission boundaries
   - tenant isolation
   - data exposure and sensitive field handling
   - secret / token / credential handling
   - audit logging and traceability
   - external trust boundaries such as webhooks, callbacks, uploads, and scanners
4. Describe an exploit path or misuse path for each serious finding.
5. Report findings in the required security severity schema.

## Rules

- Do not inflate ordinary quality issues into security issues.
- Do not downplay auth bypass, tenant isolation breaks, PII exposure, or secret leakage because tests passed.
- A missing audit trail can be a meaningful finding when operations or compliance depend on it.
- If a path is security-sensitive but insufficiently tested, call that out explicitly.
- Prefer concrete exploitability over vague fear language.

## Output Contract

Mirror `../../docs/templates/SECURITY_REVIEW_TEMPLATE.md`.

## Failure Modes To Avoid

- Missing an auth or permission bypass
- Missing a tenant-boundary or cache-scope exposure
- Treating secret handling as a normal refactor detail
- Ignoring audit logging regressions on privileged flows
