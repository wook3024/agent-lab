#!/usr/bin/env python3
"""Run benchmark candidates against local sandbox tasks using Codex CLI."""

import argparse
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parent.parent
SANDBOX_ROOT = REPO_ROOT / "sandboxes"
ARTIFACT_ROOT = REPO_ROOT / "artifacts" / "benchmark_runs"
REVIEW_SCHEMA = REPO_ROOT / "benchmark" / "review_findings.schema.json"
PROMPTS = {
    "c0": REPO_ROOT / "agents" / "candidates" / "c0-solo.prompt.md",
    "c2_triage": REPO_ROOT / "agents" / "candidates" / "c2-triage.prompt.md",
    "c2_execution": REPO_ROOT / "agents" / "candidates" / "c2-execution.prompt.md",
    "review": REPO_ROOT / "agents" / "evaluators" / "review-evaluator.prompt.md",
}


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text())


def load_json(path: Path):
    return json.loads(path.read_text())


def ensure_clean_dir(path: Path):
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def init_git_repo(workspace: Path):
    subprocess.run(["git", "init", "-q"], cwd=workspace, check=True)
    subprocess.run(["git", "config", "user.name", "Benchmark Bot"], cwd=workspace, check=True)
    subprocess.run(["git", "config", "user.email", "benchmark@example.com"], cwd=workspace, check=True)
    subprocess.run(["git", "add", "."], cwd=workspace, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "baseline"], cwd=workspace, check=True)


def render_prompt(path: Path, task_manifest: Path):
    template = path.read_text()
    return template.format(repo_root=str(REPO_ROOT), task_manifest=str(task_manifest))


def run_codex(prompt: str, workspace: Path, model: str, effort: str, output_path: Path, jsonl_path: Path, schema: Path = None):
    cmd = [
        "codex",
        "-a",
        "never",
        "exec",
        "-m",
        model,
        "-c",
        f'model_reasoning_effort="{effort}"',
        "--sandbox",
        "workspace-write",
        "--add-dir",
        str(REPO_ROOT),
        "--json",
        "--output-last-message",
        str(output_path),
        "-C",
        str(workspace),
        "--skip-git-repo-check",
    ]
    if schema is not None:
        cmd.extend(["--output-schema", str(schema)])
    cmd.append(prompt)
    started_at = time.perf_counter()
    result = subprocess.run(cmd, capture_output=True, text=True)
    elapsed_seconds = round(time.perf_counter() - started_at, 3)
    jsonl_path.write_text(result.stdout)
    if result.stderr:
        jsonl_path.with_suffix(".stderr.txt").write_text(result.stderr)
    if result.returncode != 0:
        raise RuntimeError(result.stderr or result.stdout)
    return {
        "usage": parse_usage(result.stdout),
        "elapsed_seconds": elapsed_seconds,
    }


def parse_usage(jsonl_text: str):
    usage = {}
    for line in jsonl_text.splitlines():
        line = line.strip()
        if not line or not line.startswith("{"):
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "turn.completed":
            usage = event.get("usage", {})
    return usage


def run_gate_commands(task_manifest: dict, workspace: Path):
    results = {}
    for gate in task_manifest.get("gate_commands", []):
        started_at = time.perf_counter()
        proc = subprocess.run(
            gate["cmd"],
            cwd=workspace,
            shell=True,
            capture_output=True,
            text=True,
        )
        results[gate["name"]] = {
            "passed": proc.returncode == 0,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "returncode": proc.returncode,
            "elapsed_seconds": round(time.perf_counter() - started_at, 3),
        }
    return results


def git_changed_files(workspace: Path):
    proc = subprocess.run(
        ["git", "diff", "--name-only"],
        cwd=workspace,
        capture_output=True,
        text=True,
        check=True,
    )
    return [line for line in proc.stdout.splitlines() if line.strip()]


def classify_failures(gate_results: dict, changed_files):
    tags = []
    if any(not item["passed"] for item in gate_results.values()):
        if "docs_sync_check" in gate_results and not gate_results["docs_sync_check"]["passed"]:
            tags.append("docs_desync")
        if "tests_pass" in gate_results and not gate_results["tests_pass"]["passed"]:
            tags.append("missed_test")
    if len(changed_files) > 6:
        tags.append("over_edit")
    return sorted(set(tags))


def write_trace(run_dir: Path, payload: dict):
    trace_path = run_dir / "trace_record.json"
    trace_path.write_text(json.dumps(payload, indent=2))


def update_batch_summary(batch_id: str, trace: dict):
    out_path = ARTIFACT_ROOT / batch_id / "batch_summary.json"
    existing = []
    if out_path.exists():
        try:
            existing = json.loads(out_path.read_text())
        except json.JSONDecodeError:
            existing = []

    by_run_id = {item["run_id"]: item for item in existing if "run_id" in item}
    by_run_id[trace["run_id"]] = trace
    merged = [by_run_id[key] for key in sorted(by_run_id)]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(merged, indent=2))


def run_review(task_manifest_path: Path, workspace: Path, model: str, effort: str, run_dir: Path):
    output_path = run_dir / "review_findings.json"
    jsonl_path = run_dir / "review_codex_events.jsonl"
    prompt = render_prompt(PROMPTS["review"], task_manifest_path)
    result = run_codex(prompt, workspace, model, effort, output_path, jsonl_path, schema=REVIEW_SCHEMA)
    findings = load_json(output_path)
    return findings, result


