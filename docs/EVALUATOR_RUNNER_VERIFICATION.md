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

## Additional Lane Verification

### `c0-gpt54-high__tenant-cache-scope`

실행:

```bash
python3 scripts/run_codex_benchmark.py \
  --config benchmark/deep_validation_matrix.yaml \
  --existing-run-dir artifacts/benchmark_runs/refined-skill-batch/c0-gpt54-high__tenant-cache-scope
```

결과:

- `security` lane 생성 완료
- `security_findings.json`: `high=1`, `medium=0`, `low=0`
- disagreement scaffold 생성:
  - [disagreement_security.md](../artifacts/benchmark_runs/refined-skill-batch/c0-gpt54-high__tenant-cache-scope/evaluators/disagreement_security.md)

### `c2-execution-xhigh__presence-race`

실행:

```bash
python3 scripts/run_codex_benchmark.py \
  --config benchmark/deep_validation_matrix.yaml \
  --existing-run-dir artifacts/benchmark_runs/refined-skill-batch/c2-execution-xhigh__presence-race \
  --reuse-existing-review
```

결과:

- `architecture` lane 생성 완료
- `architecture_findings.json`: `high=1`, `medium=0`, `low=0`
- review와 architecture가 같은 severity signature를 보여 disagreement scaffold는 생성되지 않았다

### `c2-mini-triage-context__presence-race`

이 run은 최초 refined batch 실행에서 executor가 정상 종료하지 않아
`gate_results.json`, `review_findings.json`, `trace_record.json`이 비어 있었다.
복구 과정은 다음 순서로 진행했다.

1. 기존 `workspace`와 `c2_*_codex_events.jsonl`에서 execution 산출물과 usage를 회수
2. gate를 재실행해 `gate_results.json` 생성
3. review lane를 다시 실행해 `review_findings.json` 확보
4. provisional `trace_record.json`을 만든 뒤 `architecture` lane를 backfill

결과:

- `review_findings.json`: `high=1`, `medium=0`, `low=1`
- `architecture_findings.json`: `high=1`, `medium=0`, `low=0`
- disagreement scaffold 생성:
  - [disagreement_architecture.md](../artifacts/benchmark_runs/refined-skill-batch/c2-mini-triage-context__presence-race/evaluators/disagreement_architecture.md)
- candidate usage는 기존 jsonl에서 복구했지만, candidate wall-clock timing은 recover-only metadata로만 남겼다

## Existing-Batch Planning Verification

```bash
python3 scripts/run_codex_benchmark.py \
  --config benchmark/deep_validation_matrix.yaml \
  --existing-batch-root artifacts/benchmark_runs/refined-skill-batch \
  --plan-only
```

관찰 결과:

- planned run:
  - `c0-gpt54-high__tenant-cache-scope`
  - `c2-all-gpt54-high__flag-rollout-fallback`
  - `c2-execution-xhigh__presence-race`
  - `c2-mini-triage-context__presence-race`
- skipped run: 없음

## Remaining Gap

현재는 아래까지 자동화되어 있다.

- plan-only lane selection
- manifest generation / validation
- existing-run evaluator backfill
- existing-batch planning with skip handling
- `evaluators/index.json` 생성
- disagreement scaffold auto-generation
- trace / batch summary 갱신

다음 단계는 lane별 human calibration hook과
deep-validation scorecard 자동 승격 규칙 연결이다.
