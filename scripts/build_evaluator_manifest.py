#!/usr/bin/env python3
"""Build a normalized evaluator manifest for a benchmark or pilot run directory."""

import argparse
import json
from pathlib import Path


ALLOWED_LANES = {"review", "security", "release_gate", "architecture"}


def optional_path(path: Path):
    return str(path) if path.exists() else None


def required_path(path: Path, label: str):
    if not path.exists():
        raise FileNotFoundError(f"missing required {label}: {path}")
    return str(path)


def build_manifest(run_dir: Path, lane: str):
    if lane not in ALLOWED_LANES:
        raise ValueError(f"unsupported lane: {lane}")

    workspace = run_dir / "workspace"
    benchmark_outputs = workspace / "benchmark_outputs"

    manifest = {
        "lane": lane,
        "run_dir": str(run_dir),
        "workspace": required_path(workspace, "workspace"),
        "task_manifest": required_path(workspace / "benchmark_task.json", "task_manifest"),
        "task_brief": required_path(benchmark_outputs / "task_brief.md", "task_brief"),
        "context_pack": required_path(benchmark_outputs / "context_pack.md", "context_pack"),
        "execution_report": required_path(benchmark_outputs / "execution_report.md", "execution_report"),
        "gate_results": required_path(run_dir / "gate_results.json", "gate_results"),
        "trace_record": required_path(run_dir / "trace_record.json", "trace_record"),
        "review_findings": required_path(run_dir / "review_findings.json", "review_findings"),
        "optional_artifacts": {
            "approval_decision": optional_path(benchmark_outputs / "approval_decision.md"),
            "release_gate_decision": optional_path(benchmark_outputs / "release_gate_decision.md"),
            "release_artifact_package": optional_path(benchmark_outputs / "release_artifact_package.md"),
            "security_review_findings": optional_path(benchmark_outputs / "security_review_findings.json"),
            "architecture_review_findings": optional_path(benchmark_outputs / "architecture_review_findings.json"),
        },
        "diff_command": ["git", "diff", "HEAD"],
    }
    return manifest


def dump_manifest(manifest: dict, output_path: Path):
    output_path.write_text(json.dumps(manifest, indent=2, sort_keys=True))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--lane", required=True, choices=sorted(ALLOWED_LANES))
    parser.add_argument("--output")
    args = parser.parse_args()

    run_dir = Path(args.run_dir).resolve()
    manifest = build_manifest(run_dir, args.lane)

    if args.output:
        dump_manifest(manifest, Path(args.output))
    else:
        print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
