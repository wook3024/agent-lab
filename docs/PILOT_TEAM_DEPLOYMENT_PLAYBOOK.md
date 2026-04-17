# Pilot Team Deployment Playbook

## 목적

이 문서는 현재 `agent-lab`에서 만든 control-plane 자산을 실제 팀에 제한적으로 적용하기 위한 pilot 운영 절차다.

pilot의 목표는 두 가지다.

1. complex-case에서 실제 품질과 운영 통제력이 올라가는지 확인한다
2. control-plane이 조직 속도를 과도하게 늦추지 않는지 확인한다

## Pilot Scope

### Recommended Team Shape

- 팀 수: 1~2개
- 도메인: auth, payments, platform runtime, shared data path처럼 complex-case가 자주 나오는 팀
- 성격: 이미 코드 리뷰와 테스트 문화가 어느 정도 있는 팀

### Task Types In Scope

- cross-file bug fix
- regression-prone reliability hardening
- rollout / release sensitive changes
- ownership이 중요한 shared service 변경

### Task Types Out Of Scope

- 단순 문서 수정
- trivial refactor
- 대규모 조직 개편 수준의 multi-team rewrite
- production shell 직접 조작이 필요한 emergency only 작업

## Pilot Default Route

pilot 기본값은 아래 route를 사용한다.

1. `Triage Agent`
2. `Owner-Aware Context Builder`
3. `Execution Agent`
4. `Deterministic Gates`
5. `Review Agent`
6. `Security Review Agent` if triggered
7. `Approval Policy`
8. `Release Gate Agent`
9. `Release Artifact Generator`
10. `Trace + Scorecard`

## Recommended Model Policy

- Triage / Context / Review / Governance: `gpt-5.4 / high`
- Execution: `gpt-5.4 / high`
- `mini`는 pilot 기본값으로 쓰지 않는다
- `xhigh`는 예외적 조사 run에서만 허용한다

## Entry Criteria

pilot에 넣을 작업은 아래 조건 중 3개 이상을 만족해야 한다.

- 3개 이상 파일 수정
- 테스트 수정 또는 추가 필수
- 문서 또는 runbook 반영 필요
- release / approval / owner routing relevance 존재
- 회귀 위험이 높음
- shared service 또는 critical service 관련

## Operating Sequence

### Step 1. Intake And Classification

- task class 분류
- risk class 분류
- owner team 식별
- approval 필요 가능성 표시

### Step 2. Triage And Owner-Aware Context

- goal / non-goals / invariants / reviewer focus 정리
- owner team, service criticality, runbook, recent incident context 포함

### Step 3. Execution

- smallest coherent diff
- regression coverage
- docs sync

### Step 4. Review Lanes

- 일반 review
- security review if triggered
- architecture review if structural risk detected

### Step 5. Governance

- approval classification
- release gate decision
- release artifact package

### Step 6. Observation

- trace record
- pilot scorecard entry
- intervention count 기록

## Companion Assets

- `docs/PILOT_OWNER_MAP_SAMPLE.yaml`
- `docs/templates/PILOT_SCORECARD_TEMPLATE.md`
- `docs/PILOT_BATCH_EVALUATION_FLOW.md`

## Trigger Rules

### Security Review Trigger

- auth / RBAC touched
- tenant isolation touched
- PII or secret flow touched
- trust boundary touched

### Architecture Review Trigger

- shared module abstraction 추가
- migration sequencing 포함
- coupling 증가 가능성
- ownership 경계가 흐려지는 변경

### Release Gate Trigger

- production behavior changed
- rollout / migration / config / operator action 포함
- approval-required classification

## Required Artifacts Per Pilot Run

- task brief
- owner-aware context pack
- execution report
- gate results
- general review findings
- security review findings if triggered
- approval decision
- release gate decision
- release artifact package
- trace record

## Pilot Scorecard Fields

- task id
- service name
- owner team
- risk class
- pass / fail
- high findings
- release hold count
- approval escalation count
- elapsed time
- estimated cost
- human intervention count

## Success Criteria

- baseline 대비 High finding rate 감소
- docs drift 감소
- approval-required task의 silent progression 감소
- release hold precision 상승
- pilot 팀이 “운영은 가능하다”고 판단

## Failure Criteria

- control-plane이 every task를 느리게 만들기만 함
- owner routing이 부정확해 reviewer 품질이 떨어짐
- security review가 noise만 늘리고 precision이 낮음
- release gate가 blocker와 residual risk를 구분하지 못함

## Weekly Pilot Cadence

### Weekly Review

- 이번 주 pilot run 수
- hold / escalate 비율
- human intervention 사례
- quality-first route 유지 여부

### Retro Questions

- 어떤 lane이 실제 defect를 잡았는가
- 어떤 lane이 noise를 만들었는가
- 어느 task type에서 mini downshift를 검토할 수 있는가
- owner metadata가 어디서 부족했는가

## Exit Decision

pilot 종료 시 아래 셋 중 하나를 결정한다.

- `promote`: 조직 표준에 점진 적용
- `narrow`: 특정 task type에만 유지
- `rework`: control-plane 조정 후 재시도
