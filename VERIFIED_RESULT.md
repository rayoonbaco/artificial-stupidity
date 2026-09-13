# Verified protected-holdout result

## Outcome

The candidate passed every preregistered empirical boundary.

| Metric (lower is better) | Baseline runs | Candidate runs | Baseline median | Candidate median | Relative improvement |
|---|---|---|---:|---:|---:|
| Validation BPB | 0.999791, 1.000213, 1.001808 | 0.990674, 0.990934, 0.991104 | 1.000213 | 0.990934 | 0.928% |
| Protected-holdout BPB | 0.998995, 0.999357, 1.001117 | 0.989901, 0.990126, 0.990284 | 0.999357 | 0.990126 | 0.924% |

- All three candidate validation scores beat all three baseline validation scores: **9/9 pairwise wins**.
- All three candidate protected-holdout scores beat all three baseline holdout scores: **9/9 pairwise wins**.
- Even the worst candidate beat the best baseline by 0.869% on validation and 0.872% on holdout.
- Peak VRAM fell from 45,060.2 MB to 44,908.2 MB: **0.337% lower**.
- All six runs exited successfully.
- Baseline and candidate scripts have exactly one functional difference: `TOTAL_BATCH_SIZE` changed from `2**19` to `2**18`.

## Formal machine decision

**ESCALATE** — not because the empirical test failed, but because
`human_comprehensibility` is intentionally `unknown`. The gate is designed so
that a machine cannot authorize its own result. A named human must review the
one-line change, this report, and the preserved evidence before choosing KEEP
or REJECT.

## Human authorization

On September 13, 2026, named reviewer **Raymond Anthony Gomez** reviewed the
bounded result and the one-line batch-size change and authorized **KEEP**. The
final governed decision is therefore **KEEP**. The machine's original
**ESCALATE** remains preserved as a separate record.

## What the experiment establishes

On this H100 SXM setup, across three interleaved five-minute runs per arm,
halving the total batch size produced a repeatable improvement on both the
ordinary validation shard and the separately stored protected-holdout shard.
The result survived the exact disconfirming condition declared before the run:
there were no failed runs, no overlapping score distributions, and no candidate
holdout score worse than any baseline holdout score.

## Limits

This is strong evidence for this bounded configuration, dataset, hardware, and
time budget. Three runs per arm are not enough to claim universal superiority
across all models or environments. The holdout was sequestered from training
and tokenizer preparation by the harness, but it was not cryptographically
secret from the project author.
