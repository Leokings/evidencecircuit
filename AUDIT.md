# EvidenceCircuit v2 remediation review — 2026-10-18

Scope: local contracts/evidence_circuit.py, its tests, release tooling and
documentation on branch codex/fix-review-blockers. No deployment, push,
repository visibility change or Portal submission was performed.

Current source SHA-256:
f0831e410fe29740a16dbdcdc6e4fab323180fc729811dbaa8e3e3fc9663e0de

Git blob: a8496cd27dd4b19cb460ad2b4119d47ebe10548c
Base commit: c32e791ffe08ba27ad2c55596478f9477320041b
The changes remain uncommitted; a blob identifier is not a pushed release commit.

## Reproduced findings and fixes

| Finding | Severity | Local resolution |
| --- | --- | --- |
| EVC-1: validator checked truth_mask but stored unbound leader true_inputs | High | Strict complete per-label assessment normalization; canonical comparison of every field; derive masks/label lists deterministically; normalize again before storage |
| EVC-2: unsupported input was false, allowing NOT to create a positive result from absence | High | Three-valued inputs and gates; insufficient evidence stays UNKNOWN and output null; neither output_is expectation authorizes unknown |
| Missing current lifecycle/adversarial live proof | Review blocker | Release tests and pending manifest prepared; still requires authorized fresh deployment |
| Private repository / unpushed fixes | Evidence blocker | Unchanged, pending owner approval; do not submit as public evidence |

Additional hardening: exact quote membership and bounds, bounded pre-parse JSON
and serialized records, immutable circuit/evidence digests, explicit v2 schema.
The old direct test treating missing evidence as false was migrated to UNKNOWN;
its missing-evidence safety case was retained and strengthened.

## Local verification

- GenVM AST lint and SDK validation: PASS.
- Strict Pyright: PASS, zero diagnostics.
- Direct contract tests: 33 PASS, including forged extra fields, changed valid
  quotes, unknown vs explicit contradiction, replay/namespaces, malformed
  programs, parsing bounds and exhaustive truth tables for each supported gate.
- GLSim: 9 PASS, five mocked validators per semantic transaction; all gate
  operators, definite true/false, unknown, NOT, replay and invalid programs.
- Offline journal tests: 11 PASS; hash before finality wait, pending resume,
  request/source binding, uncertain broadcast, finalized errors, lock/network
  checks and checkpoint survival of gltest artifact cleanup.

These are local native-Python/mocked-model checks, not hosted GenVM or real
heterogeneous-model consensus evidence. The opt-in live test was not executed.
Strict exact quote agreement may reduce liveness; it is not relaxed silently.

## History and gates

The August v1 audit is preserved at docs/history/AUDIT_2026-08-25.md.
Its original no-blockers conclusion is superseded by the reproduced findings.
The v1 manifest remains at deployments/historical/studionet-v1.json. Its source
hash and positive live smoke do not prove any v2 change.

Technical readiness: PASS for the scoped local remediation; fresh live runtime,
model behavior and compatibility remain unproven, so not production-certified.
Distinctiveness: PASS only against the 22 prior submissions and selected peer;
do not also submit PredicateGraphInterlock. Wider cohort/global novelty unproven.
Evidence readiness: FAIL until an approved pushed/public release and new live
proof exist. deployments/studionet.json intentionally says NOT_DEPLOYED.

Before release follow REVIEW_CHECKLIST.md and deployments/README.md. A real
model injection case, negative/unknown cases, finalized expected failures,
readbacks and exact deployed source must all be recorded truthfully.
