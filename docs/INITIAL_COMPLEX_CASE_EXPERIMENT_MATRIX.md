# Initial Complex-Case Experiment Matrix

## Goal

복잡한 제품 개발 작업에서 어떤 조합이 실제 품질을 가장 안정적으로 끌어올리는지 3단계 실험으로 좁힌다.

## Experiment Order

### Experiment 0. Model And Effort Benchmark Setup

- 목적:
  - `gpt-5.4`와 `gpt-5.4-mini`의 역할별 sufficiency를 먼저 파악
- 상세 계획:
  - [MODEL_EFFORT_BENCHMARK_PLAN.md](/Users/shinukyi/Gallary/projects/proto/agent-lab/docs/MODEL_EFFORT_BENCHMARK_PLAN.md:1)
- 규칙:
  - skill과 role contract를 고정한 채 `model`과 `effort`만 비교
  - simple smoke set이 아니라 complex-case 결과를 우선

### Experiment 1. Baseline Reality Check

- 후보:
  - `C0`: Codex Solo
  - `C2`: Triage -> Context -> Execution -> Gates -> Review
- 목적:
  - 단일 실행 대비 dual-pass 구조가 복잡한 케이스에서 실제로 품질 이득이 있는지 확인
- 평가 세트:
  - 복잡한 구현 4개
  - 회귀성 버그 수정 3개
  - 테스트 구조 보강 2개
  - 문서-코드 동기화 1개
- 승격 조건:
  - `C2`가 `C0` 대비 gate pass rate, review high finding rate, docs sync success rate에서 우세

### Experiment 2. Research Injection Test

- 후보:
  - `C2`
  - `C3`: C2 + Research Agent on-demand
- 목적:
  - 외부 SDK/플랫폼/정책 불확실성이 있는 작업에서 research pass가 shallow fix를 줄이는지 확인
- 평가 세트:
  - 외부 SDK 변경 영향 분석 2개
  - 정책/문서 반영 포함 기능 수정 2개
  - 설계 선택이 필요한 구현 2개
- 승격 조건:
  - `hallucinated_assumption`, `insufficient_spec`, `docs_desync`가 감소

### Experiment 3. Multi-Agent Admission Test

- 후보:
  - `C2` 또는 `C3` 중 우세 후보
  - `C4`: Manager + Worker(구현/테스트/리뷰)
- 목적:
  - 병렬화가 복잡한 케이스 품질을 실제로 개선하는지 확인
- 평가 세트:
  - 독립 write set이 있는 대형 작업 4개
  - 리뷰/테스트 분리가 명확한 작업 2개
- 승격 조건:
  - handoff failure 증가 없이 success rate 또는 rework rate가 유의미하게 개선

## Decision Rules

- `High` review finding이 1개라도 나오면 해당 run은 fail
- gate failure가 반복되면 candidate를 고치기 전까지 다음 실험으로 넘기지 않는다
- cost와 latency는 tie-breaker로만 사용한다
- simple smoke set 결과는 보조 지표이며, complex-case 결과보다 우선하지 않는다

## Minimum Dataset Before Promotion

- Candidate 승격 전 최소 조건:
  - 복잡한 task 10개 이상
  - task type 4종 이상 포함
  - 동일 rubric으로 review 수행
  - trace taxonomy 누락 없음

## First Revision Priorities

- `wrong_context`가 많으면 `context-pack-builder`부터 수정
- `over_edit`가 많으면 `task-brief-author`와 `execution-engineering` 계약부터 수정
- `missed_test`가 많으면 `quality-gates-runner`와 `execution-engineering` 강화
- `docs_desync`가 많으면 `docs-sync` skill 추가 또는 강화
- `handoff_failure`가 많으면 멀티에이전트 실험 중단 후 단일 specialist 조합으로 복귀
