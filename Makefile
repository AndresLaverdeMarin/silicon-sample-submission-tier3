.PHONY: help env check clean manifest zenodo_citation materials predictions test

help:
	@echo "make env                    create the uv environment (.venv) from pyproject.toml"
	@echo "make materials              step 1: build forecast/materials/ (no GPU, no deps)"
	@echo "make predictions RUN=<dir>  step 3: rebuild predictions/ from a run (no GPU)"
	@echo "make test                   run the forecast tests"
	@echo "make check                  validate this submission (files, metadata, data)"
	@echo "make clean                  clean the raw Tier-1 export in raw_data_deposit/ into predictions/"
	@echo "make clean INPUT=raw.csv    clean a specific raw export instead"
	@echo "make manifest               fingerprint predictions/ and record them in metadata.json"
	@echo "make zenodo_citation        (re)generate .zenodo.json from metadata.json (Zenodo deposit metadata)"

env:
	uv sync

materials:
	uv run forecast/extract_materials.py

predictions:
	@if [ -z "$(RUN)" ]; then \
	  echo "usage: make predictions RUN=forecast/runs/2026-08-31_B_pop_on_t050"; exit 1; fi
	uv run forecast/build_predictions.py "$(RUN)" \
	  --out predictions/team_27_T3_primary_v1.csv

test:
	uv run forecast/tests/test_render_parity.py

check:
	Rscript scripts/check.R

clean:
	@if [ -n "$(INPUT)" ]; then Rscript scripts/clean.R "$(INPUT)"; else Rscript scripts/clean.R; fi

manifest:
	Rscript scripts/manifest.R

zenodo_citation:
	Rscript scripts/zenodo_citation.R
