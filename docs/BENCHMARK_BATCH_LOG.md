# Benchmark Batch Log

## Batch

- Current batch: `initial-complex-case-batch`

## Goal

- `C0`와 `C2`의 complex-case 품질 차이를 본다.
- `gpt-5.4`와 `gpt-5.4-mini`의 역할별 sufficiency 신호를 모은다.
- benchmark 결과를 바탕으로 다음 skill 수정 포인트를 도출한다.

## Recording Format

### Run

- run id: `c0-gpt54-medium`
- task id: `tenant-cache-scope`
- result: `pass`
- changed files: `app/cache_keys.py`, `app/project_summary_service.py`, `docs/caching.md`, `docs/multi-tenant-architecture.md`
- gate summary: `tests_pass=true`, `compile_pass=true`, `docs_sync_check=true`
- review summary: `high=0`, `medium=1`, `low=1`
- notes: 기능 수정과 문서 반영은 성공했지만 same-tenant cache-hit 회귀 테스트가 빠졌고, execution report의 근거 품질이 약했다.

- run id: `c2-mini-triage-context`
- task id: `tenant-cache-scope`
- result: `pass`
- changed files: `app/cache_keys.py`, `app/project_summary_service.py`, `docs/caching.md`, `docs/multi-tenant-architecture.md`, `tests/test_tenant_cache_scope.py`
- gate summary: `tests_pass=true`, `compile_pass=true`, `docs_sync_check=true`
- review summary: `high=0`, `medium=0`, `low=1`
- notes: triage를 `gpt-5.4-mini / medium`로 낮춰도 핵심 수정은 성공했다. 다만 execution report의 compile gate 서술이 실제 실행 결과와 어긋나는 low finding이 남았다.

- run id: `c2-all-gpt54-high`
- task id: `tenant-cache-scope`
- result: `pass`
- changed files: `app/cache_keys.py`, `app/project_summary_service.py`, `docs/caching.md`, `docs/multi-tenant-architecture.md`, `tests/test_tenant_cache_scope.py`
- gate summary: `tests_pass=true`, `compile_pass=true`, `docs_sync_check=true`
- review summary: `high=0`, `medium=0`, `low=0`
- notes: 첫 complex-case에서 가장 깨끗한 결과를 냈다. 품질 우선 기준의 현시점 선두 조합이다.

- run id: `c0-gpt54mini-high`
- task id: `tenant-cache-scope`
- result: `fail`
- changed files: `app/cache_keys.py`, `app/project_summary_service.py`, `docs/caching.md`, `docs/multi-tenant-architecture.md`, `tests/test_tenant_cache_scope.py`
- gate summary: `tests_pass=true`, `compile_pass=true`, `docs_sync_check=true`
- review summary: `high=1`, `medium=0`, `low=0`
- notes: `project-summary:{tenant_id}:{project_slug}` 형태의 단순 문자열 결합으로 구분자 충돌이 생겨 tenant isolation hole이 남았다. `gpt-5.4-mini / high` 단일 실행이 complex-case에서 겉보기 정답 뒤의 숨은 결함을 놓칠 수 있다는 신호다.

- run id: `c2-execution-xhigh`
- task id: `tenant-cache-scope`
- result: `pass`
- changed files: `app/cache_keys.py`, `app/project_summary_service.py`, `docs/caching.md`, `docs/multi-tenant-architecture.md`, `tests/test_tenant_cache_scope.py`
- gate summary: `tests_pass=true`, `compile_pass=true`, `docs_sync_check=true`
- review summary: `high=0`, `medium=0`, `low=0`
- notes: 첫 태스크 기준으로는 `c2-all-gpt54-high`와 동급 품질을 보였다. 토큰 총량은 더 낮아 `minimum sufficient` 후보로 우세하다.

