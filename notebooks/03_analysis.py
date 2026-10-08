# ---
# jupyter:
#   jupytext:
#     formats: py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # 03 — Run the open implementation and compare with the authors' results
#
# **Implementation under test:** FAIR2Adapt `urban_pfr_toolbox_hamburg`, pinned in
# `pixi.toml` to commit `afadc561` (tip of `feature/v3-paper-scientific-validation`).
#
# **Reference:** the authors' ArcGIS output layer in their Zenodo deposit — v2
# ([10.5281/zenodo.19860733](https://doi.org/10.5281/zenodo.19860733)), the
# version the published paper cites. v1
# ([10.5281/zenodo.17986182](https://doi.org/10.5281/zenodo.17986182)) is compared
# too, as a historical check only.
#
# **Settings** are those of the paper (Sect. 3) and of the toolbox's own
# validation notebook (`notebooks/scientific_validation_synthetic_small_dataset_local.ipynb`
# at the same commit): TOPSIS weights 0.7/0.3 (sensitivity), 0.5/0.5 (coping
# capacity), 0.5/0.5 (SVI); flood-susceptibility threshold 0.25 × mean and
# exponent 2; HMA buffers 5/15/30 m at 30 cm; HWB buffer 2 m over 30–100 cm.
# The CRS is EPSG:3857, the CRS the authors stored the buildings in.
#
# This notebook only measures. Interpretation belongs in the Outcome.

# %%
import json
import platform
from importlib.metadata import distribution
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from urban_pfr.analyzer import PFRAnalyzer

# %%
INTERIM = Path("../data/interim")
RESULTS = Path("../results")
RESULTS.mkdir(parents=True, exist_ok=True)
STAGE = INTERIM / "pipeline_inputs"
STAGE.mkdir(parents=True, exist_ok=True)

REFERENCE = "v2"
DEPTHS = list(range(30, 101, 10))

# %% [markdown]
# ## 1. Stage the inputs the toolbox expects
#
# The authors' input building layer already carries their derived columns
# (`R`, `R_G`, and in v2 `RB`, `RBG`; in v1 `Sen`). They are dropped so the toolbox
# computes them itself, as its validation notebook does.

# %%
src = INTERIM / REFERENCE / "example.gpkg"
buildings = gpd.read_file(src, layer="buildings")
published_exposure = buildings[["ID", "RB", "RBG"]].assign(ID=lambda d: d["ID"].astype(int))
buildings = buildings.drop(columns=[c for c in ["Sen", "R", "R_G", "RB", "RBG"] if c in buildings])
buildings.to_file(STAGE / "buildings.gpkg", driver="GPKG")
gpd.read_file(src, layer="statistical_units").to_file(STAGE / "statistical_units.gpkg", driver="GPKG")
gpd.read_file(src, layer="streets").to_file(STAGE / "streets.gpkg", driver="GPKG")
floods = STAGE / "Floodlevels"
floods.mkdir(exist_ok=True)
for d in DEPTHS:
    gpd.read_file(src, layer=f"flood_{d}").to_file(floods / f"Flood_{d}.gpkg", driver="GPKG")

# %% [markdown]
# ## 2. Run the pipeline

# %%
config = {
    "project": {"city_name": "vogelbacher2026_example", "crs": "EPSG:3857",
                "paths": {"input_gdb": None,
                          "buildings": str(STAGE / "buildings.gpkg"),
                          "statistical_units": str(STAGE / "statistical_units.gpkg"),
                          "streets": str(STAGE / "streets.gpkg"),
                          "flood_dir": str(floods),
                          "output_dir": str(INTERIM / "pipeline_run")}},
    "topsis_granularity": "building",
    "schema": {"stat_unit_col": "StatisticalUnit", "residents_col": "Residents",
               "living_area_col": "LivingArea", "floors_col": "Floors",
               "building_type_col": "Building_type",
               "sensitivity_fields": ["ES", "C"], "coping_fields": ["WR", "EDQ"]},
    "hazard_settings": {"hma_buffers": [5, 15, 30], "hwb_buffer": 2, "flood_threshold": 0.3,
                        "flood_depths": DEPTHS, "shape_param": 0.25,
                        "min_area_threshold": 0.0, "hwb_clip_max": None},
    "risk_settings": {"weight_hazard": 1.0, "weight_exposure": 1.0,
                      "weight_vulnerability": 1.0, "normalize_exposure": False},
    "topsis_weights": {"sensitivity": [0.7, 0.3], "coping_capacity": [0.5, 0.5], "svi": [0.5, 0.5]},
    "svpf_threshold": 0.25, "svpf_transform": 2.0,
}

analyzer = PFRAnalyzer(config)
analyzer.load_data()
analyzer.run_pipeline(skip_smoothing=True, skip_thiessen=True)
port = analyzer.buildings.drop(columns="geometry").copy()
port["ID"] = port["ID"].astype(int)
port.to_csv(RESULTS / "port_output.csv", index=False)
print(f"{len(port)} buildings computed")

# %% [markdown]
# ### Scenario B — exposure as published
#
# The paper's example does not disaggregate population: "we included a simple
# disaggregation tool within the toolbox, which is not used in this study"
# (Sect. 2.1); the exposure is a synthesised building-level realisation, carried
# in the v2 input layer as `RB` (all residents) and `RBG` (ground floor). The run
# above (scenario A) recomputes exposure by living-area disaggregation, as the
# toolbox does by default. Scenario B runs the same pipeline but takes exposure
# from `RB`/`RBG`, so the remaining differences isolate vulnerability and hazard.

