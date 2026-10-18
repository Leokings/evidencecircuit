# EvidenceCircuit v2 design

## Mechanism

A publisher freezes a bounded input vocabulary and acyclic predicate program.
A caller submits public text under a caller-scoped run key. GenLayer's
nondeterministic step classifies only the fixed labels; deterministic code
validates every field and computes all masks, nodes and the output.

This is an interpreter, not a fixed weighted acceptance rubric or graph-repair
proposal. No model writes gate references, masks, balances or consequences.

## Consensus data contract

The only accepted model object is:

```json
{"assessments":[{"label":"EXACT FROZEN LABEL","status":"SUPPORTED","quote":"exact source excerpt"}]}
```

There must be one assessment per label in frozen order, with exactly those
three keys. Status is SUPPORTED, CONTRADICTED, or INSUFFICIENT_EVIDENCE.
Supported/contradicted rows require a nonempty, non-whitespace, exact evidence
substring of at most 240 characters. Insufficient evidence may use an empty
quote. Invented labels, duplicates, omitted rows and extra fields fail closed.

The leader and each validator independently normalize a model response against
the same local evidence snapshot. Canonical JSON comparison binds every status,
label and quote, not just a headline mask. Deterministic execution normalizes the
returned value again before storing it. Invalid/model-disagreeing execution
creates no successful run; the caller can retry under a key only if no run was
committed. There is no contract-level pending queue or escrow.

## Three-valued VM

SUPPORTED maps to TRUE, CONTRADICTED to FALSE, insufficient to UNKNOWN.
NOT preserves unknown; AND is false if either operand is false; OR is true if
either is true; otherwise uncertainty propagates. XOR is unknown if either
operand is unknown. ATLEAST2 is true once two operands are true, false if fewer
than two can possibly be true, otherwise unknown. No assumption is made that
missing evidence explicitly refutes a label.

The final node is the result. output_is returns true only for an exact Boolean
match to a known output; an unknown result never satisfies either expectation.

## Bounds and storage

12 labels, 24 gates, 48-character keys, 80-character labels, 6,000-character
evidence, 240-character quotes. Inputs and programs are capped before parsing
(2,048 and 8,192 characters); serialized records are capped at 32,768 characters.
References must be true integers, not Boolean/float values, and point backward.
All caller text is normalized ASCII. Per-run work and record size are bounded;
persistent maps can grow through separate transactions but are never globally
scanned. Counters do not authorize anything.

Circuit digests bind the contract address, immutable terms, publisher and
creation time. Every run stores that digest and SHA-256 of normalized evidence.
Records are append-only and IDs isolate publishers/callers. Public hashes do not
authenticate who authored the evidence.

## Migration

Schema v2 requires complete three-state assessments and introduces null output.
There is no in-place upgrade. Deploy new source, verify its exact bytes, then
update consumer addresses and parsing explicitly. The v1 manifest and audit are
retained as historical records, not current safety evidence.
