#!/usr/bin/env python3
"""Run benchmark candidates against local sandbox tasks using Codex CLI."""

import argparse
import json
import shutil
import subprocess
import time
from pathlib import Path

import yaml

from build_evaluator_manifest import build_manifest, dump_manifest
from validate_evaluator_bundle import validate_manifest


REPO_ROOT = Path(__file__).resolve().parent.parent
SANDBOX_ROOT = REPO_ROOT / "sandboxes"
ARTIFACT_ROOT = REPO_ROOT / "artifacts" / "benchmark_runs"
REVIEW_SCHEMA = REPO_ROOT / "benchmark" / "review_findings.schema.json"
PROMPTS = {
    "c0": REPO_ROOT / "agents" / "candidates" / "c0-solo.prompt.md",
    "c2_triage": REPO_ROOT / "agents" / "candidates" / "c2-triage.prompt.md",
    "c2_execution": REPO_ROOT / "agents" / "candidates" / "c2-execution.prompt.md",
    "review": REPO_ROOT / "agents" / "evaluators" / "review-evaluator.prompt.md",
    "security": REPO_ROOT / "agents" / "evaluators" / "security-evaluator.prompt.md",
    "release_gate": REPO_ROOT / "agents" / "evaluators" / "release-gate-evaluator.prompt.md",
    "architecture": REPO_ROOT / "agents" / "evaluators" / "architecture-evaluator.prompt.md",
}
DISAGREEMENT_TEMPLATE = REPO_ROOT / "docs" / "templates" / "DISAGREEMENT_ANALYSIS_TEMPLATE.md"
MAX_CODEX_ATTEMPTS = 3
TRANSIENT_CODEX_ERROR_MARKERS = (
    "failed to connect to websocket",
    "failed to lookup address information",
    "TimedOut",
    "error sending request for url",
)


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text())


def load_json(path: Path):
    return json.loads(path.read_text())


def write_json(path: Path, payload: dict):
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))


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


def render_prompt(path: Path, task_manifest: Path, run_dir: Path = None, workspace: Path = None):
    template = path.read_text()
    return template.format(
        repo_root=str(REPO_ROOT),
        task_manifest=str(task_manifest),
        run_dir=str(run_dir) if run_dir else "",
        workspace=str(workspace) if workspace else "",
    )


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
    combined_elapsed = 0.0
    last_error = None
    for attempt in range(1, MAX_CODEX_ATTEMPTS + 1):
        started_at = time.perf_counter()
        result = subprocess.run(cmd, capture_output=True, text=True)
        elapsed_seconds = round(time.perf_counter() - started_at, 3)
        combined_elapsed += elapsed_seconds
        jsonl_path.write_text(result.stdout)
        if result.stderr:
            jsonl_path.with_suffix(".stderr.txt").write_text(result.stderr)
        if result.returncode == 0:
            return {
                "usage": parse_usage(result.stdout),
                "elapsed_seconds": round(combined_elapsed, 3),
            }

        last_error = result.stderr or result.stdout
        if attempt < MAX_CODEX_ATTEMPTS and any(marker in last_error for marker in TRANSIENT_CODEX_ERROR_MARKERS):
            time.sleep(5 * attempt)
            continue
        raise RuntimeError(last_error)

    raise RuntimeError(last_error or "codex execution failed without stderr/stdout")


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


def summarize_findings(findings: dict):
    return {
        "high": len(findings.get("high", [])),
        "medium": len(findings.get("medium", [])),
        "low": len(findings.get("low", [])),
        "residual_risks": findings.get("residual_risks", []),
    }


def findings_signature(summary: dict):
    return (
        summary.get("high", 0),
        summary.get("medium", 0),
        summary.get("low", 0),
        len(summary.get("residual_risks", [])),
    )


def determine_run_result(gate_results: dict, review_findings: dict, extra_evaluators: dict):
    extra_high_findings = sum(item["summary"]["high"] for item in extra_evaluators.values())
    return (
        "pass"
        if all(v["passed"] for v in gate_results.values())
        and len(review_findings["high"]) == 0
        and extra_high_findings == 0
        else "fail"
    )


