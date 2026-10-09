# 04 — FORRT Replication Study

> Run the pre-flight checklist in `docs/forrt-form-fields.md` § Pre-flight checklist before drafting.
>
> **Verify code first:** read the actual reproduction script in `notebooks/03_analysis.py` before writing the methodology field. See `docs/verify-before-drafting.md`.

## Field-by-field draft

<!-- field: study -->
### Short URI suffix for study ID (text input, required)

Slug. Use kebab-case.

```
vogelbacher2026-pfr-independent-reproduction
```

<!-- field: label -->
### Label/name of replication study (text input, required)

Human-readable title.

```
Independent open reproduction of building-level pluvial flood risk (Vogelbacher et al. 2026, Hamburg example)
```

<!-- field: type -->
### Choose the study type (dropdown, required)

- [ ] Replication Study - replication with different methodology or conditions
- [ ] Reproduction/Replication Study - study that is both, reproduction and replication
- [x] Reproduction Study - direct reproduction: same methodology, same tools

*Rationale (Anne, 2026-10-09): same data and same method as the paper; the tools
differ (open Python instead of ArcGIS), which is stated as deviation (1).*

<!-- field: claim -->
### Choose FORRT claim (search/select, required)

Left empty here: the chain wizard carries the step-03 URI forward.

URI of the Claim published in step 03. Pull from `nanopubs/PUBLISHED.md`.

```

```

<!-- field: scope -->
### Describe what part of the claim is reproduced/replicated. (textarea, required)

The **scope** of the claim being tested. Which aspect, what's in/out of scope. NOT methodology. NOT results. See `docs/pico-study-outcome-levels.md`.

```
Whether the building-level pluvial flood risk of the paper's framework, and the pattern that risk is highest for buildings close to flooded areas and streets where exposure and hazard coincide, is reproduced from the authors' published inputs. In scope: the authors' worked example as deposited on Zenodo (version 2, the version the paper cites): synthetic building-level data for a Hamburg city quarter (37 buildings), the 100-year design rainfall scenario, flood depths 30-100 cm; every intermediate index (sensitivity, coping capacity, social vulnerability, exposure, both hazard indices), both risk indices and the five risk classes shown in the paper's maps. Out of scope: real city-wide data, other cities, other rainfall scenarios, the sensitivity analysis of Sect. 4.3, and the population disaggregation tool, which the paper states it does not use.
```

<!-- field: methodology -->
### Describe how the claim is reproduced/replicated. (textarea, required)

The **method** in plain prose. Read `notebooks/03_analysis.py` and any config files first. NOT exact numerical results.

```
An independent implementation in Python (geopandas, shapely, scipy), written from the paper's Sect. 3 and the authors' exported scripts on Zenodo (CC BY 4.0), without ArcGIS and without other existing implementations. Inputs are the authors' layers from their ArcGIS layer package. Social vulnerability: TOPSIS for sensitivity (children, elderly singles), coping capacity (welfare recipients, school leavers without diploma) and their combination, each multiplied by the Shannon-entropy index, then the flood-sensitivity transformation (SV + mean/4)^2. Exposure: residents per building and per ground floor as given in the authors' input layer. Hazard to well-being: for each depth 30-100 cm, the flooded fraction of a 2 m ring around each building, passed through a log-normal CDF (sigma 0.25, x4) and summed. Hazard to mobility: the maximum of the flooded fraction of a 5 m ring and of the street area within the 0-15 m and 15-30 m rings at 30 cm, through the same CDF. Risk: social vulnerability x exposure x hazard (Eqs. 14-15). Risk classes: the authors' iterated-mean rule. Every index is compared building by building with the authors' ArcGIS output layer, and the classes with the classes that rule gives on the authors' values. The run is a Snakemake pipeline from download to figures.
```

<!-- field: deviation -->
### Describe any deviations from original methodology. (textarea, optional)

What's different from the original method. Verify against the actual code, don't guess.

```
(1) Tools: open Python instead of ArcGIS Pro, so this is a reproduction with different tools. (2) Where the paper and the authors' results disagree, the implementation follows the results and the authors' scripts: TOPSIS uses vector normalisation (scripts) rather than the sum of Eq. 4; sensitivity weights are children 0.3 and elderly singles 0.7 (Eq. 2 and the results), while the text of Sect. 3.1.1 gives 0.7 and 0.3; the entropy factor is applied in all three TOPSIS steps. (3) Hazard rings exclude every building footprint, not only the building's own, as the authors' stored intermediate fractions require; the paper mentions this only for semi-detached houses. (4) Buffers are drawn in the coordinate system of the authors' buildings (Web Mercator), as in their data; fractions are ratios, so area units cancel. (5) The number of iterations of the class rule (three) is inferred from the paper's four non-zero risk classes. (6) For comparison only, the FAIR2Adapt urban_pfr toolbox (an existing open implementation) is also run as is; I co-wrote parts of it. It is not used to compute the reproduced results.
```

<!-- field: keyword -->
### Search keywords (Wikidata) (search/select, optional)

Provide labels (not QIDs) — the Wikidata search picks up labels.

- _Label 1: ___
- _Label 2: ___

Each checked with `wikidata_lookup` (2026-10-09).

```
flood risk assessment (Q5460077)
social vulnerability (Q581445)
TOPSIS (Q1235853)
reproducibility (Q1425625)
urban flooding (Q15909735)
```

<!-- field: discipline -->
### Search discipline (Wikidata) (search/select, optional)

Provide labels.

- _Discipline label: ___

```
hydrology (Q42250)
```

## Publication note

After publishing, paste the resulting URI into `nanopubs/PUBLISHED.md` step 04.
