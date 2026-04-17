# CTO Required Agent And Skill Assessment

## 목적

이 문서는 현재 `agent-lab`에서 설계하고 검증한 에이전트, 스킬, 조합을 CTO 관점에서 다시 평가해:

- 무엇이 실제 조직 운영에 필수인지
- 무엇이 품질 향상에는 유효하지만 조건부인지
- 무엇이 과하게 세분화되어 통합하거나 후순위로 내려도 되는지
- 현재 자산에 무엇이 빠져 있는지

를 명확히 정리하기 위한 판단 문서다.

이 문서의 평가는 “프롬프트가 흥미로운가”가 아니라 아래 기준을 따른다.

- 조직 전체에 반복 적용 가능한가
- 복잡한 개발 작업의 실패율을 줄이는가
- 승인, 보안, 배포, 비용 통제를 돕는가
- trace와 gate를 통해 감사 가능성이 확보되는가
- 사람 수가 늘어나도 운영 모델이 유지되는가

## Executive Verdict

결론부터 말하면, 현재 자산 중 CTO 관점에서 정말 가치가 큰 것은 “스킬 개수”가 아니라 아래 구조다.

`Triage -> Context -> Execution -> Deterministic Gates -> Independent Review`

즉, 현재 프로젝트의 핵심 가치는 개별 스킬을 많이 만든 것보다:

- 작업을 시작하기 전에 범위를 고정하고
- 필요한 컨텍스트만 좁혀서 제공하고
- 구현 후 gate를 강제하고
- 독립 리뷰를 통해 숨은 결함을 발견하고
- 그 결과를 trace로 비교 가능하게 만든

운영 구조 자체에 있다.

이 구조는 CTO 관점에서 의미가 있다. 이유는 아래와 같다.

1. 개발 품질 향상을 “개인의 실력”이나 “좋은 프롬프트”에 덜 의존하게 만든다.
2. 회귀, 과도한 변경, 테스트 누락, 문서 드리프트를 조직 차원에서 줄일 수 있다.
3. 감사 가능성과 재현성이 생겨, 특정 성공 사례를 팀 표준으로 승격할 수 있다.

반대로, 현재 스킬 세트 전체가 모두 필수인 것은 아니다.  
CTO 관점에서는 `C2 구조 + gates + trace + independent review`가 핵심이고, 나머지는 이 구조를 더 잘 작동하게 만드는 보조 장치로 봐야 한다.

## 평가 원칙

### 필수로 간주하는 조건

- complex-case 품질에 직접적인 영향이 있다
- 여러 팀/서비스에 공통 적용 가능하다
- failure taxonomy와 연결되어 효과를 측정할 수 있다
- 조직 운영 리스크를 줄인다

### 조건부로 간주하는 조건

- 특정 작업 유형에서만 가치가 크다
- baseline 품질 구조 위에 붙었을 때만 효과가 난다
- 조직의 성숙도에 따라 우선순위가 달라진다

### 통합 또는 후순위로 보는 조건

- 다른 스킬의 하위 규칙으로 흡수 가능하다
- 운영 복잡도를 늘리지만 품질 증분이 작다
- CTO가 직접 챙겨야 할 control-plane 가치가 약하다

## CTO 기준 분류

### 1. Must Have

조직 수준에서 바로 표준화할 가치가 있는 항목들이다.

