# Deployment evidence and approved-release procedure

Current v2: NOT_DEPLOYED. studionet.json is a readiness record, not a finalized
deployment claim. historical/studionet-v1.json preserves the August source,
address and positive smoke proof; that deployment does not contain these fixes.

No live-network test ran during this remediation. Both current source and
tooling remain local. Do not deploy or publish without the owner's approval.

## Preflight before a later authorized run

1. Confirm current official network settings, SDK/runtime compatibility, runner
   support and polling guidance; probe the pinned runner first. The pinned
   Python client was inspected locally, but this is not a current network probe.
2. Review and push the intended source commit; record commit and blob hashes.
3. Supply fresh repository-specific disposable test accounts in a wallet bundle
   OUTSIDE the repository. Never reuse historical test wallets, print keys, or
   commit wallet material. StudioNet requires no faucet funding.
4. The opt-in test expects RUN_STUDIONET=1 and
   GENLAYER_STUDIONET_WALLET_FILE pointing to that external bundle. Run only
   tests/integration/test_studionet_smoke.py with --network studionet after
   approval. Normal CI leaves the test disabled.
5. Verify finalized execution, final-state readbacks, code byte equality and
   schema methods, not merely an ACCEPTED/FINALIZED status.

The bundle uses schema genlayer-studionet-wallet-bundle/v1, repository
evidencecircuit, and an accounts array. Each external entry contains an address
and matching private_key. EvidenceCircuit needs one fresh account. No bundle
was opened or created during the local fix.

## Checkpointing

tests/studionet_journal.py uses verified hash-returning SDK methods and saves the
transaction hash BEFORE waiting for GenLayer finality. Public checkpoints live
in ignored .studionet-runs/v2.json, not .artifacts (gltest clears that folder).

A finality timeout remains PENDING; rerunning the same bound source/accounts/
arguments polls the existing hash rather than submitting again. A broadcast
whose response was lost stays SUBMISSION_UNCERTAIN and requires manual public
nonce/transaction reconciliation. The SDK itself waits for the transport's
receipt before returning the consensus hash, so that uncertainty window cannot
be claimed atomic. Do not delete a journal just to retry.

An exclusive lock prevents concurrent runs. After a crash, confirm no process
is active and reconcile submitted transactions before removing a stale lock.
The polling wait is bounded at 100 attempts, 6 seconds apart; recheck current
network guidance before enabling it.

The EVC live plan checks definite true/false, missing evidence, NOT on unknown
and explicit contradiction, injection, and replay. It intentionally uses actual
network models without validator mocks; stop on any unexpected classification.

After a successful authorized run, inspect the public-only journal and assemble
a release manifest with source commit/blob/runner, all receipts including
EXPECTED FAILURE labels, votes, addresses and readbacks. Its VERIFIED status
means only the listed test assertions passed, not production safety. Never
overwrite historical evidence or promote NOT_DEPLOYED without fresh proof.
