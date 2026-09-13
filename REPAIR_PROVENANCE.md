# Repair provenance

- Original RunPod archive SHA-256: `beae21136a79afc8d11fafe4c5b92c8ea7f3b311b0c812218d694d429d4a9010`
- Original run identifier: `20260913T212840Z`
- Original failure: `ModuleNotFoundError: No module named 'gate'`
- Failure stage: final decision-module import, after all six training and holdout evaluations completed successfully.
- Repair action: reconstructed the baseline and candidate gate records from the original `partial_results.json`, then executed the captured `source_snapshot/gate/as_gate.py` with the captured `gate_config.json`.
- Additional GPU training during repair: none.
- Original evidence mutation: none; the original archive and its extracted checksum manifest are preserved under `original_evidence/`.

The import failure was traced to the runner process not inserting the project
root into its own `sys.path`. Child training processes already received the
correct `PYTHONPATH`, which is why all six expensive runs completed normally.
