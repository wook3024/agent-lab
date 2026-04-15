# Model Effort Benchmark Plan

## Goal

`gpt-5.4`와 `gpt-5.4-mini`를 다양한 `reasoning effort` 조합으로 비교해, 복잡한 제품 개발 작업에서:

- 어느 역할에 어느 정도 추론 깊이가 필요한지
- `mini`가 충분한 역할과 충분하지 않은 역할이 무엇인지
- 품질 향상에 비해 과도한 비용과 지연을 유발하는 조합이 무엇인지

를 파악한다.

이 계획은 단순 응답 품질이 아니라 `complex-case golden set` 기준의 실제 개발 품질을 평가한다.

## Official Guidance Incorporated

공식 OpenAI 문서에서 반영한 원칙은 아래와 같다.

- reasoning effort는 품질을 올리는 주 수단이 아니라 `last-mile tuning knob`로 다룬다.
- `xhigh`는 기본값으로 두지 않고 eval에서 분명한 이득이 있을 때만 유지한다.
- `gpt-5.4-mini`는 빠른 분류/라우팅/경량 컨텍스트 정리에 유리할 수 있다.
- 복잡한 작업에서는 단순히 모델명만 바꾸지 말고 prompt/contract/verification loop를 함께 본다.

참고:

- https://developers.openai.com/api/docs/guides/prompt-guidance#treat-reasoning-effort-as-a-last-mile-knob
- https://developers.openai.com/tracks/building-agents#how-to-choose
- https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_troubleshooting_guide#overthinking
- https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_troubleshooting_guide#laziness--underthinking

## What We Are Measuring

### Primary Metrics

- complex-case success rate
- deterministic gate pass rate
- `High` review finding rate
- rework rate
- docs sync success rate

### Secondary Metrics

- failure taxonomy distribution
- average latency
- average model cost
- human intervention frequency

### Role-Specific Sufficiency

각 역할마다 아래 질문에 답할 수 있어야 한다.

- `Triage`는 `mini`로도 충분한가
- `Context`는 `mini` + 낮은 effort에서 잘 버티는가
- `Execution`은 언제 `gpt-5.4`가 반드시 필요한가
- `Review`는 `mini`로 돌리면 결함 탐지력이 얼마나 떨어지는가

## Experiment Design Principles

### 1. Do Not Confound Skill And Model Changes

- 같은 실험군에서는 skill과 role contract를 고정한다
- 한 번에 바꾸는 변수는 `model`, `effort`, 또는 `role allocation` 중 하나만 허용한다

### 2. Complex Cases Only

- 기본 평가 대상은 [complex-case-golden-set](/Users/shinukyi/Gallary/projects/proto/agent-lab/evals/complex-case-golden-set/INDEX.md:1)이다
- simple smoke set은 보조 지표로만 사용한다

### 3. Start Narrow, Then Expand

- 전 조합 full factorial로 시작하지 않는다
- 먼저 baseline과 boundary를 잡고, 그 다음 role-specific sweep으로 들어간다

### 4. Compare Equal Structure First

- 먼저 같은 candidate 구조 안에서 model/effort 차이를 본다
- 그 다음 candidate 구조 차이와 상호작용을 본다

## Phase Plan

### Phase 0. Prompt And Contract Freeze

목적:

- reasoning effort 실험 전에 prompt/skill/output contract를 먼저 고정한다

규칙:

- `Task Brief`, `Context Pack`, `Review Findings`, `Gate` 구조를 고정
- skill 문구는 이 phase 이후 변경하지 않는다
- 변경이 필요하면 새 benchmark batch를 만든다

### Phase 1. Single-Role Baseline Sweep

대상:

- `C0` only

목적:

- 구조를 고정한 상태에서 단일 에이전트의 model/effort 민감도를 파악

실험군:

1. `gpt-5.4 / low`
2. `gpt-5.4 / medium`
3. `gpt-5.4 / high`
4. `gpt-5.4 / xhigh`
5. `gpt-5.4-mini / low`
6. `gpt-5.4-mini / medium`
7. `gpt-5.4-mini / high`
8. `gpt-5.4-mini / xhigh`

평가 세트:

- complex-case 6개부터 시작
- 결함 분포를 본 뒤 10개 전체로 확장

목적 결과:

- 단일 에이전트에서 `mini`가 복잡한 구현에 어느 정도까지 버티는지 확인
- `xhigh`가 실제로 의미 있는지 확인

### Phase 2. Controlled Dual-Pass Equal-Model Sweep

대상:

- `C2` only

목적:

- role 분리가 있을 때 effort를 전반적으로 얼마나 낮출 수 있는지 확인

실험군:

1. all roles `gpt-5.4 / medium`
2. all roles `gpt-5.4 / high`
3. all roles `gpt-5.4-mini / medium`
4. all roles `gpt-5.4-mini / high`

주의:

- 여기서는 role별 모델 혼합을 하지 않는다
- 먼저 구조 자체가 model family에 얼마나 민감한지 본다

### Phase 3. Role-Specific Effort Sweep

대상:

- `C2` only

목적:

- 어떤 역할이 진짜 비싼 모델/높은 effort를 먹는지 분해해서 확인

기본 anchor:

- `Triage / Context / Review = gpt-5.4 / high`
- `Execution = gpt-5.4 / xhigh`

이 anchor에서 아래 축을 하나씩 흔든다.

#### 3A. Triage And Context Downshift

- `Triage / Context = gpt-5.4-mini / low`
- `Triage / Context = gpt-5.4-mini / medium`
- `Triage / Context = gpt-5.4 / low`

고정:

- `Execution = gpt-5.4 / xhigh`
- `Review = gpt-5.4 / high`

검증 질문:

- context quality가 떨어져 `wrong_context`가 늘어나는가

#### 3B. Execution Downshift

- `Execution = gpt-5.4 / high`
- `Execution = gpt-5.4 / medium`
- `Execution = gpt-5.4-mini / xhigh`
- `Execution = gpt-5.4-mini / high`

고정:

- `Triage / Context / Review = gpt-5.4 / high`

검증 질문:

- execution에서 `mini`가 `shallow_fix`, `missed_test`, `over_edit`를 늘리는가
- `xhigh`가 `high` 대비 실제 quality gain을 내는가

#### 3C. Review Downshift

- `Review = gpt-5.4 / medium`
- `Review = gpt-5.4-mini / high`
- `Review = gpt-5.4-mini / medium`

고정:

- `Triage / Context = gpt-5.4 / high`
- `Execution = gpt-5.4 / xhigh`

검증 질문:

- review에서 `mini`가 `High` severity 검출률을 얼마나 떨어뜨리는가

### Phase 4. Minimum Sufficient Configuration Search

목적:

- 품질 기준을 만족하는 가장 저렴한 조합을 찾는다

탐색 방식:

1. `quality-first champion`을 고른다
2. 한 역할씩 더 저렴한 모델/effort로 낮춘다
3. 품질 기준이 무너지면 바로 직전 조합을 minimum sufficient config로 기록한다

## Initial Recommended Matrix

초기 실행은 아래 6개 조합으로 시작한다.

### C0 Baseline Set

1. `C0 / gpt-5.4 / medium`
2. `C0 / gpt-5.4 / high`
3. `C0 / gpt-5.4-mini / high`

### C2 Baseline Set

4. `C2 / all roles gpt-5.4 / high`
5. `C2 / triage-context-review=gpt-5.4/high, execution=gpt-5.4/xhigh`
6. `C2 / triage-context=gpt-5.4-mini/medium, execution=gpt-5.4/xhigh, review=gpt-5.4/high`

이 6개면 아래를 먼저 볼 수 있다.

- 구조 개선 효과: `C0` vs `C2`
- 동일 모델군에서 effort 상승 효과
- `mini`가 triage/context에서 충분한지
- execution에서 `xhigh`가 worth it인지 탐색할 출발점

## Pass / Fail Interpretation

### Model Or Effort Is Not Sufficient If

- `High` review finding rate가 기준 조합보다 분명히 높다
- `wrong_context`, `missed_test`, `over_edit`, `docs_desync`가 증가한다
- gate pass rate가 떨어진다

### Model Or Effort Is Over-Provisioned If

- 품질 차이는 미미한데 latency/cost만 크게 증가한다
- `xhigh`가 `high` 대비 복잡한 케이스에서 유의미한 이득이 없다

### Mini Is Considered Sufficient For A Role If

- 해당 역할을 `mini`로 내려도 primary metrics가 거의 유지된다
- failure taxonomy가 role-specific으로 악화되지 않는다

## Recording Format

각 run은 아래 필드를 함께 남긴다.

- candidate id
- role-to-model mapping
- role-to-effort mapping
- task ids
- gate results
- review severity totals
- failure taxonomy totals
- elapsed time
- estimated cost

기록은 기존 [TRACE_RECORD_TEMPLATE.json](/Users/shinukyi/Gallary/projects/proto/agent-lab/docs/templates/TRACE_RECORD_TEMPLATE.json:1)와 [SCORECARD_TEMPLATE.md](/Users/shinukyi/Gallary/projects/proto/agent-lab/docs/templates/SCORECARD_TEMPLATE.md:1)를 확장해서 사용한다.

## Decision Output

최종적으로는 아래 3개를 도출해야 한다.

1. `quality champion`
- 복잡한 케이스 품질이 가장 높은 조합

2. `minimum sufficient config`
- 품질 기준을 만족하는 가장 저렴한 조합

3. `role routing policy`
- 어떤 역할은 `mini`로 충분하고 어떤 역할은 `gpt-5.4` 이상이 필요한지에 대한 운영 규칙