def selector_matches(selector: dict, task_manifest: dict, run_cfg: dict):
    if not selector:
        return True

    if selector.get("task_ids") and task_manifest.get("id") not in selector["task_ids"]:
        return False

    if selector.get("task_types") and task_manifest.get("task_type") not in selector["task_types"]:
        return False

    axes = set(task_manifest.get("complexity_axes", []))
    any_axes = set(selector.get("any_complexity_axes", []))
    if any_axes and not axes.intersection(any_axes):
        return False

    all_axes = set(selector.get("all_complexity_axes", []))
    if all_axes and not all_axes.issubset(axes):
        return False

    if selector.get("run_ids") and run_cfg["id"] not in selector["run_ids"]:
        return False

    if selector.get("candidates") and run_cfg["candidate"] not in selector["candidates"]:
        return False

    return True


def get_evaluator_lanes(batch_cfg: dict, task_manifest: dict, run_cfg: dict):
    lanes = {
        "review": {
            "model": batch_cfg["review_evaluator"]["model"],
            "effort": batch_cfg["review_evaluator"]["effort"],
        }
    }

    for lane, lane_cfg in batch_cfg.get("additional_evaluators", {}).items():
        if not lane_cfg.get("enabled", True):
            continue
        if selector_matches(lane_cfg.get("when", {}), task_manifest, run_cfg):
            lanes[lane] = {
                "model": lane_cfg["model"],
                "effort": lane_cfg["effort"],
            }

    return lanes


def list_existing_run_dirs(batch_root: Path):
    return sorted(
        path
        for path in batch_root.iterdir()
        if path.is_dir() and (path / "workspace" / "benchmark_task.json").exists()
    )


def missing_existing_run_artifacts(run_dir: Path):
    required = [
        run_dir / "workspace" / "benchmark_task.json",
        run_dir / "gate_results.json",
        run_dir / "review_findings.json",
        run_dir / "trace_record.json",
    ]
    return [str(path.relative_to(run_dir)) for path in required if not path.exists()]


def parse_run_dir_name(run_dir: Path):
    try:
        return run_dir.name.rsplit("__", 1)
    except ValueError as exc:
        raise ValueError(f"run directory name must look like <run_id>__<task_id>: {run_dir.name}") from exc


def resolve_existing_run_cfg(run_dir: Path, batch_cfg: dict, task_manifest: dict):
    run_id, task_id = parse_run_dir_name(run_dir)
    matched = next((run for run in batch_cfg.get("runs", []) if run["id"] == run_id), None)
    if matched:
        return matched, run_id, task_id

    trace = load_json(run_dir / "trace_record.json")
    return {
        "id": run_id,
        "candidate": trace["candidate_id"],
        "roles": trace["model_mapping"],
    }, run_id, task_id


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
    prompt = render_prompt(PROMPTS["review"], task_manifest_path, run_dir=run_dir, workspace=workspace)
    result = run_codex(prompt, workspace, model, effort, output_path, jsonl_path, schema=REVIEW_SCHEMA)
    findings = load_json(output_path)
    return findings, result


def reuse_review(run_dir: Path, existing_trace: dict):
    return load_json(run_dir / "review_findings.json"), {
        "usage": existing_trace.get("usage", {}).get("review", {}),
        "elapsed_seconds": existing_trace.get("timing", {}).get("review_seconds", 0.0),
    }


def write_evaluator_index(run_dir: Path, review_manifest_path: Path, review_findings: dict, evaluator_lanes: dict, extra_evaluators: dict):
    evaluator_dir = run_dir / "evaluators"
    evaluator_dir.mkdir(exist_ok=True)
    payload = {
        "review": {
            "model": evaluator_lanes["review"],
            "manifest_path": str(review_manifest_path),
            "findings_path": str(run_dir / "review_findings.json"),
            "summary": summarize_findings(review_findings),
        },
        "additional_lanes": extra_evaluators,
    }
    write_json(evaluator_dir / "index.json", payload)


