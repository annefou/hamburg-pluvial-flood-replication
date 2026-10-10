# Published nanopub chain — URI registry

This file is the canonical registry of published nanopub URIs for this replication. Update it as you publish each step.

## Chain

| Step | Template | URI | Published |
|---|---|---|---|
| 01 | Quote-with-comment | https://w3id.org/sciencelive/np/RA2rRZOLe5fhat4AghXzq0ymDP71nR_miJ9iljUnaaaD4 | 2026-10-09 |
| 02 | AIDA Sentence | https://w3id.org/sciencelive/np/RAg-Em1_q5H25bdX0zkQD_AAXnZQjII3j_XnQ7aGKp-dg | 2026-10-09 |
| 03 | FORRT Claim | https://w3id.org/sciencelive/np/RA5O9-MZKGMZtWNCZcu00QtpwW-wOE6MtX8YDXMPvh5GY | 2026-10-09 |
| 04 | FORRT Replication Study | https://w3id.org/sciencelive/np/RAwD-DCUir9JDcqk8lQkRnT91aRGfRZ_p2N7j_uQ9mBw0 | 2026-10-09 |
| 05 | FORRT Replication Outcome | https://w3id.org/sciencelive/np/RA6V_jAy2OFjYBwQMOH92fIM6199bjez7hRkY90vkxx7U | 2026-10-09 |
| 06 | CiTO Citation | https://w3id.org/sciencelive/np/RAI00BYTAPLTsNoY19DGNKF04vAjTuVv6K3WbYmo055CA | 2026-10-09 |

Published 2026-10-09 through the Science Live chain wizard, from `nanopubs/chain-draft.json`.
Reproduction Study; Outcome **Validated** (high confidence), CiTO **confirms**
[Vogelbacher et al. 2026](https://doi.org/10.5194/nhess-26-2765-2026). The Outcome pins the
v0.1.1 release, [10.5281/zenodo.23270558](https://doi.org/10.5281/zenodo.23270558).

## Optional layers

| Step | Template | URI | Published |
|---|---|---|---|
| 07 | Research Software (if applicable) | _not applicable_ (no reusable software produced) | |
| 08 | Research Synthesis (if applicable) | _not applicable_ (single chain) | |

## Format

URIs from Science Live are of the form `https://w3id.org/sciencelive/np/RA…`. URIs from Nanodash (used as a fallback when the Science Live UI hits a bug) are of the form `https://w3id.org/np/RA…`. Both are valid and citable.

If a URI is not in the Science Live namespace, view it via the Science Live viewer by wrapping the URI:

```
https://platform.sciencelive4all.org/np/?uri=<full-URI>
```

## Cross-references

- Drafts: `nanopubs/drafts/`
- Form structure: `docs/forrt-form-fields.md`
- Chain shape decision: `docs/chain-decision-tree.md`

## Verification

`verify_chain` (forrt-research MCP) run on 2026-10-09 against the Science Live dev API:
**green**, 12/12 checks passed — every step reachable, the Outcome's archived version DOI
resolves, the cited DOI resolves, and the Outcome's verdict (Validated) agrees with the
CiTO relation (confirms) on the quoted paper.

## Geographical coverage of the original paper (standalone, not a chain step)

Published from the Logroño replication (annefou/logrono-pluvial-flood-replication), which
documents the same paper; geometry generated there by `scripts/geo_coverage_wkt.py`.

| Location | URI | Published | Status |
|---|---|---|---|
| Hamburg, Germany (mainland, from OSM relation 62782) | https://w3id.org/sciencelive/np/RA1NTaGnBgz1AFkx-Xbpl8FLq16t6wINM-XyP4PrsXnK8 | 2026-10-10 | current |
| Hamburg, Germany (first attempt, bounding box) | https://w3id.org/sciencelive/np/RAXrw7VYNnaHeaIrX4hJsOCJ7Aqy17nbt77LRzP9WOQWc | 2026-10-10 | superseded, retraction pending |
