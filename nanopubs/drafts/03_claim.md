# 03 — FORRT Claim

> Run the pre-flight checklist in `docs/forrt-form-fields.md` § Pre-flight checklist before drafting.

**Form heading:** *"FORRT Claim — Declare an original claim according to FORRT, linking it to an AIDA sentence with a specific FORRT type."*

## Field-by-field draft

<!-- field: claim -->
### Short URI suffix as claim ID (text input, required)

Slug becomes part of the nanopub URI. Use kebab-case.

```
pluvial-flood-risk-exposure-hazard-coincidence
```

<!-- field: label -->
### Label of the claim, to find it later (text input, required)

A descriptive title (not a sentence). Used for searches/discovery.

```
Building-level pluvial flood risk highest where exposure and flood hazard coincide
```

<!-- field: aida -->
### Search for an AIDA sentence (search/select, required)

URI of the AIDA published in step 02. Pull from `nanopubs/PUBLISHED.md`.
Left empty here: the chain wizard carries the step-02 URI forward.

> _If the AIDA was published via Nanodash (`w3id.org/np/...` namespace), the platform's search may not find it — paste the URI manually._

```

```

<!-- field: forrtType -->
### Type of FORRT claim (dropdown, required)

Pick one. See `docs/claim-type-vocabulary.md` for the seven options and how to choose.


*Rationale: the claim is a pattern in where risk falls (buildings close to flooded areas
and streets, where exposure and hazard coincide); the risk index is the instrument, not
the claim — the "descriptive pattern vs. model performance" rule in
`docs/claim-type-vocabulary.md`. There is no statistical test in the paper.*

- [ ] computational performance (Computational & Performance)
- [ ] data governance (access control, licensing, FAIR compliance)
- [ ] data quality (preprocessing, validation, normalization)
- [x] descriptive pattern (distribution, trend, proportion)
- [ ] model performance (accuracy, F1 score, evaluation metrics)
- [ ] scalability (Computational & Performance)
- [ ] statistical significance (significant difference, relationship, or effect)

<!-- field: source -->
### Source URI (text input, optional)

Full URL form: `https://doi.org/...` (NOT bare DOI).

```
https://doi.org/10.5194/nhess-26-2765-2026
```

## Publication note

After publishing, paste the resulting URI into `nanopubs/PUBLISHED.md` step 03.
