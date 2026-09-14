# Real H100 benchmark

## Outcome

Three original-baseline runs and three candidate runs completed on the same
RunPod NVIDIA H100 PCIe. Halving `TOTAL_BATCH_SIZE` from `2**19` to `2**18`
lowered median validation bits per byte from **1.052944** to **1.030131**, an
absolute improvement of **0.022813** or **2.17%**. Every candidate run beat
every baseline run. Peak memory fell **0.34%**.

| Condition | Runs | Median `val_bpb` | Range | Peak VRAM |
|---|---:|---:|---:|---:|
| Original baseline | 3 | 1.052944 | 1.050835-1.053579 | 45060.2 MB |
| `TOTAL_BATCH_SIZE = 2**18` | 3 | 1.030131 | 1.025939-1.030497 | 44908.2 MB |

The candidate completed 904-957 optimizer steps rather than 464-475 because
gradient accumulation fell from two passes to one. Two candidate runs processed
fewer tokens than every baseline while still producing materially lower
`val_bpb`, so token count alone does not explain the observed gain.

## Two acceptance boundaries

- **Original metric rule: KEEP.** The candidate lowered `val_bpb`.
- **Artificial Stupidity Gate: ESCALATE.** Repeatability, resource use,
  failure-mode review, and human comprehensibility are supported, but protected
  held-out robustness remains unknown.

This divergence is the experiment's principal result. The gate does not deny
the measured improvement; it prevents a repeatedly optimized validation score
from being promoted into a broader claim without independent evidence.

## Failed probe

An earlier one-line probe doubled `DEVICE_BATCH_SIZE` from 128 to 256. It used
79.08 GiB and terminated with CUDA out-of-memory before producing a score. It
is recorded as **REJECT**, not silently discarded.

## Provenance and limitation

The original cloud ZIP was lost after the pod was terminated. This package was
reconstructed from the terminal transcript preserved by the operator in the
ChatGPT conversation. The transcript contains the environment output, data
preparation result, run summaries, failed-probe traceback, and gate output.
Individual raw training log files are not available and are not represented as
available. The result supports a repeatable same-hardware validation gain for
one hyperparameter change; it does not demonstrate independent held-out
robustness, generalization to other hardware, or a machine-learning safety
benefit.
