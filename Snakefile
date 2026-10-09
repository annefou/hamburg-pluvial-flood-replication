# Snakefile — orchestrates the replication pipeline end-to-end.
#
# One rule per notebook; each executes the jupytext notebook in place, so the
# notebook stays the source of truth and the Snakefile only sequences them.
#
# Usage:
#   snakemake --cores 1                  # run everything
#   snakemake --cores 1 -n               # dry run

NOTEBOOKS = "notebooks"
DATA = "data"
RESULTS = "results"
FIGURES = "figures"


rule all:
    input:
        f"{FIGURES}/main_result.png",
        f"{FIGURES}/risk_class_maps.png",
        f"{FIGURES}/ring_rule.png",
        f"{RESULTS}/comparison.csv",
        f"{RESULTS}/risk_classes_v2_C.csv",


# ---------- 01: both versions of the authors' Zenodo deposit ----------
rule data_download:
    output:
        f"{DATA}/raw/sources.json",
        f"{DATA}/raw/v2/PluvialFloodRiskMap_Data_V2.zip",
        f"{DATA}/raw/v1/UrbanPluvialFloodRiskToolbox.zip",
    log:
        f"{RESULTS}/logs/01_data_download.log",
    shell:
        f"cd {NOTEBOOKS} && jupytext --to notebook --execute 01_data_download.py > ../{{log}} 2>&1"


# ---------- 02: unpack the ArcGIS layer packages ----------
rule data_clean:
    input:
        f"{DATA}/raw/v2/PluvialFloodRiskMap_Data_V2.zip",
        f"{DATA}/raw/v1/UrbanPluvialFloodRiskToolbox.zip",
    output:
        f"{DATA}/interim/v2/example.gpkg",
        f"{DATA}/interim/v1/example.gpkg",
        f"{DATA}/interim/manifest.json",
    log:
        f"{RESULTS}/logs/02_data_clean.log",
    shell:
        f"cd {NOTEBOOKS} && jupytext --to notebook --execute 02_data_clean.py > ../{{log}} 2>&1"


# ---------- 03: run the toolbox, reproduce, compare ----------
rule analysis:
    input:
        f"{DATA}/interim/v2/example.gpkg",
        f"{DATA}/interim/v1/example.gpkg",
    output:
        f"{RESULTS}/comparison.csv",
        f"{RESULTS}/authors_formula_check.csv",
        f"{RESULTS}/per_building_v2_A_toolbox_exposure.csv",
        f"{RESULTS}/per_building_v2_C_independent.csv",
        f"{RESULTS}/risk_classes_v2_C.csv",
        f"{RESULTS}/risk_classes_per_building_v2_C.csv",
        f"{RESULTS}/ring_rule_cells.csv",
        f"{RESULTS}/run_provenance.json",
    log:
        f"{RESULTS}/logs/03_analysis.log",
    shell:
        f"cd {NOTEBOOKS} && jupytext --to notebook --execute 03_analysis.py > ../{{log}} 2>&1"


# ---------- 04: figures ----------
rule figures:
    input:
        f"{RESULTS}/per_building_v2_A_toolbox_exposure.csv",
        f"{RESULTS}/per_building_v2_C_independent.csv",
        f"{RESULTS}/risk_classes_per_building_v2_C.csv",
        f"{RESULTS}/ring_rule_cells.csv",
        f"{DATA}/interim/v2/example.gpkg",
    output:
        f"{FIGURES}/main_result.png",
        f"{FIGURES}/risk_class_maps.png",
        f"{FIGURES}/ring_rule.png",
    log:
        f"{RESULTS}/logs/04_figures.log",
    shell:
        f"cd {NOTEBOOKS} && jupytext --to notebook --execute 04_figures.py > ../{{log}} 2>&1"
