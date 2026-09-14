# Bill X-Ray second-domain validation contract (v0.9.3)

Status: **FROZEN BEFORE ADAPTER IMPLEMENTATION**  
Recorded: 2026-09-14 UTC  
Registration boundary: repository-local predeclaration, not a trusted third-party preregistration.

## Decision

Can the Artificial Stupidity evidence-boundary doctrine govern a materially different decision: whether a proposed plain-English statement about Illinois SB 1570 may be published as supported, must be refused as contradicted, or must be paused because the statute cannot establish the claimed real-world consequence?

## Operator and consequence

The operator is a Bill X-Ray editor preparing public legislative explanations. Readers bear the consequence of an inaccurate or overstated claim. The machine may govern publication only within the declared evidence boundary; legal advice, business conclusions, motive, and real-world outcome claims remain outside its authority.

## Upstream source

- Repository: `https://github.com/rayoonbaco/Bill_XRay_Next`
- Inspected commit: `5462bab5717bc4b9459aee195616652b8c47089b`
- Snapshot supplied from GitHub on 2026-09-14.
- Baseline verification: 105 repository tests passed locally before this contract was written.
- License status: no license file was present in the inspected Bill X-Ray snapshot. No Bill X-Ray code will be redistributed or modified by this validation; only bounded factual receipts and provenance metadata will be recorded in Artificial Stupidity.

## Protected cores

1. The Bill X-Ray repository and its deployed product remain unchanged.
2. The Artificial Stupidity v0.9.2 autoresearch gate remains unchanged.
3. The preserved H100 measurements, machine decision, human authorization, and adversarial receipts remain unchanged.

## Transformative delta

Add a separate deterministic law-claim adapter that reuses the doctrine, not the H100 metric schema. The adapter binds a proposed claim, source record, policy, evidence checks, and producer identities by canonical SHA-256. It returns the same three governed actions: KEEP, REJECT, or ESCALATE.

## Source of truth

Primary legal sources only for statutory claims:

- Illinois Public Act 103-0491, the foundation act: `https://www.ilga.gov/Legislation/PublicActs/PrinterFriendly/103-0491`
- Illinois Public Act 104-0395, effective 2025-07-01: `https://www.ilga.gov/Legislation/PublicActs/PrinterFriendly/104-0395`
- Current municipal provision, 65 ILCS 5/11-39.2-25.

Bill X-Ray's own derived receipts are comparison inputs, not independent proof of their own correctness.

## Predeclared cases

### BX01 — supported statutory statement

Candidate: A municipality receiving only one Phase I response may proceed with a Phase II evaluation of that respondent if the municipality, in its discretion, finds proceeding to be in its best interest.

Expected action: **KEEP**.

Required evidence: official authority, current-law status, direct statutory-text match, scope restraint, and source/claim/policy hash binding all pass.

### BX02 — contradicted overclaim

Candidate: Illinois law requires every municipality to use design-build and guarantees a pipeline of funded projects.

Expected action: **REJECT**.

Disqualifier: the official law authorizes municipalities to elect the method; it does not require adoption, appropriate project money, or guarantee a pipeline.

### BX03 — plausible consequence beyond the statute

Candidate: The amendment will increase a contractor's win rate and market demand.

Expected action: **ESCALATE**.

Reason: the statute can establish legal permission and procedure, but not future owner behavior, market demand, or a contractor's win rate. Independent outcome evidence and a named human decision would be required.

## Gate rules

- **KEEP** only if every required check passes and all integrity/provenance bindings validate.
- **REJECT** when a declared critical check fails or the claim conflicts with the authoritative source.
- **ESCALATE** when no declared disqualifier is known but required evidence is unknown or the conclusion exceeds machine authority.
- Malformed input, duplicate JSON keys, unapproved producers, missing hashes, mismatched hashes, undeclared checks, and unsupported authority fail closed as REFUSE errors rather than receiving a publication decision.

## Required checks

1. `official_source_authority` — critical.
2. `current_law_status` — critical.
3. `statutory_text_match` — critical.
4. `scope_boundary` — critical.
5. `external_outcome_evidence` — required but noncritical; it may be marked not applicable for a purely statutory claim.

## Acceptance tests

1. BX01 returns KEEP.
2. BX02 returns REJECT with an authorization-versus-mandate reason.
3. BX03 returns ESCALATE because outcome evidence or authority is insufficient.
4. Claim, source, or policy substitution is refused.
5. Candidate-supplied evidence or authorization is refused.
6. Duplicate JSON keys are refused.
7. Unapproved producers and authorities are refused.
8. Missing required checks and undeclared checks are refused.
9. Re-running the frozen matrix produces an identical machine-readable receipt.
10. All pre-existing Artificial Stupidity and Bill X-Ray tests remain green in their respective unchanged trees.

## Excluded claims

This test will not claim legal advice, proof of general AI safety, proof of scientific novelty, real-world error-rate reduction, market impact, production security, cryptographic identity, or independent scientific reproduction. It tests deterministic conformance on three predeclared claims and associated negative controls.

## Recovery and rollback

All new files will live under the Bill X-Ray second-domain benchmark, its tests, documentation, and runner. Removing those files and their CI invocation restores v0.9.2 behavior; neither protected core requires reversal.

## Cost and stopping conditions

- Authorized compute: CPU only.
- Authorized external spend: $0.
- Authorized network evidence: official public Illinois sources.
- Stop on any protected-core modification, ambiguous current-law text, failed legacy test, unexpected action, or non-deterministic receipt.
