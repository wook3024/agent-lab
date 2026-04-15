# agent-lab

복잡한 제품 개발 작업에서 최고 품질의 `agent + skill + model + effort` 조합을 찾기 위한 실험 저장소다.

## 포함 내용

- complex-case 운영 계획과 실험 문서
- Codex용 role card, candidate prompt, skill 자산
- runnable benchmark sandboxes 3종
- benchmark runner / scorer 스크립트
- initial batch와 refined batch의 scorecard 및 로그

## 핵심 결과

- broad-sweep champion: `C2 + triage/context=gpt-5.4-mini/medium + execution=gpt-5.4/xhigh + review=gpt-5.4/high`
- refined high-confidence default: `C2 + all roles gpt-5.4/high`
- complex-case 기본 운영에서는 `C0` single-pass 계열을 승격하지 않음
- `execution=xhigh`는 기본값으로 두지 않음

자세한 권장 구성은 [docs/RECOMMENDED_AGENT_SKILL_MODEL_CONFIGS.md](docs/RECOMMENDED_AGENT_SKILL_MODEL_CONFIGS.md)를 보면 된다.

## 바로 볼 문서

- [docs/FINAL_SCORECARD.md](docs/FINAL_SCORECARD.md)
- [docs/BENCHMARK_BATCH_LOG.md](docs/BENCHMARK_BATCH_LOG.md)
- [docs/PROGRAM_CHECKLIST.md](docs/PROGRAM_CHECKLIST.md)
- [docs/RECOMMENDED_AGENT_SKILL_MODEL_CONFIGS.md](docs/RECOMMENDED_AGENT_SKILL_MODEL_CONFIGS.md)

## 재현

초기 배치:

```bash
python3 scripts/run_codex_benchmark.py --config benchmark/initial_matrix.yaml
python3 scripts/score_codex_benchmark.py --root artifacts/benchmark_runs/initial-complex-case-batch
```

refined 확인 배치:

```bash
python3 scripts/run_codex_benchmark.py --config benchmark/refined_matrix.yaml
python3 scripts/score_codex_benchmark.py --root artifacts/benchmark_runs/refined-skill-batch
```