def create_disagreement_scaffold(run_dir: Path, task_id: str, lane: str, review_summary: dict, lane_summary: dict):
    evaluator_dir = run_dir / "evaluators"
    evaluator_dir.mkdir(exist_ok=True)
    output_path = evaluator_dir / f"disagreement_{lane}.md"
    template_name = DISAGREEMENT_TEMPLATE.name

    body = f"""# Disagreement Analysis

Autogenerated scaffold based on `{template_name}`.

## Context

- batch id: `{run_dir.parent.name}`
- task id: `{task_id}`
- lane: `{lane}`
- compared evaluators: `review` vs `{lane}`
- human reviewer involved: `TBD`

## Disagreement Summary

- 무엇이 충돌했는가: `review`와 `{lane}`의 severity 분포가 다르다.
- verdict mismatch: `review high={review_summary['high']}` / `{lane} high={lane_summary['high']}`
- severity mismatch: `review=({review_summary['high']},{review_summary['medium']},{review_summary['low']})`, `{lane}=({lane_summary['high']},{lane_summary['medium']},{lane_summary['low']})`
- release / approval mismatch: `TBD`

## Shared Evidence

- task brief: `{run_dir / 'workspace' / 'benchmark_outputs' / 'task_brief.md'}`
- diff: `git diff HEAD` from `{run_dir / 'workspace'}`
- trace: `{run_dir / 'trace_record.json'}`
- review findings: `{run_dir / 'review_findings.json'}`
- governance artifacts: `{run_dir / 'evaluators' / f'{lane}_findings.json'}`

## Interpretation Gap

- evaluator A는 어떻게 해석했는가: `review` 결과를 기준으로 정리 필요
- evaluator B 또는 human은 어떻게 해석했는가: `{lane}` 결과를 기준으로 정리 필요
- 어느 artifact가 가장 다르게 읽혔는가: `TBD`

## Root Cause Guess

- prompt issue: `TBD`
- rubric issue: `TBD`
- missing artifact issue: `TBD`
- owner metadata issue: `TBD`
- true ambiguity: `TBD`

## Resolution

- 최종 accepted interpretation: `TBD`
- 왜 그렇게 결정했는가: `TBD`
- next batch에서 무엇을 바꿀 것인가: `TBD`

## Registry / Prompt Follow-Up

- registry update needed: `TBD`
- evaluator prompt update needed: `TBD`
- trigger narrowing needed: `TBD`
- additional human calibration needed: `TBD`
"""
    output_path.write_text(body)
    return output_path


def run_additional_evaluator(lane: str, task_manifest_path: Path, workspace: Path, model: str, effort: str, run_dir: Path):
    evaluator_dir = run_dir / "evaluators"
    evaluator_dir.mkdir(exist_ok=True)

    manifest = build_manifest(run_dir, lane)
    manifest_path = evaluator_dir / f"{lane}_manifest.json"
    dump_manifest(manifest, manifest_path)
    validate_manifest(manifest)

    output_path = evaluator_dir / f"{lane}_findings.json"
    jsonl_path = evaluator_dir / f"{lane}_codex_events.jsonl"
    prompt = render_prompt(PROMPTS[lane], task_manifest_path, run_dir=run_dir, workspace=workspace)
    result = run_codex(prompt, workspace, model, effort, output_path, jsonl_path, schema=REVIEW_SCHEMA)
    findings = load_json(output_path)

    return findings, result, manifest_path, output_path


