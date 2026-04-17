# Skill Spec: ownership-routing

## Trigger Description Draft

변경 파일과 서비스 criticality를 기준으로 owner team, required reviewers, stricter gate lane을 계산하는 routing skill이다. 품질만큼 “누가 책임지는가”를 운영 계층에서 분명히 하기 위해 사용한다.

## Core Workflow

1. changed files 또는 relevant files를 읽는다
2. path-to-owner 매핑과 service criticality를 조회한다
3. primary owner, secondary owner, required reviewers를 계산한다
4. critical path 여부에 따라 stricter gate와 approval escalation을 붙인다
5. owner-aware routing decision을 기록한다

## Required Inputs

- changed files
- owner map config
- service criticality map
- task risk class

## Output Contract

- [OWNER_ROUTING_DECISION_TEMPLATE.md](/Users/shinukyi/Gallary/projects/proto/agent-lab/docs/templates/OWNER_ROUTING_DECISION_TEMPLATE.md:1) 형식을 따른다
- owner가 없으면 `unmapped`로 남기고 조용히 통과시키지 않는다

## Likely Failure Modes

- `unowned_change_silence`
- `critical_service_under_routing`
- `reviewer_gap`

## Forward-Test Scenarios

- payment schema migration
- auth service permission change
- tenant cache scope regression
- release affecting shared platform module
