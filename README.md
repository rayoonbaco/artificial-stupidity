# Artificial Stupidity

**A MONAHINGA™ Evidence Project**

> Intelligence proposes. Artificial Stupidity challenges. Evidence adjudicates. A human authorizes.

Artificial Stupidity is an experimental evidence gate for autonomous AI research. It adds a separate acceptance boundary around Andrej Karpathy's `autoresearch` loop so a promising metric cannot quietly certify itself. The gate can return `KEEP`, `REJECT`, or `ESCALATE` based on repeatability, separately stored holdout performance, resource use, critical failures, and human review.

This repository contains the working prototype, 74 automated tests, a reproducible six-run H100 protocol, complete raw logs, source snapshots, SHA-256 manifests, a separately recorded machine decision, a named human authorization, preserved before/after adversarial receipts, and a frozen same-team portability demonstration using Bill X-Ray legislative claims.

## The result in one glance

The tested candidate changed one functional line:

```python
TOTAL_BATCH_SIZE = 2**19  # baseline
TOTAL_BATCH_SIZE = 2**18  # candidate
```

Under a declared fixed-wall-clock H100 SXM protocol, three baseline runs and three candidate runs were interleaved B1/C1/B2/C2/B3/C3:

| Metric (lower is better) | Baseline median | Candidate median | Relative improvement |
|---|---:|---:|---:|
| Validation BPB | 1.000213 | 0.990934 | 0.928% |
| Protected-holdout BPB | 0.999357 | 0.990126 | 0.924% |
| Peak VRAM | 45,060.2 MB | 44,908.2 MB | 0.337% lower |

- Each of the three candidate runs beat each of the three baseline runs on validation (all nine cross-arm comparisons).
- Each of the three candidate runs beat each of the three baseline runs on the separately stored holdout (all nine cross-arm comparisons).
- All six training runs exited successfully.
- The machine returned **ESCALATE** because human comprehensibility was intentionally unknown.
- Raymond Anthony Gomez reviewed the bounded evidence and one-line change and authorized **KEEP** on September 13, 2026.

The machine and human decisions remain separate in the record. That separation is the point.

## What this establishes

It establishes that the current gate is executable, fail-closed, and capable of withholding automatic acceptance after a metric improves. It also establishes that, under this specific fixed-wall-clock H100 protocol, each candidate run recorded lower validation and holdout BPB than each baseline run.

The protocol did not hold total optimizer steps or tokens processed constant, so it does not isolate batch size as the cause of the observed difference. It does **not** establish that the candidate is universally better, that smaller batches generally improve model performance, that the gate improves safety in every domain, or that the holdout was cryptographically secret. This is a bounded engineering result, not a causal scientific finding or safety certification.

## Start here

Choose the shortest useful path:

1. **Plain-English orientation:** [Human Companion v0.9.4](docs/Artificial_Stupidity_Human_Companion_v0.9.4.pdf).
2. **Three-minute review:** [Executive Summary v0.9.4](docs/Artificial_Stupidity_Executive_Summary_Ray_Gomez_2026.pdf).
3. **Full record:** [Research Dossier v0.9.4](docs/Artificial_Stupidity_Dossier_Ray_Gomez_2026.pdf).
4. **Visual chronology:** [Joke → build → test → fail → repair → invite review](static/evidence-chronology-v0.9.4.png).
5. **Machine record:** inspect [`VERIFIED_RESULT.md`](benchmark/evidence/h100_sxm_20260913/repaired_decision/VERIFIED_RESULT.md).
6. **Integrity:** verify the nested `SHA256SUMS.txt` files and repository-wide `INTEGRITY_SHA256.txt`.
7. **Adversarial record:** compare the frozen [`v0.9.2 plan`](docs/ADVERSARIAL_TEST_PLAN_v0.9.2.md), preserved [`v0.9.1 failure receipt`](benchmark/adversarial/v091_failure_receipt.json), and [`v0.9.2 campaign receipt`](benchmark/adversarial/v092_campaign_receipt.json).
8. **Portability exercise:** inspect the pre-implementation [`Bill X-Ray contract`](docs/BILL_XRAY_SECOND_DOMAIN_CONTRACT_v0.9.3.md), [`results`](docs/BILL_XRAY_SECOND_DOMAIN_RESULTS_v0.9.3.md), and machine-readable [`receipt`](benchmark/second_domain_bill_xray/machine_receipt.json).

## Run locally without a GPU

Python 3.10+ is recommended.

```bash
uv sync
uv run python -m unittest discover -s tests -v

uv run python -m gate.as_gate --baseline gate/examples/baseline.json --candidate gate/examples/candidate_keep.json --evidence gate/examples/evidence_keep.json
```

Windows users can extract the repository and double-click `START_ARTIFICIAL_STUPIDITY.bat` for a plain-language menu.

