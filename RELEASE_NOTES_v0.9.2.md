# Artificial Stupidity v0.9.2 - adversarial hardening candidate

This prerelease preserves the v0.9.1 trust-boundary failures, repairs them, and publishes machine-readable before/after receipts. The H100 measurements and original human authorization are unchanged.

## Frozen campaign

The attack plan was written before implementation. Nine v0.9.1 probes exposed eight unjustified KEEP outcomes under direct control of inputs that the implementation had assumed were trusted, plus one duplicate-key ambiguity. The original gate source and failure receipt are preserved under `benchmark/adversarial/`.

The repaired gate then passed 12 attack cases and four action controls. The full regression suite now contains 55 CPU-only tests and passes with Flask installed.

## Repairs

- Evidence is bound to baseline, candidate, and policy hashes.
- Core required and critical checks cannot be silently removed from policy.
- Policy thresholds require finite numeric types; booleans and numeric strings are refused.
- Required evidence producers must match explicit role-and-ID allowlists.
- Human-comprehensibility PASS requires the complete review payload, bound to the same baseline, candidate, and policy, with a matching canonical digest.
- Ambiguous JSON with duplicate keys is refused.
- Undeclared checks and producers are refused.
- Missing run status is refused instead of defaulting to success.
- The hardened H100 replay fixture now binds to the protected-holdout baseline record rather than the earlier PCIe-stage baseline; this corrects replay facts without changing any preserved measurement or decision.

## Preserved limitations

Producer allowlists identify expected labels but do not cryptographically authenticate people or processes. A party controlling the policy, evidence, and runtime can still forge the record. Production deployment requires OS-level separation, signed attestations, or an independently administered gate service.

The designed attack suite measures conformance to declared rules, not real-world incident probability or general AI safety. External reproduction and qualified review remain pending.
