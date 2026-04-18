#!/usr/bin/env python3
"""Render a markdown scorecard for benchmark traces with deep evaluator results."""

import argparse
from pathlib import Path

from score_codex_benchmark import derive_recommendations, summarize


def render_table(summary: dict):
    lines = [
        "| Run | Tasks | Pass | Review High | Addl High | Review Medium | Addl Medium | Review Low | Addl Low | Avg Seconds | Token Total |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for run_id, stats in sorted(summary.items()):
        avg_seconds = round(stats["total_seconds"] / stats["total"], 3) if stats["total"] else 0.0
        lines.append(
            f"| `{run_id}` | {stats['total']} | {stats['pass']} | {stats['high']} | {stats['additional_high']} | "
            f"{stats['medium']} | {stats['additional_medium']} | {stats['low']} | {stats['additional_low']} | "
            f"{avg_seconds} | {stats['token_total']} |"
        )
    return "\n".join(lines)


def render_failure_notes(summary: dict):
    lines = []
    for run_id, stats in sorted(summary.items()):
        if not stats["failures"]:
            continue
        pairs = ", ".join(f"`{key}`={value}" for key, value in sorted(stats["failures"].items()))
        lines.append(f"- `{run_id}`: {pairs}")
    return "\n".join(lines) if lines else "- 없음"


def render_deep_gaps(summary: dict):
    lines = []
    for run_id, stats in sorted(summary.items()):
        if stats["additional_high"] == 0 and stats["additional_medium"] == 0 and stats["additional_low"] == 0:
            continue
        lines.append(
            f"- `{run_id}`: additional evaluator findings "
            f"`high={stats['additional_high']}`, `medium={stats['additional_medium']}`, `low={stats['additional_low']}`"
        )
    return "\n".join(lines) if lines else "- 없음"


def render_markdown(root: Path, batch_label: str):
    summary = summarize(root)
    quality_champion, min_sufficient = derive_recommendations(summary)

    return f"""# Deep Validation Scorecard

## Scope

- batch label: `{batch_label}`
- artifact root: `{root}`

## Summary

- quality champion: `{quality_champion}`
- minimum sufficient config: `{min_sufficient}`

## Score Table

{render_table(summary)}

## Deep Evaluator Gaps

{render_deep_gaps(summary)}

## Failure Taxonomy Notes

{render_failure_notes(summary)}
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--batch-label", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()

    markdown = render_markdown(Path(args.root), args.batch_label)
    if args.output:
        Path(args.output).write_text(markdown)
    else:
        print(markdown)


if __name__ == "__main__":
    main()
