# `forecast/` — how to run the pipeline

*Written in ASD-STE100 Simplified Technical English.*

This folder holds the whole pipeline that makes the submitted values. It reads
**only files of this repository** and makes **no network call**. A full rebuild
takes about **4 minutes** on one H100 and costs **$0.00**.

> **The submitted run is `runs/2026-08-31_B_pop_on_t050_uv/`**, at temperature 0.5.
> Its control is `runs/2026-08-31_A_pop_off_t050_uv/`.
> `runs/2026-08-30_*_v2/` (temperature 0.85), `runs/B_pop_on/` and
> `runs/A_pop_off/` are **superseded**, kept as a record. **No submitted value
> comes from them.**

## The environment

The repository is a **uv project**. `pyproject.toml` and `uv.lock` are
deposited; `.venv/` is not, because `uv sync` rebuilds it.

```bash
uv sync          # or: make env
```

**Steps 1 and 3 and the tests have NO dependencies.** They import the Python
standard library only. `uv sync` therefore installs nothing and finishes in
under a second. That is deliberate: **a reader can rebuild `predictions/` from
`forecast/runs/` with a bare Python 3.11.**

**Step 2 needs the GPU stack**, and only step 2:

```bash
uv sync --extra gpu    # vllm 0.19.1, transformers 5.14.1, torch 2.10.0
```

This downloads several gigabytes and needs a CUDA GPU. **A DRY RUN of step 2
does not need it**: `run_vllm.py` imports vLLM only after `--go`, so you can
build and inspect every prompt with the plain environment.

> **Which interpreter produced the submitted values: this one.** Every step,
> the model run included, ran under `uv run` in the environment that
> `uv sync --extra gpu` builds from `pyproject.toml` and `uv.lock`. The
> environment reports vLLM 0.19.1, transformers 5.14.1 and torch 2.10.0+cu128,
> which are the pinned versions. Nothing outside this repository was used.

**Run every command from the repository root**, not from this folder.

## The three steps

### Step 1 — build the materials (once)

```bash
uv run forecast/extract_materials.py
```

Reads **two files of this repository only**: `survey/questionnaire.txt` (the
instrument, whose `### <title>` sections hold the full text of every condition)
and `codebook.csv` (the item wording, the anchors and the composite rule). Writes `forecast/materials/`: the 16 intervention texts, the 13
outcome blocks, the recruitment quotas, and a `MANIFEST.json` with a sha256 for
every file. It is idempotent: run it again and nothing changes.

### Step 2 — run the model (needs the GPU)

```bash
# the submitted variant: the population block is ON
uv run forecast/run_vllm.py --label B_pop_on_t050 --population --temperature 0.5 --go

# the control variant: the population block is OFF
uv run forecast/run_vllm.py --label A_pop_off_t050 --temperature 0.5 --go
```

**Leave out `--go` for a dry run.** It builds every prompt, prints the call
count and the prompt sizes, and sends nothing. Use it first, always.

Each variant writes `runs/<date>_<label>/` with three files:
`forecast.jsonl` (every draw of every arm), `forecast.meta.json` (the exact
settings, the call window, the sizes, and a sha256 for every input file) and
`AUDIT.txt`.

Each variant is **104 calls** (13 outcomes x 8 draws) and takes about
**1.8 minutes**.

**To see a prompt without running anything:**

```bash
uv run forecast/run_vllm.py --print-prompts --mode listwise
```

### Step 3 — build the prediction file

```bash
uv run forecast/build_predictions.py forecast/runs/2026-08-31_B_pop_on_t050_uv \
     --out predictions/team_27_T3_primary_v1.csv
```

It takes the **mean** of the 8 draws for each of the 208 (condition, outcome)
cells, writes the rows in the template's own row order, and prints the audits
that `make check` cannot make. **Read those audits.** `check.R` does not
range-check the Tier 3 `ate` on purpose, so a units error passes validation in
silence and only shows up in the score.

To compare two runs:

```bash
uv run forecast/build_predictions.py --compare \
     forecast/runs/2026-08-31_B_pop_on_t050_uv forecast/runs/2026-08-31_A_pop_off_t050_uv
```

### After step 3, always

