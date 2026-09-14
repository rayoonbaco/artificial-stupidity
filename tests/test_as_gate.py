import json
import copy
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from gate.as_gate import build_evidence_bundle, canonical_sha256, evaluate  # noqa: E402
from gate.build_candidate import build_record, parse_run_summary  # noqa: E402


def load(name):
    return json.loads((ROOT / "gate" / name).read_text(encoding="utf-8"))


class ArtificialStupidityGateTests(unittest.TestCase):
    def setUp(self):
        self.config = load("gate_config.json")
        self.baseline = load("examples/baseline.json")
        self.candidate = load("examples/candidate_keep.json")
        self.evidence = load("examples/evidence_keep.json")

    def bound_evidence(self, candidate, config=None, checks=None, producers=None):
        policy = config or self.config
        check_values = checks or self.evidence["checks"]
        producer_values = copy.deepcopy(producers or self.evidence["producers"])
        artifacts = {}
        if check_values.get("human_comprehensibility") == "pass":
            reviewer = producer_values["human_comprehensibility"]["id"]
            artifact = {
                "schema_version": 2,
                "reviewer": reviewer,
                "reviewer_role": "human_reviewer",
                "baseline_sha256": canonical_sha256(self.baseline),
                "candidate_sha256": canonical_sha256(candidate),
                "policy_sha256": canonical_sha256(policy),
                "finding": "human_comprehensibility",
                "state": "pass",
                "scope": "unit-test fixture",
            }
            artifacts["human_comprehensibility"] = artifact
            producer_values["human_comprehensibility"]["artifact_sha256"] = canonical_sha256(artifact)
        return build_evidence_bundle(
            self.baseline,
            candidate,
            policy,
            check_values,
            producer_values,
            artifacts,
        )

    def test_keeps_supported_improvement(self):
        decision = evaluate(self.baseline, self.candidate, self.config, self.evidence)
        self.assertEqual(decision.action, "KEEP")

    def test_rejects_metric_regression(self):
        candidate = dict(self.candidate, val_bpb=1.01)
        decision = evaluate(
            self.baseline, candidate, self.config, self.bound_evidence(candidate)
        )
        self.assertEqual(decision.action, "REJECT")

    def test_rejects_failed_critical_check(self):
        candidate = dict(self.candidate)
        checks = dict(self.evidence["checks"], held_out_robustness="fail")
        decision = evaluate(
            self.baseline,
            candidate,
            self.config,
            self.bound_evidence(candidate, checks=checks),
        )
        self.assertEqual(decision.action, "REJECT")

    def test_escalates_unknown_critical_evidence(self):
        candidate = load("examples/candidate_escalate.json")
        evidence = load("examples/evidence_escalate.json")
        decision = evaluate(self.baseline, candidate, self.config, evidence)
        self.assertEqual(decision.action, "ESCALATE")

    def test_escalates_missing_noncritical_required_evidence(self):
        candidate = dict(self.candidate)
        checks = dict(self.evidence["checks"])
        checks.pop("human_comprehensibility")
        decision = evaluate(
            self.baseline,
            candidate,
            self.config,
            self.bound_evidence(candidate, checks=checks),
        )
        self.assertEqual(decision.action, "ESCALATE")
        self.assertTrue(any("required evidence is unknown" in reason for reason in decision.reasons))

    def test_escalates_missing_falsifiability_statement(self):
        candidate = dict(self.candidate, disconfirming_result="")
        decision = evaluate(
            self.baseline, candidate, self.config, self.bound_evidence(candidate)
        )
        self.assertEqual(decision.action, "ESCALATE")
        self.assertTrue(any("falsifiability fields" in reason for reason in decision.reasons))

    def test_escalates_untrusted_input_in_cli_contract(self):
        evidence = self.bound_evidence(
            self.candidate, checks={"repeatability": "maybe"}
        )
        with self.assertRaises(ValueError):
            evaluate(self.baseline, self.candidate, self.config, evidence)

    def test_rejects_negative_complexity_input_as_untrusted(self):
        candidate = dict(self.candidate, complexity_delta_lines=-1)
        with self.assertRaises(ValueError):
            evaluate(
                self.baseline, candidate, self.config, self.bound_evidence(candidate)
            )

    def test_rejects_boolean_complexity_input_as_untrusted(self):
        candidate = dict(self.candidate, complexity_delta_lines=True)
        with self.assertRaises(ValueError):
            evaluate(
                self.baseline, candidate, self.config, self.bound_evidence(candidate)
            )

    def test_rejects_missing_complexity_input_as_untrusted(self):
        candidate = dict(self.candidate)
        candidate.pop("complexity_delta_lines")
        with self.assertRaises(ValueError):
            evaluate(
                self.baseline, candidate, self.config, self.bound_evidence(candidate)
            )

    def test_rejects_invalid_check_configuration(self):
        config = dict(self.config, critical_checks=["not_required"])
        with self.assertRaises(ValueError):
            evaluate(
                self.baseline,
                self.candidate,
                config,
                self.bound_evidence(self.candidate, config=config),
            )

    def test_rejects_unsafe_numeric_configuration(self):
        config = dict(self.config, minimum_evidence_coverage=1.5)
        with self.assertRaises(ValueError):
            evaluate(
                self.baseline,
                self.candidate,
                config,
                self.bound_evidence(self.candidate, config=config),
            )

    def test_rejects_nonboolean_policy_toggle(self):
        config = dict(self.config, require_falsifiable_hypothesis="false")
        with self.assertRaisesRegex(ValueError, "must be a boolean"):
            evaluate(
                self.baseline,
                self.candidate,
                config,
                self.bound_evidence(self.candidate, config=config),
            )

    def test_rejects_human_review_payload_digest_mismatch(self):
        evidence = self.bound_evidence(self.candidate)
        evidence["artifacts"]["human_comprehensibility"]["scope"] = "tampered"
        with self.assertRaisesRegex(ValueError, "digest does not match"):
            evaluate(self.baseline, self.candidate, self.config, evidence)

    def test_rejects_candidate_supplied_human_approval(self):
        candidate = dict(self.candidate, human_authorization="KEEP")
        with self.assertRaisesRegex(ValueError, "reserved authority fields"):
            evaluate(
                self.baseline, candidate, self.config, self.bound_evidence(candidate)
            )

    def test_rejects_candidate_supplied_checks(self):
        candidate = dict(self.candidate, checks=self.evidence["checks"])
        with self.assertRaisesRegex(ValueError, "reserved authority fields"):
            evaluate(
                self.baseline, candidate, self.config, self.bound_evidence(candidate)
            )

    def test_rejects_evidence_bound_to_another_candidate(self):
        candidate = dict(self.candidate, val_bpb=0.9900)
        with self.assertRaisesRegex(ValueError, "not bound to this candidate"):
            evaluate(self.baseline, candidate, self.config, self.evidence)

    def test_rejects_evidence_bound_to_another_policy(self):
        config = dict(self.config, maximum_complexity_delta_lines=999)
        with self.assertRaisesRegex(ValueError, "not bound to this policy"):
            evaluate(self.baseline, self.candidate, config, self.evidence)

    def test_human_pass_requires_human_producer_and_artifact(self):
        producers = dict(self.evidence["producers"])
        producers["human_comprehensibility"] = {
            "role": "independent_harness",
            "id": "candidate-controlled",
        }
        evidence = self.bound_evidence(self.candidate, producers=producers)
        with self.assertRaisesRegex(ValueError, "approved|human_reviewer"):
            evaluate(self.baseline, self.candidate, self.config, evidence)

    def test_parses_upstream_run_summary(self):
        summary = parse_run_summary("---\nval_bpb: 0.997900\npeak_vram_mb: 45060.2\n")
        self.assertEqual(summary, {"val_bpb": 0.9979, "peak_vram_mb": 45060.2})

    def test_builds_candidate_without_inventing_evidence(self):
        evidence = {"checks": {"repeatability": "unknown"}}
        record = build_record({"val_bpb": 1.0, "peak_vram_mb": 100.0}, evidence, 7)
        self.assertEqual(record["complexity_delta_lines"], 7)
        self.assertNotIn("checks", record)


if __name__ == "__main__":
    unittest.main()
