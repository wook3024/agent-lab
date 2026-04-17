# Skill Spec: release-artifact-generator

## Trigger Description Draft

코드 변경 이후 operator와 release approver가 바로 사용할 수 있는 릴리즈 패키지를 생성하는 skill이다. release note, operator checklist delta, rollback note를 표준 형식으로 만들어 handoff 품질을 높인다.

## Core Workflow

1. task brief, execution report, release gate decision, approval state를 읽는다
2. user-visible impact, operator-visible impact, rollback implications를 분리한다
3. release note draft를 작성한다
4. operator checklist delta를 정리한다
5. rollback note와 known risks를 기록한다

## Output Contract

- [RELEASE_ARTIFACT_PACKAGE_TEMPLATE.md](/Users/shinukyi/Gallary/projects/proto/agent-lab/docs/templates/RELEASE_ARTIFACT_PACKAGE_TEMPLATE.md:1) 형식을 따른다
- release-ready와 hold 상태를 혼동하지 않도록 decision state를 명시한다

## Likely Failure Modes

- `operator_handoff_gaps`
- `rollback_note_omission`
- `user_impact_underdescribed`

## Forward-Test Scenarios

- feature flag rollout with operator toggles
- schema migration with rollback caveats
- auth hotfix requiring temporary runbook update
