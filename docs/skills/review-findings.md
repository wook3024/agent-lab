# Skill Spec: review-findings

## Trigger Description Draft

구현 결과를 독립적으로 검토해 `High / Medium / Low / Residual Risks` 형식으로 실제 결함을 찾는 skill이다. 복잡한 구현, 회귀 위험이 큰 수정, 테스트 보강 여부가 중요한 작업에서 사용한다.

## Core Workflow

1. task brief와 gate 결과를 먼저 읽는다
2. diff와 관련 파일을 검토한다
3. 요구사항 누락, 회귀 위험, 테스트 부족, 운영/보안 문제를 severity별로 정리한다
4. 구현을 다시 하지 않고 findings만 남긴다

## Output Contract

- [REVIEW_FINDINGS_TEMPLATE.md](/Users/shinukyi/Gallary/projects/proto/agent-lab/docs/templates/REVIEW_FINDINGS_TEMPLATE.md:1) 형식을 따른다
- 칭찬 위주 요약보다 결함 탐지를 우선한다

## Likely Failure Modes

- `false reassurance`
- `missed regression`
- `test gap blindness`

## Forward-Test Scenarios

- authorization scope bug
- async flaky test hardening
- SDK adapter upgrade
