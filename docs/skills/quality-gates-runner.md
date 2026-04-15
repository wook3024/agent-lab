# Skill Spec: quality-gates-runner

## Trigger Description Draft

복잡한 작업 결과를 동일한 deterministic gate 아래에서 평가하는 skill이다. `test`, `lint`, `typecheck`, `security`, `docs sync`, 조건부 migration/performance checks를 일관되게 실행해야 할 때 사용한다.

## Core Workflow

1. task type과 complexity axes에 맞는 gate 목록을 고른다
2. 기본 gate를 실행한다
3. migration, retry, performance, contract 같은 조건부 gate를 추가한다
4. 실패한 gate를 taxonomy와 함께 기록한다

## Output Contract

- pass/fail
- gate별 결과
- 수정 루프로 되돌려야 하는 이유

## Likely Failure Modes

- `missed_test`
- `policy_violation`
- `cross_file_regression`

## Forward-Test Scenarios

- search schema migration
- payment retry semantics
- upload quarantine security
