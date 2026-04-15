# Complex-Case Golden Set v0

초기 복잡한 케이스 `golden set` 10개 초안이다.

## Composition

- 4개: cross-file implementation
- 3개: regression-prone bug fix
- 2개: test and reliability hardening
- 1개: external SDK research-heavy implementation

## Files

- `complex-case-001-payment-idempotency-retry.json`
- `complex-case-002-rbac-scope-leak.json`
- `complex-case-003-realtime-presence-race.json`
- `complex-case-004-search-schema-migration.json`
- `complex-case-005-offline-sync-conflict-resolution.json`
- `complex-case-006-feature-flag-rollout-fallback.json`
- `complex-case-007-multi-tenant-cache-scope.json`
- `complex-case-008-upload-quarantine-security.json`
- `complex-case-009-async-job-flaky-hardening.json`
- `complex-case-010-sdk-upgrade-adapter.json`

## Usage Notes

- simple smoke set보다 complex-case 결과를 우선한다
- `C0`와 `C2`의 첫 비교는 이 세트 중 10개 전부 또는 최소 6개 이상으로 시작한다
- `High` review finding이 있으면 해당 run은 fail 처리한다
