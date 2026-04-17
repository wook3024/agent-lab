# Skill Spec: approval-policy

## Trigger Description Draft

변경 작업을 `read-only`, `safe write`, `moderate`, `risky`, `irreversible`로 분류하고, 어떤 승인과 escalation이 필요한지 판정하는 control-plane skill이다.

## Core Workflow

1. task brief와 change surface를 읽는다
2. destructive, privileged, production-affecting, policy-sensitive 변경 여부를 확인한다
3. approval tier를 판정한다
4. 지금 허용 가능한 작업과 사람 승인이 필요한 작업을 분리한다
5. required approvers와 escalation reason을 기록한다

## Output Contract

- [APPROVAL_DECISION_TEMPLATE.md](/Users/shinukyi/Gallary/projects/proto/agent-lab/docs/templates/APPROVAL_DECISION_TEMPLATE.md:1) 형식을 따른다
- ambiguous case는 낮은 tier로 내리지 않고 보수적으로 분류한다

## Likely Failure Modes

- `silent_risky_allow`
- `irreversible_action_underclassification`
- `approval_scope_confusion`

## Forward-Test Scenarios

- schema migration with backfill
- external service permission update
- production config change hidden inside feature work
