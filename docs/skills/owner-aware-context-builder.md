# Skill Spec: owner-aware-context-builder

## Trigger Description Draft

일반 context pack에 owner team, service criticality, relevant runbook, last incident context, approval path를 추가해 reviewer와 governance lane의 품질을 높이는 skill이다. ownership이 중요한 서비스 변경에서 사용한다.

## Core Workflow

1. task brief와 changed/relevant files를 읽는다
2. owner map과 service criticality를 조회한다
3. owner-specific 문서, runbook, release note 관점에서 필요한 자료만 골라 넣는다
4. last incident 또는 known risk context가 있으면 최소한으로 포함한다
5. execution, review, release gate가 같은 ownership reality를 공유하도록 handoff pack을 만든다

## Added Lenses Versus Basic Context Pack

- primary owner and secondary owner
- service criticality
- owner-specific runbooks
- last incident or recent operational change
- approval and release path hints

## Output Contract

- [OWNER_AWARE_CONTEXT_PACK_TEMPLATE.md](/Users/shinukyi/Gallary/projects/proto/agent-lab/docs/templates/OWNER_AWARE_CONTEXT_PACK_TEMPLATE.md:1) 형식을 따른다
- broad context를 늘리는 방식이 아니라 ownership-relevant 정보만 정밀하게 추가한다

## Likely Failure Modes

- `owner_context_omission`
- `criticality_blind_context`
- `runbook_gap_in_handoff`

## Forward-Test Scenarios

- auth service permission hotfix
- shared cache regression on a critical platform service
- release with known recent incident overlap
