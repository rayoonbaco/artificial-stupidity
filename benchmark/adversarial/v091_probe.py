"""Preserve known v0.9.1 trust-boundary failures before repair."""

from __future__ import annotations

import copy
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from benchmark.adversarial.v091_as_gate_snapshot import (  # noqa: E402
    _load_json,
    build_evidence_bundle,
    evaluate,
)


def load(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def outcome(action, observed, expected="REFUSE") -> dict:
    escaped = observed == "KEEP" and expected != "KEEP"
    return {"attack": action, "expected": expected, "observed": observed, "unjustified_keep": escaped}


def main() -> None:
    baseline = load("benchmark/adversarial/v091_fixtures/baseline.json")
    candidate = load("benchmark/adversarial/v091_fixtures/candidate_keep.json")
    config = load("benchmark/adversarial/v091_fixtures/gate_config.json")
    evidence = load("benchmark/adversarial/v091_fixtures/evidence_keep.json")
    rows = []

    substituted_baseline = dict(baseline, val_bpb=2.0)
    rows.append(outcome("A01 baseline substitution", evaluate(substituted_baseline, candidate, config, evidence).action))

    producers = copy.deepcopy(evidence["producers"])
    for name in ("repeatability", "held_out_robustness", "failure_mode_review"):
        producers[name]["id"] = "candidate-process"
    forged = build_evidence_bundle(candidate, config, evidence["checks"], producers)
    rows.append(outcome("A04 harness impersonation", evaluate(baseline, candidate, config, forged).action))

    producers = copy.deepcopy(evidence["producers"])
    producers["human_comprehensibility"] = {
        "role": "human_reviewer",
        "id": "candidate-process",
        "artifact_sha256": "0" * 64,
    }
    forged = build_evidence_bundle(candidate, config, evidence["checks"], producers)
    rows.append(outcome("A05 reviewer impersonation", evaluate(baseline, candidate, config, forged).action))
    rows.append(outcome("A06 unbound review digest", evaluate(baseline, candidate, config, forged).action))

    extra_checks = dict(evidence["checks"], candidate_says_safe="pass")
    extra_producers = copy.deepcopy(evidence["producers"])
    extra_producers["candidate_says_safe"] = {"role": "independent_harness", "id": "candidate-process"}
    forged = build_evidence_bundle(candidate, config, extra_checks, extra_producers)
    rows.append(outcome("A08 undeclared evidence", evaluate(baseline, candidate, config, forged).action))

    missing_status = dict(candidate)
    missing_status.pop("run_status")
    forged = build_evidence_bundle(missing_status, config, evidence["checks"], evidence["producers"])
    rows.append(outcome("A09 missing run status", evaluate(baseline, missing_status, config, forged).action))

    weakened = dict(config, required_checks=[], critical_checks=[], minimum_evidence_coverage=0.0)
    forged = build_evidence_bundle(candidate, weakened, {}, {})
    rows.append(outcome("A10 removed core policy", evaluate(baseline, candidate, weakened, forged).action))

    string_policy = dict(config, minimum_val_bpb_improvement="0.000001")
    forged = build_evidence_bundle(candidate, string_policy, evidence["checks"], evidence["producers"])
    rows.append(outcome("A11 string numeric policy", evaluate(baseline, candidate, string_policy, forged).action))

    with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8", delete=False) as handle:
        handle.write('{"val_bpb": 9.99, "val_bpb": 0.99}')
        duplicate_path = Path(handle.name)
    try:
        parsed = _load_json(duplicate_path)
        duplicate_observed = "ACCEPTED_LAST_VALUE" if parsed["val_bpb"] == 0.99 else "ACCEPTED"
    finally:
        duplicate_path.unlink(missing_ok=True)
    rows.append(outcome("A07 duplicate JSON key", duplicate_observed))

    report = {
        "subject": "v0.9.1 before adversarial repair",
        "frozen_plan": "docs/ADVERSARIAL_TEST_PLAN_v0.9.2.md",
        "attacks_executed": len(rows),
        "unjustified_keeps": sum(row["unjustified_keep"] for row in rows),
        "results": rows,
        "interpretation": "These are implementation trust gaps, not measured real-world incidents.",
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
