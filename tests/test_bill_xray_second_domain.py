import copy
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASE_ROOT = ROOT / "benchmark" / "second_domain_bill_xray"
sys.path.insert(0, str(ROOT))

from benchmark.second_domain_bill_xray.claim_gate import (  # noqa: E402
    build_evidence_bundle,
    evaluate_claim,
    load_object,
)
from tools.run_bill_xray_second_domain import (  # noqa: E402
    PRODUCER_IDS,
    build_receipt,
)


def producers():
    return {
        name: {"role": "external_gate_harness", "id": producer_id}
        for name, producer_id in PRODUCER_IDS.items()
    }


class BillXRaySecondDomainTests(unittest.TestCase):
    def setUp(self):
        self.policy = load_object(CASE_ROOT / "policy.json")
        self.source = load_object(CASE_ROOT / "official_source_record.json")
        self.matrix = load_object(CASE_ROOT / "case_matrix.json")

    def case(self, case_id):
        return next(item for item in self.matrix["cases"] if item["id"] == case_id)

    def claim(self, case_id):
        case = self.case(case_id)
        return load_object(CASE_ROOT / case["claim_file"])

    def evidence(self, case_id, *, claim=None, source=None, policy=None, checks=None, producer_map=None):
        case = self.case(case_id)
        return build_evidence_bundle(
            claim or self.claim(case_id),
            source or self.source,
            policy or self.policy,
            checks or copy.deepcopy(case["checks"]),
            producer_map or producers(),
        )

    def test_predeclared_cases_reach_all_three_actions(self):
        observed = {}
        for case in self.matrix["cases"]:
            claim = self.claim(case["id"])
            decision = evaluate_claim(
                claim, self.source, self.policy, self.evidence(case["id"])
            )
            observed[case["id"]] = decision.action
        self.assertEqual(
            observed, {"BX01": "KEEP", "BX02": "REJECT", "BX03": "ESCALATE"}
        )

    def test_bx02_names_declared_authorization_falsifier(self):
        claim = self.claim("BX02")
        decision = evaluate_claim(claim, self.source, self.policy, self.evidence("BX02"))
        self.assertEqual(decision.action, "REJECT")
        self.assertIn("merely authorizes", " ".join(decision.reasons))

    def test_bx03_preserves_unknown_outcome_evidence(self):
        claim = self.claim("BX03")
        decision = evaluate_claim(claim, self.source, self.policy, self.evidence("BX03"))
        self.assertEqual(decision.action, "ESCALATE")
        self.assertIn("external_outcome_evidence", " ".join(decision.reasons))

    def test_claim_substitution_is_refused(self):
        original = self.claim("BX01")
        evidence = self.evidence("BX01", claim=original)
        changed = dict(original, text="Substituted claim")
        with self.assertRaisesRegex(ValueError, "claim_sha256"):
            evaluate_claim(changed, self.source, self.policy, evidence)

    def test_source_substitution_is_refused(self):
        claim = self.claim("BX01")
        evidence = self.evidence("BX01")
        changed = dict(self.source, retrieved_utc="2099-01-01")
        with self.assertRaisesRegex(ValueError, "source_sha256"):
            evaluate_claim(claim, changed, self.policy, evidence)

    def test_policy_substitution_is_refused(self):
        claim = self.claim("BX01")
        evidence = self.evidence("BX01")
        changed = copy.deepcopy(self.policy)
        changed["critical_checks"].remove("scope_boundary")
        with self.assertRaisesRegex(ValueError, "policy_sha256"):
            evaluate_claim(claim, self.source, changed, evidence)

    def test_candidate_supplied_evidence_is_refused(self):
        claim = dict(self.claim("BX01"), checks={"statutory_text_match": "pass"})
        evidence = self.evidence("BX01", claim=claim)
        with self.assertRaisesRegex(ValueError, "reserved authority fields"):
            evaluate_claim(claim, self.source, self.policy, evidence)

    def test_duplicate_json_keys_are_refused(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "duplicate.json"
            path.write_text('{"claim_id":"BX01","claim_id":"BX99"}', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
                load_object(path)

    def test_unapproved_producer_is_refused(self):
        claim = self.claim("BX01")
        producer_map = producers()
        producer_map["statutory_text_match"]["id"] = "candidate-self-certifier"
        evidence = self.evidence("BX01", producer_map=producer_map)
        with self.assertRaisesRegex(ValueError, "producer is not approved"):
            evaluate_claim(claim, self.source, self.policy, evidence)

    def test_unapproved_source_authority_is_refused(self):
        claim = self.claim("BX01")
        source = dict(self.source, authority="Anonymous summary")
        evidence = self.evidence("BX01", source=source)
        with self.assertRaisesRegex(ValueError, "source authority is not approved"):
            evaluate_claim(claim, source, self.policy, evidence)

    def test_missing_required_check_is_refused(self):
        claim = self.claim("BX01")
        checks = copy.deepcopy(self.case("BX01")["checks"])
        checks.pop("current_law_status")
        evidence = self.evidence("BX01", checks=checks)
        with self.assertRaisesRegex(ValueError, "every and only required check"):
            evaluate_claim(claim, self.source, self.policy, evidence)

    def test_undeclared_check_is_refused(self):
        claim = self.claim("BX01")
        checks = copy.deepcopy(self.case("BX01")["checks"])
        checks["candidate_confidence"] = "pass"
        evidence = self.evidence("BX01", checks=checks)
        with self.assertRaisesRegex(ValueError, "every and only required check"):
            evaluate_claim(claim, self.source, self.policy, evidence)

    def test_unknown_critical_evidence_escalates(self):
        claim = self.claim("BX01")
        checks = copy.deepcopy(self.case("BX01")["checks"])
        checks["current_law_status"] = "unknown"
        evidence = self.evidence("BX01", checks=checks)
        self.assertEqual(
            evaluate_claim(claim, self.source, self.policy, evidence).action,
            "ESCALATE",
        )

    def test_not_applicable_is_invalid_for_outcome_claim(self):
        claim = self.claim("BX03")
        checks = copy.deepcopy(self.case("BX03")["checks"])
        checks["external_outcome_evidence"] = "not_applicable"
        evidence = self.evidence("BX03", checks=checks)
        with self.assertRaisesRegex(ValueError, "not_applicable is invalid"):
            evaluate_claim(claim, self.source, self.policy, evidence)

    def test_contract_hash_is_bound_to_matrix(self):
        contract = ROOT / "docs" / "BILL_XRAY_SECOND_DOMAIN_CONTRACT_v0.9.3.md"
        digest = hashlib.sha256(contract.read_bytes()).hexdigest()
        self.assertEqual(digest, self.matrix["frozen_contract_sha256"])

    def test_machine_receipt_is_deterministic(self):
        expected = load_object(CASE_ROOT / "machine_receipt.json")
        self.assertEqual(build_receipt(), expected)

    def test_upstream_snapshot_is_named_and_bounded(self):
        upstream = load_object(CASE_ROOT / "upstream_record.json")
        self.assertEqual(upstream["commit"], "5462bab5717bc4b9459aee195616652b8c47089b")
        self.assertEqual(upstream["baseline_tests"], 105)
        self.assertFalse(upstream["license_file_present"])
        self.assertIn("No Bill X-Ray code copied", upstream["reuse_boundary"])


if __name__ == "__main__":
    unittest.main()
