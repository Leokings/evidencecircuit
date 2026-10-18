# Evidence source policy

EvidenceCircuit v2 interprets only a bounded caller-supplied public text packet.
It does not fetch URLs or establish provenance. Each validator receives the same
transaction-bound text; quote membership is checked against its exact normalized
copy. No independently fetched website or real-world authenticity is implied.

The client is responsible for source selection, immutable capture, permissions,
licensing, freshness and attribution. Show that provenance beside the run.
Do not submit private information or allow instructions in evidence to replace
the frozen label vocabulary and evaluation policy.

Evidence is normalized to LF, trimmed and restricted to 20–6,000 ASCII
characters. Labels and gate program are immutable. SHA-256 identifies the
normalized evidence and circuit terms; it cannot prove those contents true.

Adding external fetching, callbacks, custody, or a different evidence policy is
a new trust boundary requiring review, tests and a fresh deployment.
