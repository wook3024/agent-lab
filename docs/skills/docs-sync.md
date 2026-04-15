# Skill Spec: docs-sync

## Trigger Description Draft

코드 변경이 설계 문서, 운영 문서, ADR, runbook 반영을 요구하는지 판별하고 필요한 문서를 함께 업데이트하게 하는 skill이다. 복잡한 기능 변경, migration, 운영 리스크가 있는 작업에서 사용한다.

## Core Workflow

1. 변경 파일에서 사용자/운영 영향이 있는지 확인한다
2. 연관된 설계 문서와 runbook을 찾는다
3. 문서 반영이 필수인지 선택인지 분리한다
4. docs sync check 대상에 포함한다

## Output Contract

- 바뀐 코드와 연결된 문서 목록
- 문서 반영 필요 여부
- 누락 시 위험

## Likely Failure Modes

- `docs_desync`
- `insufficient_spec`
- `over_edit`

## Forward-Test Scenarios

- search reindex runbook update
- payment retry incident doc update
- billing SDK upgrade ADR
