# Complex-Case Agent Program Plan

## Objective

복잡한 제품 개발 작업에서 응답 품질을 대폭 향상시키는 `agent + skill + eval + trace` 운영 시스템을 설계한다.

이 계획의 목표는 다음과 같다.

- 단순한 요청 처리 품질이 아니라 `복잡한 구현`, `고위험 버그 수정`, `멀티파일 변경`, `설계-구현-검증 연쇄 작업`의 성공률을 높인다.
- 에이전트 성능을 프롬프트 감각이 아니라 `golden eval set`, `deterministic gate`, `trace`, `review finding`으로 비교한다.
- 멀티에이전트는 기본값이 아니라 `복잡도 감소`와 `품질 개선`이 수치로 확인될 때만 승격한다.

## Non-Goals

- 간단한 CRUD, 짧은 문서 수정, 한두 줄 답변 품질을 최적화하는 것
- 프롬프트 미세 조정만으로 품질을 올리려는 접근
- trace와 gate 없이 "좋아 보이는" 조합을 채택하는 것

## Core Hypothesis

복잡한 케이스에서 가장 먼저 검증해야 할 기준 조합은 다음이다.

`Triage -> Context Loader -> Execution -> Deterministic Gates -> Review`

이 조합은 아래 이유로 기본 후보가 된다.

- 복잡한 작업은 구현 능력보다 `범위 통제`, `컨텍스트 선택`, `회귀 검증`, `독립 리뷰`에서 많이 실패한다.
- 플레이북 기준으로 `single specialist agent`가 기본이며, 멀티에이전트는 병렬성이 분명할 때만 써야 한다.
- OpenAI 공식 문서도 `Agents SDK`의 강점을 `handoff`, `guardrail`, `session`, `tracing`에 둔다. 따라서 최초 baseline은 에이전트 수를 늘리기보다 운영 관측성과 orchestration 구조를 강화하는 편이 유리하다.

참고:

- https://developers.openai.com/tracks/building-agents#foundations-of-the-agents-sdk
- https://developers.openai.com/cookbook/examples/partners/eval_driven_system_design/receipt_inspection#graders

## What Counts As A Complex Case

이 프로그램에서 복잡한 케이스는 아래 항목 중 3개 이상을 만족하는 작업으로 정의한다.

- 3개 이상 파일을 함께 수정해야 한다.
- 구현과 함께 테스트 추가 또는 수정이 필수다.
- 퍼블릭 API, 데이터 흐름, 상태 전이가 관련된다.
- 설계 문서 또는 정책 문서를 같이 반영해야 한다.
- 최근 변경사항과 충돌할 가능성이 높다.
- 외부 의존성, SDK, 인프라 제약을 고려해야 한다.
- 회귀 위험이 높아서 독립 리뷰가 의미 있게 작동한다.
- 단일 함수 수정이 아니라 cross-module reasoning이 필요하다.
- 작업 범위와 비목표를 분명하게 잡지 않으면 과도한 변경으로 번지기 쉽다.

간단한 작업은 smoke set으로 소량 유지하되, 최적화 대상은 아니다.

## Evaluation Philosophy

복잡한 케이스 품질은 아래 순서로 최적화한다.

1. 요구사항 충족
2. 회귀 방지
3. 테스트와 검증 추가
4. 문서 및 운영 반영
5. 처리 속도와 비용

속도나 비용이 좋아도 `High severity review finding`, `gate failure`, `missed test`가 늘면 실패한 조합으로 본다.

## Candidate Agent Architectures

### C0. Codex Solo

- 단일 실행 에이전트만 사용
- 비교 기준점으로 유지
- 가장 단순하지만 복잡한 케이스에서 범위 통제와 독립 리뷰가 약할 가능성이 높다

### C1. Execution-Centric Single Specialist

- `Task Brief`와 `Context Pack`만 제공받는 단일 실행 에이전트
- 구현, 테스트, 문서 반영까지 수행
- gate는 외부 deterministic step으로 분리

### C2. Controlled Dual-Pass

- `Triage/Context` -> `Execution` -> `Deterministic Gates` -> `Review`
- 복잡한 케이스의 기본 목표 조합
- 구현과 리뷰를 분리해서 과도한 낙관을 줄인다

### C3. Research-Assisted Execution

- C2에 `Research Agent`를 on-demand로 추가
- 외부 SDK, 정책, 플랫폼 제약, 설계 옵션 비교가 필요한 작업에만 활성화
- 추측성 구현을 줄이는 것이 목적이다

### C4. Managed Multi-Agent

- Manager가 `구현`, `테스트`, `리뷰`를 병렬 분배
- 독립 write set과 handoff 품질이 충분할 때만 후보로 승격
- baseline이 아니라 후속 비교 후보

## Planned Skill System

실제 품질 개선은 에이전트 persona보다 `skill`의 절차 강제력에서 많이 나온다. 초기 skill 백로그는 아래와 같다.

### 1. task-brief-author

- 입력 요청을 `Goal`, `Done When`, `Non-Goals`, `Risk`, `Approval Requirements`로 정규화
- 복잡한 케이스에서 범위 폭주를 막는 첫 관문

### 2. context-pack-builder

- 저장소 전체가 아니라 관련 파일, 최근 변경, 테스트 기준, 정책 문서만 압축
- 하위 에이전트가 잘못된 파일을 건드리는 비율을 줄이는 역할

### 3. execution-engineering

- 구현, 테스트 보강, 문서 반영, 로컬 검증 순서를 강제
- 범위를 벗어난 리팩터링을 억제

