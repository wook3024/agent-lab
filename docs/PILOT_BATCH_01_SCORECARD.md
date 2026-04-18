# Pilot Batch 01 Scorecard

## Batch Metadata

- batch id: `pilot-batch-01`
- review window: `2026-04-18`
- pilot team: `platform-runtime`
- service scope: `shared-cache`, `feature-flag-delivery`, `auth-service`, `payments`
- default route: `C2 + owner-aware context + governance lanes on trigger`
- model / effort policy: `gpt-5.4/high`
- compared baseline: `C2 baseline without pilot control-plane`

## Batch Composition

- total tasks: `6`
- critical service tasks: `4`
- high risk class tasks: `4`
- approval-required tasks: `3`
- release-sensitive tasks: `2`
- security-review-triggered tasks: `3`
- architecture-review-triggered tasks: `1`

## Outcome Summary

- accepted changes: `4`
- held changes: `1`
- escalated changes: `1`
- rejected changes: `0`
- batch completion rate: `83%`

## Quality Metrics

- task success rate: `5 / 6`
- deterministic gate pass rate: `6 / 6`
- High review finding rate: `0 / 6`
- rework rate: `1 / 6`
- docs sync success rate: `6 / 6`
- rollout or release defect count: `0`

## Governance Metrics

- approval-required detection rate: `3 / 3`
- approval escalation count: `2`
- release hold precision notes: `hold 1건은 타당했고 false hold는 없었음`
- security review trigger precision notes: `3건 중 2건은 유의미, 1건은 다소 보수적`
- owner routing accuracy: `5 / 6`
- rollback readiness miss count: `1`

## Efficiency Metrics

- median elapsed time per task: `24m`
- median elapsed time by risk class:
  - `critical / risky`: `31m`
  - `high / moderate`: `19m`
- estimated median cost per task: `$4.80`
- human intervention count: `3`
- human intervention per accepted change: `0.75`
- governance overhead note: `baseline 대비 느려졌지만 hold / escalation 품질을 고려하면 수용 가능`

## Failure Taxonomy Totals

- wrong_context: `0`
- wrong_tool: `0`
- hallucinated_assumption: `1`
- over_edit: `0`
- missed_test: `0`
- handoff_failure: `1`
- cross_file_regression: `0`
- docs_desync: `0`
- approval_miss: `0`
- release_gate_false_positive: `0`
- release_gate_false_negative: `0`
- owner_routing_gap: `1`
- security_review_noise: `1`

## Strong Signals

- batch에서 가장 가치가 컸던 lane: `owner-aware context + release gate`
- complex-case에서 baseline보다 좋아진 점:
  - `release-ready`와 `code-ready`를 분리해서 판단할 수 있었음
  - owner routing이 있는 task에서는 reviewer focus가 더 빨리 정렬됨
  - approval-required 변경이 조용히 진행되지 않았음
- 운영자가 실제로 신뢰할 수 있었던 artifact:
  - release gate decision
  - release artifact package
  - owner-aware context pack

## Friction Signals

- 가장 많이 느려진 구간: `security review가 붙은 auth / tenant 경계 변경`
- noise가 많았던 lane: `security review 1건은 실익보다 보수적 해석이 강했음`
- owner metadata가 부족했던 영역: `frontend/flags/` 경계의 secondary reviewer 정의
- model / effort가 과한 것으로 보인 구간: `low-risk docs sync only follow-up에는 gpt-5.4/high가 과함`

## Representative Cases

### Best Example

- task id: `tenant-cache-scope`
- 이유:
  - owner-aware context와 security review가 실제 tenant isolation risk를 잘 좁혔음
  - release gate가 rollback note 누락을 잡아내고 hold 대신 보완 후 진행이 가능했음
- evidence links:
  - `docs/PILOT_SAMPLE_RUN_PACKAGE.md`
  - `docs/PILOT_BATCH_01_ASSET_REVIEW.md`

### Worst Example

- task id: `flag-rollout-fallback`
- 이유:
  - owner routing은 맞았지만 security review trigger가 다소 과보수적으로 붙었음
  - release artifact package는 유용했으나 secondary owner metadata가 부족했음
- evidence links:
  - `docs/PILOT_BATCH_01_ASSET_REVIEW.md`
  - `docs/PILOT_BATCH_01_REGISTRY_UPDATE_EXAMPLE.md`

## Decision

- decision: `rework-and-continue`
- decision rationale:
  - pilot control-plane은 운영 가치가 분명했지만
  - owner map 정밀도와 security review trigger 범위는 한 번 더 다듬어야 함
- next batch에서 유지할 것:
  - `release-gate`
  - `approval-policy`
  - `owner-aware-context-builder`
- next batch에서 제거하거나 약화할 것:
  - `security-review` trigger를 일부 release-only task에서 약화
- next batch에서 추가 검증할 것:
  - `ownership-routing` metadata quality
  - `release-artifact-generator`의 operator usefulness

## Required Evidence Links

- batch run package: `docs/PILOT_SAMPLE_RUN_PACKAGE.md`
- trace directory: `artifacts/benchmark_runs/`
- review findings bundle: `docs/PILOT_BATCH_01_ASSET_REVIEW.md`
- approval decision bundle: `docs/PILOT_BATCH_01_REGISTRY_UPDATE_EXAMPLE.md`
- release gate bundle: `docs/PILOT_BATCH_01_REGISTRY_UPDATE_EXAMPLE.md`
- cost governance report: `docs/templates/COST_GOVERNANCE_REPORT_TEMPLATE.md`
