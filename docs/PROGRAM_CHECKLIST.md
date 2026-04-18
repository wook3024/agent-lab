# Program Checklist

## Objective

복잡한 제품 개발 작업에서 최고 수준의 응답 품질을 내는 `agent + skill + model + effort` 조합을 설계하고, 실제 benchmark를 통해 기준별 최적 조합을 도출한다.

## Working Rules

- simple task 품질보다 complex-case 품질을 우선한다
- `skill`, `agent contract`, `model/effort`는 분리해서 실험한다
- checklist 상태를 기준으로 문서를 갱신한다
- benchmark 결과가 없으면 최적 조합 판정을 내리지 않는다

## Checklist

### Phase 1. Program Control

- [x] 운영 계획 문서 작성
- [x] complex-case 실험 매트릭스 작성
- [x] model/effort benchmark 계획 작성
- [x] program checklist 생성 및 지속 갱신

### Phase 2. Skill And Agent Assets

- [x] repo-local skill 폴더 구조 생성
- [x] core skill 1: `task-brief-author` 생성
- [x] core skill 2: `context-pack-builder` 생성
- [x] core skill 3: `execution-engineering` 생성
- [x] core skill 4: `review-findings` 생성
- [x] core skill 5: `quality-gates-runner` 생성
- [x] core skill 6: `trace-eval-recorder` 생성
- [x] core skill 7: `docs-sync` 생성
- [x] optional skill: `research-grounded` 생성
- [x] skill validation 수행
- [x] benchmark용 agent prompt 자산 생성

### Phase 3. Benchmark Workloads

- [x] abstract complex-case golden set 초안 작성
- [x] runnable local sandbox 1 생성
- [x] runnable local sandbox 2 생성
- [x] runnable local sandbox 3 생성
- [x] sandbox별 task brief 정리
- [x] sandbox별 deterministic gate 정의

### Phase 4. Benchmark Tooling

- [x] Codex CLI smoke verification
- [x] benchmark runner 구현
- [x] benchmark config/model matrix 작성
- [x] benchmark scoring/aggregation 구현
- [x] trace artifact schema 확정
- [x] scorecard artifact schema 확정

### Phase 5. First Benchmark Batch

- [x] C0 baseline runs 실행
- [x] C2 baseline runs 실행
- [x] gpt-5.4 vs gpt-5.4-mini 비교
- [x] 핵심 effort(`medium/high/xhigh`) 비교
- [x] 결과 trace 저장
- [x] 결과 scorecard 생성

### Phase 6. Recommendation

- [x] quality champion 도출
- [x] minimum sufficient config 도출
- [x] role routing policy 도출
- [x] remaining gaps / next batch 계획 반영

### Phase 7. CTO Control Plane Assets

- [x] CTO 관점 필수/선택 자산 재분류
- [x] CTO-grade target architecture 문서화
- [x] control-plane backlog 작성 및 우선순위화
- [x] 90일 도입 로드맵 작성
- [x] `release-gate` 자산 작성
- [x] `approval-policy` 자산 작성
- [x] `security-review` 자산 작성
- [x] `ownership-routing` 자산 작성
- [x] `cost-governance-trace` 자산 작성
- [x] `incident-mode-policy` 자산 작성
- [x] `architecture-review` 자산 작성
- [x] `release-artifact-generator` 자산 작성
- [x] `owner-aware-context-builder` 자산 작성

### Phase 8. Pilot Operations Package

- [x] pilot deployment playbook 작성
- [x] pilot sample run package 작성
- [x] pilot owner map sample 작성
- [x] pilot scorecard template 작성
- [x] pilot batch evaluation flow 작성
- [x] dossier / backlog / roadmap에 pilot 자산 반영
- [x] 공개 저장소 sync 준비

### Phase 9. Operating Governance And Registry

- [x] 운영 governance 모델 문서화
- [x] asset registry schema 정의
- [x] asset status baseline 분류
- [x] machine-readable asset registry 작성
- [x] dossier에 governance 자산 반영
- [x] 공개 저장소 sync 준비

### Phase 10. Registry Update Loop

- [x] asset review workflow 문서화
- [x] asset status change template 작성
- [x] registry validator 스크립트 작성
- [x] registry validator 실행 확인
- [x] dossier에 registry 운영 자산 반영
- [x] 공개 저장소 sync 준비

### Phase 11. Sample Batch Rehearsal

- [x] `pilot-batch-01` sample scorecard 작성
- [x] `pilot-batch-01` asset review 예시 작성
- [x] `pilot-batch-01` registry update example 작성
- [x] dossier에 sample batch 자산 반영
- [x] 공개 저장소 sync 준비

### Phase 12. LLM Deep Validation System

- [x] LLM 심층 검증 운영 모델 문서화
- [x] LLM eval rubric template 작성
- [x] disagreement analysis template 작성
- [x] human calibration batch template 작성
- [x] security / release / architecture evaluator prompt 작성
- [x] dossier에 LLM validation 자산 반영
- [x] 공개 저장소 sync 준비

### Phase 13. Evaluator Runner Integration

- [x] evaluator runner contract 문서화
- [x] sample LLM evaluation summary 작성
- [x] sample disagreement analysis 작성
- [x] evaluator manifest builder 작성
- [x] evaluator bundle validator 작성
- [x] sample manifest 생성 및 validator 실행 기록
- [x] dossier에 evaluator runner 자산 반영
- [x] 공개 저장소 sync 준비

### Phase 14. Inline Evaluator Lane Planning

- [x] `run_codex_benchmark.py`에 config-driven evaluator lane selection 추가
- [x] `deep_validation_matrix.yaml` 작성
- [x] `--plan-only` 검증 모드 추가
- [x] sample task별 lane selection 검증
- [x] score aggregation에 additional evaluator finding 반영
- [x] dossier에 lane planning 자산 반영
- [x] 공개 저장소 sync 준비

## Current Assumptions

- actual benchmark execution은 로컬 `codex exec`를 사용한다
- reasoning effort 설정은 `model_reasoning_effort` config key를 사용한다
- repo 안의 `skills/`는 버전 관리용 자산으로 두고, benchmark prompt에서 명시 경로로 사용한다
- benchmark 우선 대상 candidate는 `C0`와 `C2`다

## Completion Rule

이 checklist에서 `Phase 1`부터 `Phase 14`까지 모두 완료되면 현재 프로그램 배치를 완료로 간주한다.

## Current Outcome

- broad-sweep champion: `c2-mini-triage-context`
- refined high-confidence default: `c2-all-gpt54-high`
- 제외 대상:
  - `C0` family for complex-case work
  - `execution = xhigh` as default
- 후속 확장:
  - refined 기준으로 `mini triage/context` 재검증
  - task type 다양화
  - pilot batch를 feature / migration / ops benchmark로 확장
