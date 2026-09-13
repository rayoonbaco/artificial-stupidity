# Preregistered H100 validation + protected-holdout protocol

Protocol version: 1.0, fixed before the rerun.

## Question

Does the one-line candidate `TOTAL_BATCH_SIZE = 2**18` outperform the
instrumented upstream baseline `TOTAL_BATCH_SIZE = 2**19` both on the pinned
validation shard and on a separately sequestered holdout shard under the same
five-minute H100 training budget?

## Fixed design

- Hardware: exactly one NVIDIA H100.
- Software: this archive's lockfile and source snapshot.
- Training data: upstream default shards 00000–00009.
- Validation data: upstream pinned shard 06542.
- Protected holdout: preregistered shard 06541.
- Holdout location: `~/.cache/autoresearch/protected_holdout`, outside the
  upstream `DATA_DIR`; it is unavailable to tokenizer training, model training,
  and validation loading.
- Evaluation budget: 20,971,520 tokens for validation and separately for
  holdout, using the same BPB formula.
- Runs: three baseline and three candidate, interleaved B1/C1/B2/C2/B3/C3.
- Functional candidate diff: one line, total batch size `2**19` to `2**18`.

## Predeclared boundaries

- Repeatability passes only if **every** candidate validation BPB is lower
  (better) than **every** baseline validation BPB.
- Protected-holdout robustness passes only if **every** candidate holdout BPB
  is lower than **every** baseline holdout BPB.
- A completed holdout comparison that misses that boundary is a critical
  failure and produces `REJECT`.
- Missing or incomplete evidence remains `unknown` and produces `ESCALATE`
  unless a completed run has failed, in which case the failure review rejects.
- Peak VRAM growth may not exceed 15%.
- The automated runner never marks human comprehensibility `pass`. A named
  human must review the source diff and authorize any final `KEEP`.
- Use `benchmark/HUMAN_REVIEW_TEMPLATE.json` to record that separate decision;
  the training process must never populate or approve it.

## One-command run

From the extracted project directory on the H100 pod:

```bash
bash RUN_H100_EVIDENCE.sh
```

The runner streams progress, preserves full merged stdout/stderr for every
command, records environment and file hashes, writes structured results, and
creates both a timestamped archive and the unmistakable alias:

`/workspace/ARTIFICIAL_STUPIDITY_H100_EVIDENCE_DOWNLOAD_ME.zip`

Download that ZIP before stopping the pod.

## Evidence limitation

“Protected” means sequestered by the harness from the upstream data and
tokenizer paths and identified by a recorded SHA-256 hash. It does not mean the
dataset is cryptographically secret, adversary-proof, or a proxy for general AI
safety. This is a bounded empirical test of one training change on one setup.
