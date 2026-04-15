# Candidate C2: Controlled Dual-Pass

## Summary

복잡한 케이스용 기본 목표 후보다. `Triage -> Context -> Execution -> Gates -> Review`를 분리해 범위 통제와 회귀 검증을 강화한다.

## Purpose

복잡한 제품 개발 작업에서 단일 실행보다 더 높은 안정성과 품질을 제공하는지 검증한다.

## Workflow

1. `Triage Agent`가 작업 유형, done condition, non-goals, risk를 정리
2. `Context Loader`가 관련 파일, 최근 변경, 테스트 기준, 정책 문서만 추린다
3. `Execution Agent`가 구현, 테스트, 문서 반영을 수행한다
4. deterministic gate를 실행한다
5. `Review Agent`가 독립적으로 findings를 작성한다
6. `High` finding 또는 gate failure가 있으면 수정 루프로 되돌린다

## Linked Role Cards

- [TRIAGE_AGENT_ROLE.md](/Users/shinukyi/Gallary/projects/proto/agent-lab/docs/roles/TRIAGE_AGENT_ROLE.md:1)
- [EXECUTION_AGENT_ROLE.md](/Users/shinukyi/Gallary/projects/proto/agent-lab/docs/roles/EXECUTION_AGENT_ROLE.md:1)
- [REVIEW_AGENT_ROLE.md](/Users/shinukyi/Gallary/projects/proto/agent-lab/docs/roles/REVIEW_AGENT_ROLE.md:1)

## Required Skills

- `task-brief-author`
- `context-pack-builder`
- `execution-engineering`
- `quality-gates-runner`
- `review-findings`
- `docs-sync`
- `trace-eval-recorder`

## Why This Candidate Exists

- 복잡한 케이스는 코드 생성보다 `범위 축소`, `검증 설계`, `독립 리뷰`에서 많이 무너진다
- dual-pass 구조는 과도한 낙관과 shallow fix를 줄일 가능성이 높다

## Expected Strengths

- unrelated change 감소
- missed test 감소
- docs sync 누락 감소
- review finding 품질 향상

## Expected Weaknesses

- 운영 시간이 늘어날 수 있다
- triage와 context 품질이 낮으면 전체가 흔들린다
- review가 구현과 충분히 분리되지 않으면 효과가 약해진다

## Promotion Criteria

- complex-case golden set에서 `C0` 대비 success rate 상승
- `High` review finding rate 감소
- `wrong_context`, `over_edit`, `missed_test`, `docs_desync` 감소

## Rejection Criteria

- 문서상 단계는 늘었지만 품질이 실질적으로 개선되지 않는 경우
- triage/context 단계가 병목만 만들고 gate failure를 줄이지 못하는 경우
