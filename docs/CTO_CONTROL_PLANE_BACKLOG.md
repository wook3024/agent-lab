# CTO Control Plane Backlog

## 목적

이 문서는 현재 `agent-lab`을 CTO-grade 운영 체계로 끌어올리기 위해
추가해야 할 control-plane 자산을 우선순위 순으로 정리한 backlog다.

핵심 원칙은 다음과 같다.

- 새로운 implementation skill보다 control-plane 자산을 먼저 만든다
- backlog는 “흥미로운 실험”이 아니라 “운영 리스크 감소” 기준으로 우선순위를 매긴다
- 각 항목은 산출물, 의존성, 수용 기준이 있어야 한다

## Prioritization Framework

### P0

- 없으면 운영 리스크가 크다
- 승인, 배포, 보안, 비용 통제와 직결된다
- complex-case 품질 향상 이후 가장 먼저 붙여야 한다

### P1

- 조직 운영 효율을 높인다
- baseline이 안정화되면 바로 이어서 붙인다

### P2

- 확장 단계에서 필요하다
- 아직은 조건부이거나 특정 규모에서만 이득이 크다

## P0 Backlog

### P0-1. Release Gate Agent

#### Why

현재 체계는 구현 품질에는 강하지만, “이 변경을 배포해도 되는가”를 판정하는 표준 에이전트가 없다.

#### Current Status

- role card 작성 완료
- skill scaffold 작성 완료
- output template 작성 완료

#### Scope

- release blocker 판정
- rollback readiness 확인
- migration safety 확인
- owner approval completeness 확인
- release note / runbook completeness 확인

#### Deliverables

- `docs/roles/RELEASE_GATE_AGENT_ROLE.md`
- `skills/release-gate/SKILL.md`
- release gate output schema
- release blocker severity rubric

#### Depends On

- `quality-gates-runner`
- `docs-sync`
- owner mapping data

#### Acceptance Criteria

- risky release 후보에서 명시적 blocker가 나오고
- rollback 준비 부족을 검출하며
- release-ready / hold / escalate 판정을 일관되게 생성한다

### P0-2. Approval Policy Skill

#### Why

현재 approval 개념은 문서상 존재하지만, benchmark 시스템 안에서 강제되는 skill로는 아직 없다.

#### Current Status

- skill scaffold 작성 완료
- approval decision template 작성 완료
- policy matrix 세부 규칙은 후속 정교화 필요

#### Scope

- read-only / safe write / moderate / risky / irreversible 분류
- approval-required change detection
- destructive action preflight
- human escalation trigger generation

#### Deliverables

- `skills/approval-policy/SKILL.md`
- approval matrix schema
- escalation reason taxonomy

#### Depends On

- task brief
- change surface detection

#### Acceptance Criteria

- risky or irreversible task를 auto-allow하지 않는다
- approval 필요 여부를 trace에 남긴다
- release gate와 일관된 판정을 낸다

### P0-3. Security Review Skill

#### Why

현재 Review Agent는 일반 defect finding에는 강하지만,
보안과 정책을 별도 축으로 강하게 보지 않는다.

#### Current Status

- role card 작성 완료
- skill scaffold 작성 완료
- security review output template 작성 완료

#### Scope

- auth / RBAC review
- data exposure review
- secret handling review
- audit logging review
- external integration risk review

#### Deliverables

- `skills/security-review/SKILL.md`
- security review rubric
- trigger conditions for security review routing

#### Depends On

- diff inspection
- ownership router
- policy docs

#### Acceptance Criteria

- auth or PII 관련 변경 시 security review lane이 자동으로 붙는다
- 일반 리뷰와 다른 severity contract를 유지한다
- 최소 1개 이상 보안성 benchmark task에서 유의미한 finding을 만든다

### P0-4. Ownership Routing Layer

#### Why

실제 조직에서는 품질만큼 “누가 책임지는가”가 중요하다.

#### Scope

- repo path to owner team mapping
- service criticality mapping
- reviewer route selection
- approval owner mapping

#### Current Status

- skill scaffold 작성 완료
- owner routing decision template 작성 완료
- owner map template 작성 완료

#### Deliverables

- owner map config
- routing rules
- owner-aware review context format

#### Depends On

- service inventory
- team ownership metadata

#### Acceptance Criteria

- 변경 파일 기준으로 owner team이 계산된다
- critical path 서비스는 stricter review/gate로 자동 라우팅된다
- release gate와 approval policy에서 owner를 참조할 수 있다

