# Asset Status Baseline

## 목적

이 문서는 현재 `agent-lab` 자산을
`standard / pilot / conditional / deprecated` 기준으로 재분류한 첫 운영 기준선이다.

registry가 기계 판독 가능한 원본이라면,
이 문서는 사람이 빠르게 읽는 운영 판단 요약본이다.

## Executive Summary

현재 가장 중요한 방향은 단순하다.

- `standard`는 최소 강력 세트만 유지
- control-plane은 대부분 `pilot`로 관리
- 조사성/예외성 자산은 `conditional`
- complex-case 기본값으로 부적합한 경로는 `deprecated`

## Standard

### Topology

- `C2`

### Agents

- `triage-agent`
- `execution-agent`
- `review-agent`

### Skills

- `task-brief-author`
- `context-pack-builder`
- `execution-engineering`
- `quality-gates-runner`
- `review-findings`
- `docs-sync`
- `trace-eval-recorder`

### Model Policy

- `complex-case-default-gpt54-high`

## Pilot

pilot은 실제 운영 가치가 높지만,
아직 default route의 항상-on standard로는 승격하지 않은 자산이다.

### Agents

- `release-gate-agent`
- `security-review-agent`

### Skills

- `release-gate`
- `approval-policy`
- `security-review`
- `ownership-routing`
- `owner-aware-context-builder`
- `release-artifact-generator`

## Conditional

조건부 자산은 default route에 조용히 섞지 않고,
명확한 trigger가 있을 때만 쓴다.

### Skills

- `research-grounded`
- `cost-governance-trace`
- `incident-mode-policy`
- `architecture-review`

### Model Policies

- `mini-triage-context-downshift`

## Deprecated

deprecated는 운영 기본값으로는 쓰지 않지만,
기준선 비교 또는 historical reference로 남겨두는 자산이다.

### Topology

- `C0`

### Model Policies

- `execution-xhigh-default`

## Why This Split Makes Sense

### 1. Standard는 작아야 한다

표준 운영 경로는 복잡해질수록 조직 전체 품질이 아니라 운영 마찰만 키울 수 있다.  
따라서 현재는 `C2 + 핵심 execution/review/gate/trace skill`만 standard로 둔다.

### 2. Control-plane은 먼저 pilot로 붙인다

`release-gate`, `approval-policy`, `security-review`, `ownership-routing`은
매우 중요하지만 false positive와 운영 overhead를 먼저 봐야 한다.

### 3. Conditional은 강하지만 항상 켜면 안 된다

`research-grounded`, `incident-mode-policy`, `architecture-review`는
상황이 맞으면 강력하지만, 기본값으로 켜면 속도와 일관성을 해칠 수 있다.

### 4. Deprecated를 명시해야 실수로 재사용되지 않는다

`C0`와 `execution=xhigh default`는 참고용으로는 가치가 있지만,
complex-case 운영 기본값으로는 명시적으로 내려놔야 한다.

## Next Promotion Targets

현재 가장 유력한 승격 후보는 아래다.

1. `release-gate`
2. `approval-policy`
3. `security-review`
4. `owner-aware-context-builder`

이 자산들은 pilot batch에서 precision과 운영 마찰이 관리 가능하면
다음 standard 후보가 될 수 있다.

## Next Deprioritization Review

아래는 다음 batch에서 통합 또는 후순위화를 검토할 만하다.

- `review-findings`가 별도 skill로 계속 남아야 하는지
- `release-artifact-generator`가 release-gate 하위 contract로 흡수 가능한지
- `cost-governance-trace`가 conditional에서 pilot로 올라갈 만큼 실제로 쓰이는지
