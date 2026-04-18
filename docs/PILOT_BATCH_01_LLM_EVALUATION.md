# Pilot Batch 01 LLM Evaluation

## 목적

이 문서는 `pilot-batch-01`에 대해
LLM deep validation lane이 어떤 식으로 작동하는지 보여주는 샘플 결과 요약이다.

이 문서는 실제 prompt 출력 원문이 아니라,
lane별 verdict와 핵심 finding을 운영 문서 형태로 정리한 것이다.

## Batch Context

- batch id: `pilot-batch-01`
- route: `C2 + owner-aware context + governance lanes on trigger`
- evaluator policy:
  - review evaluator: `gpt-5.4 / high`
  - security evaluator: `gpt-5.4 / high`
  - release-gate evaluator: `gpt-5.4 / high`
  - architecture evaluator: `gpt-5.4 / high`

## Lane Summary

### 1. Review Evaluator

- overall verdict: `concern`
- strongest contribution:
  - `presence-race` 계열에서 hidden stale-state regression 가능성을 잘 짚음
  - execution report가 얕은 run에서는 artifact quality 자체를 지적함
- repeated weakness:
  - 일부 low-risk task에서는 medium/low finding이 다소 장황함

### 2. Security Evaluator

- overall verdict: `concern`
- strongest contribution:
  - `tenant-cache-scope`에서 tenant isolation risk articulation이 좋았음
  - auth boundary touched task에서 trust boundary language가 명확했음
- repeated weakness:
  - `flag-rollout-fallback`에서는 trigger가 과보수적이라 noise가 있었음

### 3. Release Gate Evaluator

- overall verdict: `pass`
- strongest contribution:
  - `code-ready`와 `release-ready` 분리를 일관되게 유지
  - rollback note 누락과 operator-visible missing artifact를 잘 드러냄
- repeated weakness:
  - low-risk task에서는 operator package completeness를 다소 엄격하게 보는 경향이 있음

### 4. Architecture Evaluator

- overall verdict: `pass`
- strongest contribution:
  - task-scoped fix가 잘 유지된 run을 positive signal로 읽을 수 있었음
  - shared abstraction 추가가 없을 때 “오히려 잘한 것”으로 판정 가능
- repeated weakness:
  - 구조 변화가 작은 task에서는 활용 가치가 제한적

## Representative Task Notes

### `tenant-cache-scope`

- review evaluator:
  - `pass`
  - tenant-scoped keying과 docs sync 정합성이 좋다고 평가
- security evaluator:
  - `concern`
  - delimiter collision과 tenant key canonicalization 잔여 리스크를 지적
- release-gate evaluator:
  - `pass`
  - rollback note만 보완되면 release-ready라고 판단

### `flag-rollout-fallback`

- review evaluator:
  - `pass`
  - fallback semantics와 docs sync가 깔끔하다고 평가
- security evaluator:
  - `concern`
  - 직접적 trust boundary 변경이 없는데도 secret/rollout path를 과하게 경계
- release-gate evaluator:
  - `pass`
  - operator checklist delta가 충분하다고 평가

## What The LLM Judges Added

- 일반 gate가 못 보는 reasoning quality를 드러냄
- release gate 판단의 적절성을 별도 lane으로 읽어냄
- owner-aware context가 실제로 artifact quality를 높였는지 읽을 수 있었음
- security trigger noise를 구체적으로 드러내 disagreement 분석 대상으로 만들었음

## What They Did Not Replace

- 테스트 통과 사실 자체
- 실제 배포 승인
- owner metadata 정확성의 최종 보증
- security absence proof

## Batch-Level Conclusion

`pilot-batch-01` 샘플 기준으로 보면
LLM deep validation은 다음처럼 쓰는 것이 맞다.

- review evaluator: default lane 유지
- release-gate evaluator: release-sensitive task에서 강한 가치
- security evaluator: 계속 쓰되 trigger를 더 좁혀야 함
- architecture evaluator: structural-risk task에서만 conditional 유지
