Project name: EvidenceCircuit

Category: Intelligent Contracts

Batch: A

One-line description: Evidence-bound Boolean circuit execution.

What it does: Consensus converts narrative evidence into a closed truth vector; deterministic code executes a caller-published acyclic gate circuit.

Why GenLayer: GenLayer consensus performs the bounded semantic step, then deterministic contract code executes and stores the mechanism-specific result.

Reusable: Yes. One deployment supports many independently keyed records and callers; the live fixture is only an example.

Repository: Standalone local repository. No GitHub remote is configured and nothing was pushed.

Contract source: contracts/evidence_circuit.py

Source SHA-256: 788bb4165bf2557d3c0890b381dc9ca9d53d33c90a1eb7dff98a20d258cc8518

StudioNet contract: https://explorer-studio.genlayer.com/address/0x07bBb3C3B33FF4567fd65acb8aD2C01aD2b3776A

Deployment transaction: https://explorer-studio.genlayer.com/tx/0x70d389c680943a43e94f6a2f914f26e2e88f56b5c10685cc77c67156e7eda600

Intelligent transaction: https://explorer-studio.genlayer.com/tx/0x411896c21f02e47970cce90536e69433779cf622e75998b7449195c69e3aa7fb

Verification: GenVM lint PASS; strict typecheck PASS; 5 direct tests PASS; five-validator GLSim PASS; finalized StudioNet intelligent write and latest-final readback PASS; exact deployed-source and schema verification PASS.

Originality: Compared with 161 workspace contract sources. Nearest pre-existing structural score is 0.187706; mechanism and source hash are distinct.

Data boundary: Caller-supplied public data only. No external source fetching, funds, identity attestation, legal effect, or private-data guarantee.
