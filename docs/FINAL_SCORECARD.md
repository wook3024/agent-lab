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
  - `c2-mini-triage-context` on `presence-race` (artifact recovery + deep-validation backfill)

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
| `c2-mini-triage-context` | 1 | 0 | 1 | 0 | 1 | 123.224 | 11724619 | stale reconnect ordering bug와 report fidelity mismatch가 함께 드러났고, candidate timing은 artifact recovery로만 복구됨 |

## Decisions

- Broad-sweep champion: `c2-mini-triage-context`
- Refined high-confidence champion: `c2-all-gpt54-high`
- Do not promote:
  - `C0` family for complex-case work
  - `execution = xhigh` as the default
  - `mini triage/context` as a promoted default until the refined rerun regression is fixed

## Deep Validation Overlay

`refined-skill-batch`에 additional evaluator lane를 붙인 뒤 결과는 더 보수적으로 바뀌었다.

| Run | Review High | Addl High | Review Medium | Addl Medium | Pass | Interpretation |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `c0-gpt54-high` | 1 | 1 | 1 | 0 | 0 | code quality와 security 모두 승격 불가 |
| `c2-all-gpt54-high` | 0 | 2 | 0 | 2 | 0 | 구현 품질은 가장 안정적이지만 release/approval artifact 부족으로 governance 승격 불가 |
| `c2-execution-xhigh` | 1 | 1 | 0 | 0 | 0 | code correctness와 architecture 모두 승격 불가 |
| `c2-mini-triage-context` | 1 | 1 | 0 | 0 | 0 | refined rerun에서도 stale reconnect ordering bug와 architecture boundary 문제를 함께 남겨 승격 불가 |

보수적으로 보면, deep validation 기준 refined batch에서는 `minimum sufficient config`가 아직 없다.  
즉 현재 상태는 “기본 engineering default 추천”은 가능하지만, “governance까지 포함한 fully promoted default”는 아직 미확정이다.

## Interpretation Update

- `c2-mini-triage-context`는 broad sweep에서 가장 효율적인 조합이었지만, refined confirmatory rerun에서는 같은 `presence-race` 계열 복잡 케이스를 안정적으로 통과하지 못했다.
- 이 run은 execution artifact는 성공적으로 남겼지만 executor가 정상 종료하지 않아 candidate wall-clock timing은 recover-only 상태로 집계했다.
- 따라서 현재 시점의 mini downshift는 “흥미로운 비용 절감 가설”이지, standard나 pilot 승격 후보는 아니다.