- run id: `c0-gpt54-high`
- task id: `tenant-cache-scope`
- result: `pass`
- changed files: `app/cache_keys.py`, `app/project_summary_service.py`, `docs/caching.md`, `docs/multi-tenant-architecture.md`, `tests/test_tenant_cache_scope.py`
- gate summary: `tests_pass=true`, `compile_pass=true`, `docs_sync_check=true`
- review summary: `high=0`, `medium=1`, `low=1`
- notes: `medium` effort 대비 눈에 띄는 품질 개선이 없었다. same-tenant cache-hit 회귀 테스트 누락과 execution report 부정확성이 그대로 남았다.

- run id: `c2-all-gpt54-high`
- task id: `flag-rollout-fallback`
- result: `pass`
- changed files: `app/flags.py`, `app/telemetry.py`, `docs/feature_flags.md`, `ops/feature_rollout.md`, `tests/test_flag_rollout_fallback.py`
- gate summary: `tests_pass=true`, `compile_pass=true`, `docs_sync_check=true`
- review summary: `high=0`, `medium=1`, `low=0`
- notes: fail-closed와 중복 이벤트 제거는 맞췄지만 telemetry dedupe를 `(flag, user, variant)` 단위로 일반화하면서 “한 evaluation당 1건” 불변식을 완전히 강제하지 못했다.

- run id: `c2-execution-xhigh`
- task id: `flag-rollout-fallback`
- result: `pass`
- changed files: `app/flags.py`, `app/telemetry.py`, `docs/feature_flags.md`, `ops/feature_rollout.md`, `tests/test_flag_rollout_fallback.py`
- gate summary: `tests_pass=true`, `compile_pass=true`, `docs_sync_check=true`
- review summary: `high=0`, `medium=0`, `low=0`
- notes: `execution xhigh`는 과제를 넘는 일반화 없이 “한 evaluation당 1건”에 딱 맞는 수정으로 reviewer finding을 없앴다.

- run id: `c0-gpt54-high`
- task id: `flag-rollout-fallback`
- result: `pass`
- changed files: `app/flags.py`, `app/telemetry.py`, `docs/feature_flags.md`, `ops/feature_rollout.md`, `tests/test_flag_rollout_fallback.py`
- gate summary: `tests_pass=true`, `compile_pass=true`, `docs_sync_check=true`
- review summary: `high=0`, `medium=1`, `low=1`
- notes: 두 번째 태스크에서도 baseline single-pass는 disabled-by-config 경로 회귀 테스트를 놓쳤고 execution report 신뢰도가 떨어졌다.

- run id: `c2-mini-triage-context`
- task id: `flag-rollout-fallback`
- result: `pass`
- changed files: `app/flags.py`, `app/telemetry.py`, `docs/feature_flags.md`, `ops/feature_rollout.md`, `tests/test_flag_rollout_fallback.py`
- gate summary: `tests_pass=true`, `compile_pass=true`, `docs_sync_check=true`
- review summary: `high=0`, `medium=0`, `low=0`
- notes: 두 번째 태스크에서도 `triage/context = gpt-5.4-mini / medium` 조합이 무너지지 않았다. 현재까지는 mini를 triage/context에 내리는 것이 유효한 비용 절감 후보로 보인다.

### Observed Weaknesses

- execution coverage gap: `C0 / gpt-5.4 / medium`은 캐시 키 수정은 맞췄지만 same-tenant cache-hit 회귀 검증이 빠졌다.
- execution coverage gap: `C0 / gpt-5.4 / high`도 두 태스크 연속으로 회귀 테스트 보강이 얕았다. single-pass의 약점이 재현되고 있다.
- docs sync gap: 현재까지 완료된 다섯 run 모두 docs gate는 통과했다. `docs-sync` skill의 최소 효용은 확인됐다.
- review sensitivity gap: `gpt-5.4-mini / high` 단일 실행은 gate를 모두 통과하고도 독립 리뷰에서 `High` 결함이 잡혔다. complex-case에서는 review 분리가 필수라는 신호다.
- over-edit or noise: `c2-all-gpt54-high`는 telemetry를 더 일반화하다가 오히려 task invariant를 흐렸다. 범위를 넘는 일반화가 medium finding으로 이어질 수 있다.

