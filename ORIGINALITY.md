# Originality audit

The final source was compared against 161 GenLayer
contract sources in the workspace. All twenty new target contracts were excluded
from the pre-existing comparison pool.

Nearest pre-existing source: `baggate\contracts\bag_lane_registry.py`

Combined structural score: `0.187706`

Token score: `0.311026`

AST score: `0.09198`

Nearest contract in this new set: `coveragemosaic\contracts\coverage_mosaic.py` with combined
score `0.246715`. That score reflects shared safe GenLayer
boilerplate. The mechanisms differ materially:

- This repository: Consensus converts narrative evidence into a closed truth vector; deterministic code executes a caller-published acyclic gate circuit.
- Other repository: Consensus verifies which claimed cells are supported by one observation; deterministic bitmap union and gap calculation control sealing.

The two do not share the same semantic input, deterministic algorithm, storage
record, state lifecycle, or decision views. Exact source SHA-256 values are also
unique across all twenty repositories. The complete machine-readable reports are
`review-tools/twenty-originality-audit.json` and
`review-tools/twenty-pairwise-audit.json` at the workspace level.

Similarity scoring is a review aid, not a guarantee of a human review outcome.