### 4. review-findings

- 리뷰 출력 형식을 severity 기반으로 강제
- 구현 요약보다 결함 탐지를 우선시킴

### 5. quality-gates-runner

- `test`, `lint`, `typecheck`, `security`, `docs sync`를 일관된 순서로 실행
- 통과 실패 시 수정 루프로 자동 되돌림

### 6. research-grounded

- 외부 문서는 1차 출처 우선
- 주장-근거 매핑과 불확실성 표기를 강제

### 7. trace-eval-recorder

- 입력, 참조 파일, tool 호출, 시간, 비용, 실패 taxonomy를 기록
- 감으로 개선하지 않고 실패 패턴을 축적

### 8. docs-sync

- 코드 변경이 설계/운영 문서에 어떤 반영을 요구하는지 체크
- 복잡한 케이스에서 문서 누락을 방지

## Benchmark Design

복잡한 케이스 중심의 golden set은 최소 30개, 목표 50개로 설계한다.

권장 비율:

- 30%: cross-file feature implementation
- 25%: regression-prone bug fix
- 15%: test rescue / flaky behavior hardening
- 10%: architecture-sensitive refactor
- 10%: docs + code consistency update
- 10%: design / investigation with implementation implications

simple smoke set은 별도로 5~10개 정도만 유지한다. scorecard 합산에서는 보조 지표로만 사용한다.

각 task는 아래 항목을 가진다.

- 복잡도 축
- 관련 파일
- 필수 테스트
- 필수 문서 반영
- 허용 범위
- 금지 행동
- reviewer가 반드시 봐야 할 위험 포인트

## Deterministic Gates

모든 후보 조합은 동일한 gate 아래에서 비교한다.

기본 gate:

- unit / integration test
- lint
- typecheck
- security scan
- docs sync check
- changed-files scope check

복잡한 케이스에서는 아래를 조건부 gate로 추가한다.

- migration safety check
- API contract snapshot check
- performance smoke check
- concurrency or retry behavior check

Gate를 통과하지 못한 실행은 점수 계산 전에 `failed run`으로 태깅한다.

## Review Rules

리뷰는 구현과 독립된 pass로 수행한다.

- 출력 형식은 `High / Medium / Low / Residual Risks`
- 리뷰 에이전트는 구현을 다시 하지 않는다
- `High`가 1개라도 있으면 후보는 수정 루프로 되돌린다
- `Medium`은 복잡한 케이스에서 누적 추세를 본다

## Trace And Failure Taxonomy

최소 수집 항목:

- candidate id
- task id
- task type
- complexity axes
- referenced files/docs
- tool calls
- changed files
- gate results
- review findings count by severity
- human intervention needed
- elapsed time
- estimated cost

기본 taxonomy:

- wrong_context
- wrong_tool
- hallucinated_assumption
- over_edit
- missed_test
- policy_violation
- handoff_failure
- insufficient_spec

복잡한 케이스용 보조 태그:

- cross_file_regression
- docs_desync
- shallow_fix
- incomplete_reproduction
- unsafe_dependency_change

## Iteration Loop

### Loop A. Baseline Establishment

1. 후보 조합 정의
2. task brief와 context pack 작성
3. golden set 일부 실행
4. deterministic gate 실행
5. review finding 기록
6. trace 분석
7. failure taxonomy 분류

### Loop B. Skill Revision

1. 실패 패턴별 원인 추정
2. prompt가 아니라 skill 절차와 출력 계약을 수정
3. 동일 task 재실행
4. 수정 전후 score 비교

### Loop C. Architecture Promotion

1. C2 대비 C3 또는 C4를 같은 task set으로 실행
2. 품질 향상이 통계적으로 의미 있는지 확인
3. handoff_failure나 over_edit가 증가하면 승격 보류

## OpenAI Agents SDK Adoption Plan

Agents SDK는 초기 baseline의 필수 요소가 아니라, 아래 단계에서 도입한다.

### Stage 1. Manual Controlled Loop

- Codex + 로컬 문서/템플릿/skill 설계
- 사람이 후보 조합과 결과를 직접 비교
- 목표는 좋은 baseline과 안정된 rubric 확보

### Stage 2. Experiment Runner

- Agents SDK로 candidate orchestration을 코드화
- handoff, guardrail, tracing을 이용해 반복 실험 자동화
- 동일 task에 대한 A/B 비교를 쉽게 만듦

### Stage 3. Bounded Multi-Agent Trials

- 분리 가능한 write set에만 병렬 worker 적용
- tracing으로 handoff cost와 failure taxonomy를 분석
- 성능 향상이 아니라 품질 향상이 확인될 때만 유지

## Exit Criteria

초기 프로그램이 성공으로 간주되려면 아래 조건을 만족해야 한다.

- 복잡한 golden set에서 baseline 대비 성공률이 유의미하게 상승
- `High severity` review finding 비율이 감소
- `missed_test`, `over_edit`, `wrong_context`가 눈에 띄게 감소
- docs sync 누락이 줄어듦
- 사람이 개입해야 하는 빈도가 감소하거나 더 고위험 판단에 집중됨

## First Build Sequence

계획 단계 다음 구현 순서는 아래를 권장한다.

1. 운영 계획 문서 확정
2. 템플릿 세트 작성
3. complex-case golden set 10개 초안 작성
4. C0 / C2 후보 정의
5. trace schema와 scorecard 정의
6. 첫 실험 수행
7. 실패 taxonomy 기반 skill 수정
8. 필요 시 Agents SDK 실험 러너 설계
