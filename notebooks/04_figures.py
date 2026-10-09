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
# # 04 — Figures
#
# Three figures, all read from `results/` (written by `03_analysis.py`) and the
# unpacked example in `data/interim/`:
#
# 1. **Main result** — the authors' risk indices against ours, per building,
#    for the toolbox as is (scenario A) and the reproduction (scenario C).
# 2. **Risk-class maps** — the classes the paper maps (Figs. 6f, 7f), authors
#    and ours side by side.
# 3. **Ring rule** — the evidence behind the one code difference: flooded
#    fractions of the 2-m ring per building and depth, with and without
#    neighbouring footprints removed, against the authors' intermediates.
#
# Each figure is saved to `figures/` and shown inline.

# %%
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

# %%
RESULTS = Path("../results")
INTERIM = Path("../data/interim")
FIGURES = Path("../figures")
FIGURES.mkdir(parents=True, exist_ok=True)

# Validated palette (dataviz default): categorical slots 1–2, ordinal blue ramp.
OURS, TOOLBOX = "#2a78d6", "#eb6834"
CLASS_COLORS = ["#e4e3df", "#86b6ef", "#3987e5", "#1c5cab", "#0d366b"]
CLASS_NAMES = ["no risk", "low", "medium", "high", "very high"]
INK, MUTED, GRID = "#0b0b0b", "#52514e", "#e4e3df"
FLOOD = "#d4efe5"  # pale aqua: context layer, outside the blue risk ramp

plt.rcParams.update({
    "figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb",
    "axes.edgecolor": MUTED, "axes.labelcolor": INK, "axes.titlecolor": INK,
    "xtick.color": MUTED, "ytick.color": MUTED, "font.size": 10,
    "axes.spines.top": False, "axes.spines.right": False,
})

LABELS = {"PFR_WB": "Risk to well-being (PFR$_{WB}$)",
          "PFR_MA": "Risk to mobility and accessibility (PFR$_{MA}$)"}

# %% [markdown]
# ## 1. Main result

# %%
a = pd.read_csv(RESULTS / "per_building_v2_A_toolbox_exposure.csv")
c = pd.read_csv(RESULTS / "per_building_v2_C_independent.csv")
cls = pd.read_csv(RESULTS / "risk_classes_per_building_v2_C.csv")

fig, axes = plt.subplots(1, 2, figsize=(10, 4.6))
for ax, field in zip(axes, ("PFR_WB", "PFR_MA")):
    top = max(a[[f"{field}_ref", f"{field}_port"]].max().max(),
              c[[f"{field}_ref", f"{field}_port"]].max().max()) * 1.05
    ax.plot([0, top], [0, top], color=MUTED, lw=1, ls="--", zorder=1)
    ax.scatter(a[f"{field}_ref"], a[f"{field}_port"], s=46, color=TOOLBOX,
               edgecolor="#fcfcfb", linewidth=1.5, zorder=2, label="Toolbox as is (A)")
    ax.scatter(c[f"{field}_ref"], c[f"{field}_port"], s=46, color=OURS,
               edgecolor="#fcfcfb", linewidth=1.5, zorder=3, label="Independent reproduction (C)")
    same = int((cls[f"{field}_class_ref"] == cls[f"{field}_class_ours"]).sum())
    maxdiff = float((c[f"{field}_port"] - c[f"{field}_ref"]).abs().max())
    ax.text(0.03, 0.97, f"(C) max |difference| {maxdiff:.3f}\n"
                        f"(C) same risk class: {same}/{len(cls)}",
            transform=ax.transAxes, va="top", color=INK, fontsize=9)
    ax.set_xlim(0, top); ax.set_ylim(0, top)
    ax.set_xlabel("Authors (ArcGIS, Zenodo v2)")
    ax.set_ylabel("This reproduction")
    ax.set_title(LABELS[field], fontsize=10, loc="left")
    ax.grid(color=GRID, lw=0.6); ax.set_axisbelow(True)