# %%
analyzer_b = PFRAnalyzer(config)
analyzer_b.load_data()
analyzer_b.compute_vulnerability()
analyzer_b.compute_hazard()
b = analyzer_b.buildings
b["ID"] = b["ID"].astype(int)
b = b.merge(published_exposure, on="ID", how="left")
b["R"], b["R_G"] = b["RB"].astype(float), b["RBG"].astype(float)
analyzer_b.buildings = b
analyzer_b.compute_risk()
port_b = analyzer_b.buildings.drop(columns="geometry").copy()
port_b.to_csv(RESULTS / "port_output_published_exposure.csv", index=False)
print(f"scenario B: {len(port_b)} buildings, exposure from RB/RBG")

# %% [markdown]
# ## 3. The authors' own risk formula
#
# Before comparing, check which exposure field the authors' risk indices are
# built from (Eqs. 14–15: PFR = SV_PF · E · H with unit exponents). v2 carries
# two resident counts per building, `R`/`R_G` and `RB`/`RBG`; v1 called its
# exposure `EMA`/`EWB`.

# %%
refs = {v: gpd.read_file(INTERIM / v / "example.gpkg", layer="results").drop(columns="geometry")
        for v in ("v2", "v1")}
for ref in refs.values():
    ref["ID"] = ref["ID"].astype(int)

formula_rows = []
CANDIDATES = {"v2": {"PFR_MA": ("HMA", ["R", "RB"]), "PFR_WB": ("HWB", ["R_G", "RBG"])},
              "v1": {"PFR_MA": ("HMA", ["EMA"]), "PFR_WB": ("HWB", ["EWB"])}}
for v, ref in refs.items():
    for risk, (hazard, exposures) in CANDIDATES[v].items():
        for e in exposures:
            recomputed = ref["SV_PF"] * ref[e] * ref[hazard]
            formula_rows.append({"version": v, "risk": risk, "formula": f"SV_PF * {e} * {hazard}",
                                 "max_abs_diff": float((recomputed - ref[risk]).abs().max())})
formula = pd.DataFrame(formula_rows)
formula.to_csv(RESULTS / "authors_formula_check.csv", index=False)
print(formula.to_string(index=False))

# %% [markdown]
# ## 4. Field-by-field comparison
#
# For each field: the authors' value (`ref`) against the toolbox's (`port`), per
# building. `exact` = max |difference| ≤ 1e-6; `near` = correlation ≥ 0.95;
# otherwise `CHECK`. Exposure is compared against the field the authors' own
# risk formula uses (section 3) and against the raw count.

# %%
PORT = {"Sen": "Sensitivity", "CCap": "CopingCapacity", "SV": "SVI", "SV_PF": "SVPF",
        "HMA": "HMA", "HWB": "HWB", "PFR_MA": "PFRMA", "PFR_WB": "PFRWB"}
EXPOSURE = {"v2": {"E_MA (RB)": ("RB", "R"), "E_MA (R)": ("R", "R"),
                   "E_WB (RBG)": ("RBG", "R_G"), "E_WB (R_G)": ("R_G", "R_G")},
            "v1": {"E_MA (EMA)": ("EMA", "R"), "E_WB (EWB)": ("EWB", "R_G")}}


def compare(ref: pd.DataFrame, version: str, port: pd.DataFrame,
            scenario: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    m = ref.merge(port.add_prefix("port_").rename(columns={"port_ID": "ID"}), on="ID", how="inner")
    pairs = {f: (f, p) for f, p in PORT.items()}
    pairs.update({k: v for k, v in EXPOSURE[version].items()})
    rows, per_building = [], {"ID": m["ID"]}
    for field, (rcol, pcol) in pairs.items():
        r, p = m[rcol].astype(float), m["port_" + pcol].astype(float)
        d = (p - r).abs()
        corr = float(r.corr(p)) if r.std() > 0 and p.std() > 0 else np.nan
        rows.append({
            "version": version, "scenario": scenario, "field": field, "ref_column": rcol, "port_column": pcol,
            "n": int(len(m)), "ref_mean": r.mean(), "port_mean": p.mean(),
            "MAE": d.mean(), "max_abs_err": d.max(), "n_differ": int((d > 1e-6).sum()),
            "correlation": corr,
            "verdict": "exact" if d.max() <= 1e-6 else ("near" if corr >= 0.95 else "CHECK"),
        })
        per_building[f"{field}_ref"] = r
        per_building[f"{field}_port"] = p
    return pd.DataFrame(rows), pd.DataFrame(per_building)


SCENARIOS = {"A_toolbox_exposure": port, "B_published_exposure": port_b}
summaries = []
for scenario, run_output in SCENARIOS.items():
    for version, ref in refs.items():
        summary, per_building = compare(ref, version, run_output, scenario)
        per_building.to_csv(RESULTS / f"per_building_{version}_{scenario}.csv", index=False)
        summaries.append(summary)
        label = "reference" if version == REFERENCE else "historical check"
        print(f"\n== scenario {scenario} vs {version} ({label})")
        print(summary[["field", "ref_column", "MAE", "max_abs_err",
                       "n_differ", "correlation", "verdict"]].round(4).to_string(index=False))
pd.concat(summaries).to_csv(RESULTS / "comparison.csv", index=False)

# %% [markdown]
# ## 5. Provenance of this run

# %%
dist = distribution("urban-pfr")
run = {
    "implementation": "FAIR2Adapt/urban_pfr_toolbox_hamburg",
    "urban_pfr_version": dist.version,
    "urban_pfr_source": json.loads(dist.read_text("direct_url.json")),
    "reference": {"v2": "10.5281/zenodo.19860733", "v1": "10.5281/zenodo.17986182"},
    "config": config,
    "python": platform.python_version(),
    "geopandas": gpd.__version__,
}
with open(RESULTS / "run_provenance.json", "w") as f:
    json.dump(run, f, indent=2, default=str)
print(json.dumps(run["urban_pfr_source"], indent=2))
