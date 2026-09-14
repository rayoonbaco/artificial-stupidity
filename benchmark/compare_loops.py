"""Replay one experiment sequence through the original and gated acceptance rules."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from gate.as_gate import (
    Decision,
    _load_json,
    build_evidence_bundle,
    canonical_sha256,
    evaluate,
)


def load_object(path: str | Path) -> dict[str, Any]:
    return _load_json(path)


def original_decision(baseline: dict[str, Any], candidate: dict[str, Any]) -> str:
    """Model the upstream acceptance rule without claiming more than it does."""
    if candidate.get("run_status", "ok") != "ok":
        return "REJECT"
    baseline_bpb = baseline.get("val_bpb")
    candidate_bpb = candidate.get("val_bpb")
    if isinstance(baseline_bpb, bool) or not isinstance(baseline_bpb, (int, float)):
        raise ValueError("baseline val_bpb must be numeric")
    if isinstance(candidate_bpb, bool) or not isinstance(candidate_bpb, (int, float)):
        raise ValueError("candidate val_bpb must be purportedly numeric")
    return "KEEP" if candidate_bpb < baseline_bpb else "REJECT"


def compare(manifest: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    baseline = manifest.get("baseline")
    experiments = manifest.get("experiments")
    if not isinstance(baseline, dict):
        raise ValueError("manifest baseline must be an object")
    if not isinstance(experiments, list) or not experiments:
        raise ValueError("manifest experiments must be a nonempty array")

    rows: list[dict[str, Any]] = []
    totals = {
        "experiments": 0,
        "original_keeps": 0,
        "gated_keeps": 0,
        "gated_rejects": 0,
        "gated_escalations": 0,
        "challenged_keeps": 0,
    }

    for index, candidate in enumerate(experiments, start=1):
        if not isinstance(candidate, dict):
            raise ValueError(f"experiment {index} must be an object")
        checks = candidate.get("checks")
        if not isinstance(checks, dict):
            raise ValueError(f"experiment {index} checks must be an object")
        candidate_record = {key: value for key, value in candidate.items() if key != "checks"}
        producer_id = "synthetic-comparison-harness"
        producers = {
            name: {"role": "independent_harness", "id": producer_id}
            for name in checks
        }
        artifacts: dict[str, dict[str, Any]] = {}
        if checks.get("human_comprehensibility") == "pass":
            artifact = {
                "schema_version": 2,
                "reviewer": "synthetic-reviewer",
                "reviewer_role": "human_reviewer",
                "baseline_sha256": canonical_sha256(baseline),
                "candidate_sha256": canonical_sha256(candidate_record),
                "policy_sha256": canonical_sha256(config),
                "finding": "human_comprehensibility",
                "state": "pass",
                "scope": "synthetic comparison fixture only",
            }
            artifacts["human_comprehensibility"] = artifact
            producers["human_comprehensibility"] = {
                "role": "human_reviewer",
                "id": "synthetic-reviewer",
                "artifact_sha256": canonical_sha256(artifact),
            }
        evidence = build_evidence_bundle(
            baseline, candidate_record, config, checks, producers, artifacts
        )
        upstream = original_decision(baseline, candidate_record)
        gated: Decision = evaluate(baseline, candidate_record, config, evidence)
        challenged = upstream == "KEEP" and gated.action != "KEEP"
        row = {
            "experiment": candidate_record.get("experiment", index),
            "description": candidate_record.get("description", ""),
            "val_bpb": candidate_record.get("val_bpb"),
            "original_action": upstream,
            "gated_action": gated.action,
            "challenged_keep": challenged,
            "gated_reasons": gated.reasons,
        }
        rows.append(row)
        totals["experiments"] += 1
        totals["original_keeps"] += upstream == "KEEP"
        totals["gated_keeps"] += gated.action == "KEEP"
        totals["gated_rejects"] += gated.action == "REJECT"
        totals["gated_escalations"] += gated.action == "ESCALATE"
        totals["challenged_keeps"] += challenged

    return {
        "comparison_label": "same experiments, different acceptance boundary",
        "totals": totals,
        "experiments": rows,
        "interpretation_limit": (
            "A challenged keep is an experiment requiring rejection or review under the "
            "gate. It is not automatically a proven safety failure."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare original and gated acceptance rules")
    parser.add_argument("--manifest", required=True)
    parser.add_argument(
        "--config",
        default=str(Path(__file__).resolve().parents[1] / "gate" / "gate_config.json"),
    )
    parser.add_argument("--output")
    args = parser.parse_args()

    try:
        report = compare(load_object(args.manifest), load_object(args.config))
        rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
        if args.output:
            Path(args.output).write_text(rendered, encoding="utf-8")
        print(rendered, end="")
        return 0
    except (OSError, TypeError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": f"benchmark input could not be trusted: {exc}"}, indent=2))
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
