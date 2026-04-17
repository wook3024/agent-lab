# CTO 90-Day Roadmap

## 목적

이 문서는 현재 `agent-lab` baseline을 바탕으로,
90일 안에 CTO-grade 운영 체계의 첫 버전을 만드는 실행 로드맵이다.

목표는 세 가지다.

1. 현재 검증된 `C2` baseline을 유지한다.
2. control-plane을 추가해 release / approval / security / cost governance를 갖춘다.
3. pilot 팀에 실제 적용 가능한 운영 패키지로 승격한다.

## Success Definition At Day 90

90일 시점에서 아래가 가능해야 한다.

- complex-case 기본값으로 `C2 + all gpt-5.4/high`가 조직 표준으로 문서화되어 있다
- `Release Gate Agent`와 `Approval Policy Skill`이 작동한다
- auth / PII / secrets touched 변경에는 `Security Review`가 자동으로 붙는다
- owner routing이 최소 한 팀/서비스 군에서 동작한다
- cost/latency/quality scorecard가 role/task type별로 나온다
- 최소 1개 pilot 팀에서 실제 업무에 제한적으로 적용된다

## Roadmap Structure

### Day 0-30

목표:

- governance baseline을 추가한다
- control-plane MVP를 완성한다

### Day 31-60

목표:

- ownership, security, cost 관측성을 붙인다
- policy-aware routing을 시작한다

### Day 61-90

목표:

- pilot 적용
- 운영 지표 수집
- 승격/보류 의사결정

## Day 0-30: Control Plane MVP

## Primary Outcome

“좋은 benchmark 시스템”에서 “배포와 승인 리스크를 통제하는 시스템”으로 전환한다.

## Deliverables

### 1. Release Gate Agent spec and prototype

- role card 작성
- output schema 정의
- release blocker rubric 정의
- rollback readiness checklist 정의

### 2. Approval Policy Skill

- approval matrix 구현
- risky / irreversible detection 규칙 구현
- escalation contract 정의

### 3. Security Review Skill spec

- trigger conditions 정의
- severity rubric 정의
- 일반 리뷰와의 경계 정의

### 4. Trace schema extension

- approval state 필드 추가
- risk class 필드 추가
- owner hint 필드 추가
- cost telemetry placeholder 추가

## Work Breakdown

### Week 1

- target architecture 문서 확정
- control-plane backlog 확정
- approval matrix 초안 작성

### Week 2

- Release Gate Agent role/spec 작성
- Approval Policy Skill 초안 작성
- trace schema 확장 설계

### Week 3

- security review rubric 작성
- risky task classification test cases 설계
- benchmark runner에 control-plane hook 포인트 정의

### Week 4

- control-plane MVP review
- 문서 정리
- Day 31-60 적용 범위 확정

## Exit Criteria

- release gate와 approval policy의 문서/스키마가 완성됨
- 최소 3개 complex-case 태스크에 control-plane dry-run 가능
- 보안 리뷰 trigger 정의가 명확함

## Day 31-60: Routing And Governance Expansion

## Primary Outcome

누가 리뷰하고 누가 승인할지, 어떤 비용으로 운영할지를 구조적으로 볼 수 있게 만든다.

## Deliverables

### 1. Ownership Routing MVP

- path to owner map
- service criticality map
- reviewer routing rules

### 2. Security Review Lane

- security review skill prototype
- security trigger execution path
- benchmark security task 1개 이상 추가

### 3. Cost Governance Layer

- role/task별 token cost 집계
- latency bucket 집계
- quality 대비 비용 보고서 생성

### 4. Model Routing Policy v1

- quality-first default 유지
- triage/context downshift 조건 정의
- review downshift 금지 기준 정의

## Work Breakdown

### Week 5

- owner map schema 정의
- critical service 기준 정의
- security review input contract 확정

### Week 6

- owner-aware routing 문서 작성
- cost report template 구현
- benchmark output에 role별 비용 기록 추가

### Week 7

- security review prototype 작성
- benchmark security 태스크 설계
- model routing policy v1 정리

### Week 8