```bash
make manifest   # write the new sha256 into metadata.json
make check      # the benchmark's own validator. It must say PASS
```

**Make targets, if you prefer them:**

```bash
make env                                              # uv sync
make materials                                        # step 1
make predictions RUN=forecast/runs/2026-08-31_B_pop_on_t050_uv   # step 3
make test                                             # the parity tests
make manifest && make check
```

`make check` fails with `sha256 matches` if you rebuild `predictions/` and
forget `make manifest`. That is the expected failure, and `make manifest` is
the fix.

## The run settings, and why each one

| Setting | Value | Why |
|---|---|---|
| `--mode` | `listwise` | All 16 interventions in one call. It beat `pointwise` in **6 of 6** comparisons on the public archives — 3 models x 2 archives, no exception. `docs/EVIDENCE.md` section 14.1 |
| `--temperature` | **0.5** | The whole deposited evidence base ran at 0.5. Temperature did not change any score: 0 of 46 paired tests were significant |
| `--samples` | 8 | Each draw reshuffles the intervention order. At temperature 0 a reshuffle alone moves the predictions to r = 0.57-0.73 against each other, so one call is not a stable estimate |
| `--seed` | 1 | The sampler seed is `seed + draw index`, so the 8 draws differ and the run repeats |
| `--population` | ON for the submitted variant | It is the tested variant. The block changed almost nothing: the two variants agree at r = +0.9941 |
| `--framings` | 1 | One fixed prompt. 0 of 45 framing comparisons were significant |
| thinking | OFF | Reasoning improved calibration and produced no new best score, at up to 408 times the output tokens. `docs/EVIDENCE.md` section 14.3 |

## What the submitted run measured

| | `2026-08-31_B_pop_on_t050_uv` — submitted | `2026-08-31_A_pop_off_t050_uv` — control |
|---|---|---|
| temperature | **0.5** | 0.5 |
| calls | **104** | 104 |
| arms asked / parsed | **1,664 / 1,664 — 100.0 per cent** | 1,664 / 1,664 — 100.0 per cent |
| draws for each of the 208 cells | **min 8, max 8, mean 8.00** | min 8, max 8, mean 8.00 |
| wall clock | **110.9 s** | 106.7 s |
| API calls / cost | **0 / $0.00** | 0 / $0.00 |
| call window | **2026-08-31T13:41:39Z to 13:43:30Z** | 2026-08-31T13:44:21Z to 13:46:08Z |

The two variants agree at **Pearson r = +0.9941** over the 208 cells.

## Two engine facts. Do not remove them

1. **`additional_config={"gdn_prefill_backend": "triton"}` is necessary.**
   `Qwen3.8-27B` has Gated Delta Net layers. vLLM picks the FlashInfer prefill
   kernel by default and builds it at run time. The build needs `nvcc`, and this
   machine has no CUDA toolkit, so the engine dies at the first prefill.
2. **The chat template must be applied with `enable_thinking=False`.** Without
   it the model writes `<think>...` and 88 per cent of the answers never reach a
   number.

## The rest of the folder

| Path | What it is |
|---|---|
| `core.py` | The prompt skeleton (six sections), the parsers, the work plan. Study-free and model-free |
| `megastudy.py` | The target study as ONE spec that fills the six slots. **The study is never named in any prompt** |
| `materials/` | The extracted stimuli and outcome blocks, with `MANIFEST.json` |
| `tests/test_render_parity.py` | Proves the prompt is the source prompt, byte for byte |
| `PROVENANCE.json` | Every input file with its sha256 |
| `runs_*.log` | The console log of each run |

## Rebuild everything from nothing

```bash
uv sync --extra gpu     # step 2 needs this; steps 1 and 3 do not
uv run forecast/extract_materials.py
uv run forecast/run_vllm.py --label B_pop_on_t050 --population --temperature 0.5 --go
uv run forecast/run_vllm.py --label A_pop_off_t050 --temperature 0.5 --go
uv run forecast/build_predictions.py forecast/runs/<date>_B_pop_on_t050 \
     --out predictions/team_27_T3_primary_v1.csv
make manifest && make check
```

**The run folder name carries the date**, so a rebuild on another day writes a
new folder and does not overwrite the deposited one. Put the new folder name
into step 3.
