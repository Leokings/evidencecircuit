# EvidenceCircuit v2 release review — 2026-10-18

The two reproduced high-severity source findings are fixed and the changed
source has now been deployed and exercised on StudioNet.

Source commit: 139bc262a628bdc96851b30f900f7953e8b20a99
Source SHA-256: f0831e410fe29740a16dbdcdc6e4fab323180fc729811dbaa8e3e3fc9663e0de
Git blob: a8496cd27dd4b19cb460ad2b4119d47ebe10548c

Studio: https://studio.genlayer.com/?import-contract=0xd60070656AeC65E1809A42627144CF4d3576C790
Explorer: https://explorer-studio.genlayer.com/address/0xd60070656AeC65E1809A42627144CF4d3576C790

## Findings resolved

| Finding | Severity | Resolution |
| --- | --- | --- |
| Leader-controlled stored labels were not bound by the validator | High | Strict complete assessments, canonical comparison of every field and deterministic derivation of stored masks/label lists |
| Missing evidence could become a positive result through NOT | High | Three-valued evaluation; unknown remains unknown and satisfies neither Boolean expectation |
| Old proof concerned different source | Release blocker | Fresh source-matched v2 deployment and six real-model cases; historical proof preserved separately |

Exact quote membership, schema/record bounds, backward-only integer references,
immutable circuit/evidence digests and a deterministic normalization backstop
are covered by regression tests. v2 intentionally changes the response schema;
v1 consumers must migrate UNKNOWN/null handling and deploy a new address.

## Verified locally and in CI

- GenVM lint and SDK semantic validation: PASS.
- Strict Pyright: PASS, zero diagnostics.
- Direct contract/regression tests: 33 PASS.
- Local five-validator GLSim cases: 9 PASS, mocked model outputs.
- Offline release/journal/export tests: 15 PASS.
- Linux CI includes all existing tests; no tests were deleted or weakened.
- Windows and Linux raw-clock fixture compatibility was corrected without
  changing contract source. Old failed CI remains visible as history.

## Fresh live proof

The manifest deployments/studionet.json records all 11 primary transactions:
nine successful executions and two EXPECTED_FAILURE executions. All finalized;
the transaction statuses and execution outcomes are separate.

Six real-model cases verified support, contradiction, missing evidence, NOT on
unknown, NOT on explicit contradiction, and embedded prompt injection. Replay
and invalid references were deliberately rejected. Final records, exact source
bytes and schema were read back. The independent wallet-free verifier passed
all six cases and all 11 receipts.

A separate pinned-runtime deploy/write/read probe passed before the main
deployment. A new disposable repository-specific wallet was generated for this
release; no historical wallet or funded account was used.

An HTTP 502 interrupted a read after a finalized write. The test resumed from its
saved hash/receipt without redeploying or rebroadcasting. Bounded gateway retries
apply only to whitelisted read-only RPC calls, never transaction broadcasts.

## Votes and limits

The manifest preserves actual MAJORITY_AGREE results, including agree, idle and
disagree votes. Do not call the live run unanimous 5/5. Model configuration
names are recorded without plugin/config secrets; these do not certify actual
fallback selection or heterogeneous-model independence.

Validators interpret synthetic public packets, not authenticated external facts.
Prompt injection passed this bounded fixture, not every possible attack.
Exact quote agreement can reduce liveness. No funds, identity or legal effect
are established. StudioNet availability/state persistence is not guaranteed.

## Readiness gates

Technical readiness: PASS for the documented local and live StudioNet scope.
Distinctiveness: PASS against the 22 prior submissions and selected peer;
never submit PredicateGraphInterlock as a distinct companion mechanism.
Evidence readiness: PASS. The repository is public; repository, pinned source,
proof, Studio and Explorer links returned HTTP 200 without authentication.
The anonymously fetched pinned source also matched the deployed SHA-256.

Historical v1 evidence is retained at deployments/historical/studionet-v1.json
and docs/history/AUDIT_2026-08-25.md. The old no-blockers conclusion was superseded;
it is not used to prove any v2 protection. Final Portal submission is the owner’s
action.
