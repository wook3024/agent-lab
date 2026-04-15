# agent-lab

복잡한 제품 개발 작업에서 `agent + skill + model + effort` 조합을 실험하고, 가장 높은 응답 품질을 안정적으로 재현할 수 있는 운영 구성을 찾기 위한 benchmark 저장소입니다.

이 저장소의 초점은 간단한 질의응답이 아니라 아래 같은 complex-case입니다.

- 여러 파일에 걸친 기능 구현과 회귀 방지
- race condition, cache scope, rollout fallback, tenant isolation 같은 숨은 결함
- 코드 변경과 테스트, 문서, 운영 가드의 동기화
- single-pass보다 더 안전한 multi-stage 개발 워크플로우 검증

## 핵심 결론

- 최고 품질 기본값: `C2 + all roles gpt-5.4/high`
- 비용 효율이 좋은 유망 후보: `C2 + triage/context=gpt-5.4-mini/medium + execution/review=gpt-5.4`
- complex-case 기본 운영에서는 `C0` single-pass 계열을 승격하지 않음
- `execution=xhigh`는 기본값으로 두지 않음

최종 권고안은 [docs/RECOMMENDED_AGENT_SKILL_MODEL_CONFIGS.md](docs/RECOMMENDED_AGENT_SKILL_MODEL_CONFIGS.md)에 정리되어 있습니다.

## 저장소 구성

- [`docs/`](docs): 운영 계획, 역할 카드, 실험 로그, 최종 권고안
- [`skills/`](skills): 검증 대상 Codex skill 자산
- [`agents/`](agents): candidate agent prompt와 evaluator 자산
- [`evals/complex-case-golden-set/`](evals/complex-case-golden-set): complex-case 평가 태스크 세트
- [`benchmark/`](benchmark): 배치 실행 설정
- [`scripts/`](scripts): benchmark 실행 및 스코어링 스크립트
- [`sandboxes/`](sandboxes): 재현 가능한 테스트용 샘플 프로젝트
- [`artifacts/benchmark_runs/`](artifacts/benchmark_runs): 대표 실행 결과 요약

## 추천 진입 문서

- [docs/FINAL_SCORECARD.md](docs/FINAL_SCORECARD.md)
- [docs/RECOMMENDED_AGENT_SKILL_MODEL_CONFIGS.md](docs/RECOMMENDED_AGENT_SKILL_MODEL_CONFIGS.md)
- [docs/BENCHMARK_BATCH_LOG.md](docs/BENCHMARK_BATCH_LOG.md)
- [docs/COMPLEX_CASE_AGENT_PROGRAM_PLAN.md](docs/COMPLEX_CASE_AGENT_PROGRAM_PLAN.md)
- [docs/MODEL_EFFORT_BENCHMARK_PLAN.md](docs/MODEL_EFFORT_BENCHMARK_PLAN.md)

## 현재 검증된 운영 형태

권장 topology는 `C2`입니다.

`Triage/Context -> Execution -> Deterministic Gates -> Independent Review`

이 구조는 complex-case에서 다음 특성을 보였습니다.

- single-pass 대비 scope control이 더 안정적임
- deterministic gate를 통과한 뒤에도 independent review가 숨은 결함을 계속 잡아냄
- brief와 context pack을 먼저 고정하면 execution의 과도한 일반화를 줄일 수 있음

## 빠른 재현

초기 broad sweep:

```bash
python3 scripts/run_codex_benchmark.py --config benchmark/initial_matrix.yaml
python3 scripts/score_codex_benchmark.py --root artifacts/benchmark_runs/initial-complex-case-batch
```

refined confirmatory batch:

```bash
python3 scripts/run_codex_benchmark.py --config benchmark/refined_matrix.yaml
python3 scripts/score_codex_benchmark.py --root artifacts/benchmark_runs/refined-skill-batch
```

## 참고

- 공개 저장소에는 representative artifact만 포함했습니다.
- 대용량 실행 로그, 중간 `workspace/` 복제본, 원시 `jsonl` 스트림은 제외했습니다.
- 이 저장소는 “어떤 모델이 무조건 최고인가”보다 “어떤 workflow와 역할 분리가 complex-case에서 실제 품질을 올리는가”를 검증하는 데 더 큰 비중을 둡니다.
