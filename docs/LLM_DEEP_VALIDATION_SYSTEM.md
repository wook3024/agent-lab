# LLM Deep Validation System

## 목적

이 문서는 `agent-lab`에서 skill, agent, model, effort 조합을 검증할 때
LLM 기반 심층 검증을 어디에, 어떤 방식으로 붙여야 하는지 정의한다.

핵심 원칙은 단순하다.

- `LLM judge only`는 충분하지 않다
- `deterministic validation + artifact-grounded LLM evaluation + human calibration` 조합이 맞다

## Executive Position

LLM 기반 심층 검증은 반드시 필요하다.  
다만 역할은 `최종 진실 판정기`가 아니라 아래에 가깝다.

- reasoning quality evaluator
- hidden regression hypothesis generator
- review quality assessor
- governance decision quality checker

즉, LLM은 `사실성`을 전부 증명하는 장치가 아니라,
복잡한 개발 품질을 더 깊게 읽는 상위 평가 레이어로 써야 한다.

## Four-Layer Validation Stack

### Layer 1. Deterministic Validation

이 레이어는 objective truth를 다룬다.

- test
- lint
- typecheck
- schema validation
- trace completeness
- policy-format checks

이 레이어는 “코드가 실제로 돌아가는가”를 본다.

### Layer 2. Artifact-Grounded LLM Evaluation

이 레이어는 artifact를 읽고 고차 품질을 평가한다.

읽는 대상:

- task brief
- context pack
- execution report
- diff
- review findings
- security review
- approval decision
- release gate decision
- release artifact
- trace record

이 레이어는 아래를 본다.

- reasoning의 질
- hidden regression 가능성
- release hold의 적절성
- approval decision의 타당성
- handoff completeness

### Layer 3. Adversarial / Counterfactual Evaluation

이 레이어는 “무엇을 놓쳤는가”를 본다.

예시 질문:

- 이 변경이 깨뜨릴 수 있는 가장 현실적인 반례는 무엇인가
- reviewer가 놓쳤을 수 있는 `High` finding은 무엇인가
- release gate가 false ready일 가능성은 어디에 있는가
- owner routing이 잘못되었을 때 어떤 실패가 생기는가

### Layer 4. Human Calibration

이 레이어는 LLM judge의 한계를 보정한다.

- high-risk batch 일부 샘플링
- 사람 판정과 judge 판정 차이 기록
- disagreement taxonomy 축적
- rubric과 prompt 보정

## Where LLM Validation Is Strong

LLM judge가 특히 강한 영역은 아래다.

- review findings의 질 평가
- architecture drift 탐지
- release gate reasoning의 적절성
- approval decision의 설명력
- docs / runbook / operator handoff completeness
- skill contract가 complex-case에서 실제로 먹히는지 평가

## Where LLM Validation Must Not Be Sole Authority

아래는 LLM만으로 최종 보증하면 안 된다.

- 테스트가 실제로 통과했는지 여부
- 보안 결함이 “없다”는 최종 보증
- 실제 배포 승인
- 실제 비용 / latency 수치의 사실성
- owner metadata의 조직 정확도

## Judge Design Rules

### 1. Artifact First

judge는 산출물 기반으로만 판정한다.

- diff가 없으면 diff를 추정하지 않는다
- trace가 없으면 trace를 보정하지 않는다
- execution report가 빈약하면 그 자체를 finding으로 본다

### 2. No Style Scoring

판정 기준은 “그럴듯함”이 아니다.

- concrete defect likelihood
- governance correctness
- handoff completeness
- invariant preservation

만 본다.

### 3. Separate Evaluator Lanes

가능하면 judge를 lane별로 나눈다.

- general review evaluator
- security evaluator
- release gate evaluator
- architecture evaluator

### 4. Structured Output Only

자유 서술형 감상문보다 structured rubric을 우선한다.

최소 출력 요소:

- verdict
- concrete findings
- evidence references
- residual risk
- confidence note

### 5. No Shared Hidden Assumptions

judge는 구현 에이전트의 의도나 내부 reasoning을 전제하지 않는다.  
오직 artifact만 보고 판정한다.

## Recommended Judge Policy

현재 저장소 기준으로 가장 실전적인 judge 운영 정책은 아래다.

- default LLM judge: `gpt-5.4 / high`
- low-risk calibration probe only: `gpt-5.4-mini / high`
- `xhigh`는 judge 기본값으로 두지 않는다

이유:

- judge의 핵심은 reasoning quality와 artifact reading 안정성
- complex-case judge는 `mini`로도 일부 가능하지만 아직 기본값으로는 이르다
- `xhigh`는 judge에서 과도한 추론과 verbosity를 만들 수 있다

## Lane-Specific Judge Responsibilities

### Review Evaluator

- hidden regression 가능성
- missed test
- over-edit
- docs sync 누락

### Security Evaluator

- auth / RBAC / tenant isolation
- PII / secret flow
- trust boundary changes
- auditability gap

### Release Gate Evaluator

- hold / ready / escalate 판단 적절성
- rollback readiness
- operator-visible missing artifact
- approval completeness

### Architecture Evaluator

- boundary erosion
- coupling 증가
- migration sequencing 문제
- ownership 흐림

## Disagreement Handling

judge와 사람, 또는 judge와 judge 사이 disagreement는 버그가 아니라 데이터다.

반드시 아래로 남긴다.

- disagreement type
- 어떤 artifact를 다르게 해석했는지
- root cause가 prompt인지 rubric인지 owner metadata인지
- 다음 batch에서 무엇을 고칠지

## Human Calibration Policy

다음 중 하나를 만족하면 사람 calibration을 반드시 붙인다.

- critical service change
- approval-required task
- release hold / escalate 발생
- security review lane이 실제로 켜진 task
- judge 간 verdict가 충돌한 task

## Minimum Required Artifacts For Deep Validation

LLM 심층 검증을 돌리려면 최소 아래가 있어야 한다.

- task brief
- context pack
- execution report
- diff
- gate results
- trace record

없으면 judge 결과 신뢰도가 급격히 떨어진다.

## Recommended Immediate Rollout

지금 당장은 아래 순서가 가장 좋다.

1. review evaluator를 기본 lane으로 유지
2. security / release / architecture evaluator를 conditional lane으로 추가
3. pilot batch마다 disagreement sample 1개 이상 남김
4. human calibration batch를 월 1회 수행

## What Good Looks Like

LLM deep validation이 잘 작동하는 상태는 아래다.

- deterministic gate를 대체하지 않는다
- artifact 품질이 낮으면 judge도 그 사실을 지적한다
- batch가 끝나면 disagreement가 학습 자산으로 남는다
- 사람은 모든 것을 읽지 않아도 high-risk disagreement만 보면 된다

이 상태가 되면 LLM 평가는 “그럴듯한 코멘트 생성기”가 아니라,
실제 complex-case 품질을 더 깊게 읽는 운영 장치가 된다.