| 항목 | 현재 상태 | CTO 판단 | 이유 |
| --- | --- | --- | --- |
| `C2` agent topology | 검증 완료 | 반드시 유지 | 현재 자산 중 가장 가치가 큰 운영 구조. 범위 통제, 검증, 독립 리뷰, 재작업 감축에 직접 기여 |
| `Triage Agent` | 정의 완료 | 필수 | 잘못된 목표와 과도한 범위 확장을 초기 단계에서 막음 |
| `Execution Agent` | 정의 완료 | 필수 | 구현, 테스트, 문서 반영을 하나의 실행 계약으로 묶는 핵심 역할 |
| `Review Agent` | 정의 완료 | 필수 | gate를 통과한 숨은 결함을 찾는 마지막 방어선 |
| `task-brief-author` | 구현 완료 | 필수 | complex-case에서 goal, non-goals, invariants를 명시해 scope creep를 줄임 |
| `context-pack-builder` | 구현 완료 | 필수 | broad context dump를 막고 wrong-context 확률을 줄임 |
| `execution-engineering` | 구현 완료 | 필수 | shallow fix, over-edit, missed test 방지에 직결 |
| `quality-gates-runner` | 구현 완료 | 필수 | 품질을 subjective judgment가 아니라 deterministic verification으로 고정 |
| `trace-eval-recorder` | 구현 완료 | 필수 | 어떤 조합이 실제로 좋았는지 조직적으로 비교 가능하게 만듦 |

#### CTO 코멘트

이 범주는 “없으면 품질 체계가 붕괴하는 것들”이다.  
특히 `quality-gates-runner`와 `trace-eval-recorder`는 단순 개발 지원 스킬이 아니라, CTO 입장에서 운영을 통제 가능한 체계로 만드는 핵심 control plane이다.

### 2. Strongly Recommended

필수 바로 아래 단계지만, complex-case 중심 조직이라면 사실상 거의 필수로 보는 것이 맞다.

| 항목 | 현재 상태 | CTO 판단 | 이유 |
| --- | --- | --- | --- |
| `docs-sync` | 구현 완료 | 강하게 권장 | 코드만 맞고 문서/런북이 틀리는 조직 문제를 줄임 |
| reviewer-first severity contract | 적용 중 | 강하게 권장 | 리뷰가 구현 요약으로 흐르지 않게 만드는 운영 계약 |
| role-specific model routing | 부분 검증 | 강하게 권장 | 모든 역할에 같은 모델/effort를 고정하는 것보다 비용 통제에 유리 |
| `C2 + all gpt-5.4/high` default | 검증 완료 | 강하게 권장 | 현재 기준 최고 품질 기본값 |

#### CTO 코멘트

이 범주는 “조직에서 실제로 사고를 줄이는 운영 습관”에 가깝다.  
`docs-sync`는 개발자 입장에서는 부가 작업처럼 보일 수 있지만, CTO 관점에서는 운영 비용과 onboarding 비용을 줄이는 데 매우 중요하다.

### 3. Conditional

특정 조건에서만 우선순위가 올라가는 항목들이다.

| 항목 | 현재 상태 | CTO 판단 | 언제 필요한가 |
| --- | --- | --- | --- |
| `research-grounded` | 구현 완료 | 조건부 | 외부 SDK, 정책, 프로토콜, 플랫폼 제약 해석이 핵심일 때 |
| `gpt-5.4-mini` on triage/context | broad sweep 유망 | 조건부 승격 | refined 기준 추가 검증 후 비용 최적화 대상으로 활용 가능 |
| task-type expansion beyond bugfix | 계획 단계 | 조건부 | feature implementation, migration, ops sync까지 확장할 때 |
| `C3` research-assisted execution | 설계만 존재 | 조건부 | local repo context만으로는 안전한 의사결정이 어려운 경우 |
| `C4` managed multi-agent | 설계만 존재 | 조건부 | write set이 분리 가능하고 병렬화 이득이 분명할 때 |

#### CTO 코멘트

이 범주는 “좋은 옵션이지만 baseline이 아니다.”  
특히 `research-grounded`는 매우 유용하지만, 모든 작업에 강제로 넣으면 속도만 떨어뜨리고 조직 전체의 latency를 키울 수 있다.

### 4. Merge Or Deprioritize Candidates

현재 자산이 나쁘다는 뜻은 아니지만, CTO 시선에서는 별도 핵심 축으로 과하게 관리할 필요가 없는 것들이다.

