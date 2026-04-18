# Operating Governance Model

## 목적

이 문서는 `agent-lab`을 단순 실험 저장소가 아니라
반복 가능한 운영 표준 저장소로 관리하기 위한 기본 governance 모델을 정의한다.

핵심 목표는 세 가지다.

1. 현재 표준 조합과 pilot 자산을 분리한다
2. 새 skill/agent 추가보다 승격, 유지, 폐기를 더 엄격하게 관리한다
3. batch 기반 검증 없이는 운영 기본값을 바꾸지 않는다

## Executive Direction

지금부터 `agent-lab`은 아래 두 역할을 동시에 가져가야 한다.

- `operating standard repo`
- `measured experimentation repo`

둘을 섞어 관리하면 빠르게 복잡해진다.  
따라서 모든 자산은 아래 네 상태 중 하나를 가져야 한다.

- `standard`
- `pilot`
- `conditional`
- `deprecated`

그리고 어떤 자산이 현재 기본 운영 경로에 포함되는지는
`ASSET_REGISTRY.yaml` 하나만 authoritative source로 둔다.

## Default Operating Contract

현재 complex-case 기준 기본 운영 경로는 아래다.

1. `Triage`
2. `Owner-Aware Context`
3. `Execution`
4. `Deterministic Gates`
5. `Independent Review`
6. `Security / Approval / Release Gate` if triggered
7. `Release Artifact`
8. `Trace + Scorecard`

현재 기본 모델 정책은 아래다.

- production-like complex-case default: `C2 + gpt-5.4/high`
- `mini` downshift: 기본값 아님
- `xhigh`: 조사성 예외 run에서만 허용

## Governance Layers

### 1. Standard Layer

이 레이어는 조직 기본값이다.

- batch 검증으로 효과가 입증됨
- 운영 시 설명 가능함
- reviewer, approver, operator가 이해 가능한 contract를 가짐
- 예외 없이 기본 route에 포함됨

변경 조건:

- 같은 task family에서 2개 이상 batch 근거 필요
- scorecard 기준 품질 퇴행이 없어야 함
- human intervention 증가가 관리 가능해야 함

### 2. Pilot Layer

pilot은 유망하지만 아직 조직 기본값은 아닌 자산이다.

- 하나 이상의 pilot batch에서 테스트 중
- 특정 task class에서만 유효할 수 있음
- false positive / 운영 noise 검증이 끝나지 않음

변경 조건:

- `promote`, `narrow`, `rework`, `stop` 중 하나로 주기적 판정
- 두 번 연속 근거 없는 pilot 유지 금지

### 3. Conditional Layer

조건부 자산은 항상 필요한 것은 아니지만,
특정 상황에서만 분명한 이득이 있는 자산이다.

예시:

- `research-grounded`
- `incident-mode-policy`
- `architecture-review`

관리 원칙:

- trigger가 명확해야 함
- default route에 조용히 섞이면 안 됨
- 켜졌을 때의 이유가 trace에 남아야 함

### 4. Deprecated Layer

deprecated는 “삭제 대상”과 “역사적 baseline”을 함께 포함한다.

예시:

- complex-case 운영 기본값으로서의 `C0`
- default route로서의 `execution = xhigh`

관리 원칙:

- 운영 경로에서는 기본 비활성
- 유지 이유가 benchmark 비교 또는 historical reference일 때만 존치

## Document Hierarchy

문서는 역할별로 나눠 관리한다.

### Authoritative Documents

- `docs/RECOMMENDED_AGENT_SKILL_MODEL_CONFIGS.md`
- `docs/OPERATING_GOVERNANCE_MODEL.md`
- `docs/ASSET_REGISTRY.yaml`

### Decision And Status Documents

- `docs/ASSET_STATUS_BASELINE.md`
- `docs/CTO_REQUIRED_AGENT_SKILL_ASSESSMENT.md`
- `docs/CTO_CONTROL_PLANE_BACKLOG.md`

### Execution And Pilot Documents

- `docs/PILOT_TEAM_DEPLOYMENT_PLAYBOOK.md`
- `docs/PILOT_BATCH_EVALUATION_FLOW.md`
- `docs/templates/PILOT_SCORECARD_TEMPLATE.md`

### Evidence Documents

- `docs/FINAL_SCORECARD.md`
- `docs/BENCHMARK_BATCH_LOG.md`
- batch-level traces and artifacts

### Summary Document

- `docs/agent_lab_dossier.html`

주의:

- `agent_lab_dossier.html`은 요약본이지 표준 원본이 아니다
- 상태 판단은 registry와 status baseline에서만 바꾼다

## Change Policy

### What Can Change In A Single Batch

한 batch에서는 아래 중 하나만 크게 바꾼다.

- model / effort policy
- skill contract
- routing rule
- review / governance trigger

두 개 이상을 동시에 크게 바꾸면 원인 추적이 어려워진다.

### What Requires Explicit Review

아래는 registry 변경 전에 반드시 검토가 필요하다.

- `standard` 자산의 status 변경
- default model policy 변경
- release / approval / security lane의 default-on 여부 변경
- deprecated 자산의 재승격

### Promotion Rule

pilot 또는 conditional 자산이 `standard`로 올라가려면:

- 동일 계열 batch 2회 이상에서 품질 악화가 없고
- governance false positive가 수용 가능하며
- 운영자가 artifact를 실제로 신뢰할 수 있어야 한다

### Deprecation Rule

자산은 아래 중 하나면 deprecated 후보가 된다.

- standard 대비 품질 증분이 없는데 복잡도만 증가
- trigger precision이 낮아 noise를 반복 생성
- 더 단순한 자산으로 흡수 가능
- 최근 2개 batch에서 사용 근거가 없음

## Weekly And Monthly Rhythm

### Weekly

- pilot batch 1회
- pilot scorecard 1회 업데이트
- registry의 `last_validated_batch` 갱신

### Biweekly

- pilot asset review
- `promote / narrow / rework / stop` 판정

### Monthly

- `standard / pilot / conditional / deprecated` 재분류
- default route 변경 여부 검토
- CTO-level 운영 요약 업데이트

## Recommended Immediate Management Policy

지금 당장 가장 현실적인 운영 정책은 아래다.

- 기본 표준은 하나만 유지: `C2 + gpt-5.4/high`
- `mini`는 triage/context 비용 절감 후보로만 관리
- control-plane 자산은 일단 대부분 `pilot`
- 새 skill 추가보다 registry 정합성과 batch 증거 유지가 우선

## What Good Management Looks Like

운영이 잘 되고 있는 상태는 아래다.

- 팀이 “지금 표준이 무엇인지”를 바로 말할 수 있다
- pilot 자산이 왜 pilot인지 설명 가능하다
- deprecated 자산이 기본 경로로 몰래 쓰이지 않는다
- 새 제안은 항상 batch와 scorecard를 통해 들어온다

이 상태가 되면 `agent-lab`은 문서가 많은 저장소가 아니라,
운영 기준과 실험 기준이 분리된 통제 가능한 저장소가 된다.
