import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from benchmark.compare_loops import compare, original_decision  # noqa: E402


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


class BenchmarkComparisonTests(unittest.TestCase):
    def setUp(self):
        self.manifest = load("benchmark/example_experiments.json")
        self.config = load("gate/gate_config.json")

    def test_original_rule_only_uses_completion_and_primary_metric(self):
        baseline = self.manifest["baseline"]
        brittle = self.manifest["experiments"][1]
        self.assertEqual(original_decision(baseline, brittle), "KEEP")

    def test_same_sequence_produces_expected_comparison(self):
        report = compare(self.manifest, self.config)
        self.assertEqual(
            report["totals"],
            {
                "experiments": 4,
                "original_keeps": 3,
                "gated_keeps": 1,
                "gated_rejects": 2,
                "gated_escalations": 1,
                "challenged_keeps": 2,
            },
        )

    def test_challenged_keep_distinguishes_failure_from_uncertainty(self):
        rows = {row["experiment"]: row for row in compare(self.manifest, self.config)["experiments"]}
        self.assertEqual(rows["brittle-gain"]["gated_action"], "REJECT")
        self.assertEqual(rows["unsupported-gain"]["gated_action"], "ESCALATE")
        self.assertTrue(rows["brittle-gain"]["challenged_keep"])
        self.assertTrue(rows["unsupported-gain"]["challenged_keep"])

    def test_rejects_empty_experiment_manifest(self):
        manifest = dict(self.manifest, experiments=[])
        with self.assertRaises(ValueError):
            compare(manifest, self.config)


if __name__ == "__main__":
    unittest.main()
