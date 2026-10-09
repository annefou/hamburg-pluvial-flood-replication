# 01 — Quote-with-comment (paper-rooted chains)

> Run the pre-flight checklist in `docs/forrt-form-fields.md` § Pre-flight checklist before drafting.
>
> If this is a question-rooted chain, use `01_pico.md` or `01_pcc.md` instead — see `docs/chain-decision-tree.md`.
>
> **After choosing the chain shape, delete the two step-1 alternates you aren't using.** Once you've decided this chain is paper-rooted and keep `01_quote.md`, run:
> ```bash
> rm nanopubs/drafts/01_pico.md nanopubs/drafts/01_pcc.md
> ```

**Form heading:** *"Annotate a paper quotation — Annotating a paper quotation with personal interpretation"*

## Field-by-field draft

<!-- field: paper -->
### Cited DOI (text input, required)

Format: starts with `10.` — bare DOI, **NOT** `https://doi.org/...` form.

```
10.5194/nhess-26-2765-2026
```

### Quote mode (radio button)

- [x] **Quote whole text (less than 500 characters)**
- [ ] Quote start/end *(use this if the quote exceeds 500 chars)*

<!-- field: quotation -->
### The exact quotation from the paper (max. 500 characters) (textarea, required)

Verbatim from `paper/vogelbacher-2026.pdf`, p. 10 (Sect. 4.2, Risk to mobility and accessibility).
`verify_quote` → found, match `normalized` (whitespace / line-break hyphenation only),
pdf sha256 `88121b0e…a7d5`.

```
The application of the pluvial flood risk toolbox revealed higher risks for buildings in close vicinity to flooded areas and streets, especially, where high exposure and high hazard categories coincide.
```

Character count: 202 / 500.

<!-- field: quotation-end -->
### End of quotation (optional - use when quoting beginning and end of a longer passage, max. 500 characters) (textarea, optional)

Only when quoting the beginning *and* end of a longer passage — set the mode above to
**Quote start/end**, put the opening phrase under the previous heading and the closing
phrase here. Leave empty for a single short quote.

```

```

<!-- field: comment -->
### Our interpretation and explanation of why this quotation is relevant (max. 800 characters) (textarea, required)

Why this quote matters and what the replication tests. Connect the paper's claim to the work this repo does. Don't repeat the quote.

```
Headline result of Vogelbacher et al. (2026) for their building-level pluvial flood risk framework. We test it as a computational reproduction: the authors' own example (synthetic data for a Hamburg city quarter, 37 buildings, Zenodo 10.5281/zenodo.19860733) recomputed with an open, non-ArcGIS implementation (FAIR2Adapt urban_pfr toolbox), and compared building by building with the authors' ArcGIS output and risk classes. Scope is that example only: not real city data, other cities or other rainfall scenarios. I co-wrote parts of that toolbox, so the reproduction is not fully independent.
```

Character count: 595 / 800.

## Publication note

After publishing, paste the resulting URI into `nanopubs/PUBLISHED.md` step 01.
