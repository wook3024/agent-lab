# Asset Registry Schema

## 목적

이 문서는 `docs/ASSET_REGISTRY.yaml`이 따라야 하는 최소 스키마를 정의한다.

registry의 목적은 세 가지다.

1. 현재 표준 자산을 한 곳에서 확인한다
2. pilot / conditional / deprecated 상태를 명시적으로 관리한다
3. 각 자산의 마지막 검증 근거와 다음 의사결정 지점을 기록한다

## Root Structure

registry는 아래 top-level group을 가진다.

- `topologies`
- `agents`
- `skills`
- `model_policies`

필요하면 이후 `templates`, `benchmarks`, `governance_rules` 그룹을 추가할 수 있다.

## Required Fields

각 entry는 최소 아래 필드를 가진다.

- `asset_id`
- `asset_type`
- `status`
- `owner`
- `default_on`
- `last_validated_batch`
- `evidence`
- `notes`

## Field Definitions

### `asset_id`

- registry 내에서 유일한 식별자
- kebab-case 권장
- 예: `c2-controlled-dual-pass`, `security-review`

### `asset_type`

허용 값:

- `topology`
- `agent`
- `skill`
- `model_policy`

### `status`

허용 값:

- `standard`
- `pilot`
- `conditional`
- `deprecated`

의미:

- `standard`: 현재 기본 운영 경로에 포함
- `pilot`: 실제 운영 검증 중
- `conditional`: 명시 trigger가 있을 때만 사용
- `deprecated`: 운영 기본 경로에서는 비활성

### `owner`

자산 유지 책임을 가진 owner를 나타낸다.

권장 형식:

- `human`: 특정 사람 또는 역할
- `team`: 특정 팀

예:

- `cto-office`
- `platform-runtime`
- `agent-lab-maintainer`

### `default_on`

- `true`면 기본 운영 경로에 포함
- `false`면 trigger 또는 예외 상황에서만 켜짐

주의:

- `status = standard`인데 `default_on = false`인 경우는 특별한 이유가 notes에 있어야 한다

### `last_validated_batch`

가장 최근에 의미 있는 검증이 된 batch 또는 증거 id.

예:

- `refined-batch-2026-q2`
- `pilot-batch-01`
- `not-yet-validated`

### `evidence`

검증 근거 문서 리스트.

권장 값:

- 상대 경로 배열
- 최소 1개 이상

예:

- `docs/FINAL_SCORECARD.md`
- `docs/RECOMMENDED_AGENT_SKILL_MODEL_CONFIGS.md`

### `depends_on`

선택 필드.

이 자산이 의미 있게 작동하기 위해 필요한 다른 자산 id 목록.

### `replacement_candidate`

선택 필드.

향후 이 자산을 대체하거나 흡수할 가능성이 있는 후보.

### `decision_gate`

선택 필드.

다음 status 변경을 위해 필요한 조건을 짧게 적는다.

예:

- `needs-2-pilot-batches`
- `needs-security-trigger-precision-check`

### `notes`

상태 해석, 예외, 제한사항을 짧게 설명한다.

## Recommended Validation Rules

registry를 갱신할 때 아래 규칙을 지킨다.

- `deprecated` 자산은 `default_on = false`
- `pilot` 자산은 `last_validated_batch`가 비어 있으면 안 됨
- `standard` 자산은 evidence가 2개 이상인 것이 바람직함
- `conditional` 자산은 notes에 trigger를 적는 것이 바람직함

## Example Entry

```yaml
- asset_id: "security-review"
  asset_type: "skill"
  status: "pilot"
  owner: "security-engineering"
  default_on: false
  last_validated_batch: "pilot-batch-01"
  evidence:
    - "docs/CTO_CONTROL_PLANE_BACKLOG.md"
    - "docs/skills/security-review.md"
  depends_on:
    - "ownership-routing"
    - "approval-policy"
  decision_gate: "needs-security-trigger-precision-check"
  notes: "auth, PII, secret, trust-boundary touched changes에서만 trigger"
```

## Operating Rule

registry는 설명 문서가 아니라 운영 표준의 상태값이다.  
따라서 status를 바꿀 때는 반드시:

1. evidence 문서 갱신
2. pilot 또는 benchmark 결과 반영
3. dossier 링크 정합성 확인

을 함께 수행한다.
