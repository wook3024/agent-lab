# Skill Spec: release-gate

## Trigger Description Draft

구현과 검증이 끝난 변경을 실제 릴리즈 가능한지 판정하는 control-plane skill이다. gate 통과 여부만이 아니라 review finding, owner approval, rollback readiness, runbook completeness를 함께 본다.

## Core Workflow

1. task brief, execution report, gate 결과, review findings를 읽는다
2. release risk class와 변경 표면을 정리한다
3. unresolved blocker, missing approval, rollback readiness를 판정한다
4. `release-ready`, `hold`, `escalate` 중 하나로 결론을 내린다
5. operator follow-up과 release note / runbook 상태를 함께 기록한다

## Output Contract

- [RELEASE_GATE_DECISION_TEMPLATE.md](/Users/shinukyi/Gallary/projects/proto/agent-lab/docs/templates/RELEASE_GATE_DECISION_TEMPLATE.md:1) 형식을 따른다
- skipped gate와 missing approval은 blocker 또는 explicit risk로 남긴다

## Likely Failure Modes

- `false_release_ready`
- `missing_approval_blindness`
- `rollback_omission`
- `operator_handoff_failure`

## Forward-Test Scenarios

- feature rollout with partial telemetry coverage
- auth scope change without owner signoff
- schema migration without rollback note
