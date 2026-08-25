# EvidenceCircuit

Evidence-bound Boolean circuit execution.

Batch: A

## Why it is GenLayer-native

Consensus converts narrative evidence into a closed truth vector; deterministic code executes a caller-published acyclic gate circuit.

The LLM handles only the bounded semantic step. Deterministic contract code owns
the reusable algorithm, state transitions, access control, tie-breaking, and
views. One deployment supports many caller-keyed records; it is not tied to the
StudioNet fixture or one organization.

## Public interface

Write methods: `publish_circuit`, `evaluate_circuit`

View methods: `get_circuit`, `get_run`, `output_is`

## Verification

```text
pip install -r requirements.txt
genvm-lint check contracts/evidence_circuit.py
genvm-lint typecheck contracts/evidence_circuit.py --strict
pytest tests/direct -q
python tests/run_glsim.py --port 4000 --validators 5
gltest tests/integration -q --network localnet
```

The live smoke test is opt-in and requires a repository-specific wallet bundle
outside the repository. It waits for finalized receipts, reads `LATEST_FINAL`,
retrieves deployed source and schema from StudioNet, and fails unless the source
bytes exactly match this repository.

StudioNet contract: https://explorer-studio.genlayer.com/address/0x07bBb3C3B33FF4567fd65acb8aD2C01aD2b3776A

See `AUDIT.md`, `ORIGINALITY.md`, `SOURCE_POLICY.md`, `SECURITY.md`,
`SUBMISSION.md`, and `deployments/studionet.json` for the final evidence.

## Boundary

The contract moves no funds and does not establish identity, ownership,
professional authority, source authenticity, physical truth, or legal effect.
All caller inputs and calldata are public. Off-chain clients own authentication,
privacy, source curation, indexing, and the decision to rely on a result.
