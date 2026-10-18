# EvidenceCircuit v2 — release submission

Form fields: SUBMISSION.txt. Description: 968/1,000 characters.
Final contribution submission remains the owner's action.

## Live evidence

- Repository: https://github.com/Leokings/evidencecircuit
- Pinned deployed source: https://github.com/Leokings/evidencecircuit/blob/139bc262a628bdc96851b30f900f7953e8b20a99/contracts/evidence_circuit.py
- Release manifest: https://github.com/Leokings/evidencecircuit/blob/main/deployments/studionet.json
- Studio: https://studio.genlayer.com/?import-contract=0xd60070656AeC65E1809A42627144CF4d3576C790
- Explorer: https://explorer-studio.genlayer.com/address/0xd60070656AeC65E1809A42627144CF4d3576C790

The manifest contains six finalized real-model cases, nine successful primary
transactions and two EXPECTED_FAILURE transactions, final-state snapshots,
source/commit/blob/runtime identity, actual vote maps and a separate runner probe.
Idle/disagree votes are preserved; do not relabel the result as unanimous 5/5.

The key-free verifier was run against the live deployment:
```text
python scripts/verify_studionet.py
```

Public visibility and logged-out links must be verified before using these
fields. Do not edit evidenced source while the Portal contribution is reviewed.
The August v1 audit and manifest are historical, not proof of v2.
