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
# All inputs come from the authors' own Zenodo deposit for Vogelbacher et al.
# (2026, NHESS), **Urban Pluvial Flood Risk Toolbox**, CC BY 4.0, concept DOI
# [10.5281/zenodo.17986181](https://doi.org/10.5281/zenodo.17986181). Both
# versions are fetched:
#
# - **v2** — [10.5281/zenodo.19860733](https://doi.org/10.5281/zenodo.19860733),
#   the version the published paper cites in its Data availability statement.
#   This is the **reference**.
# - **v1** — [10.5281/zenodo.17986182](https://doi.org/10.5281/zenodo.17986182),
#   deposited with the discussion paper. Its hazard-to-mobility (HMA) results
#   differ from v2 for 14 of the 37 buildings: the method was revised during
#   peer review. Kept as a historical check, not as the reference.
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

# Per version: the files this pipeline needs. The ArcGIS toolbox itself and the
# exported scripts are archived as provenance, not executed.
RECORDS = {
    "v2": {"id": "19860733", "doi": "10.5281/zenodo.19860733", "files": [
        "PluvialFloodRiskMap_Data_V2.zip",          # .lpkx: inputs + authors' output layer
        "Floodlevels.zip",                          # flood-depth shapefiles, 30–100 cm
        "Building_ExampleLayer_V2_AttributeTable.xlsx",
        "PluvialFloodRiskMapToolbox_Scripts_V2.zip",
        "PluvialFloodRiskMapToolbox_V2.zip",
        "### READ ME ###.txt",
    ]},
    "v1": {"id": "17986182", "doi": "10.5281/zenodo.17986182", "files": [
        "UrbanPluvialFloodRiskToolbox.zip",         # everything, incl. PluvialFloodRiskMap_Data.lpkx
        "### READ ME ###.txt",
    ]},
}


# %%
def _digest(path: Path, algo: str) -> str:
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def download(entry: dict, dest: Path) -> Path:
    """Fetch one Zenodo file and verify it against the published MD5."""
    dest.mkdir(parents=True, exist_ok=True)
    out = dest / entry["key"]
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
log = {}
for version, rec in RECORDS.items():
    record = requests.get(f"https://zenodo.org/api/records/{rec['id']}", timeout=60).json()
    files = {f["key"]: f for f in record["files"]}
    missing = [k for k in rec["files"] if k not in files]
    assert not missing, f"not in Zenodo record {rec['id']}: {missing}"
    print(f"{version}: {rec['doi']} (Zenodo version {record['metadata'].get('version')})")
    sources = []
    for key in rec["files"]:
        path = download(files[key], RAW_DIR / version)
        print(f"  {key}  ({path.stat().st_size:,} bytes, checksum OK)")
        sources.append({
            "name": key,
            "url": files[key]["links"]["self"],
            "md5": files[key]["checksum"].split(":", 1)[1],
            "sha256": _digest(path, "sha256"),
        })
    log[version] = {
        "doi": rec["doi"],
        "title": record["metadata"]["title"],
        "version": record["metadata"].get("version"),
        "license": record["metadata"]["license"]["id"],
        "creators": [c["name"] for c in record["metadata"]["creators"]],
        "accessed_on": __import__("datetime").date.today().isoformat(),
        "files": sources,
    }

# %% [markdown]
# ## Source log

# %%
with open(RAW_DIR / "sources.json", "w") as f:
    json.dump({"concept_doi": "10.5281/zenodo.17986181", "versions": log}, f, indent=2)

print(f"Logged {sum(len(v['files']) for v in log.values())} file(s) to {RAW_DIR / 'sources.json'}")
