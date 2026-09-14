# Original-versus-gated benchmark

This harness replays the **same ordered experiment records** through two
acceptance boundaries:

1. **Original rule:** keep a completed candidate when `val_bpb` is lower than
   the accepted baseline.
2. **Artificial Stupidity Gate:** require the metric gain plus bounded memory
   and complexity, a falsifiable hypothesis, and complete supporting evidence.

Run the included non-GPU demonstration from the project root:

```bash
python benchmark/compare_loops.py \
  --manifest benchmark/example_experiments.json \
  --output benchmark/example_report.json
```

The report calls an original `KEEP` that the gate rejects or escalates a
**challenged keep**. That phrase is deliberate: it does not label every
challenged experiment a safety failure. A failure claim requires failed
evidence; incomplete evidence requires human review.

## Real GPU protocol

The demonstration manifest is synthetic and tests decision logic only. A real
comparison must replace it with records from the same GPU, software version,
dataset, tokenizer, time budget, and candidate code sequence. The initial
baseline should be repeated to estimate noise. Any candidate gain should be
confirmed before `repeatability` can pass. Held-out robustness must come from a
separate protected evaluation; it cannot be inferred from `val_bpb`. Human
comprehensibility remains a human sign-off rather than being silently automated.

## September 2026 H100 result

Those initial same-hardware records now exist under `benchmark/`:

- three baseline runs;
- one failed device-batch probe;
- three repeated candidate runs using `TOTAL_BATCH_SIZE = 2**18`;
- the structured baseline, candidate, and gate-decision records;
- a recovered terminal transcript and explicit provenance limitation.

The candidate median was **1.030131**, compared with the baseline median of
**1.052944**: a **2.17%** improvement, with every candidate beating every
baseline and peak memory falling **0.34%**. The original rule returns `KEEP`.
The gate returns `ESCALATE` because protected held-out robustness remains
unknown. See `REAL_BENCHMARK_REPORT.md` for the complete bounded claim.

## Protected-holdout result

The predeclared follow-up was completed on an NVIDIA H100 SXM with three
interleaved runs per arm. The candidate improved median validation BPB by
**0.928%** and median protected-holdout BPB by **0.924%**. All nine pairwise
candidate-versus-baseline comparisons were wins on each metric, and all six
runs exited successfully.

The runner failed only at the final gate import. The preserved inputs were
verified and the decision was reconstructed without additional training. The
machine action was **ESCALATE** solely because named human authorization was
required. Raymond Anthony Gomez subsequently reviewed the bounded evidence and
authorized **KEEP** on September 13, 2026. See
`evidence/h100_sxm_20260913/repaired_decision/VERIFIED_RESULT.md`.