| 항목 | 현재 상태 | CTO 판단 | 이유 |
| --- | --- | --- | --- |
| `review-findings`를 별도 “전략 축”으로 강조 | 구현 완료 | 통합 대상 | 중요하지만 결국 Review Agent의 출력 계약으로 이해하면 충분 |
| `context-pack-builder`와 `task-brief-author`의 운영 문서 분리 | 구현 완료 | 향후 통합 가능 | 체계가 성숙하면 하나의 `planning contract`로 묶을 수 있음 |
| `docs-sync`를 독립 role처럼 확대 | 구현 완료 | role 분리는 불필요 | skill로는 유효하지만 별도 agent까지 분화할 가치는 아직 낮음 |
| `C0` family | 검증 완료 | baseline only | complex-case production default로는 부적합 |
| `execution = xhigh` default | 검증 완료 | 사용 금지 | 품질 상승보다 over-design과 숨은 회귀 가능성이 큼 |

#### CTO 코멘트

현재 구조에서 스킬 수를 더 늘리는 방향은 조심해야 한다.  
CTO 관점에서는 “분화된 skill catalog”보다 “정말 팀 품질을 움직이는 control point가 무엇인가”가 더 중요하다.

## 현재 자산의 가장 큰 강점

### 1. Prompt가 아니라 운영 계약을 만든 점

많은 AI 도입 시도가 결국 “좋은 프롬프트 만들기”에 머무르는데, 현재 프로젝트는:

- task brief
- context pack
- deterministic gates
- independent review
- trace

로 이어지는 운영 계약을 만들었다.

이건 CTO 관점에서 매우 중요하다.  
사람이 바뀌어도 반복 가능하고, 실패를 비교 가능하게 만들기 때문이다.

### 2. Complex-case에 초점을 맞춘 점

현재 benchmark는:

- cache scope
- flag rollout fallback
- presence race
- tenant isolation
- retry / idempotency
- doc sync

같은 “실제 운영 사고로 이어질 수 있는 문제”를 다룬다.

CTO는 보통 간단한 문서 수정 품질보다 이런 complex-case에서의 안정성을 본다.  
그 점에서 현재 방향은 옳다.

### 3. `mini`와 `xhigh`를 감으로 쓰지 않은 점

model/effort를 “좋아 보이는 느낌”이 아니라:

- broad sweep
- refined batch
- role별 sufficiency

관점으로 평가한 것은 매우 좋은 접근이다.

## 현재 자산의 가장 큰 부족함

현재 체계는 “코드 품질 향상용 시스템”으로는 상당히 좋다.  
하지만 CTO가 진짜 조직 운영에서 필요로 하는 항목은 아직 일부 비어 있다.

### 1. Release Gate / Approval Control 이 부족하다

현재 문서와 자산은 구현 품질에는 강하지만, 아래 같은 고위험 작업 통제는 아직 약하다.

- 배포 승인
- 데이터 마이그레이션 승인
- 권한/결제/보안 설정 변경
- 롤백 준비 상태 확인
- 변경 위험도에 따른 사람 승인 escalation

이건 CTO 관점에서 반드시 필요한 영역이다.

### 2. Security / Compliance Review 축이 없다

현재 `Review Agent`는 일반 결함 탐지에는 유효하지만, 별도의 보안/정책/컴플라이언스 관점은 아직 약하다.

예를 들면 아래는 분리된 reviewer가 필요할 수 있다.

- auth / RBAC
- data exposure
- secrets handling
- audit logging
- vendor / policy compliance

### 3. Cost / Latency / SLA 운영 지표가 약하다

현재는 token total과 average seconds를 보고 있지만, CTO 관점에서는 아래 수준으로 더 올라가야 한다.

- task type별 평균 처리 시간
- 실패 후 재작업 비용
- 사람 개입 빈도
- 팀별 월간 비용 추정
- 품질 대비 비용의 break-even point

