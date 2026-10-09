# 06 — CiTO Citation

> Run the pre-flight checklist in `docs/forrt-form-fields.md` § Pre-flight checklist before drafting.

**Description:** *"Declare citations between papers or other works, using Citation Typing Ontology"*

## Field-by-field draft

<!-- field: work -->
### Identifier for the citing creative work (text input, required)

URI of the Outcome published in step 05. Pull from `nanopubs/PUBLISHED.md`.
Left empty here: the chain wizard carries the step-05 URI forward.

```

```

### List citations (repeatable group, required ≥1)

#### Citation 1 — back to the original paper

##### Citation Type (dropdown)

Choose based on the Outcome's validation status:

- Validated → `confirms`
- PartiallySupported → `qualifies`
- Contradicted → `disputes`

For question-rooted chains where there is no original paper to confirm/dispute, use `usesMethodIn` or `citesAsAuthority` for the methodology paper(s).

Write the chosen type in the block below (a vocabulary label such as `cites as authority`, or `citesAsAuthority`). `build-chain-draft` uses it as written; leave the block empty to have the type derived from the Outcome's validation status, which is right for paper-rooted chains only.

> **Note:** `replicates` is NOT in the Science Live dropdown (despite existing in upstream CiTO). When citing a notebook/tutorial that was directly reused, use **`credits`** instead.

Outcome = Validated → `confirms`.

```
confirms
```

##### DOI or other URL of the cited work (text input)

```
https://doi.org/10.5194/nhess-26-2765-2026
```

#### Additional citations (optional)

If the Outcome cites methods papers, related replications, or upstream tools, add them here.

One line per further citation, in this exact form (each becomes a pre-filled row):

- Type: citesAsDataSource → URL: https://doi.org/10.5281/zenodo.19860733
- Type: citesAsDataSource → URL: https://doi.org/10.5281/zenodo.17986182
- Type: citesAsRelated → URL: https://github.com/FAIR2Adapt/urban_pfr_toolbox_hamburg/tree/eb651ebf3b38f444d0180af0a95807bc00326015

  (Zenodo v2: the authors' example data, ArcGIS output layer and scripts — the reference.
  Zenodo v1: the authors' earlier deposit, whose stored intermediate fractions are the
  evidence for the ring rule. Both resolve, `resolve_doi` 2026-10-09.)

  (The FAIR2Adapt toolbox is cited at the exact commit that was run, because it has no
  release or DOI yet; it is a comparison, not part of the reproduction.)

## Publication note

After publishing, paste the resulting URI into `nanopubs/PUBLISHED.md` step 06.

This completes the six-step FORRT chain. Optional next layers:

- **Research Software** (`drafts/07_research_software.md`) — if the repo *produces* a reusable software artefact.
- **Research Synthesis** (`drafts/08_synthesis.md`) — if this chain is one of several testing facets of a shared property.
