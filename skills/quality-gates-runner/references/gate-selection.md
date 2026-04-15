# Gate Selection

Always include:

- tests
- lint
- typecheck

Add docs sync when behavior, operators, or public docs changed.

Add security scan when:

- auth, permissions, data exposure, upload, billing, secrets, or tenant isolation are involved.

Add migration safety when:

- schema, backfill, or data shape changes are involved.

Add retry or concurrency checks when:

- workers, queues, reconnects, stale events, or idempotency are involved.
