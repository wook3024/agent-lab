# Skill Spec: security-review

## Trigger Description Draft

일반 리뷰와 별도로 auth, RBAC, data exposure, secret handling, audit logging, integration trust boundary를 검토하는 보안 리뷰 skill이다. security-sensitive change에 대해 독립된 severity lane을 만든다.

## Core Workflow

1. task brief, context pack, diff, gate 결과를 읽는다
2. security-sensitive surface가 실제로 touched 되었는지 확인한다
3. auth boundary, tenant isolation, secret handling, data exposure, auditability를 점검한다
4. exploit path 또는 misuse path를 기준으로 severity를 판단한다
5. `Critical / High / Medium / Low / Residual Security Risks` 형식으로 결과를 남긴다

## Trigger Conditions

- auth / RBAC / permission checks changed
- PII or sensitive data path changed
- secrets, credentials, token issuance or verification changed
- external webhook, callback, upload quarantine, scanning, signing path changed
- tenant isolation or multi-tenant cache boundary changed

## Output Contract

- [SECURITY_REVIEW_TEMPLATE.md](/Users/shinukyi/Gallary/projects/proto/agent-lab/docs/templates/SECURITY_REVIEW_TEMPLATE.md:1) 형식을 따른다
- 일반 리뷰 findings와 섞지 않고 security lane으로 유지한다

## Likely Failure Modes

- `auth_bypass_missed`
- `data_exposure_blindness`
- `secret_flow_omission`
- `audit_gap_underclassification`

## Forward-Test Scenarios

- RBAC scope leak
- upload quarantine bypass
- tenant cache isolation break
- webhook signature verification regression
