# Review checklist — current v2, 2026-10-18

- [x] Reproduced high-severity consensus-field and missing-evidence/NOT bugs fixed
- [x] Pinned runner; GenVM lint and strict typecheck pass locally
- [x] 33 direct contract tests, including forged leaders and complete gate truth tables
- [x] 9 local five-validator mocked scenarios; output/replay/invalid-program checks
- [x] 11 offline journal tests, including pending resume and uncertain broadcast
- [x] Bounded strict JSON, exact quotes, three-valued output, immutable digests
- [x] API/schema migration and public-calldata trust boundary documented
- [x] Historical v1 proof separated from current NOT_DEPLOYED manifest
- [x] Scoped comparison against 22 submitted ICs and the selected peer
- [ ] Verify current network/runner/client compatibility with an approved probe
- [ ] Push a reviewed source commit after owner approval
- [ ] Fresh repository-specific wallets and approved live deployment
- [ ] Finalized real-model positive, negative, unknown, NOT and injection cases
- [ ] Finalized expected replay rejection and final-state/source/schema readback
- [ ] Capture commit, blob hash, transactions, votes and outcomes in a new manifest
- [ ] Make repository public only with explicit approval; verify links logged out
- [ ] Replace draft Portal evidence links with the actual v2 release evidence
- [ ] Owner submits the contribution

Local success is not a live GenVM or heterogeneous-model certification.
No visibility change, push, deployment or Portal action was performed here.
