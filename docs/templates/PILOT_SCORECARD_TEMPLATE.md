# Pilot Scorecard

## 목적

이 템플릿은 pilot batch를 끝낸 뒤,
품질, governance, 효율, human intervention을 한 장의 scorecard로 정리하기 위한 기본 형식이다.

이 문서는 단순 pass/fail 기록이 아니라,
`baseline 대비 실제로 complex-case 운영 품질이 올라갔는가`를 판단하기 위한 의사결정 문서다.

## Batch Metadata

- batch id:
- review window:
- pilot team:
- service scope:
- default route:
- model / effort policy:
- compared baseline:

## Batch Composition

- total tasks:
- critical service tasks:
- high risk class tasks:
- approval-required tasks:
- release-sensitive tasks:
- security-review-triggered tasks:
- architecture-review-triggered tasks:

## Outcome Summary

- accepted changes:
- held changes:
- escalated changes:
- rejected changes:
- batch completion rate:

## Quality Metrics

- task success rate:
- deterministic gate pass rate:
- High review finding rate:
- rework rate:
- docs sync success rate:
- rollout or release defect count:

## Governance Metrics

- approval-required detection rate:
- approval escalation count:
- release hold precision notes:
- security review trigger precision notes:
- owner routing accuracy:
- rollback readiness miss count:

## Efficiency Metrics

- median elapsed time per task:
- median elapsed time by risk class:
- estimated median cost per task:
- human intervention count:
- human intervention per accepted change:
- governance overhead note:

## Failure Taxonomy Totals

- wrong_context:
- wrong_tool:
- hallucinated_assumption:
- over_edit:
- missed_test:
- handoff_failure:
- cross_file_regression:
- docs_desync:
- approval_miss:
- release_gate_false_positive:
- release_gate_false_negative:
- owner_routing_gap:
- security_review_noise:

## Strong Signals

- batch에서 가장 가치가 컸던 lane:
- complex-case에서 baseline보다 좋아진 점:
- 운영자가 실제로 신뢰할 수 있었던 artifact:

## Friction Signals

- 가장 많이 느려진 구간:
- noise가 많았던 lane:
- owner metadata가 부족했던 영역:
- model / effort가 과한 것으로 보인 구간:

## Representative Cases

### Best Example

- task id:
- 이유:
- evidence links:

### Worst Example

- task id:
- 이유:
- evidence links:

## Decision

- decision: `promote` | `narrow` | `rework` | `stop`
- decision rationale:
- next batch에서 유지할 것:
- next batch에서 제거하거나 약화할 것:
- next batch에서 추가 검증할 것:

## Required Evidence Links

- batch run package:
- trace directory:
- review findings bundle:
- approval decision bundle:
- release gate bundle:
- cost governance report:
