"""Rebuild v0.9.2 example evidence after policy or record changes."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from gate.as_gate import build_evidence_bundle, canonical_sha256  # noqa: E402


def load(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def write(relative: str, value: dict) -> None:
    (ROOT / relative).write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def rebuild_example(name: str, *, review: bool = False) -> None:
    baseline = load("gate/examples/baseline.json")
    candidate = load(f"gate/examples/candidate_{name}.json")
    config = load("gate/gate_config.json")
    previous = load(f"gate/examples/evidence_{name}.json")
    producers = previous["producers"]
    artifacts = {}
    if review:
        artifact = {
            "schema_version": 2,
            "reviewer": "demonstration-reviewer",
            "reviewer_role": "human_reviewer",
            "baseline_sha256": canonical_sha256(baseline),
            "candidate_sha256": canonical_sha256(candidate),
            "policy_sha256": canonical_sha256(config),
            "finding": "human_comprehensibility",
            "state": "pass",
            "scope": "GPU-free demonstration only",
        }
        artifacts["human_comprehensibility"] = artifact
        producers["human_comprehensibility"]["artifact_sha256"] = canonical_sha256(artifact)
        write("gate/examples/human_authorization_keep.json", artifact)
    bundle = build_evidence_bundle(
        baseline, candidate, config, previous["checks"], producers, artifacts
    )
    write(f"gate/examples/evidence_{name}.json", bundle)


def main() -> None:
    rebuild_example("keep", review=True)
    rebuild_example("reject")
    rebuild_example("escalate")

    baseline = load(
        "benchmark/evidence/h100_sxm_20260913/repaired_decision/baseline_gate_record.json"
    )
    candidate = load("benchmark/h100_v091_replay_candidate.json")
    config = load("gate/gate_config.json")
    previous = load("benchmark/h100_v091_replay_evidence.json")
    write(
        "benchmark/h100_v091_replay_evidence.json",
        build_evidence_bundle(
            baseline,
            candidate,
            config,
            previous["checks"],
            previous["producers"],
        ),
    )


if __name__ == "__main__":
    main()
