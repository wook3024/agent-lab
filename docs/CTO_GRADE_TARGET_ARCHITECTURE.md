# CTO-Grade Target Architecture

## 목적

이 문서는 현재 `agent-lab`이 검증한 complex-case 품질 운영 구조를 기반으로,
실제 조직에 배포 가능한 `CTO-grade AI development operating system`의 목표 아키텍처를 정의한다.

이 문서가 다루는 범위는 다음과 같다.

- 현재 baseline에서 무엇을 유지할 것인가
- 무엇을 control-plane으로 추가할 것인가
- 각 역할과 스킬은 어느 레이어에 속해야 하는가
- 어떤 데이터와 신호가 운영 표준이 되어야 하는가
- 어떤 순서로 승격해야 하는가

## Executive Summary

현재 프로젝트가 검증한 가장 중요한 자산은 다음 구조다.

`Triage -> Context -> Execution -> Deterministic Gates -> Independent Review`

CTO-grade target은 이 구조를 버리는 것이 아니라, 아래 네 개 레이어로 확장하는 것이다.

1. `Delivery Plane`
2. `Control Plane`
3. `Observation Plane`
4. `Governance Plane`

즉, 목표 상태는 “코드를 잘 고치는 agent”를 넘어서:

- 누가 작업을 승인할지
- 어떤 변경이 위험한지
- 어떤 리뷰가 추가로 필요한지
- 어떤 팀이 책임을 져야 하는지
- 어떤 비용으로 어떤 품질을 얻고 있는지

를 운영 계층에서 통제할 수 있는 구조다.

## Design Principles

### 1. 코드 품질과 조직 운영 품질을 분리하지 않는다

좋은 구현 결과만으로는 부족하다.  
실제 조직에서는 아래가 함께 충족돼야 한다.

- 품질이 반복 가능해야 한다
- 승인이 감사 가능해야 한다
- 리스크가 사전에 분류되어야 한다
- 비용이 추적 가능해야 한다
- 실패가 재현 가능해야 한다

### 2. Execution은 강하게, Governance는 더 강하게

현재 baseline은 execution 품질에는 강하다.  
CTO-grade target은 여기에 다음을 추가한다.

- release blocker 판정
- approval requirement 판정
- security/compliance severity
- ownership routing
- cost policy enforcement

### 3. 에이전트 수를 늘리기보다 plane을 분리한다

복잡도를 줄이는 핵심은 “agent를 많이 만드는 것”이 아니라
서로 다른 책임을 가진 plane으로 분리하는 것이다.

예를 들어:

- 코드 변경은 `Delivery Plane`
- 승인과 배포 보류는 `Governance Plane`
- token/cost/latency 추적은 `Observation Plane`

에 둬야 한다.

### 4. 모든 승격은 scorecard 기반이어야 한다

어떤 에이전트, 스킬, 모델 조합도 아래 중 하나라도 없으면 승격하지 않는다.

- deterministic gate 결과
- independent review 결과
- trace record
- 비용/시간 지표
- owner / approval 기록

## Current State

현재 프로젝트가 실제로 가진 baseline은 아래와 같다.

### Core Operating Shape

- topology: `C2`
- role: `Triage Agent`, `Execution Agent`, `Review Agent`
- skill:
  - `task-brief-author`
  - `context-pack-builder`
  - `execution-engineering`
  - `quality-gates-runner`
  - `trace-eval-recorder`
  - `docs-sync`
  - `review-findings`
  - optional `research-grounded`

### Current Strength

- complex-case 품질 향상
- independent review 기반 defect discovery
- model/effort sufficiency 실험 가능
- benchmark와 scorecard 기반 의사결정 가능

### Current Limitation

- release approval plane 부재
- security/compliance specialization 부재
- owner-aware routing 부재
- team cost governance 약함
- deployment / incident / rollback decision plane 없음

## Target Architecture Overview

```text
Request / Issue / PRD / Incident
  -> Intake Router
  -> Triage Plane
  -> Context Plane
  -> Delivery Plane
  -> Verification Plane
  -> Review Plane
  -> Governance Plane
  -> Release / Rework / Escalation
  -> Observation Plane captures everything
```

