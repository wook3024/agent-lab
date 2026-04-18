# Pilot Batch 01 Disagreement Analysis

## Context

- batch id: `pilot-batch-01`
- task id: `flag-rollout-fallback`
- lane: `security`
- compared evaluators: `security evaluator` vs `human pilot reviewer`
- human reviewer involved: `platform-runtime tech lead`

## Disagreement Summary

- 무엇이 충돌했는가:
  - security evaluator는 `concern`
  - human reviewer는 `pass-with-release-note`
- verdict mismatch:
  - `concern` vs `pass`
- severity mismatch:
  - evaluator는 `medium security concern`
  - human은 `no security finding`

## Shared Evidence

- task brief: feature flag fallback semantics 복원
- diff: `app/flags.py`, `app/telemetry.py`, `docs/feature_flags.md`, `ops/feature_rollout.md`
- trace: release-sensitive but no auth / tenant / secret touched
- review findings: general review `0 high / 0 medium / 0 low`
- governance artifacts: release artifact package 존재

## Interpretation Gap

- evaluator는 어떻게 해석했는가:
  - rollout fallback이 잘못되면 stale targeting이나 unintended exposure로 이어질 수 있으므로 security concern으로 판단
- human은 어떻게 해석했는가:
  - 이 변경은 availability / rollout correctness 문제이지 trust boundary 변경은 아니므로 release gate lane이면 충분하다고 봄
- 어느 artifact가 가장 다르게 읽혔는가:
  - task brief의 `release-sensitive` 성격과 security trigger 사이의 경계

## Root Cause Guess

- prompt issue: 일부 있음
- rubric issue: 있음
- missing artifact issue: 없음
- owner metadata issue: 일부 있음
- true ambiguity: 낮음

핵심 원인:

- `security-review` trigger가 `release-sensitive`와 `security-sensitive`를 충분히 분리하지 못했음
- evaluator prompt도 rollout risk를 security concern으로 읽을 여지가 있었음

## Resolution

- 최종 accepted interpretation:
  - 이 케이스는 `security concern`이 아니라 `release gate / rollout correctness concern`
- 왜 그렇게 결정했는가:
  - auth, PII, secret, tenant boundary가 직접 바뀌지 않았고
  - 문제의 본질은 trust boundary가 아니라 rollout fallback correctness였기 때문
- next batch에서 무엇을 바꿀 것인가:
  - security trigger를 `auth / PII / secret / tenant boundary / trust boundary`로 더 명확히 좁힘
  - release-sensitive only task는 release-gate evaluator로 우선 라우팅

## Registry / Prompt Follow-Up

- registry update needed:
  - `security-review.decision_gate = narrow-trigger-to-auth-pii-secret-tenant-boundary`
- evaluator prompt update needed:
  - release risk와 security risk를 명시적으로 분리
- trigger narrowing needed:
  - yes
- additional human calibration needed:
  - yes, release-sensitive but non-security task 1개 추가
