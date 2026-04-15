# Skill Spec: execution-engineering

## Trigger Description Draft

task brief와 context pack이 준비된 뒤, 구현, 테스트 보강, 문서 반영, 로컬 검증을 순서대로 수행하게 하는 skill이다. 복잡한 구현이나 회귀 위험이 큰 수정에서 범위를 통제하면서 결과 품질을 높일 때 사용한다.

## Core Workflow

1. task brief의 done when과 non-goals를 먼저 확인한다
2. 최소 변경으로 구현한다
3. 필요한 테스트를 추가 또는 수정한다
4. 문서 반영 여부를 점검한다
5. deterministic gate 전 최소 로컬 검증을 수행한다

## Output Contract

- 변경 요약
- 변경 파일 목록
- 테스트 결과
- 남은 리스크

## Likely Failure Modes

- `over_edit`
- `missed_test`
- `docs_desync`
- `shallow_fix`

## Forward-Test Scenarios

- retry bug with UI + worker + docs
- schema migration with backfill
- offline sync conflict resolution