이 구조를 4개 plane으로 정리하면 아래와 같다.

### 1. Delivery Plane

실제 변경을 만드는 plane이다.

- `Triage Agent`
- `Context Builder`
- `Execution Agent`
- optional `Research Agent`

목표:

- 범위를 좁힌다
- 필요한 컨텍스트만 제공한다
- 가장 작은 coherent diff를 만든다
- 테스트와 문서를 함께 갱신한다

### 2. Control Plane

“이 변경을 어떻게 다뤄야 하는가”를 결정하는 plane이다.

- `Approval Policy Engine`
- `Release Gate Agent`
- `Ownership Router`
- `Change Risk Classifier`
- `Security Review Router`

목표:

- 위험한 변경을 early detect
- 승인 필요 여부 판정
- 팀/서비스 owner 매핑
- 추가 review 필요 여부 판정
- 배포 가능 여부 결정

### 3. Observation Plane

무슨 일이 일어났는지 남기는 plane이다.

- `trace-eval-recorder`
- `scorecard aggregator`
- `cost telemetry collector`
- `latency / failure dashboard`
- `batch comparer`

목표:

- 조합 간 품질 비교
- 비용 대비 품질 추적
- taxonomy drift 감지
- 팀별 효율성 측정

### 4. Governance Plane

운영 규칙과 정책을 강제하는 plane이다.

- approval matrix
- data-risk policy
- deploy freeze policy
- production access policy
- incident mode policy

목표:

- agent가 해도 되는 것과 안 되는 것을 분명히 한다
- 비가역 작업에 사람 승인을 강제한다
- critical service에 더 강한 통제를 건다

## Detailed Target Components

## A. Intake Router

### 역할

- 요청을 `implementation`, `review`, `research`, `ops`, `incident`, `release`로 분류
- simple task와 complex-case를 구분
- owner team과 risk class의 초기 추정 생성

### Why CTO Cares

- 잘못된 lane에 들어간 작업은 전체 비용을 높인다
- incident와 release는 implementation과 다른 규칙이 필요하다

### Required Outputs

- task class
- complexity score
- risk score
- owner hint
- approval likelihood

## B. Triage Plane

### Components

- `Triage Agent`
- `task-brief-author`

### Output Contract

- goal
- done when
- non-goals
- invariants
- reviewer focus
- approval requirements
- change risk summary

### Promotion Standard

- hidden-risk omission 감소
- wrong-context 감소
- unrelated change 감소

## C. Context Plane

### Components

- `Context Builder`
- `context-pack-builder`

### Output Contract

- relevant code files
- relevant tests
- recent changes that may collide
- docs/runbooks/ADRs
- verification targets

### CTO Interpretation

이 plane은 execution 성능보다 조직 학습 효율에 더 중요하다.  
좋은 context discipline이 없으면 어떤 모델도 지속적으로 품질을 유지하기 어렵다.

## D. Delivery Plane

### Components

- `Execution Agent`
- `execution-engineering`
- optional `Research Agent`

### Output Contract

- changed files
- execution report
- gate evidence
- residual risks
- reviewer focus points

### Non-Negotiable Rules

- task invariant를 넘는 일반화 금지
- regression coverage 필수
- docs sync required when behavior changes
- gate 결과를 사실과 다르게 서술 금지

## E. Verification Plane

### Components

- `quality-gates-runner`
- task-specific gate selectors

### Base Gates

- tests
- lint
- typecheck
- docs sync

### Conditional Gates

- security scan
- migration safety
- API contract snapshot
- concurrency behavior
- retry semantics
- performance smoke
- flaky repeat

### CTO Interpretation

이 plane은 “agent quality”를 “repeatable system quality”로 바꾸는 핵심이다.

## F. Review Plane

### Components

- `Review Agent`
- `review-findings`
- future: `Security Review Agent`

### Output Contract

- High
- Medium
- Low
- Residual Risks

### Target Extension

일반 리뷰와 별도로 아래 reviewer lane이 필요해진다.

- security review
- architecture review
- release review

## G. Governance Plane

현재 baseline에 가장 부족한 layer다.

