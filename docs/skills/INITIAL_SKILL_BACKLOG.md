# Initial Skill Backlog

## Goal

`C2`를 실제로 구현 가능한 수준으로 만들기 위해 필요한 핵심 skill 초안을 우선순위대로 정리한다.

## Wave 1: Must-Have For C2

1. `task-brief-author`
2. `context-pack-builder`
3. `execution-engineering`
4. `review-findings`
5. `quality-gates-runner`
6. `trace-eval-recorder`
7. `docs-sync`

이 7개가 있어야 `Triage -> Context -> Execution -> Gates -> Review`가 운영 가능한 시스템이 된다.

## Wave 2: Conditional For C3

1. `research-grounded`

이 skill은 외부 SDK, 정책, 플랫폼 제약, 설계 비교가 실제 품질 bottleneck으로 확인될 때 활성화한다.

## Implementation Order

1. `task-brief-author`
2. `context-pack-builder`
3. `execution-engineering`
4. `review-findings`
5. `quality-gates-runner`
6. `trace-eval-recorder`
7. `docs-sync`
8. `research-grounded`

## Why This Order

- 앞의 네 skill이 복잡한 케이스의 실패 원인인 `wrong_context`, `over_edit`, `missed_test`를 가장 직접적으로 줄인다
- 뒤의 세 skill은 quality gate와 관측성, 문서 동기화를 강화한다
- `research-grounded`는 모든 작업에 필요한 기본 skill이 아니므로 baseline 이후에 붙인다
