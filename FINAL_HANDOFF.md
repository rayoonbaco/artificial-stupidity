# Artificial Stupidity - final public handoff

## What you have

This is the complete public-ready research repository for **ARTIFICIAL STUPIDITY - A MONAHINGA™ Evidence Project**. It includes the working gate, 27 tests, updated second-edition publications, raw H100 evidence, hashes, source snapshots, repair provenance, separate machine and human decision records, and a complete LinkedIn launch package.

## The bounded result

The preregistered H100 SXM experiment completed three interleaved baseline/candidate pairs. Median validation BPB improved 0.928%, median protected-holdout BPB improved 0.924%, every candidate beat every baseline on both metrics, and peak VRAM fell 0.337%.

The machine returned **ESCALATE** because human comprehensibility was intentionally unknown. Raymond Anthony Gomez then reviewed the one-line change and evidence and separately authorized **KEEP** on September 13, 2026.

## Read in this order

1. `docs/Artificial_Stupidity_Executive_Summary_Ray_Gomez_2026.pdf`
2. `README.md`
3. `docs/Artificial_Stupidity_Dossier_Ray_Gomez_2026.pdf`
4. `benchmark/evidence/h100_sxm_20260913/repaired_decision/VERIFIED_RESULT.md`
5. `launch/LINKEDIN_LAUNCH_PACKAGE.md`
6. `launch/CLAIMS_LEDGER.md`

## Verify

```bash
uv sync
uv run python -m unittest discover -s tests -v
sha256sum -c INTEGRITY_SHA256.txt
```

Windows users can double-click `START_ARTIFICIAL_STUPIDITY.bat` for the guided local demonstration.

## Publish to GitHub

1. Create an empty repository without GitHub-generated files.
2. Upload the contents of this folder, not the enclosing folder.
3. Replace `[insert-account]`, `[insert-repository]`, and contact placeholders.
4. Run the verification commands and keep the output.
5. Add the final GitHub URL to the LinkedIn post.

The repository is public research software, not a safety certification. Paid services may be offered around private deployment, integrations, custom evidence rules, audit-ready reporting, and support.
