# Evaluator Runner Contract

## 목적

이 문서는 benchmark run 또는 pilot run 결과를
LLM evaluator lane에 연결하기 위한 실행 계약을 정의한다.

목표는 두 가지다.

1. evaluator가 읽어야 하는 artifact bundle을 표준화한다
2. lane별 judge를 같은 입력 규약으로 재사용 가능하게 만든다

## Runner Scope

현재 contract는 아래 evaluator lane을 지원하는 것을 기본으로 한다.

- `review`
- `security`
- `release_gate`
- `architecture`

각 lane은 prompt는 다르지만,
artifact bundle 구조는 가능한 한 공통으로 유지한다.

## Standard Run Directory Shape

현재 benchmark run 결과는 아래 구조를 따른다.

```text
artifacts/benchmark_runs/<batch_id>/<run_id>__<task_id>/
  gate_results.json
  review_findings.json
  trace_record.json
  *_codex_events.jsonl
  workspace/
    benchmark_task.json
    benchmark_outputs/
      task_brief.md
      context_pack.md
      execution_report.md
```

이 디렉터리를 evaluator input의 기본 단위로 본다.

## Required Bundle Fields

각 evaluator invocation은 최소 아래 입력을 가져야 한다.

- `lane`
- `run_dir`
- `workspace`
- `task_manifest`
- `task_brief`
- `context_pack`
- `execution_report`
- `gate_results`
- `trace_record`
- `review_findings`

## Optional Bundle Fields

아래는 lane에 따라 선택적으로 들어간다.

- `approval_decision`
- `release_gate_decision`
- `release_artifact_package`
- `security_review_findings`
- `architecture_review_findings`

현재 benchmark artifact에는 일부 governance 문서가 항상 존재하지 않으므로 optional로 둔다.

## Lane Requirements

### Review Lane

필수:

- task brief
- context pack
- execution report
- gate results
- trace record
- diff

권장:

- release artifact package
- approval decision

### Security Lane

필수:

- task brief
- context pack
- execution report
- trace record
- diff

권장:

- approval decision
- release gate decision

### Release Gate Lane

필수:

- task brief
- execution report
- gate results
- trace record

권장:

- approval decision
- release gate decision
- release artifact package

### Architecture Lane

필수:

- task brief
- context pack
- execution report
- trace record
- diff

권장:

- review findings

## Diff Source Contract

evaluator는 작업 결과 diff를 직접 읽을 수 있어야 한다.

권장 방식:

- `git diff HEAD`

실행 위치:

- `workspace/`

원칙:

- diff가 비어 있으면 evaluator는 이를 finding 또는 invalid input으로 다룬다

## Manifest Contract

`scripts/build_evaluator_manifest.py`는 run directory를 읽어
아래 형태의 manifest를 생성한다.

```json
{
  "lane": "security",
  "run_dir": "...",
  "workspace": "...",
  "task_manifest": "...",
  "task_brief": "...",
  "context_pack": "...",
  "execution_report": "...",
  "gate_results": "...",
  "trace_record": "...",
  "review_findings": "...",
  "optional_artifacts": {
    "approval_decision": null,
    "release_gate_decision": null,
    "release_artifact_package": null
  },
  "diff_command": [
    "git",
    "diff",
    "HEAD"
  ]
}
```

## Validation Contract

`scripts/validate_evaluator_bundle.py`는 아래를 확인한다.

- required files 존재 여부
- workspace가 실제 git repo인지
- lane 값이 허용 범위인지
- diff command가 실행 가능한지

실패하면 exit code `1`로 종료한다.

## Minimal Command Sequence

예시:

```bash
scripts/build_evaluator_manifest.py \
  --run-dir artifacts/benchmark_runs/refined-skill-batch/c2-all-gpt54-high__flag-rollout-fallback \
  --lane review \
  --output /tmp/review_manifest.json
```

그 다음:

```bash
scripts/validate_evaluator_bundle.py --manifest /tmp/review_manifest.json
```

## Integration Guidance

### Near Term

- benchmark batch 종료 후 run directory별 manifest 생성
- lane별 prompt를 사용해 evaluator 실행
- 결과를 batch summary에 부가 artifact로 저장

### Medium Term

- `run_codex_benchmark.py` 후속 단계에서 evaluator lane hook 추가
- lane별 judge 결과를 trace에 연결
- disagreement analysis 자동 scaffold 생성

## Output Storage Recommendation

권장 출력 위치:

```text
artifacts/benchmark_runs/<batch_id>/<run_id>__<task_id>/evaluators/
  review_manifest.json
  review_result.json
  security_manifest.json
  security_result.json
  release_gate_manifest.json
  release_gate_result.json
  architecture_manifest.json
  architecture_result.json
```

이렇게 해야 batch review 시 lane별 evidence를 쉽게 참조할 수 있다.

## Operational Rule

evaluator runner는 구현 runner를 대체하지 않는다.  
항상 아래 순서를 따른다.

1. candidate execution
2. deterministic gates
3. artifact freeze
4. evaluator manifest build
5. evaluator execution
6. disagreement / calibration review if needed

이 순서를 깨면 evaluator가 incomplete artifact에 과도하게 의존하게 된다.
