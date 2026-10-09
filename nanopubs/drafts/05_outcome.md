# 05 — FORRT Replication Outcome

> Run the pre-flight checklist in `docs/forrt-form-fields.md` § Pre-flight checklist before drafting.
>
> **Verify the actual numerical results first** by reading `results/` and `notebooks/03_analysis.py`. Don't quote numbers from memory. See `docs/verify-before-drafting.md`.

## Field-by-field draft

<!-- field: outcome -->
### Short URI suffix for outcome ID (text input, required)

Slug. Use kebab-case.

```
vogelbacher2026-pfr-independent-reproduction-outcome
```

<!-- field: label -->
### Plain-text label for the outcome (text input, required)

Descriptive title.

```
Building-level pluvial flood risk of Vogelbacher et al. (2026) reproduced with an independent open implementation
```

<!-- field: study -->
### Choose study (search/select, required)

Left empty here: the chain wizard carries the step-04 URI forward.

URI of the Replication Study published in step 04. Pull from `nanopubs/PUBLISHED.md`.

```

```

<!-- field: repo -->
### Repository URL (text input, required)

Use the Zenodo **version DOI** URL for the release the results came from — not a
bare branch URL, and not the concept DOI.

> **Why not the bare repo URL.** `https://github.com/ORG/REPO` names a *moving
> branch*. This Outcome asserts "this code produced this number", in a signed,
> immutable record. A branch URL means that assertion points at whatever `main`
> happens to be years from now — code that may never have produced the number
> above. A concept DOI has the same flaw: it resolves to the latest version.
> The version DOI pins the exact release. `docs/chain-decision-tree.md` § Anchor
> ranks the options: SWHID > Zenodo DOI > repo URL > Wayback.
>
> Both DOIs and the SWHID are in `CITATION.cff` under `identifiers:`, recorded
> automatically at release by `.github/workflows/release-identifiers.yml`. Take
> the one described as *"Version DOI"*.

```
https://doi.org/{{ZENODO_VERSION_DOI}}
```

<!-- field: date -->
### Choose completion date (text input, required)

```
2026-10-09
```

<!-- field: validationStatus -->
### Choose validation status (dropdown, required)


This dropdown maps to the CiTO intention in step 06: Validated → `confirms`, PartiallySupported → `qualifies`, Contradicted → `disputes`.

- [ ] contradicted
- [ ] inconclusive
- [ ] not tested
- [ ] partially supported
- [x] validated

<!-- field: confidenceLevel -->
### Choose confidence level (dropdown, required)

_Vocabulary not yet captured._

*Rationale: the paper's results are reproduced to the class level, but three method
details had to be inferred from the authors' results and scripts rather than taken
from the paper's text — hence high rather than very high.*

- [x] high - Strong evidence, mostly agrees with original
- [ ] low - Limited evidence, significant disagreement
- [ ] moderate - Adequate evidence, partial agreement
- [ ] very high - Extensive evidence, high agreement with original
- [ ] very low - Minimal evidence, major disagreement

<!-- field: conclusion -->
### Describe the overall conclusion about the original claim (textarea, required)

Substantive interpretation. Headline comparison: replication's number vs the paper's number, sign + significance.

```
Validated. On the authors' own example, an independent open implementation reproduces the paper's building-level pluvial flood risk and its pattern: every building falls in the same risk class as in the authors' ArcGIS results, for both risk to well-being and risk to mobility and accessibility, and the highest risks are where high exposure and high hazard coincide, as the paper states. Reproducing the numbers required following the authors' results and scripts where they differ from the paper's text (sensitivity weights, TOPSIS normalisation, and rings that exclude neighbouring buildings). An existing open implementation run as is does not reproduce them, mainly because it recomputes exposure and keeps neighbouring footprints in the hazard rings.
```

<!-- field: evidence -->
### Describe the evidence that supports your conclusion (textarea, required)

Numerical results, test statistics, model coefficients. Read directly from `results/`.

```
Compared building by building with the authors' ArcGIS output (Zenodo 10.5281/zenodo.19860733, 37 buildings): sensitivity, coping capacity, social vulnerability and its transformed index match exactly (largest difference 4.4e-16); exposure is taken as published. Hazard to mobility differs by at most 0.0008 and hazard to well-being by at most 0.0016; risk to mobility by at most 0.013 and risk to well-being by at most 0.004. With the authors' iterated-mean class rule, 37 of 37 buildings are in the same class for both indices (well-being: 15 no risk, 13 low, 5 medium, 3 high, 1 very high; mobility: 6, 23, 5, 2, 1), with class breaks equal to three decimals. The authors' stored intermediate fractions for the 2 m ring (37 buildings x 8 depths) are matched within 0.05 percentage points when all building footprints are removed from the ring, against up to 27.8 percentage points (25 cells) when only the building's own footprint is. The authors' risk indices equal social vulnerability x published exposure x hazard to 1e-15. For comparison, the FAIR2Adapt urban_pfr toolbox run as is differs by up to 7.86 (risk to mobility) and 5.11 (risk to well-being).
```

<!-- field: limitations -->
### Describe what limits the conclusions of the study (textarea, optional)

Honest caveats. If the result is partial or contradicted, say so plainly. Don't overclaim.

```
Tested on one worked example only: synthetic building-level data for one Hamburg city quarter (37 buildings) and one rainfall scenario, as published by the authors; this does not test real city data, other cities or the transferability the paper discusses, nor the sensitivity analysis of Sect. 4.3. The remaining differences, in the fourth decimal of the hazard and risk indices, are attributed to ArcGIS geometry processing (snapping tolerance, true curves); finer buffer arcs and intersecting in the flood layers' coordinate system did not remove them. Three method details were inferred from the authors' results and exported scripts because the paper's text differs: the sensitivity weights (results: children 0.3, elderly singles 0.7; text of Sect. 3.1.1: 0.7 and 0.3), the TOPSIS normalisation (scripts: vector norm; Eq. 4: sum), and the exclusion of all building footprints from the hazard rings; the number of class iterations (three) is inferred too. Buffers follow the authors' Web Mercator units, so a 2 m buffer is about 1.2 m on the ground. The authors' exported Python scripts need ArcGIS (arcpy). I co-wrote parts of the FAIR2Adapt toolbox used for comparison, which is reported in its issue #2.
```

## Publication note

After publishing, paste the resulting URI into `nanopubs/PUBLISHED.md` step 05.
