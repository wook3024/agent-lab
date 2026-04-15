---
name: trace-eval-recorder
description: Record structured traces, evaluation metadata, and failure taxonomy for complex-case agent runs. Use when comparing candidate agents, skills, or model-effort combinations and you need reproducible evidence instead of impressions.
---

# Trace Eval Recorder

Capture enough structured data to compare runs honestly.

## Workflow

1. Record candidate id, task id, model mapping, and effort mapping.
2. Record files referenced, tools used, changed files, and gate results.
3. Record review severity totals and failure taxonomy tags.
4. Write one trace record per run.
5. Aggregate traces into scorecards after the batch finishes.

## Rules

- Missing data is not a pass.
- Keep one run per file to simplify comparisons.
- Preserve blocking failures instead of flattening them into summaries.

## Output Contract

Mirror `../../docs/templates/TRACE_RECORD_TEMPLATE.json` and `../../docs/templates/SCORECARD_TEMPLATE.md`.

## Read These References

- `references/failure-taxonomy.md`
- `scripts/aggregate_failure_tags.py`

## Failure Modes To Avoid

- Incomplete trace fields
- Missing taxonomy tags
- Aggregating unlike-for-like runs