def execute_evaluators(
    run_cfg: dict,
    batch_cfg: dict,
    task_manifest: dict,
    task_manifest_path: Path,
    workspace: Path,
    run_dir: Path,
    *,
    existing_trace: dict = None,
    reuse_existing_review: bool = False,
):
    evaluator_lanes = get_evaluator_lanes(batch_cfg, task_manifest, run_cfg)
    if reuse_existing_review and existing_trace is not None and (run_dir / "review_findings.json").exists():
        review_findings, review_result = reuse_review(run_dir, existing_trace)
    else:
        review_findings, review_result = run_review(
            task_manifest_path,
            workspace,
            evaluator_lanes["review"]["model"],
            evaluator_lanes["review"]["effort"],
            run_dir,
        )

    evaluator_dir = run_dir / "evaluators"
    evaluator_dir.mkdir(exist_ok=True)
    review_manifest = build_manifest(run_dir, "review")
    review_manifest_path = evaluator_dir / "review_manifest.json"
    dump_manifest(review_manifest, review_manifest_path)
    validate_manifest(review_manifest)

    extra_evaluators = {}
    disagreement_docs = {}
    review_summary = summarize_findings(review_findings)
    for lane, lane_cfg in evaluator_lanes.items():
        if lane == "review":
            continue
        findings, result, manifest_path, output_path = run_additional_evaluator(
            lane,
            task_manifest_path,
            workspace,
            lane_cfg["model"],
            lane_cfg["effort"],
            run_dir,
        )
        extra_evaluators[lane] = {
            "model": lane_cfg,
            "manifest_path": str(manifest_path),
            "findings_path": str(output_path),
            "summary": summarize_findings(findings),
            "usage": result["usage"],
            "elapsed_seconds": result["elapsed_seconds"],
        }
        lane_summary = extra_evaluators[lane]["summary"]
        if findings_signature(review_summary) != findings_signature(lane_summary):
            disagreement_docs[lane] = str(
                create_disagreement_scaffold(run_dir, task_manifest["id"], lane, review_summary, lane_summary)
            )

    for lane, path in disagreement_docs.items():
        extra_evaluators[lane]["disagreement_path"] = path

    write_evaluator_index(
        run_dir,
        review_manifest_path,
        review_findings,
        evaluator_lanes,
        extra_evaluators,
    )
    return evaluator_lanes, review_findings, review_result, extra_evaluators, disagreement_docs


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
    evaluator_lanes = get_evaluator_lanes(batch_cfg, task_manifest, run_cfg)

    started_at = time.perf_counter()
    if run_cfg["candidate"] == "c0":
        candidate_result = run_c0(task_manifest_path, workspace, run_cfg["roles"]["solo"], run_dir)
    elif run_cfg["candidate"] == "c2":
        candidate_result = run_c2(task_manifest_path, workspace, run_cfg["roles"], run_dir)
    else:
        raise ValueError(f"Unsupported candidate {run_cfg['candidate']}")

    gate_results = run_gate_commands(task_manifest, workspace)
    changed_files = git_changed_files(workspace)
    evaluator_lanes, review_findings, review_result, extra_evaluators, disagreement_docs = execute_evaluators(
        run_cfg,
        batch_cfg,
        task_manifest,
        task_manifest_path,
        workspace,
        run_dir,
    )

    failure_tags = classify_failures(gate_results, changed_files)
    trace = {
        "run_id": f"{run_id}__{task_id}",
        "candidate_id": run_cfg["candidate"],
        "task_id": task_id,
        "model_mapping": run_cfg["roles"],
        "review_model": evaluator_lanes["review"],
        "evaluator_lanes": evaluator_lanes,
        "changed_files": changed_files,
        "gate_results": {k: v["passed"] for k, v in gate_results.items()},
        "review_results": summarize_findings(review_findings),
        "evaluator_results": {lane: item["summary"] for lane, item in extra_evaluators.items()},
        "disagreement_docs": disagreement_docs,
        "failure_taxonomy": failure_tags,
        "usage": {
            "candidate": candidate_result["usage"],
            "review": review_result["usage"],
            "evaluators": {lane: item["usage"] for lane, item in extra_evaluators.items()},
        },
        "timing": {
            "candidate": candidate_result["timing"],
            "review_seconds": review_result["elapsed_seconds"],
            "evaluator_seconds": {lane: item["elapsed_seconds"] for lane, item in extra_evaluators.items()},
            "gate_seconds": {
                key: value["elapsed_seconds"] for key, value in gate_results.items()
            },
            "total_seconds": round(time.perf_counter() - started_at, 3),
        },
        "result": determine_run_result(gate_results, review_findings, extra_evaluators),
    }
    write_trace(run_dir, trace)
    write_json(run_dir / "gate_results.json", gate_results)
    return trace


