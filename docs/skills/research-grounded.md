# Skill Spec: research-grounded

## Trigger Description Draft

외부 SDK, 플랫폼 정책, 공식 문서, 설계 옵션 비교가 구현 품질에 직접 영향을 줄 때 1차 출처 기반으로 근거를 정리하는 skill이다. 불확실성이 큰 complex-case에서만 on-demand로 사용한다.

## Core Workflow

1. 조사 질문을 하나의 명확한 쟁점으로 좁힌다
2. 공식 문서나 1차 출처를 우선 찾는다
3. 주장과 근거를 매핑한다
4. 구현에 필요한 제약과 불확실성을 별도로 적는다

## Output Contract

- 옵션 비교
- 추천안
- 근거 링크
- 남은 불확실성

## Likely Failure Modes

- `hallucinated_assumption`
- `insufficient_spec`
- `unsafe_dependency_change`

## Forward-Test Scenarios

- external SDK major upgrade
- platform policy change impact
- third-party auth flow redesign
