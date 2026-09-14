import copy
import json
import math
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from gate.as_gate import (  # noqa: E402
    _load_json,
    build_evidence_bundle,
    canonical_sha256,
    evaluate,
)


def load(relative):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class AdversarialGateV092Tests(unittest.TestCase):
    def setUp(self):
        self.baseline = load("gate/examples/baseline.json")
        self.candidate = load("gate/examples/candidate_keep.json")
        self.config = load("gate/gate_config.json")
        self.example = load("gate/examples/evidence_keep.json")

    def bundle(self, candidate=None, config=None, baseline=None, checks=None, producers=None):
        candidate = candidate or self.candidate
        config = config or self.config
        baseline = baseline or self.baseline
        checks = copy.deepcopy(checks or self.example["checks"])
        producers = copy.deepcopy(producers or self.example["producers"])
        artifacts = {}
        if checks.get("human_comprehensibility") == "pass":
            reviewer = producers["human_comprehensibility"]["id"]
            artifact = {
                "schema_version": 2,
                "reviewer": reviewer,
                "reviewer_role": "human_reviewer",
                "baseline_sha256": canonical_sha256(baseline),
                "candidate_sha256": canonical_sha256(candidate),
                "policy_sha256": canonical_sha256(config),
                "finding": "human_comprehensibility",
                "state": "pass",
                "scope": "adversarial test fixture",
            }
            artifacts["human_comprehensibility"] = artifact
            producers["human_comprehensibility"]["artifact_sha256"] = canonical_sha256(artifact)
        return build_evidence_bundle(
            baseline, candidate, config, checks, producers, artifacts
        )

    def test_a01_rejects_baseline_substitution(self):
        changed = dict(self.baseline, val_bpb=2.0)
        with self.assertRaisesRegex(ValueError, "not bound to this baseline"):
            evaluate(changed, self.candidate, self.config, self.example)

    def test_a02_rejects_reserved_authority_field(self):
        candidate = dict(self.candidate, human_authorization="KEEP")
        with self.assertRaisesRegex(ValueError, "reserved authority fields"):
            evaluate(self.baseline, candidate, self.config, self.bundle(candidate=candidate))

    def test_a03_unicode_lookalike_never_grants_authority(self):
        candidate = dict(self.candidate)
        candidate["human_authorizatіon"] = "KEEP"
        decision = evaluate(self.baseline, candidate, self.config, self.bundle(candidate=candidate))
        self.assertEqual(decision.action, "KEEP")
        self.assertNotIn("human_authorization", decision.facts)

    def test_a04_rejects_unapproved_harness(self):
        producers = copy.deepcopy(self.example["producers"])
        producers["repeatability"] = {"role": "independent_harness", "id": "candidate-process"}
        with self.assertRaisesRegex(ValueError, "not approved"):
            evaluate(self.baseline, self.candidate, self.config, self.bundle(producers=producers))

    def test_a05_rejects_unapproved_reviewer(self):
        producers = copy.deepcopy(self.example["producers"])
        producers["human_comprehensibility"] = {"role": "human_reviewer", "id": "candidate-process"}
        with self.assertRaisesRegex(ValueError, "not approved"):
            evaluate(self.baseline, self.candidate, self.config, self.bundle(producers=producers))

    def test_a06_rejects_digest_without_review_payload(self):
        evidence = self.bundle()
        evidence.pop("artifacts")
        with self.assertRaisesRegex(ValueError, "bound review artifact"):
            evaluate(self.baseline, self.candidate, self.config, evidence)

    def test_a07_rejects_duplicate_json_keys(self):
        with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8", delete=False) as handle:
            handle.write('{"val_bpb": 9.99, "val_bpb": 0.99}')
            path = Path(handle.name)
        try:
            with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
                _load_json(path)
        finally:
            path.unlink(missing_ok=True)

    def test_a08_rejects_undeclared_evidence(self):
        evidence = self.bundle()
        evidence["checks"]["candidate_says_safe"] = "pass"
        evidence["producers"]["candidate_says_safe"] = {
            "role": "independent_harness",
            "id": "candidate-process",
        }
        with self.assertRaisesRegex(ValueError, "undeclared checks"):
            evaluate(self.baseline, self.candidate, self.config, evidence)

    def test_a09_rejects_missing_run_status(self):
        candidate = dict(self.candidate)
        candidate.pop("run_status")
        with self.assertRaisesRegex(ValueError, "run_status is required"):
            evaluate(self.baseline, candidate, self.config, self.bundle(candidate=candidate))

    def test_a10_rejects_policy_without_core_check(self):
        config = copy.deepcopy(self.config)
        config["required_checks"].remove("human_comprehensibility")
        config["trusted_producers"].pop("human_comprehensibility")
        with self.assertRaisesRegex(ValueError, "removed core required checks"):
            evaluate(self.baseline, self.candidate, config, self.bundle(config=config))

    def test_a11_rejects_string_numeric_policy(self):
        config = dict(self.config, minimum_val_bpb_improvement="0.000001")
        with self.assertRaisesRegex(ValueError, "must be a number"):
            evaluate(self.baseline, self.candidate, config, self.bundle(config=config))

    def test_a12_rejects_nonfinite_candidate_metric(self):
        candidate = dict(self.candidate, val_bpb=math.nan)
        with self.assertRaisesRegex(ValueError, "must be finite"):
            evaluate(self.baseline, candidate, self.config, self.bundle(candidate=candidate))

    def test_a13_rejects_failed_holdout(self):
        checks = dict(self.example["checks"], held_out_robustness="fail")
        self.assertEqual(
            evaluate(self.baseline, self.candidate, self.config, self.bundle(checks=checks)).action,
            "REJECT",
        )

    def test_a14_escalates_unknown_critical_evidence(self):
        checks = dict(self.example["checks"], held_out_robustness="unknown")
        self.assertEqual(
            evaluate(self.baseline, self.candidate, self.config, self.bundle(checks=checks)).action,
            "ESCALATE",
        )

    def test_a15_keeps_fully_bound_control(self):
        self.assertEqual(
            evaluate(self.baseline, self.candidate, self.config, self.bundle()).action,
            "KEEP",
        )

    def test_a16_rejects_regression_control(self):
        candidate = dict(self.candidate, val_bpb=1.01)
        self.assertEqual(
            evaluate(self.baseline, candidate, self.config, self.bundle(candidate=candidate)).action,
            "REJECT",
        )


if __name__ == "__main__":
    unittest.main()
