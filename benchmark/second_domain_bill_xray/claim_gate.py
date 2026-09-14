"""Deterministic evidence gate for bounded legislative-publication claims.

This module adapts the Artificial Stupidity doctrine to a law-and-policy domain.
It does not interpret arbitrary law, fetch sources, or provide legal advice. It
only adjudicates integrity-bound check records under a declared policy.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


VALID_STATES = {"pass", "fail", "unknown", "not_applicable"}
VALID_SCOPES = {"statutory_text", "external_outcome"}
RESERVED_CLAIM_KEYS = {
    "action",
    "authorization",
    "checks",
    "evidence",
    "evidence_bundle",
    "machine_decision",
    "policy_sha256",
    "source_sha256",
}


@dataclass(frozen=True)
class ClaimDecision:
    action: str
    reasons: list[str] = field(default_factory=list)
    facts: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {"action": self.action, "reasons": self.reasons, "facts": self.facts}


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_object(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        value = json.load(handle, object_pairs_hook=_reject_duplicate_keys)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def canonical_sha256(value: dict[str, Any]) -> str:
    payload = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def build_evidence_bundle(
    claim: dict[str, Any],
    source: dict[str, Any],
    policy: dict[str, Any],
    checks: dict[str, str],
    producers: dict[str, dict[str, str]],
) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "claim_sha256": canonical_sha256(claim),
        "source_sha256": canonical_sha256(source),
        "policy_sha256": canonical_sha256(policy),
        "checks": checks,
        "producers": producers,
    }


def _string_list(record: dict[str, Any], key: str) -> list[str]:
    value = record.get(key)
    if not isinstance(value, list) or not value:
        raise ValueError(f"{key} must be a nonempty list")
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise ValueError(f"{key} must contain nonempty strings")
    if len(value) != len(set(value)):
        raise ValueError(f"{key} must not contain duplicates")
    return value


def _validate_policy(policy: dict[str, Any]) -> tuple[list[str], set[str]]:
    if policy.get("schema_version") != 1:
        raise ValueError("unsupported policy schema_version")
    required = _string_list(policy, "required_checks")
    critical = set(_string_list(policy, "critical_checks"))
    if not critical.issubset(required):
        raise ValueError("critical_checks must be a subset of required_checks")
    trusted = policy.get("trusted_producers")
    if not isinstance(trusted, dict) or set(trusted) != set(required):
        raise ValueError("trusted_producers must define every and only required check")
    for name, ids in trusted.items():
        if not isinstance(ids, list) or not ids or not all(
            isinstance(item, str) and item.strip() for item in ids
        ):
            raise ValueError(f"trusted producer IDs required for check: {name}")
    _string_list(policy, "trusted_authorities")
    _string_list(policy, "trusted_source_urls")
    return required, critical


def _validate_claim(claim: dict[str, Any]) -> None:
    reserved = sorted(RESERVED_CLAIM_KEYS.intersection(claim))
    if reserved:
        raise ValueError(
            "claim attempted to supply reserved authority fields: " + ", ".join(reserved)
        )
    for key in ("claim_id", "text", "claim_scope", "falsifier"):
        if not isinstance(claim.get(key), str) or not claim[key].strip():
            raise ValueError(f"{key} must be a nonempty string")
    if claim["claim_scope"] not in VALID_SCOPES:
        raise ValueError("unsupported claim_scope")


def _validate_source(source: dict[str, Any], policy: dict[str, Any]) -> None:
    if source.get("schema_version") != 1:
        raise ValueError("unsupported source schema_version")
    if source.get("authority") not in policy["trusted_authorities"]:
        raise ValueError("source authority is not approved")
    urls = source.get("official_urls")
    if not isinstance(urls, list) or not urls:
        raise ValueError("official source URLs are required")
    if not set(urls).issubset(policy["trusted_source_urls"]):
        raise ValueError("source contains an unapproved URL")
    if not isinstance(source.get("retrieved_utc"), str) or not source["retrieved_utc"]:
        raise ValueError("source retrieval time is required")
    findings = source.get("paraphrased_findings")
    if not isinstance(findings, list) or not findings:
        raise ValueError("paraphrased source findings are required")
    for finding in findings:
        if not isinstance(finding, dict) or not all(
            isinstance(finding.get(key), str) and finding[key].strip()
            for key in ("source", "section", "summary")
        ):
            raise ValueError(
                "every paraphrased source finding requires source, section, and summary"
            )


def _validate_evidence(
    claim: dict[str, Any],
    source: dict[str, Any],
    policy: dict[str, Any],
    evidence: dict[str, Any],
    required: list[str],
) -> dict[str, str]:
    if not isinstance(evidence, dict) or evidence.get("schema_version") != 1:
        raise ValueError("a schema-versioned evidence bundle is required")
    bindings = {
        "claim_sha256": canonical_sha256(claim),
        "source_sha256": canonical_sha256(source),
        "policy_sha256": canonical_sha256(policy),
    }
    mismatched = [key for key, expected in bindings.items() if evidence.get(key) != expected]
    if mismatched:
        raise ValueError("evidence binding mismatch: " + ", ".join(mismatched))
    checks = evidence.get("checks")
    if not isinstance(checks, dict) or set(checks) != set(required):
        raise ValueError("evidence checks must define every and only required check")
    invalid = {name: state for name, state in checks.items() if state not in VALID_STATES}
    if invalid:
        raise ValueError(f"invalid check states: {invalid}")
    producers = evidence.get("producers")
    if not isinstance(producers, dict) or set(producers) != set(required):
        raise ValueError("evidence producers must define every and only required check")
    for name in required:
        producer = producers[name]
        if not isinstance(producer, dict) or set(producer) != {"role", "id"}:
            raise ValueError(f"producer record is malformed for check: {name}")
        if producer["role"] != "external_gate_harness":
            raise ValueError(f"producer role is not approved for check: {name}")
        if producer["id"] not in policy["trusted_producers"][name]:
            raise ValueError(f"producer is not approved for check: {name}")
    if "not_applicable" in checks.values():
        allowed = (
            claim["claim_scope"] == "statutory_text"
            and checks.get("external_outcome_evidence") == "not_applicable"
            and all(
                state != "not_applicable"
                for name, state in checks.items()
                if name != "external_outcome_evidence"
            )
        )
        if not allowed:
            raise ValueError("not_applicable is invalid for this claim or check")
    return checks


def evaluate_claim(
    claim: dict[str, Any],
    source: dict[str, Any],
    policy: dict[str, Any],
    evidence: dict[str, Any],
) -> ClaimDecision:
    required, critical = _validate_policy(policy)
    _validate_claim(claim)
    _validate_source(source, policy)
    checks = _validate_evidence(claim, source, policy, evidence, required)
    facts = {
        "claim_id": claim["claim_id"],
        "claim_scope": claim["claim_scope"],
        "source_authority": source["authority"],
        "source_checked_through": source["current_law_checked_through"],
        "evidence_coverage": sum(
            state in {"pass", "fail", "not_applicable"} for state in checks.values()
        ) / len(required),
    }
    failed_critical = sorted(name for name in critical if checks[name] == "fail")
    if failed_critical:
        return ClaimDecision(
            "REJECT",
            [
                "critical evidence failed: " + ", ".join(failed_critical),
                "declared falsifier: " + claim["falsifier"],
            ],
            facts,
        )
    unknown = sorted(name for name in required if checks[name] == "unknown")
    if unknown:
        return ClaimDecision(
            "ESCALATE",
            ["required evidence is unknown: " + ", ".join(unknown)],
            facts,
        )
    noncritical_failures = sorted(
        name for name in required if name not in critical and checks[name] == "fail"
    )
    if noncritical_failures:
        return ClaimDecision(
            "ESCALATE",
            ["noncritical evidence failed and requires human review: " + ", ".join(noncritical_failures)],
            facts,
        )
    return ClaimDecision("KEEP", ["all delegated publication checks passed"], facts)
