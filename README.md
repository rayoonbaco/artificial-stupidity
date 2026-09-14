# Artificial Stupidity

**A MONAHINGA™ Evidence Project**

> Intelligence proposes. Artificial Stupidity challenges. Evidence adjudicates. A human authorizes.

Artificial Stupidity is an experimental evidence gate for autonomous AI research. It adds a separate acceptance boundary around Andrej Karpathy's `autoresearch` loop so a promising metric cannot quietly certify itself. The gate can return `KEEP`, `REJECT`, or `ESCALATE` based on repeatability, protected-holdout performance, resource use, critical failures, and human review.

This repository contains the working prototype, 32 automated tests, a reproducible six-run H100 protocol, complete raw logs, source snapshots, SHA-256 manifests, a separately recorded machine decision, and a named human authorization.

## The result in one glance

The tested candidate changed one functional line:

```python
TOTAL_BATCH_SIZE = 2**19  # baseline
TOTAL_BATCH_SIZE = 2**18  # candidate
```

Under a predeclared H100 SXM protocol with three interleaved baseline/candidate pairs:

| Metric (lower is better) | Baseline median | Candidate median | Relative improvement |
|---|---:|---:|---:|
| Validation BPB | 1.000213 | 0.990934 | 0.928% |
| Protected-holdout BPB | 0.999357 | 0.990126 | 0.924% |
| Peak VRAM | 45,060.2 MB | 44,908.2 MB | 0.337% lower |

- Every candidate beat every baseline on validation: **9/9 pairwise wins**.
- Every candidate beat every baseline on the sequestered holdout: **9/9 pairwise wins**.
- All six training runs exited successfully.
- The machine returned **ESCALATE** because human comprehensibility was intentionally unknown.
- Raymond Anthony Gomez reviewed the bounded evidence and one-line change and authorized **KEEP** on September 13, 2026.

The machine and human decisions remain separate in the record. That separation is the point.

## What this establishes

It establishes that this gate is executable, fail-closed, and capable of withholding automatic acceptance after a metric improves. It also establishes that this particular candidate survived the predeclared validation and sequestered-holdout test on this H100 setup.

It does **not** establish that the candidate is universally better, that the gate improves safety in every domain, or that the holdout was cryptographically secret. This is a bounded research result, not a safety certification.

## Start here

1. Read [`docs/Artificial_Stupidity_Executive_Summary_Ray_Gomez_2026.pdf`](docs/Artificial_Stupidity_Executive_Summary_Ray_Gomez_2026.pdf).
2. Read [`docs/Artificial_Stupidity_Dossier_Ray_Gomez_2026.pdf`](docs/Artificial_Stupidity_Dossier_Ray_Gomez_2026.pdf).
3. Inspect [`benchmark/evidence/h100_sxm_20260913/repaired_decision/VERIFIED_RESULT.md`](benchmark/evidence/h100_sxm_20260913/repaired_decision/VERIFIED_RESULT.md).
4. Verify the raw evidence with the nested `SHA256SUMS.txt` and the repository-wide `INTEGRITY_SHA256.txt`.
5. Run the local tests.

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
| `gate/` | Independent KEEP / REJECT / ESCALATE decision logic |
| `benchmark/` | Comparison tools, protocol, reports, and preserved evidence |
| `benchmark/evidence/h100_sxm_20260913/original/raw_logs/` | Unedited run logs |
| `benchmark/evidence/h100_sxm_20260913/original/source_snapshot/` | Code and configuration captured with the experiment |
| `benchmark/evidence/h100_sxm_20260913/repaired_decision/` | Transparent post-run import repair and final records |
| `tests/` | 27 GPU-free tests, including a runner import regression test |
| `docs/` | Updated dossier and executive summary |
| `launch/` | Public launch copy, case study, claims, and commercial boundary |

## A transparent failure

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

## License

MIT. See [`LICENSE`](LICENSE) and [`UPSTREAM_LICENSE_NOTICE.md`](UPSTREAM_LICENSE_NOTICE.md).

## Build clock

This project moved from a precursor joke to a defined build in approximately 24 hours, then to a tested and independently CI-verified hardened prototype in approximately 52 hours. The clock remains open until the first complete external submission is sent.

[See the contemporaneous milestone ledger](docs/BUILD_CLOCK.md).
