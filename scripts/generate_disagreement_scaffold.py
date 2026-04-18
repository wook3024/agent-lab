#!/usr/bin/env python3
"""Generate a disagreement scaffold from existing evaluator findings."""

import argparse
import json
from pathlib import Path

from run_codex_benchmark import (
    create_disagreement_scaffold,
    findings_signature,
    load_json,
    summarize_findings,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--lane", required=True)
    args = parser.parse_args()

    run_dir = Path(args.run_dir).resolve()
    review_findings = load_json(run_dir / "review_findings.json")
    lane_findings = load_json(run_dir / "evaluators" / f"{args.lane}_findings.json")
    review_summary = summarize_findings(review_findings)
    lane_summary = summarize_findings(lane_findings)

    if findings_signature(review_summary) == findings_signature(lane_summary):
        print("no-disagreement-detected")
        return

    task_id = load_json(run_dir / "workspace" / "benchmark_task.json")["id"]
    output_path = create_disagreement_scaffold(run_dir, task_id, args.lane, review_summary, lane_summary)
    index_path = run_dir / "evaluators" / "index.json"
    if index_path.exists():
        index = json.loads(index_path.read_text())
        index.setdefault("additional_lanes", {}).setdefault(args.lane, {})["disagreement_path"] = str(output_path)
        index_path.write_text(json.dumps(index, indent=2, sort_keys=True))
    print(output_path)


if __name__ == "__main__":
    main()
