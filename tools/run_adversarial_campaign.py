"""Run the frozen v0.9.2 adversarial matrix and emit a JSON receipt."""

from __future__ import annotations

import io
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tests"))

from test_adversarial_v092 import AdversarialGateV092Tests  # noqa: E402


CASES = [
    ("A01", "test_a01_rejects_baseline_substitution", "attack"),
    ("A02", "test_a02_rejects_reserved_authority_field", "attack"),
    ("A03", "test_a03_unicode_lookalike_never_grants_authority", "attack"),
    ("A04", "test_a04_rejects_unapproved_harness", "attack"),
    ("A05", "test_a05_rejects_unapproved_reviewer", "attack"),
    ("A06", "test_a06_rejects_digest_without_review_payload", "attack"),
    ("A07", "test_a07_rejects_duplicate_json_keys", "attack"),
    ("A08", "test_a08_rejects_undeclared_evidence", "attack"),
    ("A09", "test_a09_rejects_missing_run_status", "attack"),
    ("A10", "test_a10_rejects_policy_without_core_check", "attack"),
    ("A11", "test_a11_rejects_string_numeric_policy", "attack"),
    ("A12", "test_a12_rejects_nonfinite_candidate_metric", "attack"),
    ("A13", "test_a13_rejects_failed_holdout", "control_reject"),
    ("A14", "test_a14_escalates_unknown_critical_evidence", "control_escalate"),
    ("A15", "test_a15_keeps_fully_bound_control", "control_keep"),
    ("A16", "test_a16_rejects_regression_control", "control_reject"),
]


def main() -> int:
    rows = []
    for case_id, method, kind in CASES:
        stream = io.StringIO()
        result = unittest.TextTestRunner(stream=stream, verbosity=0).run(
            AdversarialGateV092Tests(method)
        )
        passed = result.wasSuccessful()
        rows.append(
            {
                "id": case_id,
                "kind": kind,
                "test": method,
                "status": "PASS" if passed else "FAIL",
                "diagnostic": stream.getvalue().strip() if not passed else "",
            }
        )
    attack_rows = [row for row in rows if row["kind"] == "attack"]
    control_rows = [row for row in rows if row["kind"].startswith("control_")]
    report = {
        "subject": "Artificial Stupidity gate v0.9.2",
        "frozen_plan": "docs/ADVERSARIAL_TEST_PLAN_v0.9.2.md",
        "attack_cases": len(attack_rows),
        "attack_cases_blocked": sum(row["status"] == "PASS" for row in attack_rows),
        "unjustified_keep_outcomes": sum(row["status"] != "PASS" for row in attack_rows),
        "control_cases": len(control_rows),
        "control_cases_correct": sum(row["status"] == "PASS" for row in control_rows),
        "false_vetoes_on_declared_keep_controls": sum(
            row["status"] != "PASS" for row in rows if row["kind"] == "control_keep"
        ),
        "unexpected_exceptions": sum(bool(row["diagnostic"]) for row in rows),
        "ablations": [
            {
                "control_removed": "baseline binding",
                "v091_probe": "A01",
                "observed_without_control": "KEEP",
                "v092_with_control": "REFUSE",
            },
            {
                "control_removed": "producer allowlist",
                "v091_probe": "A04",
                "observed_without_control": "KEEP",
                "v092_with_control": "REFUSE",
            },
            {
                "control_removed": "review payload binding",
                "v091_probe": "A06",
                "observed_without_control": "KEEP",
                "v092_with_control": "REFUSE",
            },
            {
                "control_removed": "core policy floor",
                "v091_probe": "A10",
                "observed_without_control": "KEEP",
                "v092_with_control": "REFUSE",
            },
        ],
        "results": rows,
        "interpretation_limit": (
            "This is a deterministic, designed attack suite. Its rates are not estimates "
            "of real-world incident probability or proof of general AI safety."
        ),
    }
    output = ROOT / "benchmark" / "adversarial" / "v092_campaign_receipt.json"
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if all(row["status"] == "PASS" for row in rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
