# AI Agent Operating Playbook

이 문서는 개발 프로젝트에서 AI 에이전트를 "도구" 수준이 아니라 "품질을 높이는 운영 시스템"으로 쓰기 위한 실무 표준안이다.

목표는 세 가지다.

1. 변경 속도를 높인다.
2. 회귀와 재작업을 줄인다.
3. 위험한 자동화를 통제 가능한 절차 안으로 넣는다.

이 플레이북의 기본 철학은 다음과 같다.

- 기본값은 `single specialist agent`다.
- 품질은 프롬프트가 아니라 `eval + trace + deterministic gate`로 관리한다.
- 멀티에이전트는 병렬성이 명확할 때만 쓴다.
- 배포, 삭제, 권한 변경, 결제, 프로덕션 셸 조작은 반드시 사람 승인 경로를 둔다.

## 1. 권장 운영 모델

가장 추천하는 기본 구조는 아래와 같다.

```text
Issue / PRD / Bug report
  -> Triage Agent
  -> Context Loader
  -> Execution Agent
  -> Deterministic Quality Gates
  -> Review Agent
  -> Approval Gate
  -> Merge / Deploy / Rework
```

각 단계의 목적은 다음과 같다.

- `Triage Agent`: 요청을 작업 유형으로 분류하고 성공 기준을 명시한다.
- `Context Loader`: 관련 파일, 설계 문서, 최근 PR, 테스트, API 규약만 좁혀서 제공한다.
- `Execution Agent`: 구현, 수정, 테스트 추가, 문서 반영을 수행한다.
- `Deterministic Quality Gates`: `unit/integration test`, `lint`, `typecheck`, `security scan`을 실행한다.
- `Review Agent`: 요구사항 누락, 회귀 위험, 과도한 변경, 잘못된 툴 사용을 점검한다.
- `Approval Gate`: 위험 작업의 최종 실행을 멈추고 사람 결정을 기다린다.

## 2. 팀 표준 역할 정의

기본 역할은 아래 5개면 충분하다.

### 2.1 Triage Agent

역할:
- 요청을 `구현`, `리뷰`, `조사`, `운영` 중 하나로 분류
- 성공 기준과 비성공 조건 정의
- 필요한 컨텍스트 범위 축소

입력:
- 이슈, 버그 리포트, PRD, 사용자 요청

출력:
- 작업 유형
- 완료 조건
- 관련 파일/문서 목록
- 위험 등급

금지:
- 구현 수행
- 승인 없는 쓰기 작업

### 2.2 Execution Agent

역할:
- 코드 변경
- 테스트 추가
- 문서 반영
- 로컬 검증

입력:
- 작업 브리프
- 관련 파일
- 승인 정책

출력:
- 변경 요약
- 변경 파일 목록
- 테스트 결과
- 남은 리스크

금지:
- 범위를 벗어난 대규모 리팩터링
- 승인 없는 파괴적 작업

### 2.3 Review Agent

역할:
- 회귀 위험 탐지
- 요구사항 누락 점검
- 테스트 부족 탐지
- 보안/성능/운영 위험 점검

입력:
- diff
- 테스트 결과
- 작업 브리프

출력:
- severity별 findings
- 재현 조건
- 권장 수정 방향

금지:
- 구현을 다시 수행하며 리뷰와 혼합

### 2.4 Research Agent

역할:
- 외부 문서, 공식 레퍼런스, 경쟁 사례 조사
- 설계 옵션 비교
- 불확실성 제거

입력:
- 질문
- 제약사항

출력:
- 근거가 있는 옵션 비교
- 추천안
- 근거 링크

금지:
- 추측성 결론

### 2.5 Release Gate Agent

역할:
- 릴리즈 전 체크리스트 검증
- 승인 필요한 작업 목록화
- 롤백 준비 확인

입력:
- 배포 대상 변경
- 테스트/관측 정보

출력:
- 배포 가능/보류 판단
- 보류 사유
- 승인 요청 항목

금지:
- 사람 승인 없이 실제 배포 실행

## 3. 어떤 작업에 멀티에이전트를 쓸 것인가

멀티에이전트는 다음 조건이 동시에 만족될 때만 권장한다.

- 작업이 서로 독립적이다.
- 결과를 나중에 병합할 수 있다.
- 컨텍스트를 나눠도 품질 저하가 크지 않다.

적합한 예시:
- 구현과 테스트 작성 병렬화
- 기능 리뷰와 보안 리뷰 병렬화
- 여러 외부 문서 조사 병렬화
- 모듈별 마이그레이션 병렬화

부적합한 예시:
- 긴 함수 하나를 여러 에이전트가 동시에 수정
- 설계가 확정되지 않은 상태의 대규모 구현
- 매우 강하게 결합된 레거시 코드 수정

권장 패턴:

