# Skill Spec: task-brief-author

## Trigger Description Draft

모호하거나 범위가 넓은 개발 요청을 `Goal`, `Done When`, `Non-Goals`, `Risk`, `Approval Requirements`가 명확한 작업 브리프로 정규화하는 skill이다. 복잡한 구현, 고위험 버그 수정, cross-file 변경, 설계/운영 제약이 섞인 작업에서 사용한다.

## Core Workflow

1. 원 요청에서 변경 목표와 성공 조건을 분리한다
2. 하지 않을 일과 범위 밖 변경을 명시한다
3. 승인 대상 작업이 섞여 있는지 표시한다
4. reviewer가 특히 봐야 할 위험 포인트를 적는다

## Output Contract

- [TASK_BRIEF_TEMPLATE.md](/Users/shinukyi/Gallary/projects/proto/agent-lab/docs/templates/TASK_BRIEF_TEMPLATE.md:1) 형식을 채운다
- 작업 범위를 넓히는 모호한 표현을 남기지 않는다

## Likely Failure Modes

- `insufficient_spec`
- `over_edit`
- `wrong_context`

## Forward-Test Scenarios

- cross-file bugfix
- migration safety change
- docs + code sync change
