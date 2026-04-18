# Evaluator Runner Verification

## 목적

이 문서는 evaluator runner contract가
현재 저장소의 실제 benchmark run artifact 위에서 동작하는지 확인한 실행 기록이다.

## Verified Run

- batch: `refined-skill-batch`
- run: `c2-all-gpt54-high__flag-rollout-fallback`
- workspace:
  - `artifacts/benchmark_runs/refined-skill-batch/c2-all-gpt54-high__flag-rollout-fallback/workspace`

## Commands Run

### 1. Review Manifest Build

```bash
python3 scripts/build_evaluator_manifest.py \
  --run-dir artifacts/benchmark_runs/refined-skill-batch/c2-all-gpt54-high__flag-rollout-fallback \
  --lane review \
  --output artifacts/benchmark_runs/refined-skill-batch/c2-all-gpt54-high__flag-rollout-fallback/review_manifest.json
```

### 2. Release Gate Manifest Build

```bash
python3 scripts/build_evaluator_manifest.py \
  --run-dir artifacts/benchmark_runs/refined-skill-batch/c2-all-gpt54-high__flag-rollout-fallback \
  --lane release_gate \
  --output artifacts/benchmark_runs/refined-skill-batch/c2-all-gpt54-high__flag-rollout-fallback/release_gate_manifest.json
```

### 3. Bundle Validation

```bash
python3 scripts/validate_evaluator_bundle.py \
  --manifest artifacts/benchmark_runs/refined-skill-batch/c2-all-gpt54-high__flag-rollout-fallback/review_manifest.json
```

결과:

- `evaluator-bundle-valid`

```bash
python3 scripts/validate_evaluator_bundle.py \
  --manifest artifacts/benchmark_runs/refined-skill-batch/c2-all-gpt54-high__flag-rollout-fallback/release_gate_manifest.json
```

결과:

- `evaluator-bundle-valid`

## Generated Artifacts

- [review_manifest.json](../artifacts/benchmark_runs/refined-skill-batch/c2-all-gpt54-high__flag-rollout-fallback/review_manifest.json)
- [release_gate_manifest.json](../artifacts/benchmark_runs/refined-skill-batch/c2-all-gpt54-high__flag-rollout-fallback/release_gate_manifest.json)

## What This Proves

- 현재 run directory 구조만으로 evaluator input bundle을 재구성할 수 있다
- `benchmark_outputs/task_brief.md`, `context_pack.md`, `execution_report.md`가 evaluator contract에 충분히 연결된다
- diff는 `workspace` 내부 `git diff HEAD`로 읽을 수 있다
- lane별 manifest를 별도 저장하는 구조가 현실적으로 동작한다

## Remaining Gap

현재는 manifest 생성과 validation까지만 자동화되어 있다.

다음 단계는 아래다.

1. lane별 prompt 실행 runner 추가
2. evaluator result를 `artifacts/.../evaluators/` 아래 표준 저장
3. disagreement template 자동 scaffold 생성
