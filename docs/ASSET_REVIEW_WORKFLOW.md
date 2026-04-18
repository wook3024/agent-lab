# Asset Review Workflow

## 목적

이 문서는 pilot batch 또는 benchmark batch가 끝난 뒤
`ASSET_REGISTRY.yaml`과 자산 상태를 어떻게 갱신해야 하는지 정리한 운영 절차다.

핵심 목적은 두 가지다.

1. 결과가 나와도 registry가 방치되지 않게 한다
2. 승격, 유지, 폐기 결정을 감이 아니라 증거로 남긴다

## When To Run This Workflow

아래 중 하나가 끝나면 이 workflow를 실행한다.

- pilot batch 1회 종료
- refined benchmark batch 1회 종료
- default model policy를 건드린 실험 종료
- control-plane trigger precision을 평가한 실험 종료

## Inputs

이 workflow는 아래 artifact를 입력으로 사용한다.

- pilot scorecard
- batch trace bundle
- batch review findings
- approval / release / security decision bundle
- batch summary memo
- current `docs/ASSET_REGISTRY.yaml`

## Output

종료 시 아래가 남아 있어야 한다.

- 갱신된 `docs/ASSET_REGISTRY.yaml`
- 자산별 상태 변경 판단 기록
- 필요한 경우 갱신된 `docs/ASSET_STATUS_BASELINE.md`
- 필요한 경우 갱신된 `docs/RECOMMENDED_AGENT_SKILL_MODEL_CONFIGS.md`

## Review Sequence

### Step 1. Freeze Evidence

먼저 batch 결과를 고정한다.

- batch id 확정
- scorecard 확정
- trace 경로 확정
- review findings bundle 확정

이 단계가 없으면 `last_validated_batch`와 evidence 링크가 흔들린다.

### Step 2. Identify Touched Assets

이번 batch에서 실제로 의미 있게 평가된 자산만 추린다.

예:

- topology
- role-specific model policy
- security-review
- owner-aware-context-builder
- release-gate

모든 자산을 매 batch마다 재평가하지 않는다.

### Step 3. Evaluate Each Asset

각 자산마다 아래 질문을 본다.

- 실제로 켜졌는가
- 켜졌다면 품질 개선 근거가 있었는가
- false positive 또는 운영 noise를 만들었는가
- human intervention을 줄였는가, 늘렸는가
- 다음 batch에서도 기본 유지할 가치가 있는가

### Step 4. Make One Decision Per Asset

각 자산은 아래 중 하나로 닫는다.

- `keep`
- `promote`
- `narrow`
- `rework`
- `deprecate`

의미:

- `keep`: 상태 유지, evidence만 갱신
- `promote`: `pilot` 또는 `conditional`에서 한 단계 올림
- `narrow`: trigger 범위를 줄임
- `rework`: 상태는 유지하되 contract 수정 필요
- `deprecate`: 운영 기본 경로에서 제외

### Step 5. Update Registry

각 자산에 대해 최소 아래 필드를 갱신한다.

- `last_validated_batch`
- `evidence`
- `decision_gate`
- `notes`

상태가 바뀌면 아래도 함께 갱신한다.

- `status`
- `default_on`
- `replacement_candidate`

### Step 6. Update Human-Readable Summaries

아래 문서는 필요할 때만 갱신한다.

- `docs/ASSET_STATUS_BASELINE.md`
- `docs/RECOMMENDED_AGENT_SKILL_MODEL_CONFIGS.md`
- `docs/agent_lab_dossier.html`

원칙:

- registry가 먼저
- 사람이 읽는 요약 문서는 나중

## Decision Rubric

### Promote

아래를 만족하면 승격 후보로 본다.

- 2개 이상 batch에서 근거가 누적됨
- quality regression이 없음
- governance precision이 수용 가능함
- operator 또는 reviewer가 실제로 artifact를 신뢰함

### Keep

아래 상황이면 유지한다.

- 아직 근거가 부족하지만 성과는 긍정적
- 노이즈가 크지 않음
- 다음 batch에서 더 확인 가치가 있음

### Narrow

아래 상황이면 범위를 줄인다.

- 가치가 있지만 trigger precision이 낮음
- 특정 task class에서만 강함
- default-on으로 두기에는 마찰이 큼

### Rework

아래 상황이면 재설계가 필요하다.

- false positive가 반복됨
- trace 상으로는 켜졌지만 결과 품질 개선이 거의 없음
- batch마다 사람 해석 없이는 동작 의미가 불명확함

### Deprecate

아래 상황이면 내린다.

- standard 대비 복잡도만 늘고 품질 이득이 없음
- 최근 2개 batch에서 의미 있는 사용 근거가 없음
- 더 단순한 자산으로 흡수 가능함

## Required Update Order

항상 아래 순서를 지킨다.

1. evidence artifact 정리
2. registry 업데이트
3. validator 실행
4. status baseline 갱신
5. dossier 갱신

## Minimal Commands

```bash
scripts/validate_asset_registry.rb
```

필요 시:

```bash
git diff docs/ASSET_REGISTRY.yaml docs/ASSET_STATUS_BASELINE.md docs/RECOMMENDED_AGENT_SKILL_MODEL_CONFIGS.md
```

## Review Cadence

- weekly: touched asset의 `last_validated_batch` 갱신
- biweekly: `promote / narrow / rework / deprecate` 판정
- monthly: status baseline 전체 재검토

## Practical Default

지금 당장 현실적인 운영 규칙은 이렇다.

- standard는 거의 건드리지 않는다
- pilot 자산만 batch마다 적극 평가한다
- conditional 자산은 trigger precision을 중심으로 본다
- deprecated 자산은 baseline reference 외에는 다시 켜지지 않는다
