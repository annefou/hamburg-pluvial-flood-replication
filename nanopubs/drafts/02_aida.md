# 02 — AIDA Sentence

> Run the pre-flight checklist in `docs/forrt-form-fields.md` § Pre-flight checklist before drafting.

**Form heading:** *"AIDA Sentence — Make structured scientific claims following the AIDA model"*

## Field-by-field draft

<!-- field: aida -->
### AIDA sentence (text input, required)

Atomic, Independent, Declarative, Absolute. One empirical finding. Must end with a full stop.

> _If your draft AIDA contains "and" linking two distinct findings, split into two AIDA nanopubs._

Atomicity check: one finding — where building-level risk is highest. "exposure and
flood hazard coincide" is the single condition (their co-occurrence), not two findings.
Deliberately carries no city, dataset or number (Anne, 2026-10-09: the AIDA is more
generic than the quote), so a later chain can test the same statement in another city.
The Hamburg example, synthetic data and 37 buildings live in the Study's scope and the
Outcome's limitations.

```
Building-level pluvial flood risk is highest for buildings close to flooded areas and streets where high exposure and high flood hazard coincide.
```

<!-- field: topic -->
### Select related topics/tags (search/select, optional)

Predefined topic vocabulary — list the labels you intend to pick from the dropdown.

Each checked with `wikidata_lookup` (2026-10-09); both are classes, as this field's
`owl:Class` type requires. QID written next to the label so the build script does
not re-search by label.

| Label | QID | type (P31/P279) |
|---|---|---|
| urban flooding | Q15909735 | flood |
| flood risk | Q2288778 | disaster risk |

```
urban flooding (Q15909735)
flood risk (Q2288778)
```

<!-- field: project -->
### Relates to this nanopublication (search/select, required)

URI of the nanopub the AIDA derives from.

- For paper-rooted chains: the Quote-with-comment URI (from step 01).
- For question-rooted chains: the PICO or PCC URI (from step 01).

Pull the URI from `nanopubs/PUBLISHED.md`.

```

```

<!-- field: dataset -->
### Supported by datasets (text input, optional)

DOIs/URLs of datasets that ground the AIDA claim.

The authors' Zenodo deposit (v2, the version the published paper cites; `resolve_doi`
→ "Urban Pluvial Flood Risk Toolbox"): the example data and the ArcGIS output layer the
claim is checked against.

```
https://doi.org/10.5281/zenodo.19860733
```

<!-- field: publication -->
### Supported by other publications (text input, optional)

DOIs/URLs of publications that support the AIDA claim — e.g. peer-reviewed methods papers, or the original paper if not already cited via the Quote.

*(skip — optional)* The paper is already cited through the Quote (step 01). Leaving this
empty also avoids the known datasets + publications bug below.

> **Known platform bug (2026-04-26):** if both *Supported by datasets* AND *Supported by other publications* are populated and publishing fails, fall back to publishing this AIDA via Nanodash. The URI namespace becomes `https://w3id.org/np/...` (still valid and citable).

## Publication note

After publishing, paste the resulting URI into `nanopubs/PUBLISHED.md` step 02.
