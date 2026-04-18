# LLM Evaluation Rubric Template

## Evaluation Lane

- lane:
- evaluator model / effort:
- task id:
- candidate config:
- batch id:

## Input Artifacts

- task brief:
- context pack:
- execution report:
- diff:
- gate results:
- trace record:
- additional governance artifacts:

## Must Answer

- 가장 가능성 높은 concrete failure는 무엇인가
- 현재 artifact 기준으로 `High` severity가 있는가
- 현재 판단이 artifact evidence에 실제로 묶여 있는가
- residual risk는 무엇인가
- 사람 승인 또는 follow-up이 필요한가

## Verdict

- verdict: `pass` | `concern` | `fail`
- confidence: `high` | `medium` | `low`

## Findings

### Critical

- none or list

### High

- none or list

### Medium

- none or list

### Low

- none or list

## Evidence Discipline

- 각 finding은 artifact 근거를 가져야 한다
- artifact로 입증되지 않는 추측은 `hypothesis`로만 남긴다
- style critique는 defect risk와 연결되지 않으면 제외한다

## Residual Risks

- 아직 남아 있는 운영 리스크:
- 추가 테스트가 필요한가:
- 추가 review lane이 필요한가:

## Governance Follow-Up

- approval escalation needed:
- release hold recommendation:
- owner routing concern:

## Output Quality Check

- finding이 실제 artifact에 anchored 되어 있는가
- lane 목적과 무관한 지적이 섞였는가
- 너무 많은 noise를 만들고 있지는 않은가
