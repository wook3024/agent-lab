# Candidate C0: Codex Solo

## Summary

단일 실행 에이전트가 task brief, context pack, 검증 기준을 모두 받아 한 번에 구현까지 수행하는 baseline 후보다.

## Purpose

가장 단순한 운영 구조가 복잡한 케이스에서 어디까지 버티는지 확인하는 비교 기준점으로 사용한다.

## Workflow

1. task brief 입력
2. context pack 입력
3. 단일 execution pass 수행
4. deterministic gate 실행
5. 별도 review pass 수행

## Required Inputs

- [TASK_BRIEF_TEMPLATE.md](/Users/shinukyi/Gallary/projects/proto/agent-lab/docs/templates/TASK_BRIEF_TEMPLATE.md:1) 기반 작업 브리프
- [CONTEXT_PACK_TEMPLATE.md](/Users/shinukyi/Gallary/projects/proto/agent-lab/docs/templates/CONTEXT_PACK_TEMPLATE.md:1) 기반 컨텍스트 팩
- gate 목록
- review 형식

## Strengths

- 운영 오버헤드가 가장 낮다
- handoff failure가 없다
- trace가 단순해서 baseline 분석이 쉽다

## Expected Weaknesses

- 복잡한 케이스에서 범위 통제가 약해질 수 있다
- 잘못된 초기 가정을 스스로 교정하기 어렵다
- 구현과 검토가 심리적으로 덜 분리된다
- docs sync와 test 보강 누락 가능성이 있다

## Pass Criteria

- complex-case golden set에서 baseline reference로 점수 측정
- `High` review finding 비율과 `missed_test`, `over_edit`, `wrong_context` 추세 확인

## Kill Criteria

- `C2` 대비 gate pass rate, review high finding rate, docs sync success rate가 유의미하게 나쁘면 baseline으로만 유지하고 승격하지 않는다
