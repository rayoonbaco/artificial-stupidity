# Bill X-Ray second-domain validation results (v0.9.3)

Recorded: 2026-09-14 UTC  
Result: **PASS — all three predeclared actions observed**

## What was tested

Artificial Stupidity began as an evidence boundary around an autonomous AI-research loop. This test asked whether the doctrine could govern a materially different task: deciding whether a proposed plain-English statement about Illinois SB 1570 should be published as supported, rejected as contradicted, or paused because the authoritative source cannot establish the claimed consequence.

The contract was frozen before adapter implementation. The Bill X-Ray repository and the v0.9.2 AI-research gate were not changed. A separate law-claim adapter was then built around claim, official-source, policy, evidence, and producer records bound by canonical SHA-256.

## Results

| Case | Proposed statement | Expected | Observed | Why |
|---|---|---:|---:|---|
| BX01 | A municipality receiving one Phase I response may conditionally proceed to Phase II. | KEEP | **KEEP** | The bounded statutory statement matched the official current-law record and stayed within statutory scope. |
| BX02 | Illinois requires every municipality to use design-build and guarantees a funded-project pipeline. | REJECT | **REJECT** | The law authorizes an elective method; it does not mandate adoption, appropriate project funds, or guarantee a pipeline. |
| BX03 | The amendment will increase a contractor's win rate and market demand. | ESCALATE | **ESCALATE** | Statutory text cannot establish future owner behavior, market demand, or contractor outcomes. |

The machine-readable receipt is `benchmark/second_domain_bill_xray/machine_receipt.json`.

## Verification

- Bill X-Ray baseline: **105/105 tests passed** before the contract was frozen.
- Artificial Stupidity v0.9.3 suite: **73/73 tests passed**, comprising the protected v0.9.2 suite, 17 new portability/security tests, and one public-page disclosure test.
- Frozen cases: **3/3 matched their expected actions**.
- Negative controls refuse substituted claims, sources, and policies; candidate-supplied evidence; duplicate JSON keys; unapproved producers and authorities; and malformed check sets.
- Re-running the frozen matrix reproduces the checked-in receipt exactly.

## Sources checked

Primary Illinois General Assembly sources were used for the bounded legal statements:

- [Public Act 103-0491](https://www.ilga.gov/Legislation/PublicActs/PrinterFriendly/103-0491)
- [Public Act 104-0395](https://www.ilga.gov/Legislation/PublicActs/PrinterFriendly/104-0395)
- [Current 65 ILCS 5/11-39.2-25](https://www.ilga.gov/documents/legislation/ilcs/documents/006500050K11-39.2-25.htm)

The stored source record contains labeled paraphrases, not quotations. Reviewers should read the linked official text before relying on any legal statement.

## What this means

The result supplies initial evidence that the doctrine is portable beyond its original metric-optimization setting. The reusable element is not the H100 metric schema. It is the decision structure: a proposer cannot authorize its own evidence; acceptance rules and sources are declared separately; contradictions reject; unresolved but nondisqualifying uncertainty escalates; and only bounded, fully supported claims are kept.

That is a stronger result than another demonstration inside the same optimization task. It remains a small, designed validation conducted by the same builder/system.

## Claim boundary

This is not legal advice, a legal-accuracy certification, a real-world error-rate estimate, proof of scientific novelty, proof of general AI safety, or an independent reproduction. It does not establish that the adapter can interpret arbitrary legislation. The three cases were deterministic and hand-authored, and the evidence producer labels are allowlisted identifiers rather than cryptographic identities.

## Human decision

The machine result is **PASS for the frozen portability contract**. Human authorization is limited to publishing that bounded result and its artifacts. It does not authorize broader legal, safety, novelty, or market-effect claims.
