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

## Plan-Only Lane Verification

추가로 `benchmark/deep_validation_matrix.yaml` 기준으로
task별 lane selection이 의도대로 되는지도 확인했다.

### `tenant-cache-scope`

- selected lanes:
  - `review`
  - `security`

### `flag-rollout-fallback`

- selected lanes:
  - `review`
  - `release_gate`

### `presence-race`

- selected lanes:
  - `review`
  - `architecture`

즉, `additional_evaluators` selector가 task complexity axis 기준으로 정상 동작함을 확인했다.

## Existing-Run Backfill Verification

후처리 evaluator-only 실행도 실제로 검증했다.

```bash
python3 scripts/run_codex_benchmark.py \
  --config benchmark/deep_validation_matrix.yaml \
  --existing-run-dir artifacts/benchmark_runs/refined-skill-batch/c2-all-gpt54-high__flag-rollout-fallback
```

생성된 artifact:

- [evaluators/review_manifest.json](../artifacts/benchmark_runs/refined-skill-batch/c2-all-gpt54-high__flag-rollout-fallback/evaluators/review_manifest.json)
- [evaluators/release_gate_manifest.json](../artifacts/benchmark_runs/refined-skill-batch/c2-all-gpt54-high__flag-rollout-fallback/evaluators/release_gate_manifest.json)
- [evaluators/release_gate_findings.json](../artifacts/benchmark_runs/refined-skill-batch/c2-all-gpt54-high__flag-rollout-fallback/evaluators/release_gate_findings.json)
- [evaluators/index.json](../artifacts/benchmark_runs/refined-skill-batch/c2-all-gpt54-high__flag-rollout-fallback/evaluators/index.json)

관찰 결과:

- `review` lane는 `high=0`, `medium=0`, `low=0`
- `release_gate` lane는 `high=2`, `medium=2`, `low=0`
- 기존 run의 `trace_record.json`은 evaluator 결과를 반영해 `result=fail`로 재계산됐다
- `python3 scripts/validate_evaluator_bundle.py --manifest .../evaluators/release_gate_manifest.json`는 `evaluator-bundle-valid`를 반환했다

## Remaining Gap

현재는 아래까지 자동화되어 있다.

- plan-only lane selection
- manifest generation / validation
- existing-run evaluator backfill
- `evaluators/index.json` 생성
- trace / batch summary 갱신

다음 단계는 disagreement template 자동 scaffold 생성과
lane별 human calibration hook 연결이다.
