# Deep Validation Scorecard

## Scope

- batch label: `refined-skill-batch`
- artifact root: `artifacts/benchmark_runs/refined-skill-batch`

## Summary

- quality champion: `c2-execution-xhigh`
- minimum sufficient config: `None`

## Score Table

| Run | Tasks | Pass | Review High | Addl High | Review Medium | Addl Medium | Review Low | Addl Low | Avg Seconds | Token Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `c0-gpt54-high` | 1 | 0 | 1 | 1 | 1 | 0 | 0 | 0 | 335.788 | 6873839 |
| `c2-all-gpt54-high` | 1 | 0 | 0 | 2 | 0 | 2 | 0 | 0 | 321.019 | 5648925 |
| `c2-execution-xhigh` | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 514.858 | 8108605 |
| `c2-mini-triage-context` | 1 | 0 | 1 | 1 | 0 | 0 | 1 | 0 | 123.224 | 11724619 |

## Deep Evaluator Gaps

- `c0-gpt54-high`: additional evaluator findings `high=1`, `medium=0`, `low=0`
- `c2-all-gpt54-high`: additional evaluator findings `high=2`, `medium=2`, `low=0`
- `c2-execution-xhigh`: additional evaluator findings `high=1`, `medium=0`, `low=0`
- `c2-mini-triage-context`: additional evaluator findings `high=1`, `medium=0`, `low=0`

## Failure Taxonomy Notes

- `c2-mini-triage-context`: `timing_metadata_recovered`=1