## Reproduce the H100 protocol

On a fresh single-H100 environment:

```bash
bash RUN_H100_EVIDENCE.sh
```

The harness runs B1/C1/B2/C2/B3/C3, evaluates the pinned validation shard and separately stored holdout shard 06541, captures stdout/stderr, records the environment and source hashes, evaluates the gate, and creates a download-ready evidence ZIP even if a command fails. Read [`benchmark/H100_RERUN_PROTOCOL.md`](benchmark/H100_RERUN_PROTOCOL.md) before spending compute.

## Repository map

| Path | Purpose |
|---|---|
| `gate/` | Separate KEEP / REJECT / ESCALATE decision logic |
| `benchmark/` | Comparison tools, protocol, reports, and preserved evidence |
| `benchmark/second_domain_bill_xray/` | Frozen legislative-claim cases, separate adapter, source record, and receipt |
| `benchmark/evidence/h100_sxm_20260913/original/raw_logs/` | Unedited run logs |
| `benchmark/evidence/h100_sxm_20260913/original/source_snapshot/` | Code and configuration captured with the experiment |
| `benchmark/evidence/h100_sxm_20260913/repaired_decision/` | Transparent post-run import repair and final records |
| `tests/` | 74 CPU-only tests, including frozen adversarial, portability, and public-disclosure cases |
| `docs/` | Dossier, executive summary, audit, build clock, and adversarial reports |
| `launch/` | Public launch copy, case study, claims, and commercial boundary |

## An adversarial failure that changed the gate

The first v0.9.1 adversarial campaign exposed a serious trust-boundary weakness: 8 of 9 attack probes produced unjustified `KEEP` outcomes. Version 0.9.2 repaired those paths, added explicit unknown-state remedies, and passed the frozen follow-up attack and control matrix. The before-and-after receipts remain public so the repaired result does not erase the original failure.

## A transparent execution failure

After all six paid runs and both evaluations completed, the runner failed during its final gate import with `ModuleNotFoundError: No module named 'gate'`. The evidence archive, hashes, logs, and source snapshot were unaffected. The decision was reconstructed locally from those preserved inputs using the captured gate code and configuration; no additional model training occurred. The import path is fixed and covered by a regression test. See `REPAIR_PROVENANCE.md` in the evidence folder.

## Public and commercial use

The research prototype and evidence are public under the repository license. Organizations interested in a private pilot may inquire about integration, private deployment, customized evidence rules, audit-ready reporting, and support. Those services are not implied warranties, safety certifications, or endorsements.

Contact: **Raymond Anthony Gomez** — [GitHub profile](https://github.com/rayoonbaco)

## Origin and attribution

This project is an additive derivative of Andrej Karpathy's [`autoresearch`](https://github.com/karpathy/autoresearch), pinned here to upstream commit `228791fb499afffb54b46200aca536f79142f117`. The upstream training files and original program are preserved, and the added gate is deliberately external to the optimizer. Full attribution and MIT terms are in [`UPSTREAM_LICENSE_NOTICE.md`](UPSTREAM_LICENSE_NOTICE.md).

Concept, framing, project direction, and human authorization: **Raymond Anthony Gomez**. Research synthesis, source checking, drafting, visualization, and prototype implementation were developed through iterative work with ChatGPT.

## Trademark and claim boundary

**MONAHINGA™** is used as the source identity for this evidence project. USPTO serial 99613654 is live/pending; registration has not issued. Use of the mark does not authenticate the research or create ownership over facts, methods, code inherited under license, or historical events.

Artificial Stupidity is a working research prototype. It is not peer reviewed, production hardened, or a substitute for qualified technical, legal, safety, or domain review.

## Second-domain result

The doctrine has also been exercised against three same-team, pre-labeled Bill X-Ray legislative claims frozen before adapter implementation. It kept a source-supported statutory statement, rejected a contradicted mandate-and-funding overclaim, and escalated an unsupported contractor-outcome forecast. This is initial same-team portability evidence—not legal advice, independent reproduction, an error-rate estimate, or proof of general AI safety.

## License

MIT. See [`LICENSE`](LICENSE) and [`UPSTREAM_LICENSE_NOTICE.md`](UPSTREAM_LICENSE_NOTICE.md).

## Build clock

This project moved from a precursor joke to a defined build in approximately 24 hours, then to a tested prototype verified on GitHub-hosted CI in approximately 52 hours. The clock stopped at approximately hour 55 when the first complete external-review submission was sent on September 14, 2026 at 3:03 PM EDT. That is approximately 31 hours from the defined build project.

The external review is **pending**. Sending a packet is not a completed review, reproduction, endorsement, or validation.

[See the contemporaneous milestone ledger](docs/BUILD_CLOCK.md) and [submission record](docs/EXTERNAL_REVIEW_SUBMISSION_2026-09-14.md).