```text
Manager Agent
  -> Worker A: 구현
  -> Worker B: 테스트
  -> Worker C: 리뷰
  -> Manager가 결과 통합
```

peer-to-peer 자율 협업보다 `manager-controlled orchestration`이 개발 품질에는 더 안정적이다.

## 4. 승인 정책

아래 매트릭스를 기본 정책으로 사용한다.

| 작업 종류 | 예시 | 기본 정책 |
| --- | --- | --- |
| Read-only | 코드 읽기, 로그 조회, 문서 검색 | 자동 허용 |
| Safe write | 테스트 추가, 주석 보강, 문서 수정 | 자동 허용 또는 사후 보고 |
| Moderate write | 기능 수정, 리팩터링, 의존성 소규모 변경 | 작업 브리프 기준 허용 |
| Risky write | DB schema, 삭제, 대량 rename, 권한 변경 | 사전 승인 필요 |
| Irreversible | 배포, 결제, 실데이터 삭제, 프로덕션 셸 명령 | 반드시 명시적 승인 |

특히 아래는 항상 승인 대상이다.

- `rm`, 대량 파일 삭제
- 운영 DB 변경
- 프로덕션 환경 변수 변경
- 외부 서비스 설정 변경
- 결제/구독/권한 작업
- 민감 정보가 포함된 MCP 액션

## 5. 표준 작업 브리프 템플릿

아래 템플릿을 모든 실행 작업의 입력 계약으로 사용한다.

```md
# Task Brief

## Goal
- 무엇을 바꾸는가:

## Done When
- [ ] 기능 요구사항 충족
- [ ] 회귀 테스트 통과
- [ ] lint / typecheck 통과
- [ ] 문서 반영 완료

## Non-Goals
- 이번 작업에서 하지 않을 것:

## Relevant Context
- 관련 파일:
- 관련 이슈/PR:
- 관련 문서:

## Constraints
- 성능 제약:
- 보안 제약:
- 호환성 제약:

## Risk Level
- low / medium / high

## Approval Requirements
- 승인 필요한 작업:

## Expected Output
- 변경 파일 목록
- 테스트 결과
- 남은 리스크
```

## 6. 역할 정의 템플릿

새 에이전트를 추가할 때는 아래 형식으로 정의한다.

```md
# Agent Role Card

## Name
- 예: Backend Review Agent

## Purpose
- 이 에이전트가 잘해야 하는 한 가지 일

## Inputs
- 어떤 자료를 받는가

## Allowed Tools
- 사용할 수 있는 도구

## Forbidden Actions
- 해서는 안 되는 행동

## Output Contract
- 반드시 포함해야 하는 출력 항목

## Quality Checks
- 스스로 또는 외부에서 거칠 검증

## Escalation Rules
- 어떤 상황에서 사람에게 넘길지
```

## 7. 평가 체계

에이전트 품질은 아래 4개 층위로 측정한다.

### 7.1 Task-level

- 작업 성공률
- 재작업률
- 요구사항 누락률
- 회귀 발생률

### 7.2 Workflow-level

- 잘못된 도구 선택률
- 잘못된 파일 수정률
- 불필요한 변경량
- handoff 실패율

### 7.3 Engineering-quality

- 테스트 추가율
- lint/typecheck 실패율
- 보안 경고 수
- 성능 회귀 건수

### 7.4 Operational

- 평균 처리 시간
- 평균 비용
- 승인 요청 비율
- 사람이 개입해야 하는 빈도

## 8. Eval 세트 설계 기준

프로젝트마다 최소 `20~50`개의 대표 작업을 golden set으로 만든다.

구성 비율 예시:
- 30%: 일반 기능 수정
- 20%: 버그 수정
- 15%: 테스트 보강
- 15%: 코드 리뷰 성격 작업
- 10%: 문서/설계 반영
- 10%: 실패/엣지 케이스

각 샘플에는 아래를 저장한다.

- 입력 요청
- 정답 또는 기대 행동
- 관련 컨텍스트
- 허용 가능한 출력 형태
- 금지 행동

## 9. Eval 레코드 템플릿

```json
{
  "id": "bugfix-auth-timeout-001",
  "task_type": "implementation",
  "prompt": "로그인 timeout 버그 수정",
  "context": {
    "files": [
      "src/auth/service.ts",
      "src/auth/service.test.ts"
    ],
    "docs": [
      "docs/auth-flow.md"
    ]
  },
  "expected": {
    "must_change_files": [
      "src/auth/service.ts"
    ],
    "must_add_or_update_tests": true,
    "must_not": [
      "change public API",
      "modify unrelated modules"
    ]
  },
  "graders": [
    "tests_pass",
    "requirements_met",
    "no_unrelated_changes",
    "no_policy_violation"
  ]
}
```

## 10. Trace 운영 규칙