즉, 지금은 benchmark 지표는 좋지만, 운영 재무 관점의 관측성은 아직 약하다.

### 4. Ownership-aware routing 이 없다

실제 조직에서는 코드 복잡도만큼 중요한 것이 “누가 이 변경에 책임을 지는가”다.

현재 시스템에는 아직 아래 개념이 없다.

- 서비스 오너별 승인 경로
- 팀/도메인별 reviewer routing
- critical path 서비스에 대한 stricter gate
- 변경 영향도에 따른 triage escalation

이건 CTO가 실제 조직에 붙일 때 매우 중요하다.

## CTO 기준으로 다시 정리한 추천 구조

### Core Operating Plane

조직 기본값은 아래 정도로 압축하는 것이 좋다.

1. `Triage`
2. `Context`
3. `Execution`
4. `Deterministic Gates`
5. `Independent Review`
6. `Trace + Scorecard`

즉, 현재 프로젝트에서는 아래가 핵심 세트다.

- agent:
  - `Triage Agent`
  - `Execution Agent`
  - `Review Agent`
- skill:
  - `task-brief-author`
  - `context-pack-builder`
  - `execution-engineering`
  - `quality-gates-runner`
  - `trace-eval-recorder`
- supporting:
  - `docs-sync`

### Conditional Extensions

상황에 따라 붙이는 확장 세트는 아래 정도가 적절하다.

1. `research-grounded`
2. security-focused review
3. release gate
4. ownership-aware routing
5. cost policy layer

## 지금 당장 CTO 관점에서 추가해야 할 것

현재 프로젝트를 “좋은 agent benchmark 저장소”에서 “조직용 AI 개발 운영 시스템”으로 끌어올리려면, 다음 4개를 우선 추가하는 것이 좋다.

### 1. Release Gate Agent

역할:

- 배포 전 최종 체크리스트 검증
- rollback readiness 확인
- 승인 대상 변경 탐지
- release blocker 식별

### 2. Security Review Skill Or Agent

역할:

- auth / permission / data exposure / secret handling 집중 검토
- 일반 리뷰와 분리된 보안 severity 부여

### 3. Approval Policy Skill

역할:

- 작업 유형별 승인 필요 여부 판정
- destructive / irreversible / risky write detection
- 사람 개입 조건 명시

### 4. Cost Governance Trace Layer

역할:

- role별 token/cost/latency 추적
- task type별 처리 효율성 비교
- minimum sufficient config를 운영 정책으로 내리기 위한 근거 제공

## 최종 판단

### Yes

CTO 입장에서 현재 프로젝트는 충분히 의미 있다.  
특히 아래는 실제 조직에 도입할 가치가 있다.

- `C2` 운영 구조
- independent review 강제
- deterministic gate
- trace 기반 비교
- role별 model/effort sufficiency 사고방식

### But

현재 상태를 그대로 “최종 CTO 운영 패키지”라고 부르기에는 아직 부족하다.  
이유는 아래 때문이다.

- release/approval/security/cost governance가 아직 약하다
- 몇몇 skill은 독립 자산으로 유지하기보다 control-plane 안으로 재정리하는 편이 낫다
- complex-case engineering quality는 잡았지만, 조직 운영 품질까지는 아직 완성되지 않았다

## Bottom Line

가장 중요한 결론은 단순하다.

1. 지금 프로젝트의 핵심 자산은 “많은 skill”이 아니라 `C2 + gates + trace + independent review`다.
2. CTO 입장에서는 이 core를 유지해야 한다.
3. 다음 투자 우선순위는 새로운 구현 skill이 아니라 `release`, `approval`, `security`, `cost governance`다.
4. 따라서 현재 자산은 “좋은 실험 세트”를 넘어 “유효한 조직 운영 baseline”까지는 왔지만, “CTO-grade operating system”이 되려면 control-plane을 더 보강해야 한다.