### Next Skill Revision Candidates

- `execution-engineering`: 단순 문자열 조합 대신 delimiter collision까지 고려하도록 key-construction 검토 규칙을 강화하고, task invariant를 넘는 추상화를 경계하도록 문구를 보강할 필요가 있다.
- `review-findings`: 현재 독립 리뷰는 잘 작동하고 있다. 숨은 collision / ambiguity를 계속 집요하게 찾도록 유지한다.
- `quality-gates-runner`: gate 통과 여부뿐 아니라 execution report와 실제 gate 결과의 일치 여부를 체크하는 보조 검증을 고려한다.
- prompt asset changes: `C0` 계열 prompt에 “구분자 충돌, escaping, canonicalization” 같은 identifier composition 위험 점검 문구를 추가하고, `C2` execution prompt에는 “과제에 없는 일반화는 reviewer finding 원인이 될 수 있음”을 명시하는 것이 유효해 보인다.

## Refined Batch

### Skill / Prompt Changes Applied

- `skills/task-brief-author/SKILL.md`
  - invariant와 counterexample를 brief 단계에서 명시하도록 강화
- `skills/execution-engineering/SKILL.md`
  - task invariant 우선, 과도한 일반화 경계, collision/idempotency/stale/tie-case 점검, execution report fidelity 규칙 추가
- `agents/candidates/c0-solo.prompt.md`
  - edge case 탐지와 정확한 verification reporting 규칙 추가
- `agents/candidates/c2-execution.prompt.md`
  - task invariant 고정, broad abstraction 억제, edge-case 점검, report fidelity 규칙 추가

### Refined Run

- run id: `c2-all-gpt54-high`
- task id: `flag-rollout-fallback`
- result: `pass`
- changed files: `app/flags.py`, `app/telemetry.py`, `docs/feature_flags.md`, `ops/feature_rollout.md`, `tests/test_flag_rollout_fallback.py`
- gate summary: `tests_pass=true`, `compile_pass=true`, `docs_sync_check=true`
- review summary: `high=0`, `medium=0`, `low=0`
- notes: 초기 배치에서 남았던 telemetry dedupe 일반화 문제를 제거했다. refined skill/prompt의 실효성이 직접 확인된 run이다.

- run id: `c0-gpt54-high`
- task id: `tenant-cache-scope`
- result: `fail`
- changed files: `app/cache_keys.py`, `app/project_summary_service.py`, `docs/caching.md`, `docs/multi-tenant-architecture.md`, `tests/test_tenant_cache_scope.py`, `compileall.py`
- gate summary: `tests_pass=true`, `compile_pass=true`, `docs_sync_check=true`
- review summary: `high=1`, `medium=1`, `low=0`
- notes: single-pass는 강화 규칙을 잘못 흡수해 `compileall.py` shim으로 gate를 우회하는 부작용까지 만들었다. `C0` 계열은 complex-case 품질 보장용 기본 조합에서 제외해야 한다.

- run id: `c2-execution-xhigh`
- task id: `presence-race`
- result: `fail`
- changed files: `app/client_presence.py`, `app/presence_hub.py`, `app/session_store.py`, `docs/realtime_presence.md`, `tests/test_presence_race.py`
- gate summary: `tests_pass=true`, `compile_pass=true`, `docs_sync_check=true`
- review summary: `high=1`, `medium=0`, `low=0`
- notes: refined 규칙 아래서도 `xhigh`는 epoch memory를 잊는 과도한 state rewrite로 stale reconnect 회귀를 만들었다. `execution xhigh`는 기본값으로 두지 않는다.

- run id: `c2-mini-triage-context`
- task id: `presence-race`
- result: `cancelled`
- changed files: partial only
- gate summary: not recorded
- review summary: not recorded
- notes: broad sweep와 refined 결과만으로 최종 추천을 결정하기에 충분해 선택적 추가 검증 run은 중단했다. 후속 배치에서 이어서 돌릴 수 있다.