모든 의미 있는 실행에는 trace를 남긴다.

최소 수집 항목:
- 입력 요약
- 참조한 파일/문서
- 수행한 툴 호출
- 실행 시간
- 비용
- 실패 원인
- 최종 결과

실패 trace는 반드시 아래 taxonomy로 태깅한다.

- `wrong_context`
- `wrong_tool`
- `hallucinated_assumption`
- `over_edit`
- `missed_test`
- `policy_violation`
- `handoff_failure`
- `insufficient_spec`

이 taxonomy가 있어야 이후 prompt 개선이나 tool 개선이 가능하다.

## 11. 컨텍스트 엔지니어링 규칙

다음 원칙을 지킨다.

- 저장소 전체를 한 번에 주입하지 않는다.
- 최근 변경분과 관련 파일부터 본다.
- 설계 문서는 요약본과 원문 링크를 같이 둔다.
- 긴 로그는 그대로 넣지 말고 `핵심 오류 + 재현 경로`만 전달한다.
- 하위 에이전트에는 부모가 정제한 요약만 넘긴다.
- 세션 메모리는 `결정`, `미해결`, `주의사항`만 남긴다.

권장 순서:

1. 이슈/요청 요약
2. 관련 파일 추출
3. 최근 변경 확인
4. 설계/정책 문서 추출
5. 테스트 기준 정리
6. 실행

## 12. 코드 리뷰 운영안

리뷰 에이전트는 아래 형식으로만 답하도록 강제하는 것이 좋다.

```md
# Review Findings

## High
- 파일/라인:
- 문제:
- 왜 중요한가:
- 재현 또는 영향:

## Medium
- 파일/라인:
- 문제:
- 영향:

## Low
- 파일/라인:
- 제안:

## Residual Risks
- 아직 검증되지 않은 부분:
```

이렇게 하면 "좋아 보이는 말"보다 실제 결함 탐지에 집중시킬 수 있다.

## 13. 추천 기본 워크플로우

### 구현 작업

1. Triage Agent가 범위와 완료 조건 정리
2. Context Loader가 관련 코드와 테스트만 제공
3. Execution Agent가 구현 및 테스트 추가
4. Deterministic gate 실행
5. Review Agent가 diff 검토
6. 필요 시 수정 반복

### 조사 작업

1. 질문 분해
2. 1차 출처 우선 검색
3. 주장-근거 매핑
4. 불확실성 명시
5. 결론과 반례 정리

### 운영 작업

1. 위험도 분류
2. 승인 필요 항목 추출
3. dry-run 또는 read-only 점검
4. 사람 승인
5. 실행
6. 실행 로그와 rollback 정보 기록

## 14. 도입 로드맵

### Phase 1: Safe Assist

기간:
- 1~2주

목표:
- read 중심 사용
- 코드 수정은 작은 범위로 제한

필수:
- lint/test/typecheck
- 기본 trace

성공 기준:
- 작업 성공률 상승
- 회귀 없음

### Phase 2: Controlled Write

기간:
- 2~4주

목표:
- 구현과 테스트 추가 자동화

필수:
- golden set 구축
- 리뷰 에이전트 도입

성공 기준:
- 재작업률 감소
- 테스트 보강률 상승

### Phase 3: Bounded Multi-Agent

기간:
- 4~8주

목표:
- 병렬 가능한 작업만 멀티에이전트화

필수:
- manager-worker 구조
- handoff 규칙

성공 기준:
- 처리 시간 단축
- 품질 유지

### Phase 4: Production Governance

기간:
- 지속 운영

목표:
- 승인 정책, 추적, rollback, 모델 버전 관리 정착

필수:
- A/B 평가
- trace grading
- model/version pinning

성공 기준:
- 품질 지표 안정화
- 운영 사고 감소

## 15. 팀에서 바로 채택할 기본 규칙

초기 기본값은 아래처럼 두는 것을 권장한다.

- 기본 실행 주체는 `Execution Agent` 하나
- 모든 변경은 `Review Agent`를 한 번 거침
- `test/lint/typecheck` 통과 전 완료 처리 금지
- 위험 작업은 승인 없이는 실행 금지
- 매주 실패 trace 10건 리뷰
- 매월 golden set 업데이트
- 모델 변경 시 이전 버전과 A/B 비교

## 16. 바로 시작할 수 있는 최소 세트

이번 주 안에 도입하려면 아래만 먼저 하면 된다.

1. 작업 브리프 템플릿 도입
2. 구현용 실행 에이전트 1개 정의
3. 리뷰 에이전트 1개 정의
4. deterministic gate 연결
5. 대표 작업 20개를 golden set으로 저장
6. 승인 정책 표를 팀 문서에 명시

이 6가지만 있어도 "그럴듯한 AI 사용"에서 "품질 관리형 운영"으로 넘어갈 수 있다.