### P0-5. Cost Governance Trace Layer

#### Why

현재는 benchmark scorecard는 있지만 운영 재무 관점의 governance는 약하다.

#### Current Status

- skill scaffold 작성 완료
- cost governance report template 작성 완료
- trace schema 확장 초안 작성 완료

#### Scope

- role별 token/cost/latency 수집
- task-type별 평균 비용
- cost versus quality comparison
- minimum sufficient config policy

#### Deliverables

- extended trace schema
- cost report template
- routing recommendation policy

#### Depends On

- `trace-eval-recorder`
- benchmark runner metrics

#### Acceptance Criteria

- task type별 평균 비용을 집계할 수 있다
- `quality-first`와 `cost-optimized` routing을 수치로 비교할 수 있다
- 월간 예산 관점의 시뮬레이션이 가능하다

## P1 Backlog

### P1-1. Incident Mode Policy Skill

#### Why

incident 상황에서는 normal implementation flow와 다른 통제가 필요하다.

#### Current Status

- skill scaffold 작성 완료
- incident mode decision template 작성 완료

#### Scope

- hotfix mode rules
- freeze bypass rules
- incident documentation requirements
- postmortem capture requirements

### P1-2. Architecture Review Skill

#### Why

기능은 맞아도 architecture debt를 남기는 변경을 잡기 위한 별도 lens가 필요하다.

#### Scope

- boundary erosion review
- coupling increase detection
- migration sequencing review
- reuse versus abstraction judgment

### P1-3. Owner-Aware Context Builder

#### Why

owner 정보가 context pack에 자연스럽게 들어가야 reviewer 품질이 오른다.

#### Scope

- owner-specific docs inclusion
- service risk docs inclusion
- last incident context inclusion

### P1-4. Release Artifact Generator

#### Why

change summary, runbook delta, rollback notes를 표준화하면 배포 품질이 올라간다.

#### Scope

- release note draft
- operator checklist delta
- rollback note draft

## P2 Backlog

### P2-1. Managed Multi-Agent For Parallel Work

#### Why

현재는 baseline이 아니지만, 팀 규모가 커지면 병렬화 이득이 생길 수 있다.

#### Scope

- implementation/test/review 병렬화
- manager-controlled integration
- disjoint write-set routing

### P2-2. Org-Wide Portfolio Dashboard

#### Why

팀/서비스별 AI leverage와 risk posture를 portfolio view로 볼 필요가 생긴다.

#### Scope

- service quality leaderboard
- task type breakdown
- cost per team
- intervention rate per team

### P2-3. Benchmark Expansion To Feature/Migration/Ops

#### Why

현재 benchmark는 bugfix/reliability 중심이라 wider engineering surface로 확장해야 한다.

#### Scope

- feature implementation tasks
- migration tasks
- ops/runbook tasks
- policy-constrained tasks

## Sequencing Recommendation

### Wave 1

- Release Gate Agent
- Approval Policy Skill
- Security Review Skill

이 셋이 먼저다.  
이유는 배포, 승인, 보안이 CTO 관점의 가장 직접적인 리스크 축이기 때문이다.

### Wave 2

- Ownership Routing Layer
- Cost Governance Trace Layer
- Incident Mode Policy Skill

이 wave는 조직 운영성숙도를 올리는 단계다.

### Wave 3

- Architecture Review Skill
- Release Artifact Generator
- Benchmark Expansion

이 단계부터는 baseline 운영 위에서 품질과 확장성을 더 끌어올리는 작업이다.

### Wave 4

- Managed Multi-Agent
- Org-Wide Portfolio Dashboard

이건 baseline 안정화 이후에 붙여야 한다.

## Backlog Kill Rules

아래 항목은 backlog에 올려도 바로 진행하지 않는다.

- 품질 지표 없이 “좋아 보이는” 새 에이전트
- owner mapping 없이 auto-merge를 지향하는 기능
- release/approval 통제 없이 배포 자동화부터 붙이는 작업
- benchmark expansion 없이 prompt만 바꾸는 반복 작업

## What To Build Next

바로 다음 착수 우선순위는 명확하다.

1. `Release Gate Agent`
2. `Approval Policy Skill`
3. `Security Review Skill`
4. `Ownership Routing Layer`
5. `Cost Governance Trace Layer`

이 다섯 개가 붙으면 현재 시스템은 “complex-case engineering benchmark”에서
“조직 운영형 AI delivery control system”으로 한 단계 올라간다.
