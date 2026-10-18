# EvidenceCircuit v2 — deployment evidence

Current release: VERIFIED, 2026-10-18.

Studio: https://studio.genlayer.com/?import-contract=0xd60070656AeC65E1809A42627144CF4d3576C790
Explorer: https://explorer-studio.genlayer.com/address/0xd60070656AeC65E1809A42627144CF4d3576C790

studionet.json binds the pinned source commit/blob/SHA-256 to a fresh deployment,
six real-model final cases, nine successful primary transactions and two
EXPECTED_FAILURE transactions. It contains final state snapshots, real vote
maps and sanitized model metadata. It does not include private keys or provider
plugin/config secrets.

The separate runner probe verifies a successful finalized deploy, write, public
read, exact source and schema. historical/studionet-v1.json is unchanged August
proof of v1 only; do not substitute it for this release.

## Verify without a wallet

```text
python -m pip install -r requirements.txt
python scripts/verify_studionet.py
```

The verifier sends only read-only RPC requests. It checks chain identity, exact
source/schema, all six final records and every primary receipt/vote map.
It requires no key, external wallet bundle, faucet, signing or environment file.

## Reproduce only after explicit authorization

Confirm current official network/runner/client settings, then use fresh
repository-specific disposable accounts outside the workspace. The included
scripts/create_test_wallets.py prints only addresses and refuses to save under
the GenLayer workspace. Protect the external parent directory with an owner-only
NTFS ACL (or equivalent) BEFORE generating a bundle. Do not reuse old wallets.

The external bundle schema is genlayer-studionet-wallet-bundle/v1, repository
evidencecircuit, accounts array with address and matching private_key.
The live tests require RUN_STUDIONET=1 and GENLAYER_STUDIONET_WALLET_FILE pointing
to that external bundle. Use --network studionet, not a different network preset.

First run tests/integration/test_studionet_probe.py; only after it passes run
tests/integration/test_studionet_smoke.py. No model mocks are used in these live
tests. Stop on unexpected model outcomes; do not weaken consensus just to pass.

## Journal and recovery boundaries

Ignored .studionet-runs/probe.json and v2.json persist hashes before finality
waits, survive gltest's .artifacts cleanup and bind source/accounts/arguments.
Finalized success and finalized error are separate. A pending wait resumes the
same hash, never an automatic new transaction.

Only whitelisted read RPC calls may retry transient 429/502/503/504 responses;
broadcasts are never retried by that transport wrapper. All RPC waits are
bounded. The SDK waits for a transport receipt before returning a consensus
hash, so broadcast+checkpoint is explicitly not atomic. Unknown broadcasts
require manual public transaction/nonce reconciliation.

Original readbacks remain unchanged on resumed runs; later snapshots are labeled
separately. Inspect an interrupted process before removing any stale lock.
Use scripts/export_studionet.py with the actual pushed source commit only after
all required cases pass. It emits a sanitized public manifest, not raw RPC
provider credentials.

The tested stable StudioNet RPC reported zero gas price and the fresh unfunded
wallet completed the release; recheck network fees for future runs rather than
assuming that every network/version is free.

Actual MAJORITY_AGREE vote maps include idle/disagree voters; this is not a 5/5
unanimity claim. Configured model names do not prove fallback selection or model
independence. StudioNet is not a durable production deployment guarantee.
