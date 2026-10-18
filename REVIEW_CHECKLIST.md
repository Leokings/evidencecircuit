# EvidenceCircuit v2 release checklist — 2026-10-18

- [x] High-severity validator-field and missing-evidence/NOT flaws fixed
- [x] Pinned runtime; GenVM lint and strict typecheck
- [x] 33 direct tests, including forged leaders and three-valued truth tables
- [x] 9 local five-validator mocked scenarios
- [x] 15 offline release/journal/export tests
- [x] Linux raw-clock harness fixed; unchanged deadline tests remain enforced
- [x] Source committed and pushed before deployment
- [x] Fresh disposable test-only wallet outside the workspace
- [x] Live pinned-runtime probe: finalized deploy/write/read and source match
- [x] Six real-model cases finalized on v2
- [x] Replay and invalid-reference EXPECTED_FAILURE receipts
- [x] Exact live source/schema, case and receipt readback
- [x] Wallet-free read-only verifier executed against the live release
- [x] Real vote maps preserved; no fabricated 5/5 or production claim
- [x] Public proof exporter omits provider/plugin secrets
- [x] Historical v1 proof preserved; API/schema migration documented
- [x] Scoped distinctiveness comparison against 22 prior submissions
- [x] Public repository and logged-out evidence link verification
- [ ] Owner submits the contribution

Keep the source frozen during Portal review. Native testnet consensus and this
fixture corpus are not production safety or global originality certifications.
