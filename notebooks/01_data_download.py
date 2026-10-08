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
# # 01 — Data download
#
# All inputs come from one citable record: the authors' own Zenodo deposit for
# Vogelbacher et al. (2026, NHESS), **Urban Pluvial Flood Risk Toolbox**,
# version 2, CC BY 4.0, [10.5281/zenodo.19860733](https://doi.org/10.5281/zenodo.19860733).
#
# It holds the synthetic 37-building example for a Hamburg city quarter used in
# the paper, the flood-depth layers (30–100 cm), the ArcGIS toolbox and its
# exported Python scripts, and — inside the ArcGIS layer package — the authors'
# **output** layer (`Building_ExampleLayer_Results`). That output layer is the
# reference this reproduction compares against.
#
# Every file is checked against the MD5 checksum Zenodo publishes for it, and
# the source log (`data/raw/sources.json`) records the SHA-256 as well.
#
# No credentials are needed.

# %%
import hashlib
import json
from pathlib import Path

import requests

# %%
RAW_DIR = Path("../data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

RECORD_ID = "19860733"
RECORD_DOI = "10.5281/zenodo.19860733"
API = f"https://zenodo.org/api/records/{RECORD_ID}"

# The files this pipeline needs. The ArcGIS toolbox itself (.atbx) and the
# exported scripts are archived as provenance, not executed.
WANTED = [
    "PluvialFloodRiskMap_Data_V2.zip",          # .lpkx: inputs + authors' output layer
    "Floodlevels.zip",                          # flood-depth shapefiles, 30–100 cm
    "Building_ExampleLayer_V2_AttributeTable.xlsx",
    "PluvialFloodRiskMapToolbox_Scripts_V2.zip",
    "PluvialFloodRiskMapToolbox_V2.zip",
    "### READ ME ###.txt",
]


# %%
def _digest(path: Path, algo: str) -> str:
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def download(entry: dict) -> Path:
    """Fetch one Zenodo file and verify it against the published MD5."""
    out = RAW_DIR / entry["key"]
    algo, expected = entry["checksum"].split(":", 1)
    if not (out.exists() and _digest(out, algo) == expected):
        with requests.get(entry["links"]["self"], stream=True, timeout=300) as r:
            r.raise_for_status()
            with open(out, "wb") as f:
                for chunk in r.iter_content(chunk_size=1 << 16):
                    f.write(chunk)
    actual = _digest(out, algo)
    if actual != expected:
        raise ValueError(f"{entry['key']}: {algo} {actual} != published {expected}")
    return out


# %% [markdown]
# ## Download

# %%
record = requests.get(API, timeout=60).json()
files = {f["key"]: f for f in record["files"]}
missing = [k for k in WANTED if k not in files]
assert not missing, f"not in Zenodo record {RECORD_ID}: {missing}"

SOURCES = []
for key in WANTED:
    path = download(files[key])
    print(f"  {key}  ({path.stat().st_size:,} bytes, checksum OK)")
    SOURCES.append({
        "name": key,
        "doi": RECORD_DOI,
        "url": files[key]["links"]["self"],
        "license": record["metadata"]["license"]["id"],
        "version": record["metadata"].get("version"),
        "accessed_on": __import__("datetime").date.today().isoformat(),
        "md5": files[key]["checksum"].split(":", 1)[1],
        "sha256": _digest(path, "sha256"),
    })

# %% [markdown]
# ## Source log

# %%
with open(RAW_DIR / "sources.json", "w") as f:
    json.dump({"record": RECORD_DOI, "title": record["metadata"]["title"],
               "creators": [c["name"] for c in record["metadata"]["creators"]],
               "sources": SOURCES}, f, indent=2)

print(f"Logged {len(SOURCES)} file(s) from {RECORD_DOI} to {RAW_DIR / 'sources.json'}")
