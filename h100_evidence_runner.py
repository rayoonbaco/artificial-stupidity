"""Run and package the preregistered H100 validation + holdout experiment.

This module intentionally keeps the upstream ``prepare.py`` and ``train.py``
untouched. It runs two instrumented derivatives that differ by one functional
line, captures complete output, evaluates the evidence gate, and always builds
an evidence ZIP (including on failure).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import statistics
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from gate.as_gate import Decision, evaluate
from gate.as_gate import _load_json as load_json

BASELINE_SCRIPT = ROOT / "benchmark" / "instrumented" / "train_baseline_holdout.py"
CANDIDATE_SCRIPT = ROOT / "benchmark" / "instrumented" / "train_candidate_holdout.py"
EXPECTED_RUNS = 3
METRIC_NAMES = (
    "val_bpb",
    "holdout_bpb",
    "training_seconds",
    "total_seconds",
    "peak_vram_mb",
    "mfu_percent",
    "total_tokens_M",
    "num_steps",
    "num_params_M",
    "depth",
)
INTEGER_METRICS = {"num_steps", "depth"}
SNAPSHOT_FILES = (
    "prepare.py",
    "train.py",
    "pyproject.toml",
    "uv.lock",
    "benchmark/protected_holdout.py",
    "benchmark/instrumented/train_baseline_holdout.py",
    "benchmark/instrumented/train_candidate_holdout.py",
    "benchmark/H100_RERUN_PROTOCOL.md",
    "gate/as_gate.py",
    "gate/gate_config.json",
)


def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_metrics(text: str) -> dict[str, float | int]:
    """Parse only the final labeled metrics emitted by the training scripts."""
    values: dict[str, float | int] = {}
    for name in METRIC_NAMES:
        matches = re.findall(rf"(?m)^{re.escape(name)}:\s+(-?\d+(?:\.\d+)?)\s*$", text)
        if matches:
            number = float(matches[-1])
            values[name] = int(number) if name in INTEGER_METRICS else number
    return values


def _metric_state(
    baseline: list[dict], candidate: list[dict], metric: str, expected_runs: int
) -> str:
    if len(baseline) != expected_runs or len(candidate) != expected_runs:
        return "unknown"
    if any(record.get("exit_code") != 0 for record in baseline + candidate):
        return "unknown"
    try:
        baseline_values = [float(record["metrics"][metric]) for record in baseline]
        candidate_values = [float(record["metrics"][metric]) for record in candidate]
    except (KeyError, TypeError, ValueError):
        return "unknown"
    return "pass" if max(candidate_values) < min(baseline_values) else "fail"


def evaluate_run_sets(
    baseline: list[dict], candidate: list[dict], expected_runs: int = EXPECTED_RUNS
) -> dict:
    """Create gate inputs from complete run records without inventing evidence."""
    repeatability = _metric_state(baseline, candidate, "val_bpb", expected_runs)
    heldout = _metric_state(baseline, candidate, "holdout_bpb", expected_runs)
    complete = len(baseline) == expected_runs and len(candidate) == expected_runs
    exits_ok = complete and all(
        record.get("exit_code") == 0 for record in baseline + candidate
    )
    failure_mode = "pass" if exits_ok else ("fail" if complete else "unknown")

    def metric_values(records: list[dict], name: str) -> list[float]:
        result = []
        for record in records:
            try:
                result.append(float(record["metrics"][name]))
            except (KeyError, TypeError, ValueError):
                pass
        return result

    baseline_val = metric_values(baseline, "val_bpb")
    candidate_val = metric_values(candidate, "val_bpb")
    baseline_holdout = metric_values(baseline, "holdout_bpb")
    candidate_holdout = metric_values(candidate, "holdout_bpb")
    baseline_memory = metric_values(baseline, "peak_vram_mb")
    candidate_memory = metric_values(candidate, "peak_vram_mb")

    summary = {
        "expected_runs_per_arm": expected_runs,
        "baseline_runs_found": len(baseline),
        "candidate_runs_found": len(candidate),
        "baseline_val_bpb": baseline_val,
        "candidate_val_bpb": candidate_val,
        "baseline_holdout_bpb": baseline_holdout,
        "candidate_holdout_bpb": candidate_holdout,
        "checks": {
            "repeatability": repeatability,
            "held_out_robustness": heldout,
            "failure_mode_review": failure_mode,
            "human_comprehensibility": "unknown",
        },
        "interpretation": (
            "The automated run never grants its own human-comprehensibility sign-off. "
            "A machine result can therefore REJECT or ESCALATE, but final KEEP requires "
            "a named human review."
        ),
    }
    if baseline_val:
        summary["baseline_val_median"] = statistics.median(baseline_val)
    if candidate_val:
        summary["candidate_val_median"] = statistics.median(candidate_val)
    if baseline_holdout:
        summary["baseline_holdout_median"] = statistics.median(baseline_holdout)
    if candidate_holdout:
        summary["candidate_holdout_median"] = statistics.median(candidate_holdout)

    baseline_record = None
    candidate_record = None
    if baseline_val and baseline_memory:
        baseline_record = {
            "commit": "instrumented-baseline-total-batch-2pow19",
            "val_bpb": statistics.median(baseline_val),
            "peak_vram_mb": max(baseline_memory),
        }
    if candidate_val and candidate_memory:
        candidate_record = {
            "commit": "candidate-total-batch-2pow18",
            "run_status": "ok" if exits_ok else "failed",
            "val_bpb": statistics.median(candidate_val),
            "peak_vram_mb": max(candidate_memory),
            "complexity_delta_lines": 1,
            "hypothesis": (
                "Halving total batch size improves five-minute validation BPB and "
                "the preregistered protected-holdout BPB on the same H100 setup."
            ),
            "disconfirming_result": (
                "Any failed candidate run, overlapping validation distributions, "
                "or a candidate holdout result that does not beat every baseline run."
            ),
            "checks": summary["checks"],
        }
    return {
        "summary": summary,
        "baseline_gate_record": baseline_record,
        "candidate_gate_record": candidate_record,
    }


def render_report(payload: dict, decision: dict) -> str:
    summary = payload["summary"]

    def shown(key: str) -> str:
        value = summary.get(key)
        return f"{value:.6f}" if isinstance(value, float) else "unavailable"

    checks = summary["checks"]
    return f"""# H100 protected-holdout evidence report

