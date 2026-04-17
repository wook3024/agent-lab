# Pilot Sample Run Package

## Scenario

- task: `tenant-cache-scope`
- service: `shared-cache`
- owner team: `platform-runtime`
- criticality: `high`
- task type: `implementation`
- risk class: `risky`

이 예시는 현재 `agent-lab` 자산이 실제 pilot run에서 어떤 문서 흐름으로 연결되는지 보여주기 위한 샘플 패키지다.

## Required Run Documents

### 1. Task Brief

- goal: tenant boundary를 깨지 않으면서 project summary cache key를 정정한다
- done when:
  - cache collision이 사라진다
  - regression test가 추가된다
  - caching docs가 갱신된다
- non-goals:
  - unrelated cache refactor
  - cross-service cache abstraction 도입

### 2. Owner-Aware Context Pack

- primary owner: `platform-runtime`
- secondary owner: `tenant-safety`
- service criticality: `high`
- owner docs:
  - caching runbook
  - multi-tenant architecture doc
- recent incident:
  - tenant leakage alert on stale cache scope
- required reviewers:
  - `platform-runtime`
  - `tenant-safety`

### 3. Execution Report

- changed files:
  - `app/cache_keys.py`
  - `app/project_summary_service.py`
  - `tests/test_tenant_cache_scope.py`
  - `docs/caching.md`
- residual risks:
  - downstream cache invalidation policy는 변경하지 않음

### 4. General Review Findings

- expected outcome:
  - no High findings
  - residual risk only if invalidation semantics remain unchanged

### 5. Security Review Findings

- triggered because:
  - tenant isolation boundary touched
- expected focus:
  - cross-tenant exposure path
  - delimiter collision / canonicalization risk

### 6. Approval Decision

- classification: `risky`
- required approvals:
  - owner approval from `platform-runtime`
- blocked actions before approval:
  - production rollout

### 7. Release Gate Decision

- target default:
  - `hold` until owner approval complete
- checks:
  - rollback note present
  - operator runbook updated
  - release note mention tenant boundary risk

### 8. Release Artifact Package

- release note draft:
  - “Fix tenant-scoped cache key collision in project summary path”
- operator checklist delta:
  - verify cache key rollout and no cross-tenant hit anomalies
- rollback note:
  - revert cache key generation and flush affected cache namespace

### 9. Trace Record

- owner team
- service criticality
- role model/effort map
- approval state
- release state
- human intervention count

## What This Sample Proves

이 샘플은 현재 자산이 단순 benchmark 설명을 넘어서, 실제 운영 문서 패키지로 이어질 수 있다는 점을 보여준다.

특히 다음 흐름이 중요하다.

1. owner-aware context가 execution과 review 품질을 높인다
2. security review는 tenant boundary 변경에 자동으로 붙는다
3. approval policy는 “코드는 준비 가능하지만 배포는 보류”를 분리한다
4. release gate는 gate pass와 release-ready를 구분한다
5. release artifact package는 operator handoff를 문서화한다

## Recommended Next Sample

다음 샘플 패키지는 아래가 좋다.

- `flag-rollout-fallback`
  - release gate와 rollback note가 더 중요하게 작동하는 케이스
- `presence-race`
  - architecture review와 incident-mode-policy가 더 중요하게 작동하는 케이스
