"""Independent evidence gate for autoresearch experiment candidates.

This module never trains or edits a model. It evaluates a candidate record against
the currently accepted baseline and returns KEEP, REJECT, or ESCALATE.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


VALID_CHECK_STATES = {"pass", "fail", "unknown"}
VALID_PRODUCER_ROLES = {"independent_harness", "human_reviewer"}
RESERVED_CANDIDATE_KEYS = {
    "checks",
    "evidence",
    "evidence_bundle",
    "human_authorization",
    "authorization",
    "machine_gate_action",
    "final_governed_decision",
    "policy_sha256",
}


@dataclass(frozen=True)
class Decision:
    action: str
    reasons: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    facts: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "action": self.action,
            "reasons": self.reasons,
            "warnings": self.warnings,
            "facts": self.facts,
        }


def _finite_number(record: dict[str, Any], key: str) -> float:
    value = record.get(key)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{key} must be a number")
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{key} must be finite")
    return value


def _load_json(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _nonnegative_integer(record: dict[str, Any], key: str) -> int:
    if key not in record:
        raise ValueError(f"{key} is required")
    value = record[key]
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{key} must be an integer")
    if value < 0:
        raise ValueError(f"{key} must be nonnegative")
    return value


def _string_list(record: dict[str, Any], key: str) -> list[str]:
    value = record.get(key)
    if not isinstance(value, list) or not all(
        isinstance(item, str) and item for item in value
    ):
        raise ValueError(f"{key} must be a list of nonempty strings")
    if len(set(value)) != len(value):
        raise ValueError(f"{key} must not contain duplicates")
    return value


def canonical_sha256(record: dict[str, Any]) -> str:
    """Hash a JSON object using a stable, whitespace-independent encoding."""
    encoded = json.dumps(
        record, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def build_evidence_bundle(
    candidate: dict[str, Any],
    config: dict[str, Any],
    checks: dict[str, str],
    producers: dict[str, dict[str, str]],
) -> dict[str, Any]:
    """Build an integrity-bound bundle outside the candidate record."""
    return {
        "schema_version": 1,
        "candidate_sha256": canonical_sha256(candidate),
        "policy_sha256": canonical_sha256(config),
        "checks": checks,
        "producers": producers,
    }


def _validated_checks(
    candidate: dict[str, Any], evidence: dict[str, Any], config: dict[str, Any]
) -> dict[str, str]:
    reserved = sorted(RESERVED_CANDIDATE_KEYS.intersection(candidate))
    if reserved:
        raise ValueError(
            "candidate attempted to supply reserved authority fields: "
            + ", ".join(reserved)
        )
    if not isinstance(evidence, dict):
        raise ValueError("a separate trusted evidence bundle is required")
    if evidence.get("schema_version") != 1:
        raise ValueError("unsupported evidence schema_version")
    if evidence.get("candidate_sha256") != canonical_sha256(candidate):
        raise ValueError("evidence is not bound to this candidate")
    if evidence.get("policy_sha256") != canonical_sha256(config):
        raise ValueError("evidence is not bound to this policy")

    checks = evidence.get("checks")
    if not isinstance(checks, dict):
        raise ValueError("evidence checks must be an object")
    malformed = {
        name: state for name, state in checks.items() if state not in VALID_CHECK_STATES
    }
    if malformed:
        raise ValueError(f"invalid check states: {malformed}")

    producers = evidence.get("producers")
    if not isinstance(producers, dict):
        raise ValueError("evidence producers must be an object")
    required = _string_list(config, "required_checks")
    for name in required:
        producer = producers.get(name)
        if not isinstance(producer, dict):
            raise ValueError(f"trusted producer is required for check: {name}")
        role = producer.get("role")
        producer_id = producer.get("id")
        if role not in VALID_PRODUCER_ROLES:
            raise ValueError(f"invalid producer role for check {name}: {role}")
        if not isinstance(producer_id, str) or not producer_id.strip():
            raise ValueError(f"producer id is required for check: {name}")
        if name == "human_comprehensibility" and checks.get(name) == "pass":
            digest = producer.get("artifact_sha256")
            if role != "human_reviewer":
                raise ValueError(
                    "human_comprehensibility pass requires a human_reviewer producer"
                )
            if not isinstance(digest, str) or len(digest) != 64 or any(
                char not in "0123456789abcdef" for char in digest.lower()
            ):
                raise ValueError(
                    "human_comprehensibility pass requires an authorization artifact SHA-256"
                )
    return checks


def evaluate(
    baseline: dict[str, Any],
    candidate: dict[str, Any],
    config: dict[str, Any],
    evidence: dict[str, Any],
) -> Decision:
    """Evaluate a candidate against separately produced, integrity-bound evidence."""
    baseline_bpb = _finite_number(baseline, "val_bpb")
    candidate_bpb = _finite_number(candidate, "val_bpb")
    baseline_memory = _finite_number(baseline, "peak_vram_mb")
    candidate_memory = _finite_number(candidate, "peak_vram_mb")

    if baseline_bpb <= 0 or candidate_bpb <= 0:
        return Decision("REJECT", ["val_bpb must be positive"])
    if baseline_memory <= 0 or candidate_memory <= 0:
        return Decision("REJECT", ["peak_vram_mb must be positive"])

    min_gain = float(config["minimum_val_bpb_improvement"])
    if not math.isfinite(min_gain) or min_gain < 0:
        raise ValueError("minimum_val_bpb_improvement must be finite and nonnegative")
    gain = baseline_bpb - candidate_bpb
    memory_growth = (candidate_memory - baseline_memory) / baseline_memory
    max_memory_growth = float(config["maximum_memory_growth_fraction"])
    if not math.isfinite(max_memory_growth) or max_memory_growth < 0:
        raise ValueError("maximum_memory_growth_fraction must be finite and nonnegative")
    max_complexity = _nonnegative_integer(config, "maximum_complexity_delta_lines")
    complexity_delta = _nonnegative_integer(candidate, "complexity_delta_lines")

    checks = _validated_checks(candidate, evidence, config)

    required = _string_list(config, "required_checks")
    critical = set(_string_list(config, "critical_checks"))
    if not critical.issubset(required):
        raise ValueError("critical_checks must be a subset of required_checks")
    known = sum(checks.get(name, "unknown") != "unknown" for name in required)
    coverage = known / len(required) if required else 1.0
    minimum_coverage = float(config["minimum_evidence_coverage"])
    if not math.isfinite(minimum_coverage) or not 0 <= minimum_coverage <= 1:
        raise ValueError("minimum_evidence_coverage must be between 0 and 1")

    facts = {
        "baseline_val_bpb": baseline_bpb,
        "candidate_val_bpb": candidate_bpb,
        "val_bpb_improvement": round(gain, 9),
        "memory_growth_fraction": round(memory_growth, 6),
        "complexity_delta_lines": complexity_delta,
        "evidence_coverage": round(coverage, 3),
        "candidate_sha256": canonical_sha256(candidate),
        "policy_sha256": canonical_sha256(config),
    }

    reject_reasons: list[str] = []
    escalate_reasons: list[str] = []
    warnings: list[str] = []

    if candidate.get("run_status", "ok") != "ok":
        reject_reasons.append("candidate run did not complete successfully")
    if gain < min_gain:
        reject_reasons.append(
            f"primary metric did not improve by the required {min_gain:.6f}"
        )
    if memory_growth > max_memory_growth:
        reject_reasons.append(
            f"memory grew {memory_growth:.1%}, above the {max_memory_growth:.1%} limit"
        )
    failed_critical = sorted(name for name in critical if checks.get(name) == "fail")
    if failed_critical:
        reject_reasons.append("critical checks failed: " + ", ".join(failed_critical))

    unknown_critical = sorted(name for name in critical if checks.get(name, "unknown") == "unknown")
    if unknown_critical and config.get("escalate_on_unknown_critical_check", True):
        escalate_reasons.append("critical evidence is unknown: " + ", ".join(unknown_critical))
    unknown_required = sorted(
        name for name in required if checks.get(name, "unknown") == "unknown"
    )
    if unknown_required and config.get("escalate_on_unknown_required_check", True):
        escalate_reasons.append(
            "required evidence is unknown: " + ", ".join(unknown_required)
        )
    if coverage < minimum_coverage:
        escalate_reasons.append(
            f"evidence coverage {coverage:.0%} is below the required "
            f"{minimum_coverage:.0%}"
        )
    if complexity_delta > max_complexity:
        escalate_reasons.append(
            f"complexity grew by {complexity_delta} lines, above the {max_complexity}-line review threshold"
        )
    noncritical_failures = sorted(
        name for name in required if name not in critical and checks.get(name) == "fail"
    )
    if noncritical_failures:
        escalate_reasons.append("noncritical checks failed: " + ", ".join(noncritical_failures))
    missing_falsifiability: list[str] = []
    if not isinstance(candidate.get("hypothesis"), str) or not candidate.get("hypothesis", "").strip():
        missing_falsifiability.append("hypothesis")
    if not isinstance(candidate.get("disconfirming_result"), str) or not candidate.get(
        "disconfirming_result", ""
    ).strip():
        missing_falsifiability.append("disconfirming_result")
    if missing_falsifiability:
        message = "falsifiability fields are missing: " + ", ".join(missing_falsifiability)
        if config.get("require_falsifiable_hypothesis", True):
            escalate_reasons.append(message)
        else:
            warnings.append(message)

    if reject_reasons:
        return Decision("REJECT", reject_reasons, warnings, facts)
    if escalate_reasons:
        return Decision("ESCALATE", escalate_reasons, warnings, facts)
    return Decision(
        "KEEP",
        ["primary metric improved within resource limits and required evidence passed"],
        warnings,
        facts,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate an autoresearch candidate")
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--evidence", required=True)
    parser.add_argument("--config", default=str(Path(__file__).with_name("gate_config.json")))
    parser.add_argument("--output")
    args = parser.parse_args()

    try:
        decision = evaluate(
            _load_json(args.baseline),
            _load_json(args.candidate),
            _load_json(args.config),
            _load_json(args.evidence),
        )
    except (OSError, TypeError, ValueError, KeyError, json.JSONDecodeError) as exc:
        decision = Decision("ESCALATE", [f"gate input could not be trusted: {exc}"])

    rendered = json.dumps(decision.to_dict(), indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return {"KEEP": 0, "REJECT": 2, "ESCALATE": 3}[decision.action]


if __name__ == "__main__":
    raise SystemExit(main())
