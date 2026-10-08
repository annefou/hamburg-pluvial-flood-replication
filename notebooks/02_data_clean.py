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
# # 02 — Unpack the authors' ArcGIS layer packages
#
# Each Zenodo version ships its example as an ArcGIS layer package (`.lpkx`, a
# 7-zip archive) holding file geodatabases. This notebook extracts every layer
# into one GeoPackage per version, `data/interim/<version>/example.gpkg`, with
# the same layer names in both versions (v2 appends `_V2` to two of them).
#
# Nothing is reprojected or edited here: each layer keeps the coordinate
# reference system the authors stored it in. The buildings and streets are in
# EPSG:3857 (Web Mercator); the flood-depth layers and statistical units are in
# EPSG:25832 (ETRS89 / UTM 32N). How the pipeline handles that is a question for
# the analysis, not something to hide in the cleaning step.
#
# `data/interim/manifest.json` records, per version and layer: the source
# geodatabase, feature count, CRS and field list.

# %%
import json
import shutil
import zipfile
from pathlib import Path

import geopandas as gpd
import py7zr
import pyogrio

# %%
RAW_DIR = Path("../data/raw")
INTERIM_DIR = Path("../data/interim")

# Where each version keeps its layer package, and the name it uses for each layer.
PACKAGES = {
    "v2": {"zip": RAW_DIR / "v2" / "PluvialFloodRiskMap_Data_V2.zip",
           "lpkx": "PluvialFloodRiskMap_Data_V2.lpkx"},
    "v1": {"zip": RAW_DIR / "v1" / "UrbanPluvialFloodRiskToolbox.zip",
           "lpkx": "Zenodo/PluvialFloodRiskMap_Data.lpkx"},
}
RENAME = {
    "Building_ExampleLayer_V2": "buildings",
    "Building_ExampleLayer": "buildings",
    "Building_ExampleLayer_Results_V2": "results",
    "Building_ExampleLayer_Results": "results",
    "StatisticalExampleUnit": "statistical_units",
    "Streets": "streets",
}


def layer_name(name: str) -> str:
    """`Flood_30` -> `flood_30`; the authors' layer names -> stable names."""
    return RENAME.get(name, name.lower())


# %% [markdown]
# ## Extract and convert

# %%
manifest = {}
for version, pkg in PACKAGES.items():
    work = INTERIM_DIR / version / "_extract"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    with zipfile.ZipFile(pkg["zip"]) as z:
        z.extract(pkg["lpkx"], work)
    with py7zr.SevenZipFile(work / pkg["lpkx"]) as z:
        z.extractall(work / "lpkx")

    out = INTERIM_DIR / version / "example.gpkg"
    out.unlink(missing_ok=True)
    layers = {}
    for gdb in sorted((work / "lpkx").rglob("*.gdb")):
        for name, _geom in pyogrio.list_layers(gdb):
            target = layer_name(name)
            assert target not in layers, f"{version}: two layers map to {target!r}"
            gdf = gpd.read_file(gdb, layer=name)
            gdf.to_file(out, layer=target, driver="GPKG")
            layers[target] = {
                "source": f"{gdb.name}/{name}",
                "features": len(gdf),
                "crs": gdf.crs.to_string() if gdf.crs else None,
                "fields": [c for c in gdf.columns if c != "geometry"],
            }
    shutil.rmtree(work)
    manifest[version] = layers
    print(f"{version}: {len(layers)} layers -> {out}")
    for target, info in layers.items():
        print(f"  {target:18s} n={info['features']:3d}  {info['crs']}")

# %% [markdown]
# ## What differs between the two versions
#
# Same layers, same features, but not the same fields in the authors' results.

# %%
for layer in sorted(set(manifest["v1"]) | set(manifest["v2"])):
    f1 = set(manifest["v1"].get(layer, {}).get("fields", []))
    f2 = set(manifest["v2"].get(layer, {}).get("fields", []))
    if f1 != f2:
        print(f"{layer}: only in v1 {sorted(f1 - f2)}")
        print(f"{' ' * len(layer)}  only in v2 {sorted(f2 - f1)}")

# %%
with open(INTERIM_DIR / "manifest.json", "w") as f:
    json.dump(manifest, f, indent=2)
print(f"manifest -> {INTERIM_DIR / 'manifest.json'}")
