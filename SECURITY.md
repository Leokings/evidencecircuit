# Security — EvidenceCircuit v2

The 2026-10-18 review fixed two reproduced high-severity issues: leader-controlled
stored labels not bound by the validator, and missing support turning into a
positive result through NOT. See AUDIT.md and the regression tests.

Controls include strict complete assessment schemas, per-label quote membership,
canonical equality of all semantic fields, deterministic backstop validation,
three-valued gates, caller-scoped append-only IDs, frozen term/evidence digests,
bounded records and backward-only integer references. The pinned runner is
unchanged; its compatibility with a fresh deployment remains to be probed.

Trust boundary: validators interpret the public packet supplied in calldata.
They do not independently fetch or authenticate external facts. A matching hash
proves content binding, not authorship, freshness, authority or truth. A verbatim
quote can still be misleading; semantic re-evaluation, not substring membership
alone, is the relevant model check.

Prompts treat labels/evidence as untrusted. Local adversarial mocks establish
parsing and validator rejection, not resistance of actual heterogeneous models
to prompt injection. Positive/negative/uncertainty/injection tests must be rerun
on the approved live deployment. Exact quote equality may cause disagreement;
there is no weaker fallback that silently accepts an unvalidated result.

This contract has no funds or partially committed pending case. An invalid or
unagreed model result aborts execution. Integrators must require finalized
successful receipts, read final state, and accept only a definite authorized
output under the expected circuit digest and caller.

All calldata, evidence and storage are public. Do not send secrets, personal
data or private documents. Live test keys must be fresh, repository-specific,
outside the repository, and never printed or committed.
