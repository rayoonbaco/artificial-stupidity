# autoresearch + Artificial Stupidity Gate

This run preserves the upstream experiment loop, but the experiment agent does
not have authority to accept its own work.

## Immutable boundaries

- Read `README.md`, `prepare.py`, `train.py`, and `gate/README.md` first.
- Modify only `train.py`.
- Do not modify `prepare.py`, anything under `gate/`, or the evaluation harness.
- Do not install packages.
- A lower `val_bpb` is necessary but not sufficient for acceptance.

## Before each experiment

Write a one-sentence hypothesis and one result that would disconfirm it. Prefer
small, reversible changes. Identify the likely failure mode and the simplest
held-out or repeatability check that could reveal it.

## After each experiment

1. Capture the standard `train.py` summary.
2. Record `complexity_delta_lines` from the committed diff.
3. Populate the four evidence states in a candidate JSON record:
   `repeatability`, `held_out_robustness`, `failure_mode_review`, and
   `human_comprehensibility`. Use only `pass`, `fail`, or `unknown`.
4. Run `gate/as_gate.py` against the currently accepted baseline.
5. `KEEP` advances the branch. `REJECT` restores the prior accepted commit.
   `ESCALATE` pauses acceptance for human review; it is never silently converted
   to `KEEP`.

The research agent may propose evidence, but an independent harness or reviewer
must produce the final evidence record. Unknown evidence stays unknown.

## Decision principle

Optimize intelligence, then challenge its judgment. The gate exists to make
unsupported confidence, hidden brittleness, and metric gaming visible before an
apparently better experiment becomes the next baseline.
