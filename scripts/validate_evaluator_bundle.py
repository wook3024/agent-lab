#!/usr/bin/env python3
"""Validate a generated evaluator manifest and its referenced artifact bundle."""

import argparse
import json
import subprocess
import sys
from pathlib import Path


ALLOWED_LANES = {"review", "security", "release_gate", "architecture"}
REQUIRED_FIELDS = {
    "lane",
    "run_dir",
    "workspace",
    "task_manifest",
    "task_brief",
    "context_pack",
    "execution_report",
    "gate_results",
    "trace_record",
    "review_findings",
    "optional_artifacts",
    "diff_command",
}


def fail(message: str):
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def ensure_file(path_str: str, label: str):
    path = Path(path_str)
    if not path.exists():
        fail(f"missing {label}: {path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    if not manifest_path.exists():
        fail(f"manifest not found: {manifest_path}")

    manifest = json.loads(manifest_path.read_text())
    missing = REQUIRED_FIELDS - set(manifest.keys())
    if missing:
        fail(f"manifest missing required fields: {sorted(missing)}")

    lane = manifest["lane"]
    if lane not in ALLOWED_LANES:
        fail(f"unsupported lane: {lane}")

    for field in [
        "run_dir",
        "workspace",
        "task_manifest",
        "task_brief",
        "context_pack",
        "execution_report",
        "gate_results",
        "trace_record",
        "review_findings",
    ]:
        ensure_file(manifest[field], field)

    workspace = Path(manifest["workspace"])
    if not (workspace / ".git").exists():
        fail(f"workspace is not a git repo: {workspace}")

    optional_artifacts = manifest["optional_artifacts"]
    if not isinstance(optional_artifacts, dict):
        fail("optional_artifacts must be an object")

    diff_command = manifest["diff_command"]
    if not isinstance(diff_command, list) or not diff_command:
        fail("diff_command must be a non-empty array")

    result = subprocess.run(
        diff_command,
        cwd=workspace,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        fail(f"diff_command failed with code {result.returncode}")

    print("evaluator-bundle-valid")


if __name__ == "__main__":
    main()
