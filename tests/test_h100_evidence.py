import tempfile
import unittest
import os
import subprocess
import sys
from pathlib import Path


from benchmark.h100_evidence_runner import (
    BASELINE_SCRIPT,
    CANDIDATE_SCRIPT,
    evaluate_run_sets,
    package_evidence,
    parse_metrics,
)
from gate.as_gate import evaluate
import json


def record(val, holdout, memory=45000.0, exit_code=0):
    return {
        "exit_code": exit_code,
        "metrics": {
            "val_bpb": val,
            "holdout_bpb": holdout,
            "peak_vram_mb": memory,
        },
    }


class H100EvidenceTests(unittest.TestCase):
    def test_runner_entrypoint_can_import_gate_outside_project_directory(self):
        root = Path(__file__).resolve().parents[1]
        runner = root / "benchmark" / "h100_evidence_runner.py"
        env = os.environ.copy()
        env.pop("PYTHONPATH", None)
        with tempfile.TemporaryDirectory() as temp:
            completed = subprocess.run(
                [sys.executable, str(runner), "--help"],
                cwd=temp,
                env=env,
                text=True,
                capture_output=True,
                check=False,
            )
        self.assertEqual(completed.returncode, 0, completed.stderr)

    def test_parses_final_training_metrics(self):
        parsed = parse_metrics(
            "val_bpb: 1.050835\nholdout_bpb: 1.061234\n"
            "peak_vram_mb: 45060.2\nnum_steps: 475\n"
        )
        self.assertEqual(parsed["val_bpb"], 1.050835)
        self.assertEqual(parsed["holdout_bpb"], 1.061234)
        self.assertEqual(parsed["num_steps"], 475)

    def test_nonoverlapping_wins_pass_empirical_checks(self):
        baseline = [record(1.05, 1.07), record(1.051, 1.071), record(1.052, 1.072)]
        candidate = [record(1.02, 1.04), record(1.021, 1.041), record(1.022, 1.042)]
        result = evaluate_run_sets(baseline, candidate)
        self.assertEqual(result["summary"]["checks"]["repeatability"], "pass")
        self.assertEqual(result["summary"]["checks"]["held_out_robustness"], "pass")
        self.assertEqual(result["summary"]["checks"]["human_comprehensibility"], "unknown")
        config = json.loads(
            (Path(__file__).resolve().parents[1] / "gate" / "gate_config.json").read_text(
                encoding="utf-8"
            )
        )
        decision = evaluate(
            result["baseline_gate_record"],
            result["candidate_gate_record"],
            config,
            result["evidence_bundle"],
        )
        self.assertEqual(decision.action, "ESCALATE")

    def test_holdout_overlap_fails_critical_check(self):
        baseline = [record(1.05, 1.04), record(1.051, 1.05), record(1.052, 1.06)]
        candidate = [record(1.02, 1.03), record(1.021, 1.04), record(1.022, 1.05)]
        result = evaluate_run_sets(baseline, candidate)
        self.assertEqual(result["summary"]["checks"]["held_out_robustness"], "fail")
        config = json.loads(
            (Path(__file__).resolve().parents[1] / "gate" / "gate_config.json").read_text(
                encoding="utf-8"
            )
        )
        decision = evaluate(
            result["baseline_gate_record"],
            result["candidate_gate_record"],
            config,
            result["evidence_bundle"],
        )
        self.assertEqual(decision.action, "REJECT")

    def test_incomplete_runs_do_not_invent_evidence(self):
        baseline = [record(1.05, 1.07)]
        candidate = [record(1.02, 1.04)]
        checks = evaluate_run_sets(baseline, candidate)["summary"]["checks"]
        self.assertEqual(checks["repeatability"], "unknown")
        self.assertEqual(checks["held_out_robustness"], "unknown")
        self.assertEqual(checks["failure_mode_review"], "unknown")

    def test_failed_complete_run_fails_failure_review(self):
        baseline = [record(1.05, 1.07), record(1.051, 1.071), record(1.052, 1.072)]
        candidate = [record(1.02, 1.04), record(1.021, 1.041, exit_code=1), record(1.022, 1.042)]
        checks = evaluate_run_sets(baseline, candidate)["summary"]["checks"]
        self.assertEqual(checks["failure_mode_review"], "fail")
        self.assertEqual(checks["repeatability"], "unknown")

    def test_holdout_storage_is_outside_upstream_data(self):
        root = Path(__file__).resolve().parents[1]
        holdout_source = (root / "benchmark" / "protected_holdout.py").read_text(
            encoding="utf-8"
        )
        prepare_source = (root / "prepare.py").read_text(encoding="utf-8")
        self.assertIn(
            'HOLDOUT_DIR = Path(CACHE_DIR) / "protected_holdout"', holdout_source
        )
        self.assertIn('DATA_DIR = os.path.join(CACHE_DIR, "data")', prepare_source)

    def test_candidate_has_exactly_one_functional_diff(self):
        baseline = BASELINE_SCRIPT.read_text(encoding="utf-8").splitlines()
        candidate = CANDIDATE_SCRIPT.read_text(encoding="utf-8").splitlines()
        differences = [(left, right) for left, right in zip(baseline, candidate) if left != right]
        self.assertEqual(len(baseline), len(candidate))
        self.assertEqual(len(differences), 1)
        self.assertIn("TOTAL_BATCH_SIZE = 2**19", differences[0][0])
        self.assertIn("TOTAL_BATCH_SIZE = 2**18", differences[0][1])

    def test_failure_package_contains_checksum_manifest(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp) / "run"
            directory.mkdir()
            (directory / "evidence.txt").write_text("bounded\n", encoding="utf-8")
            archive = Path(temp) / "evidence.zip"
            package_evidence(directory, archive)
            self.assertTrue(archive.exists())
            self.assertTrue((directory / "SHA256SUMS.txt").exists())


if __name__ == "__main__":
    unittest.main()
