# Adversarial Results v0.9.2

## Plain-English result

The first hardened gate still trusted several labels because it assumed the surrounding files and processes were honest. We deliberately removed that assumption at the input boundary. The v0.9.1 probe found eight routes to an unjustified KEEP in nine targeted probes, plus one ambiguous-JSON weakness. Those failures were frozen before repair.

After repair, all 12 adversarial cases were blocked or rendered harmless, and all four declared KEEP / REJECT / ESCALATE controls produced the expected action. The complete 55-test suite passed with the web dependencies installed.

## Before and after

| Boundary | v0.9.1 observation | v0.9.2 behavior |
|---|---|---|
| Accepted baseline | Could be substituted without invalidating evidence | Bound by canonical SHA-256 |
| Harness identity | Any nonempty ID was accepted | Role-and-ID allowlist enforced |
| Human review | A correctly shaped digest could stand without its payload | Full review payload required and decision-bound |
| Policy floor | Core checks could be removed by a weakened policy | Core required and critical checks enforced in code |
| JSON parsing | Duplicate keys silently used the last value | Duplicate keys refused |
| Evidence schema | Extra undeclared checks and producers were tolerated | Undeclared fields refused |
| Run completion | Missing status defaulted to success | Explicit status required |
| Numeric policy | Numeric strings could be coerced | Exact finite numeric types required |

## Counts

- Frozen v0.9.1 probes: 9
- v0.9.1 unjustified KEEP outcomes under the targeted input-control model: 8
- v0.9.1 duplicate-key ambiguities: 1
- v0.9.2 adversarial cases: 12/12 passed
- v0.9.2 action controls: 4/4 correct
- False vetoes on the declared valid KEEP control: 0
- Full automated suite: 55/55 passed

These are deterministic tests selected to challenge known boundaries. The fractions are not statistical estimates of failure prevalence, safety improvement, or risk reduction.

## What remains unresolved

The software now verifies internal consistency and approved producer labels. It does not prove that the named producer is genuinely independent. If one actor controls the runtime, policy, evidence, and review files, that actor can forge a consistent package. Strong deployment therefore requires separated permissions, signed attestations, or an external gate service. Independent reproduction and qualified technical review remain required before broader claims.

The final consistency pass also found that the v0.9.1 hardened replay helper paired the protected-holdout candidate with the earlier PCIe-stage baseline. The historical evidence and decisions were already correct; only the later convenience replay fixture was mismatched. v0.9.2 binds that replay to the preserved protected-holdout baseline and records the correction.

## Receipts

- Frozen plan: `docs/ADVERSARIAL_TEST_PLAN_v0.9.2.md`
- Preserved v0.9.1 implementation: `benchmark/adversarial/v091_as_gate_snapshot.py`
- Preserved v0.9.1 failures: `benchmark/adversarial/v091_failure_receipt.json`
- v0.9.2 machine-readable result: `benchmark/adversarial/v092_campaign_receipt.json`
- v0.9.2 complete test log: `TEST_RESULTS_v092.txt`
