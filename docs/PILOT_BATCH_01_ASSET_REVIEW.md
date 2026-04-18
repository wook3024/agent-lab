# Pilot Batch 01 Asset Review

## 목적

이 문서는 `pilot-batch-01` 결과를 기준으로,
실제로 어떤 자산이 유지, 승격 후보, 축소, 재작업 대상인지 판단한 샘플 review다.

이 문서는 [ASSET_REVIEW_WORKFLOW.md](./ASSET_REVIEW_WORKFLOW.md)의 결과물이 어떤 모양이어야 하는지 보여주는 예시이기도 하다.

## Batch Context

- batch id: `pilot-batch-01`
- route: `C2 + owner-aware context + triggered governance lanes`
- model policy: `gpt-5.4/high`
- compared baseline: `C2 baseline without pilot control-plane`

## Asset Decisions

### 1. `release-gate`

- current status: `pilot`
- decision: `keep`
- observed value:
  - release-ready와 code-ready를 구분하는 데 가장 유용했음
  - `hold` 1건은 rollback note 누락을 적절히 잡아냈음
- observed friction:
  - 없음. 현재 batch에서는 false hold가 없었음
- registry update intent:
  - `last_validated_batch = pilot-batch-01`
  - `decision_gate = needs-1-more-pilot-batch-before-standard-consideration`

### 2. `approval-policy`

- current status: `pilot`
- decision: `keep`
- observed value:
  - approval-required 3건을 모두 잡아냈음
  - production rollout 전 human approval이 필요한 경계를 명확히 했음
- observed friction:
  - escalation note는 충분했으나 operator-friendly wording은 더 다듬을 수 있음
- registry update intent:
  - `last_validated_batch = pilot-batch-01`
  - `decision_gate = needs-one-more-batch-and-operator-feedback`

### 3. `security-review`

- current status: `pilot`
- decision: `narrow`
- observed value:
  - tenant isolation touched task에서는 확실히 가치가 있었음
  - auth boundary task에서 residual risk articulation이 좋았음
- observed friction:
  - `flag-rollout-fallback`에서는 실익보다 보수적 해석이 강했음
  - release-sensitive지만 trust-boundary가 직접 바뀌지 않는 task에선 trigger가 과함
- registry update intent:
  - `last_validated_batch = pilot-batch-01`
  - `decision_gate = narrow-trigger-to-auth-pii-secret-tenant-boundary`

### 4. `ownership-routing`

- current status: `pilot`
- decision: `rework`
- observed value:
  - `shared-cache`와 `payments` 경계에서는 reviewer route가 정확했음
- observed friction:
  - `frontend/flags/` secondary ownership 정의가 부족해 one-hop escalation에 사람이 개입해야 했음
  - owner map coverage가 아직 팀 전체 기준으로 충분하지 않음
- registry update intent:
  - `last_validated_batch = pilot-batch-01`
  - `decision_gate = needs-owner-map-coverage-improvement`

### 5. `owner-aware-context-builder`

- current status: `pilot`
- decision: `keep`
- observed value:
  - context 폭을 넓히지 않고도 reviewer focus와 runbook relevance를 높였음
  - pilot route에서 가장 실전적인 품질 향상 자산 중 하나였음
- observed friction:
  - owner metadata가 비어 있으면 바로 약해짐
- registry update intent:
  - `last_validated_batch = pilot-batch-01`
  - `decision_gate = needs-second-batch-before-standard-consideration`

### 6. `release-artifact-generator`

- current status: `pilot`
- decision: `keep`
- observed value:
  - operator handoff에서 release note / rollback note 정리가 유용했음
- observed friction:
  - 일부 low-risk task에서는 과할 수 있음
- registry update intent:
  - `last_validated_batch = pilot-batch-01`
  - `decision_gate = keep-for-release-sensitive-only`

### 7. `complex-case-default-gpt54-high`

- current status: `standard`
- decision: `keep`
- observed value:
  - pilot control-plane을 검증하는 동안 confounder를 줄이는 안정적 default였음
- observed friction:
  - low-risk tail task에는 다소 비싼 느낌이 있음
- registry update intent:
  - `last_validated_batch = pilot-batch-01`
  - `decision_gate = keep-unless-mini-downshift-proves-safe`

### 8. `mini-triage-context-downshift`

- current status: `conditional`
- decision: `keep`
- observed value:
  - 이번 batch에서는 직접 시험하지 않았음
- observed friction:
  - pilot control-plane 검증과 동시에 바꾸면 비교가 흐려짐
- registry update intent:
  - 상태 유지
  - 다음 batch에서 별도 실험 대상으로 유지

## Batch-Level Conclusion

이 sample review 기준으로 보면:

- immediate promote는 아직 없음
- `release-gate`, `approval-policy`, `owner-aware-context-builder`는 승격 유력 후보
- `security-review`, `ownership-routing`은 trigger/metadata 품질 보강이 먼저

즉, 첫 pilot batch의 가장 현실적인 판정은 다음이다.

- `keep`: `release-gate`, `approval-policy`, `owner-aware-context-builder`, `release-artifact-generator`
- `narrow`: `security-review`
- `rework`: `ownership-routing`
- `keep as standard`: `complex-case-default-gpt54-high`

## Recommended Next Batch Focus

다음 batch에서는 아래 3개를 중심으로 검증하는 것이 좋다.

1. `ownership-routing` owner map coverage 보강
2. `security-review` trigger precision 개선
3. `owner-aware-context-builder`의 second-batch 재현성 확인
