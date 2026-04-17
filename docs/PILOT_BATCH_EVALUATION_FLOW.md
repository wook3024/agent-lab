# Pilot Batch Evaluation Flow

## 목적

이 문서는 pilot 팀이 complex-case 작업 묶음을 실제로 평가할 때
어떤 순서로 batch를 구성하고, 실행하고, scorecard로 닫아야 하는지 정리한 운영 절차다.

핵심 목표는 두 가지다.

1. `좋아 보이는 사례`가 아니라 `재현 가능한 batch 결과`를 남긴다
2. quality, governance, efficiency를 같은 단위로 비교한다

## Batch Design Principles

- batch는 1개 team, 1개 operating route, 1개 default model policy로 묶는다
- 같은 batch 안에서 skill, role contract, model, effort를 동시에 여러 개 바꾸지 않는다
- trivial task는 batch에 넣지 않는다
- batch는 최소 5개, 권장 6~8개 complex-case task로 구성한다
- critical service와 high-risk change가 batch 안에 반드시 포함되어야 한다

## Recommended Batch Mix

- cross-file bug fix: 2개
- release-sensitive change: 1개 이상
- owner routing relevance가 높은 shared service change: 1개 이상
- security review trigger가 걸릴 task: 1개 이상
- docs / runbook sync가 필요한 task: 2개 이상

## Pre-Batch Checklist

### 1. Routing And Governance Inputs Freeze

- owner map freeze
- service criticality map freeze
- approval policy version freeze
- release gate rubric version freeze

### 2. Candidate Config Freeze

- topology id 확정
- role별 model / effort 확정
- enabled skill bundle 확정
- trigger rule override 여부 기록

### 3. Evidence Location Freeze

- batch output directory 확정
- task brief 저장 위치 확정
- trace 저장 위치 확정
- scorecard output 경로 확정

## Batch Execution Sequence

### Step 1. Intake

각 task마다 아래를 먼저 확정한다.

- task id
- owner team
- service criticality
- risk class
- approval-required 가능성
- security review trigger 여부

### Step 2. Triage And Context

각 task에 대해 아래 artifact를 만든다.

- task brief
- owner-aware context pack
- reviewer focus
- release / approval hint

이 단계에서는 범위를 넓히는 것이 아니라,
execution과 review가 복잡한 케이스를 놓치지 않도록 위험 지점을 선명하게 만드는 데 집중한다.

### Step 3. Execution

- smallest coherent diff 원칙 적용
- mandatory test delta 확인
- docs / runbook sync 수행
- release artifact 초안 필요 여부 표시

### Step 4. Deterministic Gates

- test
- lint
- typecheck
- security or policy scan if applicable
- docs sync check

gate 실패는 review 이전에 먼저 기록하고,
단순 오류와 구조적 결함을 구분한다.

### Step 5. Review Lanes

모든 task에 대해:

- general review

조건부로:

- security review
- architecture review

review 결과는 `finding severity`, `residual risk`, `required follow-up`로 나누어 기록한다.

### Step 6. Governance Lanes

- approval policy decision
- release gate decision
- release artifact package generation

여기서 `hold` 또는 `escalate`가 나오면,
accepted change 집계에 포함하기 전에 human intervention 상태를 함께 남긴다.

### Step 7. Observation

각 task마다 아래를 기록한다.

- trace record
- cost governance fields
- human intervention count
- final disposition: accepted / held / escalated / rejected

## Batch Scoring Sequence

### 1. Task-Level Scoring

각 task에서 먼저 본다.

- task success
- gate pass
- High finding count
- approval miss 여부
- release hold 적절성
- docs sync completeness

### 2. Batch-Level Aggregation

그 다음 batch 전체에서 본다.

- complex-case success rate
- risk class별 success rate
- owner routing accuracy
- security review precision
- median elapsed time
- estimated median cost

### 3. Baseline Comparison

비교 대상은 반드시 하나로 고정한다.

- same task set
- same owner map quality
- same gate contract
- same scoring rubric

## Stop Conditions

아래 중 하나가 발생하면 batch를 바로 `rework required` 상태로 둔다.

- approval-required task를 silent progression 시킴
- release-sensitive task에서 release gate miss 발생
- critical service change에서 owner routing이 비어 있음
- security-triggered task에서 review lane이 빠짐
- trace record가 누락되어 batch 비교가 불가능함

## Required Batch Output Package

- batch summary memo
- task briefs
- owner-aware context packs
- task-level review findings
- security review findings
- approval decisions
- release gate decisions
- release artifact bundles
- trace bundle
- pilot scorecard

## Weekly Operating Rhythm

### Batch Start

- 월요일: batch candidate freeze
- 화요일: triage / context complete
- 수요일~목요일: execution + review lanes
- 금요일: governance close + scorecard + retro

### Weekly Retro Questions

- 이번 batch에서 실제 defect를 잡은 lane은 무엇이었는가
- 어떤 lane이 운영 noise를 키웠는가
- 어떤 risk class에서 model downshift를 시험할 수 있는가
- owner metadata의 정확도는 어느 정도였는가

## Promotion Guidance

- 2개 연속 batch에서 quality KPI가 baseline보다 좋아지고
- governance false positive가 관리 가능한 수준이며
- human intervention rate가 과도하게 늘지 않으면
  `narrow`에서 `promote`로 이동할 수 있다

- batch마다 release hold나 approval escalation이 random하게 흔들리면
  model 문제가 아니라 rule contract 문제인지 먼저 의심한다
