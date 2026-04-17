# Skill Spec: architecture-review

## Trigger Description Draft

기능 요구사항은 충족했지만 boundary erosion, coupling 증가, migration sequencing 오류, 과한 추상화 같은 architecture debt를 남길 수 있는 변경을 검토하는 skill이다.

## Core Workflow

1. task brief, context pack, diff, execution report를 읽는다
2. 변경이 모듈 경계, 책임 분리, 데이터 흐름, migration sequencing에 어떤 영향을 주는지 본다
3. “지금은 동작하지만 다음 변경 비용을 크게 올리는 구조 변화”를 찾는다
4. reusable abstraction이 진짜 필요한지, task-scoped fix가 더 적절한지 판단한다
5. `High / Medium / Low / Residual Architecture Risks` 형식으로 결과를 남긴다

## Review Lenses

- boundary erosion
- coupling increase
- hidden shared state
- migration sequencing risk
- abstraction drift
- operability impact

## Output Contract

- [ARCHITECTURE_REVIEW_TEMPLATE.md](/Users/shinukyi/Gallary/projects/proto/agent-lab/docs/templates/ARCHITECTURE_REVIEW_TEMPLATE.md:1) 형식을 따른다
- 스타일 선호보다 change cost, boundary clarity, future migration safety를 우선한다

## Likely Failure Modes

- `boundary_erosion_missed`
- `coupling_growth_blindness`
- `migration_sequence_underreviewed`
- `abstraction_overacceptance`

## Forward-Test Scenarios

- shared cache path widened by convenience abstraction
- rollout fix that leaks telemetry concerns into core domain model
- migration that couples read and write path too early
