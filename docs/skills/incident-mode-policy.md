# Skill Spec: incident-mode-policy

## Trigger Description Draft

incident, hotfix, freeze, degraded-service 상황에서 normal implementation flow와 다른 승인, 검증, 커뮤니케이션 규칙을 적용하는 policy skill이다.

## Core Workflow

1. task가 incident / hotfix / degraded service / freeze override 상황인지 판정한다
2. normal flow 대신 incident mode lane으로 전환할 필요가 있는지 본다
3. 허용 가능한 shortcut과 절대 건너뛰면 안 되는 검증을 분리한다
4. required approvers, communication obligations, rollback obligations를 기록한다
5. incident mode decision과 follow-up requirements를 남긴다

## Required Inputs

- task brief
- risk class
- service criticality
- approval state
- release context

## Output Contract

- [INCIDENT_MODE_DECISION_TEMPLATE.md](/Users/shinukyi/Gallary/projects/proto/agent-lab/docs/templates/INCIDENT_MODE_DECISION_TEMPLATE.md:1) 형식을 따른다
- normal mode와 incident mode가 섞이지 않게 rule changes를 명시한다

## Likely Failure Modes

- `incident_shortcut_overreach`
- `freeze_bypass_without_record`
- `rollback_obligation_omission`

## Forward-Test Scenarios

- production auth outage hotfix
- release freeze during critical incident
- degraded-service patch with temporary mitigation
