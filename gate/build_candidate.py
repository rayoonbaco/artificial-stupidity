"""Build a gate candidate record from an autoresearch run log and evidence file."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from gate.as_gate import build_evidence_bundle


SUMMARY_FIELD = re.compile(r"^(val_bpb|peak_vram_mb):\s*([0-9]+(?:\.[0-9]+)?)\s*$")


def parse_run_summary(text: str) -> dict[str, float]:
    found: dict[str, float] = {}
    for line in text.splitlines():
        match = SUMMARY_FIELD.match(line.strip())
        if match:
            found[match.group(1)] = float(match.group(2))
    missing = {"val_bpb", "peak_vram_mb"} - found.keys()
    if missing:
        raise ValueError("run log is missing: " + ", ".join(sorted(missing)))
    return found


def diff_line_count(repo: Path, base_ref: str) -> int:
    result = subprocess.run(
        ["git", "diff", "--numstat", base_ref, "--", "train.py"],
        cwd=repo, check=True, capture_output=True, text=True,
    )
    total = 0
    for line in result.stdout.splitlines():
        added, removed, *_ = line.split("\t")
        if added.isdigit():
            total += int(added)
        if removed.isdigit():
            total += int(removed)
    return total


def build_record(summary: dict[str, float], evidence: dict[str, Any], complexity: int) -> dict[str, Any]:
    """Build only candidate-controlled facts; authority fields stay separate."""
    return {
        "commit": evidence.get("commit", "uncommitted"),
        "run_status": evidence.get("run_status", "ok"),
        "val_bpb": summary["val_bpb"],
        "peak_vram_mb": summary["peak_vram_mb"],
        "complexity_delta_lines": complexity,
        "hypothesis": evidence.get("hypothesis", ""),
        "disconfirming_result": evidence.get("disconfirming_result", ""),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a candidate record from a run")
    parser.add_argument("--run-log", required=True)
    parser.add_argument("--evidence", required=True)
    parser.add_argument("--base-ref", required=True)
    parser.add_argument("--repo", default=".")
    parser.add_argument("--output", required=True)
    parser.add_argument("--evidence-output", required=True)
    parser.add_argument(
        "--config", default=str(Path(__file__).with_name("gate_config.json"))
    )
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    summary = parse_run_summary(Path(args.run_log).read_text(encoding="utf-8"))
    evidence = json.loads(Path(args.evidence).read_text(encoding="utf-8"))
    record = build_record(summary, evidence, diff_line_count(repo, args.base_ref))
    checks = evidence.get("checks")
    producers = evidence.get("producers")
    if not isinstance(checks, dict) or not isinstance(producers, dict):
        raise ValueError("evidence input must contain checks and producers objects")
    config = json.loads(Path(args.config).read_text(encoding="utf-8"))
    bundle = build_evidence_bundle(record, config, checks, producers)
    Path(args.output).write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    Path(args.evidence_output).write_text(
        json.dumps(bundle, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
