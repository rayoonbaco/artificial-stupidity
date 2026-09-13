import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from gate.as_gate import evaluate  # noqa: E402
from gate.build_candidate import build_record, parse_run_summary  # noqa: E402


def load(name):
    return json.loads((ROOT / "gate" / name).read_text(encoding="utf-8"))


class ArtificialStupidityGateTests(unittest.TestCase):
    def setUp(self):
        self.config = load("gate_config.json")
        self.baseline = load("examples/baseline.json")
        self.candidate = load("examples/candidate_keep.json")

    def test_keeps_supported_improvement(self):
        decision = evaluate(self.baseline, self.candidate, self.config)
        self.assertEqual(decision.action, "KEEP")

    def test_rejects_metric_regression(self):
        candidate = dict(self.candidate, val_bpb=1.01)
        decision = evaluate(self.baseline, candidate, self.config)
        self.assertEqual(decision.action, "REJECT")

    def test_rejects_failed_critical_check(self):
        candidate = dict(self.candidate)
        candidate["checks"] = dict(candidate["checks"], held_out_robustness="fail")
        decision = evaluate(self.baseline, candidate, self.config)
        self.assertEqual(decision.action, "REJECT")

    def test_escalates_unknown_critical_evidence(self):
        candidate = load("examples/candidate_escalate.json")
        decision = evaluate(self.baseline, candidate, self.config)
        self.assertEqual(decision.action, "ESCALATE")

    def test_escalates_missing_noncritical_required_evidence(self):
        candidate = dict(self.candidate)
        candidate["checks"] = dict(candidate["checks"])
        candidate["checks"].pop("human_comprehensibility")
        decision = evaluate(self.baseline, candidate, self.config)
        self.assertEqual(decision.action, "ESCALATE")
        self.assertTrue(any("required evidence is unknown" in reason for reason in decision.reasons))

    def test_escalates_missing_falsifiability_statement(self):
        candidate = dict(self.candidate, disconfirming_result="")
        decision = evaluate(self.baseline, candidate, self.config)
        self.assertEqual(decision.action, "ESCALATE")
        self.assertTrue(any("falsifiability fields" in reason for reason in decision.reasons))

    def test_escalates_untrusted_input_in_cli_contract(self):
        candidate = dict(self.candidate, checks={"repeatability": "maybe"})
        with self.assertRaises(ValueError):
            evaluate(self.baseline, candidate, self.config)

    def test_rejects_negative_complexity_input_as_untrusted(self):
        candidate = dict(self.candidate, complexity_delta_lines=-1)
        with self.assertRaises(ValueError):
            evaluate(self.baseline, candidate, self.config)

    def test_rejects_boolean_complexity_input_as_untrusted(self):
        candidate = dict(self.candidate, complexity_delta_lines=True)
        with self.assertRaises(ValueError):
            evaluate(self.baseline, candidate, self.config)

    def test_rejects_missing_complexity_input_as_untrusted(self):
        candidate = dict(self.candidate)
        candidate.pop("complexity_delta_lines")
        with self.assertRaises(ValueError):
            evaluate(self.baseline, candidate, self.config)

    def test_rejects_invalid_check_configuration(self):
        config = dict(self.config, critical_checks=["not_required"])
        with self.assertRaises(ValueError):
            evaluate(self.baseline, self.candidate, config)

    def test_rejects_unsafe_numeric_configuration(self):
        config = dict(self.config, minimum_evidence_coverage=1.5)
        with self.assertRaises(ValueError):
            evaluate(self.baseline, self.candidate, config)

    def test_parses_upstream_run_summary(self):
        summary = parse_run_summary("---\nval_bpb: 0.997900\npeak_vram_mb: 45060.2\n")
        self.assertEqual(summary, {"val_bpb": 0.9979, "peak_vram_mb": 45060.2})

    def test_builds_candidate_without_inventing_evidence(self):
        evidence = {"checks": {"repeatability": "unknown"}}
        record = build_record({"val_bpb": 1.0, "peak_vram_mb": 100.0}, evidence, 7)
        self.assertEqual(record["complexity_delta_lines"], 7)
        self.assertEqual(record["checks"]["repeatability"], "unknown")


if __name__ == "__main__":
    unittest.main()
