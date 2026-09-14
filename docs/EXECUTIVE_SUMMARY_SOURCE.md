# ARTIFICIAL STUPIDITY

## An independent evidence gate for autonomous AI research

**A MONAHINGA™ Evidence Project**  
Executive brief | Raymond Anthony Gomez | September 2026

## The idea

The smarter an AI system becomes, the more persuasive and consequential its mistakes can become. Artificial Stupidity is a proposed independent counterforce: not a less intelligent model, but a separate process that challenges assumptions, seeks disconfirming evidence, preserves uncertainty, and refuses to let an optimizer certify its own work.

> Intelligence proposes. Artificial Stupidity challenges. Evidence adjudicates. A human authorizes.

## What was built

The first implementation is an external KEEP / REJECT / ESCALATE gate around Andrej Karpathy's autoresearch loop. The upstream optimizer remains intact. The gate evaluates repeatability, protected-holdout performance, resource growth, critical failures, and human comprehensibility. Malformed or missing required evidence fails closed. The public package includes 36 automated tests, a reproducible runner, complete raw logs, source snapshots, SHA-256 manifests, and separate machine and human decisions.

## What the experiment found

A candidate changed one functional line: total batch size from `2**19` to `2**18`. It was tested in three interleaved baseline/candidate pairs on one NVIDIA H100 SXM under the same five-minute training budget.

| Metric | Baseline median | Candidate median | Improvement |
|---|---:|---:|---:|
| Validation BPB | 1.000213 | 0.990934 | 0.928% |
| Protected-holdout BPB | 0.999357 | 0.990126 | 0.924% |
| Peak VRAM | 45,060.2 MB | 44,908.2 MB | 0.337% lower |

Every candidate beat every baseline on validation and holdout, producing 9/9 pairwise wins for each metric. All six runs exited successfully. The holdout was stored outside the training and ordinary validation paths, though it was not cryptographically secret.

## Why the machine still stopped

The empirical boundary passed, but the machine returned ESCALATE because `human_comprehensibility` was intentionally unknown. That was the gate doing its job: it had evidence to recommend the candidate, but no authority to grant its own final approval.

Raymond Anthony Gomez reviewed the one-line change and the bounded evidence and authorized KEEP on September 13, 2026. The original machine ESCALATE and the final governed KEEP remain separately preserved.

## The disclosed failure

After all six training runs and evaluations completed, the runner encountered a final import-path error. The raw logs, source snapshot, hashes, environment record, and partial results were intact. The decision was reconstructed from those preserved inputs without additional training; the path was fixed and a regression test added. The original failure remains in the record.

## Why it matters

Most "human in the loop" claims say little about what the human sees, what the machine may decide, or how disagreement is preserved. Artificial Stupidity makes the boundary operational: the proposer, challenger, evidence, and authorizer have distinct jobs and distinct records.

This result does not prove general AI safety or universal model improvement. It proves a bounded model-training result and demonstrates a falsifiable governance pattern that can now be tested in harder domains.

## Who could use it

The pattern is relevant to teams running autonomous research, coding agents, analytical workflows, model evaluation, regulated review, or other processes where a persuasive improvement should not become self-approval. The public core is free to inspect and reproduce. Potential paid pilots can cover private deployment, integrations, customized evidence rules, audit-ready reporting, and support.

## The opportunity

The project is distinctive because it combines a memorable thesis with executable evidence discipline. Its real value will not come from the phrase alone. It will come from proving that the gate reduces consequential error, preserves useful human authority, and fits workflows organizations already need to audit.

## Boundaries

- One model, dataset, H100 setup, candidate, and five-minute budget.
- Three runs per arm.
- Sequestered, not secret, holdout.
- Working prototype, not peer reviewed or production hardened.
- No endorsement by Karpathy, RunPod, OpenAI, or cited authors.
- MONAHINGA is live/pending, not registered; use MONAHINGA™, not the registration symbol.

## Recommended next move

Publish the clean repository and evidence, invite reproduction and criticism, and recruit one narrowly scoped pilot where the evidence rules and human authority can be declared before the system runs.

Repository: `https://github.com/rayoonbaco/artificial-stupidity`

Full citations appear in the accompanying dossier. Experiment evidence is preserved under `benchmark/evidence/h100_sxm_20260913/`.
