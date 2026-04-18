#!/usr/bin/env python3
"""Aggregate benchmark traces and derive candidate recommendations."""

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path


def load_trace_files(root: Path):
    for path in sorted(root.rglob("trace_record.json")):
        yield json.loads(path.read_text())


def summarize(root: Path):
    by_run = defaultdict(
        lambda: {
            "total": 0,
            "pass": 0,
            "high": 0,
            "additional_high": 0,
            "medium": 0,
            "additional_medium": 0,
            "low": 0,
            "additional_low": 0,
            "token_total": 0,
            "total_seconds": 0.0,
            "failures": Counter(),
        }
    )
    for trace in load_trace_files(root):
        key = trace["run_id"].split("__")[0]
        by_run[key]["total"] += 1
        if trace["result"] == "pass":
            by_run[key]["pass"] += 1
        by_run[key]["high"] += trace["review_results"]["high"]
        by_run[key]["medium"] += trace["review_results"]["medium"]
        by_run[key]["low"] += trace["review_results"]["low"]
        for evaluator in trace.get("evaluator_results", {}).values():
            by_run[key]["additional_high"] += evaluator.get("high", 0)
            by_run[key]["additional_medium"] += evaluator.get("medium", 0)
            by_run[key]["additional_low"] += evaluator.get("low", 0)
        by_run[key]["token_total"] += sum_usage_tokens(trace.get("usage", {}))
        by_run[key]["total_seconds"] += float(trace.get("timing", {}).get("total_seconds", 0.0))
        for tag in trace["failure_taxonomy"]:
            by_run[key]["failures"][tag] += 1
        by_run[key]["candidate_id"] = trace["candidate_id"]
        by_run[key]["model_mapping"] = trace["model_mapping"]
    return by_run


def sum_usage_tokens(node):
    if isinstance(node, dict):
        total = 0
        for key, value in node.items():
            if key.endswith("_tokens") and isinstance(value, int):
                total += value
            else:
                total += sum_usage_tokens(value)
        return total
    if isinstance(node, list):
        return sum(sum_usage_tokens(item) for item in node)
    return 0


def derive_recommendations(summary):
    quality_champion = None
    min_sufficient = None

    sorted_runs = sorted(
        summary.items(),
        key=lambda item: (
            -item[1]["pass"],
            item[1]["high"] + item[1]["additional_high"],
            item[1]["medium"] + item[1]["additional_medium"],
            item[1]["low"] + item[1]["additional_low"],
            sum(item[1]["failures"].values()),
            item[1]["token_total"],
        ),
    )
    if sorted_runs:
        quality_champion = sorted_runs[0][0]

    min_sufficient_candidates = []
    for run_id, stats in sorted_runs:
        if stats["high"] == 0 and stats["additional_high"] == 0 and stats["pass"] == stats["total"]:
            min_sufficient_candidates.append((run_id, stats))

    if min_sufficient_candidates:
        min_sufficient = sorted(
            min_sufficient_candidates,
            key=lambda item: (
                item[1]["medium"] + item[1]["additional_medium"],
                item[1]["low"] + item[1]["additional_low"],
                sum(item[1]["failures"].values()),
                item[1]["token_total"],
            ),
        )[0][0]

    return quality_champion, min_sufficient


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()

    root = Path(args.root)
    summary = summarize(root)
    quality_champion, min_sufficient = derive_recommendations(summary)

    printable = {}
    for run_id, stats in summary.items():
        printable[run_id] = {
            "candidate_id": stats["candidate_id"],
            "model_mapping": stats["model_mapping"],
            "total_tasks": stats["total"],
            "passed_tasks": stats["pass"],
            "high_findings": stats["high"],
            "additional_high_findings": stats["additional_high"],
            "medium_findings": stats["medium"],
            "additional_medium_findings": stats["additional_medium"],
            "low_findings": stats["low"],
            "additional_low_findings": stats["additional_low"],
            "token_total": stats["token_total"],
            "total_seconds": round(stats["total_seconds"], 3),
            "avg_seconds_per_task": round(stats["total_seconds"] / stats["total"], 3) if stats["total"] else 0.0,
            "failure_taxonomy": dict(stats["failures"]),
        }

    result = {
        "quality_champion": quality_champion,
        "minimum_sufficient_config": min_sufficient,
        "runs": printable,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