Generated: {datetime.now(timezone.utc).isoformat()}

## Result

- Machine gate action: **{decision['action']}**
- Baseline validation median: **{shown('baseline_val_median')}**
- Candidate validation median: **{shown('candidate_val_median')}**
- Baseline protected-holdout median: **{shown('baseline_holdout_median')}**
- Candidate protected-holdout median: **{shown('candidate_holdout_median')}**
- Repeatability: **{checks['repeatability']}**
- Protected holdout: **{checks['held_out_robustness']}**
- Failure-mode review: **{checks['failure_mode_review']}**
- Human comprehensibility: **{checks['human_comprehensibility']}**

## Interpretation boundary

The preregistered automated boundary requires every candidate score to beat
every baseline score in both validation and protected holdout. The holdout is
sequestered from the upstream data directory, tokenizer, training loader, and
pinned validation shard. It is protected by this harness and its recorded
hash—not cryptographically secret or tamper-proof.

The machine deliberately cannot approve its own human-comprehensibility check.
Even when all empirical checks pass, the automated result remains **ESCALATE**
until a named human reviews the one-line functional diff and authorizes KEEP.

## Gate reasons

{os.linesep.join('- ' + reason for reason in decision.get('reasons', []))}
"""


def run_logged(command: list[str], log_path: Path, env: dict[str, str]) -> int:
    """Stream a command to the terminal and preserve its complete merged output."""
    print(f"\n$ {' '.join(command)}", flush=True)
    with log_path.open("w", encoding="utf-8", errors="replace") as handle:
        process = subprocess.Popen(
            command,
            cwd=ROOT,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        assert process.stdout is not None
        for line in process.stdout:
            print(line, end="", flush=True)
            handle.write(line)
        return process.wait()


def capture_command(command: list[str]) -> dict:
    try:
        completed = subprocess.run(
            command, cwd=ROOT, text=True, capture_output=True, check=False
        )
    except OSError as exc:
        return {
            "command": command,
            "exit_code": 127,
            "stdout": "",
            "stderr": f"{type(exc).__name__}: {exc}",
        }
    return {
        "command": command,
        "exit_code": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def copy_source_snapshot(destination: Path) -> None:
    for relative in SNAPSHOT_FILES:
        source = ROOT / relative
        target = destination / "source_snapshot" / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def write_manifest(directory: Path) -> None:
    rows = []
    for path in sorted(directory.rglob("*")):
        if path.is_file() and path.name != "SHA256SUMS.txt":
            rows.append(f"{sha256_file(path)}  {path.relative_to(directory).as_posix()}")
    (directory / "SHA256SUMS.txt").write_text("\n".join(rows) + "\n", encoding="utf-8")


def package_evidence(run_dir: Path, archive_path: Path) -> Path:
    write_manifest(run_dir)
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_base = archive_path.with_suffix("")
    created = Path(shutil.make_archive(str(temporary_base), "zip", run_dir.parent, run_dir.name))
    if created != archive_path:
        os.replace(created, archive_path)
    return archive_path


def _write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs", type=int, default=EXPECTED_RUNS)
    parser.add_argument("--output-root", type=Path, default=ROOT.parent / "artificial-stupidity-evidence")
    args = parser.parse_args(list(argv) if argv is not None else None)
    if args.runs != EXPECTED_RUNS:
        parser.error("the preregistered protocol requires exactly three runs per arm")

    stamp = utc_stamp()
    run_dir = args.output_root.resolve() / stamp
    logs_dir = run_dir / "raw_logs"
    logs_dir.mkdir(parents=True, exist_ok=False)
    archive = ROOT.parent / f"artificial-stupidity-h100-evidence-{stamp}.zip"
    download_alias = ROOT.parent / "ARTIFICIAL_STUPIDITY_H100_EVIDENCE_DOWNLOAD_ME.zip"
    baseline_runs: list[dict] = []
    candidate_runs: list[dict] = []
    final_exit = 1

    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    environment = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "platform": platform.platform(),
        "python": sys.version,
        "commands": {},
    }

    try:
        environment["commands"]["nvidia_smi"] = capture_command(["nvidia-smi"])
        environment["commands"]["nvidia_query"] = capture_command(
            ["nvidia-smi", "--query-gpu=name,memory.total,driver_version", "--format=csv,noheader"]
        )
        environment["commands"]["git_head"] = capture_command(
            ["git", "rev-parse", "HEAD"]
        )
        environment["commands"]["packages"] = capture_command(
            [shutil.which("uv") or "uv", "pip", "freeze"]
        )
        _write_json(run_dir / "environment.json", environment)

        query = environment["commands"]["nvidia_query"]
        if query["exit_code"] != 0 or "H100" not in query["stdout"]:
            raise RuntimeError("preregistered hardware check failed: one NVIDIA H100 is required")
        gpu_lines = [line for line in query["stdout"].splitlines() if line.strip()]
        if len(gpu_lines) != 1:
            raise RuntimeError("preregistered hardware check failed: exactly one GPU is required")

        copy_source_snapshot(run_dir)
        preparation = run_logged(
            [sys.executable, "prepare.py"], logs_dir / "prepare.log", env
        )
        if preparation != 0:
            raise RuntimeError(f"upstream preparation failed with exit code {preparation}")
        holdout_prep = run_logged(
            [sys.executable, "benchmark/protected_holdout.py", "--prepare"],
            logs_dir / "protected_holdout_prepare.log",
            env,
        )
        if holdout_prep != 0:
            raise RuntimeError(f"protected holdout preparation failed with exit code {holdout_prep}")

        order = []
        for index in range(1, args.runs + 1):
            order.extend((("baseline", index, BASELINE_SCRIPT), ("candidate", index, CANDIDATE_SCRIPT)))
        _write_json(
            run_dir / "preregistered_order.json",
            [{"arm": arm, "run": index, "script": str(script.relative_to(ROOT))} for arm, index, script in order],
        )

        for arm, index, script in order:
            log_path = logs_dir / f"{arm}_{index}.log"
            started = datetime.now(timezone.utc).isoformat()
            exit_code = run_logged([sys.executable, str(script)], log_path, env)
            text = log_path.read_text(encoding="utf-8", errors="replace")
            record = {
                "arm": arm,
                "run": index,
                "started_at_utc": started,
                "exit_code": exit_code,
                "log": str(log_path.relative_to(run_dir)),
                "log_sha256": sha256_file(log_path),
                "metrics": parse_metrics(text),
            }
            (baseline_runs if arm == "baseline" else candidate_runs).append(record)
            _write_json(run_dir / "results_in_progress.json", {
                "baseline": baseline_runs, "candidate": candidate_runs
            })

        evidence = evaluate_run_sets(baseline_runs, candidate_runs, args.runs)
        all_records = baseline_runs + candidate_runs
        complete_failed_run = (
            len(baseline_runs) == args.runs
            and len(candidate_runs) == args.runs
            and any(record.get("exit_code") != 0 for record in all_records)
        )
        if complete_failed_run:
            decision = Decision(
                "REJECT", ["one or more preregistered training runs failed"]
            ).to_dict()
        elif evidence["baseline_gate_record"] and evidence["candidate_gate_record"]:
            decision = evaluate(
                evidence["baseline_gate_record"],
                evidence["candidate_gate_record"],
                load_json(ROOT / "gate" / "gate_config.json"),
            ).to_dict()
        else:
            decision = Decision(
                "ESCALATE", ["complete, trustworthy gate inputs were not produced"]
            ).to_dict()
        _write_json(run_dir / "results.json", {
            "baseline": baseline_runs,
            "candidate": candidate_runs,
            **evidence,
            "machine_gate_decision": decision,
        })
        _write_json(run_dir / "machine_gate_decision.json", decision)
        (run_dir / "REPORT.md").write_text(render_report(evidence, decision), encoding="utf-8")
        final_exit = {"KEEP": 0, "REJECT": 2, "ESCALATE": 3}[decision["action"]]
    except Exception as exc:  # package the failure evidence before returning
        error = {"type": type(exc).__name__, "message": str(exc)}
        _write_json(run_dir / "RUNNER_FAILURE.json", error)
        print(f"\nRUNNER FAILURE: {exc}", file=sys.stderr, flush=True)
        final_exit = 1
    finally:
        if not (run_dir / "results.json").exists():
            partial = evaluate_run_sets(baseline_runs, candidate_runs, args.runs)
            _write_json(run_dir / "partial_results.json", {
                "baseline": baseline_runs, "candidate": candidate_runs, **partial
            })
        if not (run_dir / "source_snapshot").exists():
            copy_source_snapshot(run_dir)
        package_evidence(run_dir, archive)
        shutil.copy2(archive, download_alias)
        print("\nEVIDENCE PACKAGE READY", flush=True)
        print(f"Unique archive: {archive}", flush=True)
        print(f"DOWNLOAD THIS FILE: {download_alias}", flush=True)
        print("Stop or terminate the RunPod after downloading the ZIP.", flush=True)

    return final_exit


if __name__ == "__main__":
    raise SystemExit(main())