axes[0].legend(loc="lower right", frameon=False)
fig.suptitle("Pluvial flood risk per building, Vogelbacher et al. (2026) example (37 buildings)",
             x=0.01, ha="left", fontsize=11, color=INK)
fig.tight_layout()
fig.savefig(FIGURES / "main_result.png", dpi=150, bbox_inches="tight")
plt.show()

# %% [markdown]
# ## 2. Risk-class maps
#
# Classes from the authors' step-6 rule (iterated means), applied to each set of
# values. The 30-cm flood extent is drawn underneath for context.

# %%
buildings = gpd.read_file(INTERIM / "v2" / "example.gpkg", layer="buildings")
buildings["ID"] = buildings["ID"].astype(int)
buildings = buildings.merge(cls, on="ID")
flood30 = gpd.read_file(INTERIM / "v2" / "example.gpkg", layer="flood_30").to_crs(buildings.crs)
cmap = ListedColormap(CLASS_COLORS)

fig, axes = plt.subplots(2, 2, figsize=(10, 9))
for row, field in enumerate(("PFR_WB", "PFR_MA")):
    for col, (who, column) in enumerate((("Authors (ArcGIS)", f"{field}_class_ref"),
                                         ("This reproduction", f"{field}_class_ours"))):
        ax = axes[row, col]
        flood30.plot(ax=ax, color=FLOOD, edgecolor="none")
        buildings.plot(ax=ax, column=column, cmap=cmap, vmin=-0.5, vmax=4.5,
                       edgecolor="#fcfcfb", linewidth=1.0)
        ax.set_title(f"{LABELS[field]}\n{who}", fontsize=10, loc="left")
        ax.set_axis_off()
handles = [Patch(facecolor=col, edgecolor=MUTED, linewidth=0.5, label=name)
           for col, name in zip(CLASS_COLORS, CLASS_NAMES)]
handles.append(Patch(facecolor=FLOOD, label="flood ≥ 30 cm"))
fig.legend(handles=handles, loc="lower center", ncol=6, frameon=False)
fig.tight_layout(rect=(0, 0.04, 1, 1))
fig.savefig(FIGURES / "risk_class_maps.png", dpi=150, bbox_inches="tight")
plt.show()

# %% [markdown]
# ## 3. The ring rule
#
# Each point is one building at one flood depth (37 × 8). Only cells where
# either value is non-zero are shown.

# %%
cells = pd.read_csv(RESULTS / "ring_rule_cells.csv")
cells = cells[(cells["fraction_ours"] > 0) | (cells["fraction_authors"] > 0)]
style = {"own footprint": (TOOLBOX, "Own footprint removed (toolbox)"),
         "all footprints": (OURS, "All footprints removed (authors' rule)")}

fig, ax = plt.subplots(figsize=(5.6, 5.2))
ax.plot([0, 100], [0, 100], color=MUTED, lw=1, ls="--", zorder=1)
for z, (rule, (colour, label)) in enumerate(style.items(), start=2):
    sub = cells[cells["ring_rule"] == rule]
    off = int((np.abs(sub["fraction_ours"] - sub["fraction_authors"]) > 0.5).sum())
    ax.scatter(sub["fraction_authors"], sub["fraction_ours"], s=34, color=colour,
               edgecolor="#fcfcfb", linewidth=1.2, zorder=z,
               label=f"{label}\n{off} cells off by > 0.5 percentage points")
ax.set_xlim(0, 100); ax.set_ylim(0, 100)
ax.set_xlabel("Authors' flooded fraction of the 2-m ring (%)")
ax.set_ylabel("Recomputed flooded fraction (%)")
ax.set_title("Hazard to well-being: 2-m ring per building and depth", fontsize=10, loc="left")
ax.grid(color=GRID, lw=0.6); ax.set_axisbelow(True)
ax.legend(loc="lower right", frameon=False, fontsize=8.5, labelspacing=1.0)
fig.tight_layout()
fig.savefig(FIGURES / "ring_rule.png", dpi=150, bbox_inches="tight")
plt.show()
