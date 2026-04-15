# Final Scorecard

## Scope

- Initial broad sweep:
  - `tenant-cache-scope`
  - `flag-rollout-fallback`
  - `presence-race`
- Refined confirmatory batch:
  - `c0-gpt54-high` on `tenant-cache-scope`
  - `c2-all-gpt54-high` on `flag-rollout-fallback`
  - `c2-execution-xhigh` on `presence-race`

## Initial Broad Sweep

| Run | Tasks | Pass | High | Medium | Low | Avg Seconds | Token Total | Notes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `c0-gpt54-high` | 2 | 2 | 0 | 2 | 2 | 246.757 | 6461855 | single-pass baseline, recurring coverage/reporting weakness |
| `c0-gpt54-medium` | 1 | 1 | 0 | 1 | 1 | 0.0 | 2558332 | baseline anchor only |
| `c0-gpt54mini-high` | 1 | 0 | 1 | 0 | 0 | 0.0 | 4082590 | hidden cache-key collision missed |
| `c2-all-gpt54-high` | 3 | 3 | 0 | 1 | 0 | 236.132 | 13446549 | strong but one over-generalized telemetry fix |
| `c2-execution-xhigh` | 3 | 3 | 0 | 1 | 0 | 271.113 | 13017144 | sometimes better, sometimes over-designed |
| `c2-mini-triage-context` | 3 | 3 | 0 | 0 | 1 | 230.630 | 11533738 | broad-sweep champion; fastest among robust configs |

## Refined Confirmatory Batch

| Run | Tasks | Pass | High | Medium | Low | Avg Seconds | Token Total | Notes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `c0-gpt54-high` | 1 | 0 | 1 | 1 | 0 | 335.788 | 4934566 | degraded; introduced gate-bypassing shim |
| `c2-all-gpt54-high` | 1 | 1 | 0 | 0 | 0 | 321.019 | 4617605 | refined skill/prompt fixed prior weakness |
| `c2-execution-xhigh` | 1 | 0 | 1 | 0 | 0 | 514.858 | 6601953 | degraded on ordering/state-retention case |

## Decisions

- Broad-sweep champion: `c2-mini-triage-context`
- Refined high-confidence champion: `c2-all-gpt54-high`
- Do not promote:
  - `C0` family for complex-case work
  - `execution = xhigh` as the default
