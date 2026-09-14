# Artificial Stupidity — v0.9.1 hardening candidate

This prerelease converts the prototype's central trust boundary from a prose convention into an integrity-checked software contract while preserving the original v0.9.0 evidence record.

## Security and integrity changes

- Candidate-controlled records can no longer contain checks, evidence, authorization, policy hashes, or final decisions.
- Evidence is supplied separately and bound to canonical candidate and policy SHA-256 hashes.
- Every required check identifies a producer.
- A human-comprehensibility pass requires a human-review producer and a separate authorization-artifact hash.
- Candidate/evidence replay, policy substitution, attempted self-authorization, and candidate-supplied checks are tested and rejected.
- The public demo now evaluates only server-published scenarios.
- Future H100 evidence snapshots include the runner that produced them.

## Scientific-language and packaging changes

- The completed H100 protocol is described as **predeclared**, not independently preregistered.
- Public URLs, citation version metadata, and stale placeholders are corrected.
- Dossier and executive-summary PDFs are rebuilt from corrected source.
- CPU verification now runs in GitHub Actions on Python 3.10 and 3.12.
- The suite defines 36 tests; all 32 dependency-free tests pass locally, and four Flask route tests execute when web dependencies are installed.

## Preserved result

The H100 evidence itself is unchanged. Across three runs per arm, every candidate validation and sequestered-holdout BPB was lower than every baseline value. The machine decision remains **ESCALATE** because human comprehensibility was unknown, and the separate author authorization remains **KEEP**.

## Remaining boundary

Hash binding detects mismatches; it does not authenticate an attacker who controls every file and the execution environment. Production-grade independence still requires permissions, signatures, or a separately administered gate service. This is a research prototype, not a safety certification.
