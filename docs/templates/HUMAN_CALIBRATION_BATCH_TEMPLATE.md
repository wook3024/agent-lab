# Human Calibration Batch Template

## 목적

이 템플릿은 LLM evaluator와 human reviewer를 같은 batch에 붙여
judge 품질을 보정하기 위한 calibration run 기록 형식이다.

## Batch Metadata

- calibration batch id:
- date:
- service scope:
- compared evaluators:
- human reviewers:

## Selection Criteria

- 왜 이 task들이 calibration 대상으로 뽑혔는가:
- critical service 포함 여부:
- release / security / approval relevance:

## Per-Task Comparison

### Task

- task id:
- route:
- primary lane:

### LLM Verdict

- verdict:
- top findings:
- residual risk:

### Human Verdict

- verdict:
- top findings:
- residual risk:

### Delta

- severity mismatch:
- missed issue by LLM:
- missed issue by human:
- operator usefulness difference:

### Outcome

- who was closer to ground truth:
- what should change next:

## Batch-Level Lessons

- 반복적으로 어긋나는 evaluator lane:
- 사람이 특히 더 잘 보는 영역:
- LLM이 특히 더 잘 보는 영역:
- rubric 수정 필요:
- prompt 수정 필요:

## Next Actions

- evaluator prompt update:
- disagreement analysis creation:
- registry update:
- next calibration date:
