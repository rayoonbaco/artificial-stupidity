# Artificial Stupidity Gate

The upstream loop asks one decisive question: **did `val_bpb` go down?** This gate
asks a separate question: **is the apparent improvement supported well enough to
survive?** It does not make the model less capable. It introduces disciplined
doubt at the experiment-selection boundary.

The gate is intentionally outside `train.py`, and the experiment agent is not
authorized to edit it. A candidate receives one of three decisions:

- `KEEP`: metric improvement plus complete supporting evidence and a falsifiable
  pre-run hypothesis.
- `REJECT`: no real improvement, a failed run, excess resource growth, or a
  failed critical check.
- `ESCALATE`: incomplete critical evidence, weak coverage, or complexity that
  requires human judgment.

Run a local, GPU-free example:

```bash
python gate/as_gate.py \
  --baseline gate/examples/baseline.json \
  --candidate gate/examples/candidate_keep.json \
  --evidence gate/examples/evidence_keep.json
```

Exit codes are `0` for `KEEP`, `2` for `REJECT`, and `3` for `ESCALATE`.

After a real upstream run, build the candidate record from the unedited run log,
the protected evidence record, and the `train.py` diff:

```bash
python gate/build_candidate.py \
  --run-log run.log \
  --evidence gate/examples/evidence_template.json \
  --baseline baseline.json \
  --base-ref <accepted-commit> \
  --output candidate.json \
  --evidence-output evidence-bundle.json

python gate/as_gate.py \
  --baseline baseline.json \
  --candidate candidate.json \
  --evidence evidence-bundle.json \
  --output decision.json
```

`build_candidate.py` deliberately keeps candidate facts separate from the
evidence bundle and preserves `unknown` evidence. The gate rejects candidate
records containing reserved check or authorization fields, verifies that the
evidence is bound to baseline, candidate, and policy hashes, enforces configured
producer allowlists and core policy floors, rejects ambiguous JSON, and requires
a bound human-review payload before `human_comprehensibility` can pass.

This is a research prototype, not a safety certification system. Hash binding
detects substitution but producer IDs are allowlisted labels, not cryptographic
identities. An attacker who controls every file can still forge the records. A
serious deployment must isolate or authenticate the policy, evidence producer,
and human reviewer through permissions, signatures, or a separate service.
