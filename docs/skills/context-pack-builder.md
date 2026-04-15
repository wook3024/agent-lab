# Skill Spec: context-pack-builder

## Trigger Description Draft

복잡한 작업에 필요한 관련 파일, 최근 변경, 테스트 기준, 설계/정책 문서만 좁혀서 하위 agent에 전달하는 skill이다. 저장소 전체 주입 없이도 품질 높은 실행이 가능하도록 컨텍스트를 압축해야 할 때 사용한다.

## Core Workflow

1. task brief를 읽고 핵심 변경 축을 추린다
2. 구현 파일, 테스트 파일, 문서 파일을 분리한다
3. 최근 변경 중 충돌 가능성이 있는 것만 포함한다
4. 재현 경로와 필수 테스트를 함께 적는다

## Output Contract

- [CONTEXT_PACK_TEMPLATE.md](/Users/shinukyi/Gallary/projects/proto/agent-lab/docs/templates/CONTEXT_PACK_TEMPLATE.md:1) 형식을 채운다
- 포함 이유와 제외 이유를 함께 남긴다

## Likely Failure Modes

- `wrong_context`
- `handoff_failure`
- `hallucinated_assumption`

## Forward-Test Scenarios

- authorization bug
- realtime race condition
- multi-tenant cache leak