- Day 31-60 성과 검토
- pilot 후보 팀 선정
- pilot 적용 절차 초안 작성
- pilot playbook 초안 작성

## Exit Criteria

- owner-aware review routing이 최소 1개 서비스군에서 동작함
- security review lane이 최소 1개 task에서 유효 finding을 냄
- quality/cost/latency 비교표가 생성됨

## Day 61-90: Pilot And Operating Decision

## Primary Outcome

실제 팀에 제한적으로 붙여 보고, 조직 표준으로 승격 가능한지 판단한다.

## Deliverables

### 1. Pilot Team Deployment

- 적용 대상 팀 1~2개
- 대상 작업 유형 제한
- 운영 책임자 지정

### 2. Pilot Scorecard

- success rate
- High finding rate
- rework rate
- average latency
- human intervention rate
- owner escalation count

### 3. Release Readiness Review

- 어떤 control-plane이 효과 있었는지
- 무엇이 운영 복잡도만 늘렸는지
- org-wide rollout 가능성 판단

### 4. Stage-2 Backlog Decision

- 계속 투자할 항목
- 병합/폐기할 항목
- org-wide standard로 승격할 항목

## Work Breakdown

### Week 9

- pilot runbook 작성
- 운영 책임자와 escalation path 지정
- 적용 task boundary 정의

### Week 10

- 첫 pilot batch 수행
- pilot batch evaluation flow 고정
- pilot scorecard template 기준으로 기록
- scorecard 수집
- human intervention 로그 분석

### Week 11

- second pilot batch 수행
- cost/quality comparison
- owner routing / security review 조정

### Week 12

- 90일 리뷰 문서 작성
- 승격 / 보류 / 폐기 결정
- 다음 90일 backlog 재정렬

## Exit Criteria

- pilot 팀에서 baseline 대비 complex-case 품질 개선 신호가 있다
- release/approval/security 라인이 운영 방해만 하지 않고 실제 가치가 있다
- CTO가 org-wide stage-2 rollout 여부를 판단할 수 있는 근거가 모인다

## KPI Set

### Quality KPI

- complex-case pass rate
- High review finding rate
- gate pass rate
- docs drift rate
- rework rate

### Governance KPI

- approval-required detection rate
- release blocker precision
- security review trigger precision
- owner routing accuracy

### Efficiency KPI

- task type별 평균 시간
- task type별 평균 비용
- human intervention rate
- cost per accepted change

## Risks And Mitigations

### Risk 1. Control-plane이 execution 속도를 과도하게 늦춘다

대응:

- 모든 task에 동일한 governance를 강제하지 않는다
- risk class 기반으로 policy depth를 다르게 둔다

### Risk 2. Security review가 noise를 많이 만든다

대응:

- trigger를 좁게 시작한다
- auth / PII / secrets touched 변경부터 시작한다

### Risk 3. Ownership metadata가 부정확하다

대응:

- pilot 팀 범위에서만 먼저 owner map을 유지한다
- org-wide 전개는 metadata 품질이 올라간 뒤 진행한다

### Risk 4. mini downshift가 너무 빨리 도입된다

대응:

- pilot 기본값은 quality-first route를 유지한다
- mini downshift는 triage/context에서만 제한적으로 검증한다

## Default Decisions For The Next 90 Days

- production-like pilot 기본값은 `C2 + all gpt-5.4/high`
- `execution=xhigh`는 기본값으로 사용하지 않는다
- `C0`는 baseline 용도로만 유지한다
- `mini`는 triage/context downshift 실험 외에는 기본 route로 쓰지 않는다

## What Success Looks Like

90일 뒤 성공한 상태는 아래다.

- 복잡한 변경에 대해 팀이 같은 operating contract를 쓴다
- agent output을 더 이상 “감”으로 평가하지 않는다
- release / approval / security / ownership / cost가 하나의 흐름 안에서 보인다
- CTO가 “어떤 작업에 어떤 조합을 써야 하는가”를 문서와 지표로 설명할 수 있다

이 상태가 되면 `agent-lab`은 단순한 benchmark 저장소가 아니라,
조직 차원의 AI-assisted software delivery 운영 표준의 초기 버전이 된다.
