# Pilot Batch 01 Registry Update Example

## 목적

이 문서는 `pilot-batch-01` 결과를 registry에 반영할 때
어떤 필드가 어떻게 바뀌는지 보여주는 샘플 업데이트 예시다.

주의:

- 이 문서는 설명용 예시다
- authoritative source는 여전히 `docs/ASSET_REGISTRY.yaml`이다

## Example Updates

### `release-gate`

```yaml
- asset_id: "release-gate"
  asset_type: "skill"
  status: "pilot"
  owner: "cto-office"
  default_on: false
  last_validated_batch: "pilot-batch-01"
  evidence:
    - "skills/release-gate/SKILL.md"
    - "docs/PILOT_TEAM_DEPLOYMENT_PLAYBOOK.md"
    - "docs/PILOT_BATCH_01_SCORECARD.md"
    - "docs/PILOT_BATCH_01_ASSET_REVIEW.md"
  depends_on:
    - "approval-policy"
    - "release-artifact-generator"
  decision_gate: "needs-1-more-pilot-batch-before-standard-consideration"
  notes: "release-sensitive task에서 hold precision이 좋았고 false hold는 없었음"
```

### `approval-policy`

```yaml
- asset_id: "approval-policy"
  asset_type: "skill"
  status: "pilot"
  owner: "cto-office"
  default_on: false
  last_validated_batch: "pilot-batch-01"
  evidence:
    - "skills/approval-policy/SKILL.md"
    - "docs/PILOT_TEAM_DEPLOYMENT_PLAYBOOK.md"
    - "docs/PILOT_BATCH_01_SCORECARD.md"
    - "docs/PILOT_BATCH_01_ASSET_REVIEW.md"
  decision_gate: "needs-one-more-batch-and-operator-feedback"
  notes: "approval-required detection은 좋았고 wording refinement만 남음"
```

### `security-review`

```yaml
- asset_id: "security-review"
  asset_type: "skill"
  status: "pilot"
  owner: "security-engineering"
  default_on: false
  last_validated_batch: "pilot-batch-01"
  evidence:
    - "skills/security-review/SKILL.md"
    - "docs/PILOT_TEAM_DEPLOYMENT_PLAYBOOK.md"
    - "docs/PILOT_BATCH_01_SCORECARD.md"
    - "docs/PILOT_BATCH_01_ASSET_REVIEW.md"
  depends_on:
    - "ownership-routing"
  decision_gate: "narrow-trigger-to-auth-pii-secret-tenant-boundary"
  notes: "tenant/auth 경계 변경에는 강했지만 release-only task에서는 과보수적이었음"
```

### `ownership-routing`

```yaml
- asset_id: "ownership-routing"
  asset_type: "skill"
  status: "pilot"
  owner: "platform-runtime"
  default_on: false
  last_validated_batch: "pilot-batch-01"
  evidence:
    - "skills/ownership-routing/SKILL.md"
    - "docs/PILOT_OWNER_MAP_SAMPLE.yaml"
    - "docs/PILOT_BATCH_01_SCORECARD.md"
    - "docs/PILOT_BATCH_01_ASSET_REVIEW.md"
  decision_gate: "needs-owner-map-coverage-improvement"
  notes: "critical path routing은 좋았으나 frontend/flags secondary ownership 정의가 부족했음"
```

### `owner-aware-context-builder`

```yaml
- asset_id: "owner-aware-context-builder"
  asset_type: "skill"
  status: "pilot"
  owner: "platform-runtime"
  default_on: true
  last_validated_batch: "pilot-batch-01"
  evidence:
    - "skills/owner-aware-context-builder/SKILL.md"
    - "docs/PILOT_TEAM_DEPLOYMENT_PLAYBOOK.md"
    - "docs/PILOT_BATCH_01_SCORECARD.md"
    - "docs/PILOT_BATCH_01_ASSET_REVIEW.md"
  depends_on:
    - "ownership-routing"
  decision_gate: "needs-second-batch-before-standard-consideration"
  notes: "pilot route에서 가장 실전적인 context 품질 향상 자산 중 하나"
```

## Example Status Baseline Commentary Update

이 batch 이후 사람용 상태 요약은 아래처럼 보강하면 된다.

- `release-gate`: 승격 유력 pilot
- `approval-policy`: 승격 유력 pilot
- `owner-aware-context-builder`: second-batch 확인 후 승격 검토
- `security-review`: trigger를 좁히는 방향으로 narrow
- `ownership-routing`: owner map coverage 보강 후 재평가

## Example Command Sequence

```bash
git diff docs/ASSET_REGISTRY.yaml
scripts/validate_asset_registry.rb
```

필요 시:

```bash
git diff docs/ASSET_STATUS_BASELINE.md docs/RECOMMENDED_AGENT_SKILL_MODEL_CONFIGS.md
```
