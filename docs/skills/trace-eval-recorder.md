# Skill Spec: trace-eval-recorder

## Trigger Description Draft

복잡한 작업 실행의 입력, 참조 파일, tool 호출, gate 결과, review 결과, 실패 taxonomy를 구조화해서 남기는 skill이다. 감이 아니라 trace 기반으로 후보 조합을 비교하고 수정할 때 사용한다.

## Core Workflow

1. run id, candidate id, task id를 기록한다
2. 참조 파일과 tool 호출을 남긴다
3. gate와 review 결과를 severity 기준으로 기록한다
4. failure taxonomy를 분류한다
5. 결과를 trace record와 scorecard에 반영한다

## Output Contract

- [TRACE_RECORD_TEMPLATE.json](/Users/shinukyi/Gallary/projects/proto/agent-lab/docs/templates/TRACE_RECORD_TEMPLATE.json:1) 형식을 채운다
- candidate 비교에 필요한 최소 필드를 빠뜨리지 않는다

## Likely Failure Modes

- `wrong_context`
- `wrong_tool`
- `handoff_failure`
- `docs_desync`

## Forward-Test Scenarios

- same task across C0 and C2
- gate fail versus review fail comparison
- repeated reruns after skill revision
