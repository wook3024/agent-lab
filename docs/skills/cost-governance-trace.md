# Skill Spec: cost-governance-trace

## Trigger Description Draft

복잡한 개발 작업의 trace를 비용·지연·품질·사람 개입 관점까지 확장해, CTO가 role/task/team 기준으로 운영 효율을 판단할 수 있게 만드는 control-plane skill이다.

## Core Workflow

1. run trace에서 role별 model, effort, token, latency, approval 상태를 수집한다
2. task type, team, risk class 기준으로 집계 단위를 정한다
3. quality-first route와 cost-optimized route를 비교한다
4. human intervention, blocker, rework 신호를 비용과 함께 본다
5. 운영 정책에 쓸 수 있는 cost report를 만든다

## Required Inputs

- trace record
- scorecard record
- role-to-model mapping
- role-to-effort mapping
- approval / release / owner metadata

## Output Contract

- [COST_GOVERNANCE_REPORT_TEMPLATE.md](/Users/shinukyi/Gallary/projects/proto/agent-lab/docs/templates/COST_GOVERNANCE_REPORT_TEMPLATE.md:1) 형식을 따른다
- run-level trace는 [TRACE_RECORD_TEMPLATE.json](/Users/shinukyi/Gallary/projects/proto/agent-lab/docs/templates/TRACE_RECORD_TEMPLATE.json:1) 확장 필드를 따른다

## Likely Failure Modes

- `cost_without_quality_context`
- `missing_role_breakdown`
- `latency_blind_routing`
- `human_intervention_underreporting`

## Forward-Test Scenarios

- triage/context mini downshift 비교
- quality-first versus cost-optimized routing 비교
- pilot team monthly cost simulation
