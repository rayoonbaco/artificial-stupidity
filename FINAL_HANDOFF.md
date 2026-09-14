# Artificial Stupidity - final public handoff

## What you have

This is the v0.9.3 second-domain-validation candidate for **ARTIFICIAL STUPIDITY - A MONAHINGA™ Evidence Project**. It includes the working gate, 73 passing tests, frozen before/after adversarial receipts, a frozen Bill X-Ray portability contract and receipt, second-edition source documents, raw H100 evidence, hashes, source snapshots, repair provenance, separate machine and human decision records, and a complete LinkedIn launch package.

## The bounded result

The predeclared H100 SXM experiment completed three interleaved baseline/candidate pairs. Median validation BPB improved 0.928%, median protected-holdout BPB improved 0.924%, every candidate beat every baseline on both metrics, and peak VRAM fell 0.337%.

The machine returned **ESCALATE** because human comprehensibility was intentionally unknown. Raymond Anthony Gomez then reviewed the one-line change and evidence and separately authorized **KEEP** on September 13, 2026.

## Read in this order

1. `docs/Artificial_Stupidity_Executive_Summary_Ray_Gomez_2026.pdf`
2. `README.md`
3. `docs/Artificial_Stupidity_Dossier_Ray_Gomez_2026.pdf`
4. `benchmark/evidence/h100_sxm_20260913/repaired_decision/VERIFIED_RESULT.md`
5. `launch/LINKEDIN_LAUNCH_PACKAGE.md`
6. `launch/CLAIMS_LEDGER.md`
7. `docs/BILL_XRAY_SECOND_DOMAIN_RESULTS_v0.9.3.md`

## Verify

```bash
uv sync
uv run python -m unittest discover -s tests -v
sha256sum -c INTEGRITY_SHA256.txt
```

Windows users can double-click `START_ARTIFICIAL_STUPIDITY.bat` for the guided local demonstration.

## Publish the v0.9.3 second-domain-validation update

1. Preserve the existing `v0.9.0-evidence-prototype` release unchanged.
2. Preserve the existing `v0.9.2-adversarial-hardening` prerelease unchanged.
3. Replace the working repository files with this complete package.
4. Commit as `Add Bill X-Ray second-domain validation` and push to `main`.
5. Confirm the CPU verification workflow passes on Python 3.10 and 3.12.
6. Confirm the public site shows the Bill X-Ray KEEP / REJECT / ESCALATE section.
7. Publish a separate `v0.9.3-second-domain-validation` prerelease.

The repository is public research software, not a safety certification. Paid services may be offered around private deployment, integrations, custom evidence rules, audit-ready reporting, and support.
