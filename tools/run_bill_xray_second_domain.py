"""Run the frozen Bill X-Ray second-domain validation matrix."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from benchmark.second_domain_bill_xray.claim_gate import (  # noqa: E402
    build_evidence_bundle,
    canonical_sha256,
    evaluate_claim,
    load_object,
)


CASE_ROOT = ROOT / "benchmark" / "second_domain_bill_xray"
PRODUCER_IDS = {
    "official_source_authority": "ilga-source-inspector-v1",
    "current_law_status": "ilga-source-inspector-v1",
    "statutory_text_match": "as-bill-xray-gate-harness-v1",
    "scope_boundary": "as-bill-xray-gate-harness-v1",
    "external_outcome_evidence": "as-bill-xray-gate-harness-v1",
}


def build_receipt() -> dict:
    policy = load_object(CASE_ROOT / "policy.json")
    source = load_object(CASE_ROOT / "official_source_record.json")
    matrix = load_object(CASE_ROOT / "case_matrix.json")
    producers = {
        name: {"role": "external_gate_harness", "id": producer_id}
        for name, producer_id in PRODUCER_IDS.items()
    }
    rows = []
    for case in matrix["cases"]:
        claim = load_object(CASE_ROOT / case["claim_file"])
        evidence = build_evidence_bundle(
            claim, source, policy, case["checks"], producers
        )
        decision = evaluate_claim(claim, source, policy, evidence)
        rows.append(
            {
                "id": case["id"],
                "claim_sha256": canonical_sha256(claim),
                "evidence_sha256": canonical_sha256(evidence),
                "expected_action": case["expected_action"],
                "observed_action": decision.action,
                "status": "PASS" if decision.action == case["expected_action"] else "FAIL",
                "decision": decision.to_dict(),
            }
        )
    return {
        "schema_version": 1,
        "subject": "Artificial Stupidity doctrine second-domain validation",
        "domain": "Bill X-Ray / Illinois SB 1570 legislative claims",
        "frozen_contract_sha256": matrix["frozen_contract_sha256"],
        "policy_sha256": canonical_sha256(policy),
        "source_sha256": canonical_sha256(source),
        "case_count": len(rows),
        "actions_observed": sorted({row["observed_action"] for row in rows}),
        "all_expected_actions_observed": all(row["status"] == "PASS" for row in rows),
        "rows": rows,
        "interpretation_limit": "A deterministic three-case portability test, not legal advice, an error-rate estimate, independent reproduction, or proof of general AI safety.",
    }


def main() -> int:
    receipt = build_receipt()
    output = CASE_ROOT / "machine_receipt.json"
    output.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0 if receipt["all_expected_actions_observed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
