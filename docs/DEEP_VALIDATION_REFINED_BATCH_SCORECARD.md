# Deep Validation Scorecard

## Scope

- batch label: `refined-skill-batch`
- artifact root: `artifacts/benchmark_runs/refined-skill-batch`

## Summary

- quality champion: `c2-execution-xhigh`
- minimum sufficient config: `None`

주의:

- 이 `quality champion`은 refined batch의 모든 run이 fail인 상태에서 상대적으로만 계산된 값이다.
- promotion 관점에서는 champion으로 해석하면 안 된다.
- `c2-mini-triage-context__presence-race`는 `gate_results.json`, `review_findings.json`, `trace_record.json`가 없어 이번 deep-validation 집계에서 제외됐다.

## Score Table

| Run | Tasks | Pass | Review High | Addl High | Review Medium | Addl Medium | Review Low | Addl Low | Avg Seconds | Token Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `c0-gpt54-high` | 1 | 0 | 1 | 1 | 1 | 0 | 0 | 0 | 335.788 | 6873839 |
| `c2-all-gpt54-high` | 1 | 0 | 0 | 2 | 0 | 2 | 0 | 0 | 321.019 | 5648925 |
| `c2-execution-xhigh` | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 514.858 | 8108605 |

## Deep Evaluator Gaps

- `c0-gpt54-high`: additional evaluator findings `high=1`, `medium=0`, `low=0`
- `c2-all-gpt54-high`: additional evaluator findings `high=2`, `medium=2`, `low=0`
- `c2-execution-xhigh`: additional evaluator findings `high=1`, `medium=0`, `low=0`

## Failure Taxonomy Notes

- 없음