### Required Components

#### 1. Approval Policy Engine

판정 예시:

- read-only: auto allow
- safe write: auto allow or post-report
- moderate write: brief-governed allow
- risky write: pre-approval required
- irreversible: explicit human approval required

#### 2. Release Gate Agent

판정 항목:

- release blocker 존재 여부
- rollback readiness
- migration safety
- owner approval completeness
- incident overlap risk

#### 3. Ownership Router

필수 기능:

- 서비스별 owner mapping
- 변경 영향도 기반 reviewer selection
- critical path 서비스 strict routing

#### 4. Security Review Router

trigger 조건:

- auth / RBAC touched
- secret handling touched
- PII / data exposure touched
- external integration policy touched

## H. Observation Plane

### Components

- `trace-eval-recorder`
- scorecard aggregation
- cost telemetry
- latency histogram
- failure taxonomy dashboards

### Required Data Model

각 run은 최소 아래 필드를 가져야 한다.

- run id
- task id
- candidate id
- role to model mapping
- role to effort mapping
- owner team
- risk class
- changed files
- gate outcomes
- review severities
- approval state
- elapsed time
- token cost
- taxonomy tags

### CTO Metrics

반드시 운영 지표로 승격해야 할 항목은 아래다.

- complex-case success rate
- High finding rate
- gate failure rate
- rework rate
- docs drift rate
- task-type별 평균 시간
- task-type별 평균 비용
- human intervention rate
- release blocker rate

## Target Agent / Skill Inventory

## Keep As Core

- `Triage Agent`
- `Execution Agent`
- `Review Agent`
- `task-brief-author`
- `context-pack-builder`
- `execution-engineering`
- `quality-gates-runner`
- `trace-eval-recorder`

## Keep As Supporting

- `docs-sync`
- `review-findings`
- `research-grounded`

## Add As Control Plane

- `Release Gate Agent`
- `Approval Policy Skill`
- `Security Review Skill`
- `Ownership Routing Skill`
- `Cost Governance Trace Layer`
- `Incident Mode Policy Skill`

## Recommended Model Routing In Target State

### Default Quality-First Routing

- Triage: `gpt-5.4 / high`
- Execution: `gpt-5.4 / high`
- Review: `gpt-5.4 / high`

### Candidate Cost-Optimized Routing

- Triage/Context: `gpt-5.4-mini / medium`
- Execution: `gpt-5.4 / high`
- Review: `gpt-5.4 / high`

### Explicit Policy

- `xhigh`는 예외적 실험값이다
- `mini`는 triage/context부터 검증한다
- review downshift는 마지막 단계에서만 시도한다

## Promotion Path

### Stage 1. Engineering Quality Baseline

승격 조건:

- `C2`가 complex-case에서 baseline보다 분명히 좋다
- independent review가 High 결함을 실질적으로 줄인다
- docs drift와 missed test가 감소한다

### Stage 2. Governance Layer Integration

승격 조건:

- approval matrix와 release gate가 도입된다
- risky / irreversible 작업이 policy-aware하게 멈춘다
- owner routing이 작동한다

### Stage 3. Org-Wide Rollout

승격 조건:

- 팀별 scorecard가 나온다
- task-type별 cost curve가 보인다
- release blocker trend를 추적할 수 있다

## Anti-Patterns To Avoid

- 모든 task에 multi-agent를 기본 적용
- xhigh를 기본값으로 고정
- scorecard 없이 prompt만 계속 수정
- release / approval / security를 execution 안에 섞어버림
- ownership이 없는 자동 merge path 도입
- docs sync를 nice-to-have로 취급

## Final Shape

최종적으로 CTO가 원하는 시스템은 다음과 같다.

- delivery는 빠르게
- verification은 결정적으로
- review는 독립적으로
- approval은 명시적으로
- cost는 관측 가능하게
- ownership은 추적 가능하게

현재 프로젝트는 이 중 delivery/verification/review/trace까지는 상당 부분 도달했다.  
다음 목표는 control-plane과 governance-plane을 붙여서 `good benchmark lab`을 `org-grade operating system`으로 승격하는 것이다.
