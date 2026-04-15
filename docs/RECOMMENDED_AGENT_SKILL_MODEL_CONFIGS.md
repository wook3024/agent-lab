# Recommended Agent, Skill, And Model Configs

## Final Recommendation

복잡한 제품 개발 작업에서 현재 가장 안전하게 승격할 수 있는 기본 조합은 아래다.

- Agent topology: `C2`
  - `Triage/Context -> Execution -> Deterministic Gates -> Independent Review`
- Skill bundle:
  - `task-brief-author`
  - `context-pack-builder`
  - `execution-engineering`
  - `quality-gates-runner`
  - `docs-sync`
  - `review-findings`
  - `trace-eval-recorder`
  - optional: `research-grounded`

## Best Validated Default

- `Triage/Context = gpt-5.4 / high`
- `Execution = gpt-5.4 / high`
- `Review = gpt-5.4 / high`

이 조합은 refined batch에서 이전 약점 케이스(`flag-rollout-fallback`)를 `0 finding`으로 통과했다. 현재 기준으로는 “최고 품질을 가장 보수적으로 보장하는” 설정이다.

## Best Efficiency Candidate

- `Triage/Context = gpt-5.4-mini / medium`
- `Execution = gpt-5.4 / xhigh`
- `Review = gpt-5.4 / high`

이 조합은 initial broad sweep 3개 complex-case에서:

- `high=0`
- `medium=0`
- `low=1`
- 가장 낮은 총 토큰
- robust config 중 가장 빠른 평균 wall time

을 보였다.

다만 refined skill/prompt를 적용한 confirmatory rerun은 완료하지 않았으므로, production default로 승격하기 전에는 같은 refined 기준으로 1개 batch를 더 확인하는 것이 좋다.

## Role Routing Policy

- `Triage/Context`
  - 우선 `gpt-5.4-mini / medium` 후보를 고려한다.
  - task brief와 context pack이 안정적으로 생성되고 reviewer finding이 늘지 않는 한, 이 역할에는 mini를 적극 활용할 수 있다.
- `Execution`
  - 기본값은 `gpt-5.4 / high`
  - `xhigh`는 default로 두지 않는다.
  - ordering, cache scope, reconnect, state retention처럼 설계 공간이 넓은 문제에서는 `xhigh`가 오히려 과도한 일반화와 숨은 회귀를 만들 수 있다.
- `Review`
  - 기본값은 `gpt-5.4 / high`
  - complex-case에서는 독립 review를 절대 생략하지 않는다.

## Configs To Avoid

- `C0` family
  - `gpt-5.4 / high`도 두 태스크 연속 `medium/low`를 남겼고, refined batch에서는 gate-bypassing shim까지 추가하며 `High`로 악화됐다.
  - `gpt-5.4-mini / high`는 첫 태스크에서 바로 `High` 결함을 놓쳤다.
- `Execution = gpt-5.4 / xhigh` as default
  - initial batch에서는 태스크에 따라 품질 향상이 있었지만,
  - refined batch에서는 `presence-race`에서 stale reconnect 회귀를 만들어 `High` finding이 발생했다.

## Why The Winning Shape Works

- `dual-pass`는 single-pass보다 scope 제어와 reviewer handoff가 좋다.
- invariant를 brief에 먼저 고정하면 execution이 task 밖으로 새는 것을 줄일 수 있다.
- 독립 review가 있어야 gate를 통과한 숨은 결함을 계속 잡아낼 수 있다.
- docs sync와 deterministic gate를 분리한 것이 complex-case에서 안정적으로 작동했다.

## Skill Changes That Should Be Kept

- `task-brief-author`
  - invariant와 counterexample를 brief에 명시
- `execution-engineering`
  - task-scoped fix 우선
  - collision/idempotency/stale/tie-case 점검
  - execution report fidelity 규칙
- candidate prompts
  - broad abstraction 억제
  - invariant-first execution 고정

## Next Batch

- refined 기준으로 `c2-mini-triage-context`를 2~3개 complex-case에 재검증
- `Execution = gpt-5.4 / high` + `Triage/Context = gpt-5.4-mini / medium` 조합을 직접 측정
- task type을 bugfix 밖으로 넓혀:
  - test-hardening
  - docs+ops sync
  - feature implementation
  - migration / rollout

현재 시점의 결론은 단순하다.

- 최고 품질 보장 default: `C2 + all gpt-5.4/high`
- 비용 효율 최우선 승격 후보: `C2 + mini triage/context + gpt-5.4 execution/review`
