# Independent reproduction of building-level urban pluvial flood risk (Vogelbacher et al. 2026)

[![CI](https://github.com/annefou/hamburg-pluvial-flood-replication/actions/workflows/ci.yml/badge.svg)](https://github.com/annefou/hamburg-pluvial-flood-replication/actions/workflows/ci.yml)
[![Jupyter Book](https://github.com/annefou/hamburg-pluvial-flood-replication/actions/workflows/jupyter-book.yml/badge.svg)](https://annefou.github.io/hamburg-pluvial-flood-replication/)
[![Docker](https://github.com/annefou/hamburg-pluvial-flood-replication/actions/workflows/docker.yml/badge.svg)](https://github.com/annefou/hamburg-pluvial-flood-replication/pkgs/container/hamburg-pluvial-flood-replication)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![DOI](https://zenodo.org/badge/DOI/{{ZENODO_DOI}}.svg)]({{ZENODO_DOI}})
[![FAIR4RS](https://img.shields.io/badge/FAIR4RS-conformant-brightgreen)](docs/fair4rs-checklist.md)
[![FORRT](https://img.shields.io/badge/FORRT-replication-blue)](https://forrt.org/)
[![Science Live](https://img.shields.io/badge/Science%20Live-nanopub%20chain-purple)](nanopubs/PUBLISHED.md)
[![RO-Crate](https://img.shields.io/badge/RO--Crate-1.2-orange)](ro-crate-metadata.json)
[![Software Heritage](https://archive.softwareheritage.org/badge/origin/https://github.com/annefou/hamburg-pluvial-flood-replication/)](https://archive.softwareheritage.org/browse/origin/?origin_url=https://github.com/annefou/hamburg-pluvial-flood-replication)

> **Reproduced paper:** Vogelbacher, A., von Szombathely, M., Lennartz, M., Poschlod, B. and Sillmann, J. (2026).
> *A high-resolution framework for urban pluvial flood risk mapping.* Natural Hazards and Earth System Sciences 26, 2765–2783.
> [doi:10.5194/nhess-26-2765-2026](https://doi.org/10.5194/nhess-26-2765-2026)

This is a FORRT computational reproduction. The paper computes building-level pluvial flood risk (social vulnerability × exposure × hazard, following the IPCC risk concept) in ArcGIS Pro and demonstrates it on a synthetic example for a Hamburg city quarter (37 buildings). Its authors published the example data, the toolbox and the ArcGIS output on Zenodo ([10.5281/zenodo.19860733](https://doi.org/10.5281/zenodo.19860733), CC BY 4.0).

Here the whole calculation is redone with an **independent open Python implementation**, written from the paper and the authors' exported scripts, and compared building by building with the authors' ArcGIS output.

## Result

![Authors' risk against this reproduction, per building](figures/main_result.png)

| Compared with the authors' ArcGIS output (37 buildings) | Largest difference |
|---|---|
| Sensitivity, coping capacity, social vulnerability, transformed social vulnerability | 4.4e-16 (exact) |
| Exposure (residents per building and per ground floor) | taken as published |
| Hazard to mobility / to well-being | 0.0008 / 0.0016 |
| Risk to mobility / to well-being | 0.013 / 0.004 |
| **Risk classes** (no risk → very high), both risk indices | **37 / 37 buildings identical** |

The paper's maps are reproduced exactly ([`figures/risk_class_maps.png`](figures/risk_class_maps.png)). The remaining differences, in the fourth decimal, are at the level of ArcGIS's geometry processing.

**Verdict: Validated** — the paper's building-level risk and its pattern (highest where high exposure and high hazard coincide) are reproduced on the authors' example.

### What the reproduction had to infer

Three details differ between the paper's text and the authors' results or scripts; the reproduction follows the results:

1. **Sensitivity weights.** The results need children 0.3 and elderly singles 0.7 (as in Eq. 2); the text of Sect. 3.1.1 gives 0.7 and 0.3.
2. **TOPSIS normalisation.** The authors' scripts divide by the square root of the sum of squares; Eq. 4 shows the sum.
3. **Hazard rings.** The 2 m and 5 m rings around a building exclude *every* building footprint, not only the building's own ([`figures/ring_rule.png`](figures/ring_rule.png)): the authors' stored intermediate fractions match within 0.05 percentage points this way, against up to 27.8 points otherwise.

Scope: one synthetic city-quarter example and one rainfall scenario, as published. Other cities, real city data and the paper's sensitivity analysis are not tested.

### An existing open implementation, for comparison

The FAIR2Adapt [`urban_pfr` toolbox](https://github.com/FAIR2Adapt/urban_pfr_toolbox_hamburg) is also run as is (scenarios A and B in [`notebooks/03_analysis.py`](notebooks/03_analysis.py)). It reproduces social vulnerability exactly but not the risk, because it recomputes exposure by disaggregation and keeps neighbouring footprints in the hazard rings (reported in its [issue #2](https://github.com/FAIR2Adapt/urban_pfr_toolbox_hamburg/issues/2)). It is not used for the reproduced results.

## Run it

```bash
git clone https://github.com/annefou/hamburg-pluvial-flood-replication.git
cd hamburg-pluvial-flood-replication
pixi install
pixi run snakemake --cores 1
```

The pipeline downloads both versions of the authors' Zenodo deposit (checksums verified), unpacks the ArcGIS layer package, runs the analysis and writes `results/` and `figures/`. The Jupyter Book version is at <https://annefou.github.io/hamburg-pluvial-flood-replication/>.

| Notebook | Does |
|---|---|
| [`01_data_download.py`](notebooks/01_data_download.py) | Fetches Zenodo v2 (reference) and v1 (intermediates), verifies MD5 |
| [`02_data_clean.py`](notebooks/02_data_clean.py) | Unpacks the ArcGIS layer packages into GeoPackages |
| [`03_analysis.py`](notebooks/03_analysis.py) | Independent implementation (scenario C) and the toolbox comparison (A, B); risk classes; ring-rule evidence |
| [`04_figures.py`](notebooks/04_figures.py) | The three figures |

## FORRT nanopublication chain

Quote → AIDA → FORRT Claim → Reproduction Study → Outcome → CiTO citation, drafted field by field in [`nanopubs/drafts/`](nanopubs/drafts/); published URIs go in [`nanopubs/PUBLISHED.md`](nanopubs/PUBLISHED.md).

## Credits

- **Paper, method, data and ArcGIS toolbox:** Anastasia Vogelbacher, Malte von Szombathely, Marc Lennartz, Benjamin Poschlod, Jana Sillmann ([paper](https://doi.org/10.5194/nhess-26-2765-2026); Zenodo [v2](https://doi.org/10.5281/zenodo.19860733), [v1](https://doi.org/10.5281/zenodo.17986182)).
- **FAIR2Adapt `urban_pfr` toolbox (comparison):** Esteban González, Zakieh Alizadehsani, José A. Zaino, Sonja Spälter, Anne Fouilloux.
- **This reproduction:** Anne Fouilloux (LifeWatch ERIC), with Claude (Anthropic) as coding assistant.

## Citation

Please cite both this reproduction ([`CITATION.cff`](CITATION.cff), DOI [{{ZENODO_DOI}}]({{ZENODO_DOI}})) and the original paper ([10.5194/nhess-26-2765-2026](https://doi.org/10.5194/nhess-26-2765-2026)).

## Built from a template

Created from [`sciencelivehub/forrt-replication-template`](https://github.com/sciencelivehub/forrt-replication-template), part of the [Science Live platform](https://platform.sciencelive4all.org). The operating manual for AI assistants is in [`CLAUDE.md`](CLAUDE.md) and [`AGENTS.md`](AGENTS.md); reference docs are in [`docs/`](docs/).

Licence: MIT.
