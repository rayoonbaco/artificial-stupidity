# v0.9.1 trust-boundary hardening

This release candidate responds to the September 14, 2026 submission-readiness audit while preserving the original v0.9.0 evidence files unchanged.

## What changed

- Candidate records may contain experiment facts but may not contain checks, evidence, authorization, policy hashes, or final decisions.
- Evidence is a separate bundle bound to canonical SHA-256 hashes of the candidate and policy.
- Every required check names an evidence producer.
- A passing human-comprehensibility check requires a `human_reviewer` producer and the SHA-256 of a separate authorization artifact.
- The H100 runner constructs its own machine evidence and continues to force human comprehensibility to `unknown`.
- The public web demonstration accepts only server-published scenario identifiers; arbitrary client candidates cannot be treated as trusted evidence.
- Future H100 source snapshots include the evidence-runner code itself.
- CPU tests no longer import the CUDA, Torch, or PyArrow stack merely to inspect path separation.

## Boundary that remains

Hash binding detects substitution and mismatch; it does not prove who created a file. An attacker controlling the candidate, evidence, policy, and execution environment can still forge a self-consistent bundle. Production-grade independence therefore remains **planned**, requiring isolated permissions, cryptographic signing, or a separately administered gate service.

## Verification

```bash
python -m unittest discover -s tests -v
python gate/as_gate.py --baseline gate/examples/baseline.json --candidate gate/examples/candidate_keep.json --evidence gate/examples/evidence_keep.json
```

The full suite contains 36 tests. Four Flask route tests skip in a bare Python environment and execute in CI after `requirements.txt` is installed.
