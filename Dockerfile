FROM ghcr.io/prefix-dev/pixi:0.68.1

LABEL org.opencontainers.image.source="https://github.com/annefou/hamburg-pluvial-flood-replication"
LABEL org.opencontainers.image.description="Independent reproduction of Vogelbacher et al. (2026) urban pluvial flood risk: runs the full Snakemake pipeline"
LABEL org.opencontainers.image.licenses="MIT"

WORKDIR /app

# pixi installs the FAIR2Adapt urban_pfr toolbox (used for the comparison
# scenarios) from its git commit, so the image needs git; the pixi base image
# does not ship it.
RUN apt-get update \
    && apt-get install -y --no-install-recommends git ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install the pinned environment first (separate from source copy so the lock
# layer is cached across source-only edits).
COPY pixi.toml pixi.lock /app/
RUN pixi install --locked

COPY . /app

# Mount any required credentials at runtime, e.g.:
#   docker run -v ~/.cdsapirc:/home/mambauser/.cdsapirc hamburg-pluvial-flood-replication
# See data/README.md for per-dataset credential setup.

CMD ["pixi", "run", "snakemake", "--cores", "1"]
