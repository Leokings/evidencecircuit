# EvidenceCircuit v2

A reusable GenLayer predicate interpreter: validators classify bounded public
evidence, then deterministic code executes an immutable acyclic gate program.

Status (2026-10-18): v2 deployed and live-verified on StudioNet. Six real-model
cases and two expected-failure guards finalized; every final case, receipt,
source and schema was independently re-read without a wallet. Lint, strict
typechecking, 33 direct tests, 9 five-validator local scenarios and 15 offline
tooling tests pass. The local models are mocked; the separate live cases are not.
The August deployment is historical v1, not proof of this source.

Studio: https://studio.genlayer.com/?import-contract=0xd60070656AeC65E1809A42627144CF4d3576C790

Explorer: https://explorer-studio.genlayer.com/address/0xd60070656AeC65E1809A42627144CF4d3576C790

Exact source commit: 139bc262a628bdc96851b30f900f7953e8b20a99.
See deployments/studionet.json for the complete sanitized proof, including
actual MAJORITY_AGREE vote maps, idle/disagree voters and expected failures.

| Live case | Final output |
| --- | --- |
| Explicit support | TRUE |
| Explicit contradiction | FALSE |
| Missing evidence | UNKNOWN |
| NOT on missing evidence | UNKNOWN |
| NOT on explicit contradiction | TRUE |
| Embedded prompt-injection attempt | UNKNOWN |

## What it does

Publish up to 12 labels and 24 backward-referencing gates. For every run,
validators independently assess every label as SUPPORTED, CONTRADICTED, or
INSUFFICIENT_EVIDENCE against the same caller-supplied text. Supported and
contradicted labels require a verbatim quote. Every canonical assessment field,
including quotes, must agree exactly before the deterministic result is stored.

The VM implements NOT, AND, OR, XOR, and ATLEAST2 with three-valued logic.
Missing evidence is UNKNOWN, not FALSE: NOT UNKNOWN remains UNKNOWN.

```text
Frozen labels + program -> per-label evidence consensus -> three-valued VM
                                                   -> immutable run + digests
```

## Interface and first use

```python
publish_circuit(circuit_key: str, input_labels_json: str, gate_program_json: str) -> str
evaluate_circuit(circuit_id: str, run_key: str, evidence: str) -> str
get_circuit(circuit_id: str) -> dict
get_run(run_id: str) -> dict
output_is(run_id: str, expected: bool) -> bool
```

1. Publish labels such as ["HAS_APPROVAL"] and program [{"op":"NOT","a":0}].
   Inputs occupy indexes 0..n-1; each gate appends one node. Only existing nodes
   may be referenced; the final gate is the output.
2. The circuit ID is lower-case publisher address + ":" + upper-case key.
   Anyone can evaluate it under their own caller/key namespace.
3. Submit 20–6,000 ASCII characters of public evidence. A missing approval
   produces UNKNOWN; explicit evidence refuting approval can produce TRUE
   through NOT. A quote's presence alone does not prove its semantic meaning.
4. Read get_run. Its schema is evidencecircuit/run/v2; inspect assessments,
   circuit_digest, evidence_digest, node_values, output_status, and output.
   output_status is TRUE/FALSE/UNKNOWN; output is true/false/null.
5. output_is(run_id, true) authorizes only definite TRUE. For UNKNOWN, both
   output_is(..., true) and output_is(..., false) return false. Never treat null
   as a demonstrated negative result.
6. Wait for successful finalized execution before relying on a write. Consensus
   failure rolls back the transaction; no pending run or funds become locked.

For a wallet-free first exercise, run the direct tests below and inspect the
explicit positive, negative, missing-evidence, and forged-leader cases in
tests/direct/test_review_blockers_20261018.py. These are simulations, not a live
app. The deployed v2 address and public inspection links are above.

## Local verification

Use Python 3.12+ and two terminals for the simulator and integration tests:

```text
python -m pip install -r requirements.txt
genvm-lint check contracts/evidence_circuit.py
genvm-lint typecheck contracts/evidence_circuit.py --strict
pytest tests/direct tests/tooling -v
python tests/run_glsim.py --port 4068 --validators 5 --no-browser
gltest tests/integration -v -s --network localnet --rpc-url http://127.0.0.1:4068/api
```

The last two commands run separately. Public-network tests remain skipped by
default. Do not enable RUN_STUDIONET without release approval; see
deployments/README.md for preflight, fresh-wallet requirements and checkpoints.

Inspect the existing deployment with NO wallet, key, environment file or write:

```text
python scripts/verify_studionet.py
```

This checks the current chain, exact deployed source/schema, all six final
records and all 11 primary receipts. It preserves actual votes and explicitly
distinguishes the two expected execution errors from successful writes.

## Compatibility and boundaries

v2 is a breaking response-schema revision. The v1 true_inputs-only model format
is rejected; consumers must handle UNKNOWN/null. Circuit/run IDs and public
method names remain unchanged. Immutable v1 deployments cannot be updated in
place: deploy v2 and configure consumers explicitly.

This MIT-licensed standalone contract is copyable and configurable. It fetches
no websites and moves no funds. Evidence and labels are public calldata;
validators establish interpretation of that packet, not source authenticity,
real-world identity, authority, freshness, or physical truth. Digests bind exact
normalized content and frozen circuit terms, not the truth of a statement.
Exact quote agreement is deliberately strict and may reduce model liveness.

See AUDIT.md, DESIGN.md, SECURITY.md, SOURCE_POLICY.md, ORIGINALITY.md,
REVIEW_CHECKLIST.md and the draft SUBMISSION.txt. The current deployment
manifest records the verified v2 release. StudioNet availability/persistence and
production-grade heterogeneous-model independence are not guaranteed.