def run_c0(task_manifest_path: Path, workspace: Path, role_cfg: dict, run_dir: Path):
    output_path = run_dir / "c0_last_message.txt"
    jsonl_path = run_dir / "c0_codex_events.jsonl"
    prompt = render_prompt(PROMPTS["c0"], task_manifest_path)
    result = run_codex(prompt, workspace, role_cfg["model"], role_cfg["effort"], output_path, jsonl_path)
    return {
        "usage": {"solo_usage": result["usage"]},
        "timing": {"solo_seconds": result["elapsed_seconds"]},
    }


def run_c2(task_manifest_path: Path, workspace: Path, roles: dict, run_dir: Path):
    triage_output = run_dir / "c2_triage_last_message.txt"
    triage_jsonl = run_dir / "c2_triage_codex_events.jsonl"
    triage_prompt = render_prompt(PROMPTS["c2_triage"], task_manifest_path)
    triage_result = run_codex(
        triage_prompt,
        workspace,
        roles["triage"]["model"],
        roles["triage"]["effort"],
        triage_output,
        triage_jsonl,
    )

    execution_output = run_dir / "c2_execution_last_message.txt"
    execution_jsonl = run_dir / "c2_execution_codex_events.jsonl"
    execution_prompt = render_prompt(PROMPTS["c2_execution"], task_manifest_path)
    execution_result = run_codex(
        execution_prompt,
        workspace,
        roles["execution"]["model"],
        roles["execution"]["effort"],
        execution_output,
        execution_jsonl,
    )
    return {
        "usage": {
            "triage_usage": triage_result["usage"],
            "execution_usage": execution_result["usage"],
        },
        "timing": {
            "triage_seconds": triage_result["elapsed_seconds"],
            "execution_seconds": execution_result["elapsed_seconds"],
        },
    }


def create_workspace(task_id: str, run_id: str, batch_id: str):
    source = SANDBOX_ROOT / task_id
    run_dir = ARTIFACT_ROOT / batch_id / f"{run_id}__{task_id}"
    workspace = run_dir / "workspace"
    ensure_clean_dir(run_dir)
    shutil.copytree(source, workspace)
    (workspace / "benchmark_outputs").mkdir(exist_ok=True)
    init_git_repo(workspace)
    return run_dir, workspace


def benchmark_one(run_cfg: dict, batch_cfg: dict, task_id: str):
    run_id = run_cfg["id"]
    batch_id = batch_cfg["batch_id"]
    run_dir, workspace = create_workspace(task_id, run_id, batch_id)
    task_manifest_path = workspace / "benchmark_task.json"
    task_manifest = load_json(task_manifest_path)

    started_at = time.perf_counter()
    if run_cfg["candidate"] == "c0":
        candidate_result = run_c0(task_manifest_path, workspace, run_cfg["roles"]["solo"], run_dir)
    elif run_cfg["candidate"] == "c2":
        candidate_result = run_c2(task_manifest_path, workspace, run_cfg["roles"], run_dir)
    else:
        raise ValueError(f"Unsupported candidate {run_cfg['candidate']}")

    gate_results = run_gate_commands(task_manifest, workspace)
    changed_files = git_changed_files(workspace)
    review_findings, review_result = run_review(
        task_manifest_path,
        workspace,
        batch_cfg["review_evaluator"]["model"],
        batch_cfg["review_evaluator"]["effort"],
        run_dir,
    )

    failure_tags = classify_failures(gate_results, changed_files)
    trace = {
        "run_id": f"{run_id}__{task_id}",
        "candidate_id": run_cfg["candidate"],
        "task_id": task_id,
        "model_mapping": run_cfg["roles"],
        "review_model": batch_cfg["review_evaluator"],
        "changed_files": changed_files,
        "gate_results": {k: v["passed"] for k, v in gate_results.items()},
        "review_results": {
            "high": len(review_findings["high"]),
            "medium": len(review_findings["medium"]),
            "low": len(review_findings["low"]),
        },
        "failure_taxonomy": failure_tags,
        "usage": {
            "candidate": candidate_result["usage"],
            "review": review_result["usage"],
        },
        "timing": {
            "candidate": candidate_result["timing"],
            "review_seconds": review_result["elapsed_seconds"],
            "gate_seconds": {
                key: value["elapsed_seconds"] for key, value in gate_results.items()
            },
            "total_seconds": round(time.perf_counter() - started_at, 3),
        },
        "result": "pass"
        if all(v["passed"] for v in gate_results.values()) and len(review_findings["high"]) == 0
        else "fail",
    }
    write_trace(run_dir, trace)
    summary_path = run_dir / "gate_results.json"
    summary_path.write_text(json.dumps(gate_results, indent=2))
    return trace


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=str(REPO_ROOT / "benchmark" / "initial_matrix.yaml"))
    parser.add_argument("--run-id")
    parser.add_argument("--task-id")
    args = parser.parse_args()

    batch_cfg = load_yaml(Path(args.config))
    runs = batch_cfg["runs"]
    if args.run_id:
        runs = [run for run in runs if run["id"] == args.run_id]
    tasks = batch_cfg["tasks"]
    if args.task_id:
        tasks = [task for task in tasks if task == args.task_id]

    for run_cfg in runs:
        for task_id in tasks:
            print(f"==> running {run_cfg['id']} on {task_id}")
            trace = benchmark_one(run_cfg, batch_cfg, task_id)
            update_batch_summary(batch_cfg["batch_id"], trace)
            print(json.dumps(trace, indent=2))


if __name__ == "__main__":
    main()