def evaluate_existing_run(run_dir: Path, batch_cfg: dict, *, reuse_existing_review: bool = False):
    run_dir = run_dir.resolve()
    workspace = run_dir / "workspace"
    task_manifest_path = workspace / "benchmark_task.json"
    task_manifest = load_json(task_manifest_path)
    run_cfg, run_id, task_id = resolve_existing_run_cfg(run_dir, batch_cfg, task_manifest)

    changed_files = git_changed_files(workspace)
    gate_results = load_json(run_dir / "gate_results.json")
    existing_trace = load_json(run_dir / "trace_record.json")

    evaluator_lanes, review_findings, review_result, extra_evaluators, disagreement_docs = execute_evaluators(
        run_cfg,
        batch_cfg,
        task_manifest,
        task_manifest_path,
        workspace,
        run_dir,
        existing_trace=existing_trace,
        reuse_existing_review=reuse_existing_review,
    )

    updated_trace = dict(existing_trace)
    updated_trace.update(
        {
            "run_id": f"{run_id}__{task_id}",
            "candidate_id": run_cfg["candidate"],
            "task_id": task_id,
            "model_mapping": run_cfg["roles"],
            "review_model": evaluator_lanes["review"],
            "evaluator_lanes": evaluator_lanes,
            "changed_files": changed_files,
            "gate_results": {k: v["passed"] for k, v in gate_results.items()},
            "review_results": summarize_findings(review_findings),
            "evaluator_results": {lane: item["summary"] for lane, item in extra_evaluators.items()},
            "disagreement_docs": disagreement_docs,
            "result": determine_run_result(gate_results, review_findings, extra_evaluators),
        }
    )

    usage = dict(updated_trace.get("usage", {}))
    usage["review"] = review_result["usage"]
    usage["evaluators"] = {lane: item["usage"] for lane, item in extra_evaluators.items()}
    updated_trace["usage"] = usage

    timing = dict(updated_trace.get("timing", {}))
    timing["review_seconds"] = review_result["elapsed_seconds"]
    timing["evaluator_seconds"] = {lane: item["elapsed_seconds"] for lane, item in extra_evaluators.items()}
    updated_trace["timing"] = timing

    write_trace(run_dir, updated_trace)
    update_batch_summary(run_dir.parent.name, updated_trace)
    return updated_trace


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=str(REPO_ROOT / "benchmark" / "initial_matrix.yaml"))
    parser.add_argument("--run-id")
    parser.add_argument("--task-id")
    parser.add_argument("--existing-run-dir")
    parser.add_argument("--existing-batch-root")
    parser.add_argument("--reuse-existing-review", action="store_true")
    parser.add_argument("--plan-only", action="store_true")
    args = parser.parse_args()

    batch_cfg = load_yaml(Path(args.config))
    if args.existing_batch_root:
        batch_root = Path(args.existing_batch_root)
        plans = []
        skipped = []
        failures = []
        for run_dir in list_existing_run_dirs(batch_root):
            missing = missing_existing_run_artifacts(run_dir)
            if missing:
                skipped.append({"run_dir": str(run_dir), "missing": missing})
                continue
            task_manifest = load_json(run_dir / "workspace" / "benchmark_task.json")
            run_cfg, run_id, task_id = resolve_existing_run_cfg(run_dir, batch_cfg, task_manifest)
            if args.run_id and run_id != args.run_id:
                continue
            if args.task_id and task_id != args.task_id:
                continue
            if args.plan_only:
                plans.append(
                    {
                        "run_dir": str(run_dir),
                        "run_id": run_id,
                        "task_id": task_id,
                        "candidate": run_cfg["candidate"],
                        "evaluator_lanes": get_evaluator_lanes(batch_cfg, task_manifest, run_cfg),
                    }
                )
                continue
            print(f"==> backfilling evaluators for {run_dir.name}")
            try:
                trace = evaluate_existing_run(run_dir, batch_cfg, reuse_existing_review=args.reuse_existing_review)
            except Exception as exc:  # noqa: BLE001
                failures.append({"run_dir": str(run_dir), "error": str(exc)})
                print(json.dumps({"run_dir": str(run_dir), "error": str(exc)}, indent=2))
                continue
            print(json.dumps(trace, indent=2))
        if args.plan_only:
            print(json.dumps({"planned": plans, "skipped": skipped}, indent=2))
        else:
            print(json.dumps({"skipped": skipped, "failures": failures}, indent=2))
        return

    if args.existing_run_dir:
        run_dir = Path(args.existing_run_dir)
        task_manifest = load_json(run_dir / "workspace" / "benchmark_task.json")
        run_cfg, run_id, task_id = resolve_existing_run_cfg(run_dir, batch_cfg, task_manifest)
        if args.plan_only:
            plan = {
                "run_id": run_id,
                "task_id": task_id,
                "candidate": run_cfg["candidate"],
                "evaluator_lanes": get_evaluator_lanes(batch_cfg, task_manifest, run_cfg),
            }
            print(json.dumps(plan, indent=2))
            return
        trace = evaluate_existing_run(run_dir, batch_cfg, reuse_existing_review=args.reuse_existing_review)
        print(json.dumps(trace, indent=2))
        return

    runs = batch_cfg["runs"]
    if args.run_id:
        runs = [run for run in runs if run["id"] == args.run_id]
    tasks = batch_cfg["tasks"]
    if args.task_id:
        tasks = [task for task in tasks if task == args.task_id]

    for run_cfg in runs:
        for task_id in tasks:
            task_manifest = load_json(SANDBOX_ROOT / task_id / "benchmark_task.json")
            if args.plan_only:
                plan = {
                    "run_id": run_cfg["id"],
                    "task_id": task_id,
                    "candidate": run_cfg["candidate"],
                    "evaluator_lanes": get_evaluator_lanes(batch_cfg, task_manifest, run_cfg),
                }
                print(json.dumps(plan, indent=2))
                continue
            print(f"==> running {run_cfg['id']} on {task_id}")
            trace = benchmark_one(run_cfg, batch_cfg, task_id)
            update_batch_summary(batch_cfg["batch_id"], trace)
            print(json.dumps(trace, indent=2))


if __name__ == "__main__":
    main()
