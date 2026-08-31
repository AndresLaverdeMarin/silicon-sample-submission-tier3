# Silicon Sample Benchmark — method registration form

Fill in every item before the prediction lock; this file ships inside your repo's Zenodo release
(see the README's *Deposit* step). This form covers **one entry** (one repo / one Zenodo release,
`primary` or `secondary-k` — see the README's *What counts as a submission*); if you submit several
entries, fill one form per entry. Items marked **★**
must be disclosed **fully publicly** (never escrowed or withheld). Items marked **†** must be at
minimum escrowed — they may be sealed from the public, but never withheld from the core team. Items
not applicable to your approach: write `N/A`. When several models serve different pipeline stages, complete the model
sections (B) once per model. See the call's *Disclosure policy* for escrow rules.

> **This form covers a TIER 3 entry.** It is a **direct effect forecast**, not a per-respondent
> simulation. It is a different method from `team_27`'s Tier 1 entry, not a lower-tier copy of it.
> The Tier 1 form is in a separate repository:
> <https://github.com/AndresLaverdeMarin/silicon-sample-submission>.
>
> **Read this form with [`docs/METHOD.md`](docs/METHOD.md) and
> [`docs/EVIDENCE.md`](docs/EVIDENCE.md).** `METHOD.md` gives the prompt, the sign rule and the
> ensemble in enough detail to rebuild the entry. `EVIDENCE.md` gives every measurement that shaped
> it, wins and nulls together, each naming the file that produced it.
>
> ### The submitted run
>
> **Every run fact in this form is copied from
> `forecast/runs/2026-08-31_B_pop_on_t050_uv/`.** That is the **submitted** run: 104 calls, 1,664 of
> 1,664 arms parsed (100.0 per cent), $0.00, 2026-08-31T13:41:39Z to 2026-08-31T13:43:30Z, 110.9 s,
> temperature 0.5. **It supersedes `forecast/runs/2026-08-30_B_pop_on_v2/` at temperature 0.85; see
> the supersession notice above.**
>
> **Variant A (`forecast/runs/2026-08-31_A_pop_off_t050_uv/`) is the control condition, not the
> submission.** It is the same run with the population block removed. The two variants agree at
> Pearson r = +0.9873 over the 208 cells. Rebuild that number with
> `forecast/build_predictions.py --compare` on the two run directories.
>
> **The runs `forecast/runs/B_pop_on/` and `forecast/runs/A_pop_off/` are SUPERSEDED.** They ran
> before the `Extreme weather predictions` arm was cut to what one participant read
> (`docs/METHOD.md` section 3.4). They stay on disk as a record of the first pass. **No submitted
> value comes from them.** `raw_data_deposit/` no longer holds copies of that first pass; see item K.2.
>
> **Do not retype a value that `forecast.meta.json` already holds.** Copy it.
>
> ### Items that are still open
>
> Five items need a person, not a run. Each is marked in place.
>
> | Item | What is missing | Who must supply it |
> |---|---|---|
> | I.1 | The competing-interests declaration | the members named in 0.1 |
> | I.3 | The signature on the blinding attestation | the members named in 0.1 |
> | K.1 | `code_doi` and `zenodo_doi` in `metadata.json`, after the Zenodo release | the members named in 0.1 |
> | **J.2** | **A decision on the four preregistration breaches.** They are declared in full under J.2. The choice is to keep the entry with the declaration attached, or to re-run the preregistered test as written. | the members named in 0.1 |
> | **K.3** | **A decision on the spend approval gap.** $5.6752 was spent on paid calls ($4.0108 to 2026-08-30, plus $1.6644 on 2026-08-31) and no approval from David is recorded on disk. It affects no submitted value. | the members named in 0.1 |
>
> One more item needs a file copy, not a decision:
>
> | Item | What is missing | Who must supply it |
> |---|---|---|
> | ~~**K.2**~~ | ~~`raw_data_deposit/` still holds six files of the superseded first pass.~~ **CLOSED 2026-08-31: the stale files are removed; the folder now holds the submitted pair and `method_search/`.** | done |
>
> Every other item is closed against a file. `metadata.json` now holds the real team, the real model
> id and the SHA-256 of the submitted prediction file.
>
> ### **Read this before any p value in this form**
>
> **Our own preregistration was breached in four ways, so every result reported here is
> EXPLORATORY, not confirmatory.** The full declaration is item **J.2**. The headline result —
> p = 0.0073 — was selected after seeing 34 runs, so **its true false-positive rate is higher than
> 0.0073**. The measurements themselves are real, reproducible and unfabricated. The problem is the
> inference, not the data.

---

> ### SUPERSESSION NOTICE — 2026-08-31: the submitted run changed
>
> **The submitted values now come from `forecast/runs/2026-08-31_B_pop_on_t050_uv/`,
> at temperature 0.5.** They came from `forecast/runs/2026-08-30_B_pop_on_v2/`, at
> temperature 0.85. Its control is `forecast/runs/2026-08-31_A_pop_off_t050_uv/`.
>
> **Why.** The whole deposited evidence base — all 74 scored configurations in
> `raw_data_deposit/method_search/` — ran at temperature 0.5. The submission now
> runs at the temperature its own evidence was measured at. **Nothing else
> changed**: the same model, the same prompt, the same population block, the same
> 8 draws, the same seed 1, the same 104 calls.
>
> **What it did to the numbers.** The two runs agree at **Pearson r = +0.9803**
> over the 208 cells, with a mean absolute difference of 0.2371 and sign agreement
> on 207 of 208. This is consistent with the search finding that temperature does
> not matter (0 of 46 paired tests significant). The new run parses **100.0 per
> cent** of arms (1,664 of 1,664) against 99.0 per cent before, so **every one of
> the 208 cells now rests on 8 draws** rather than 7 or 8.
>
> **The pipeline now runs entirely inside this repository's own `uv`
> environment**, the model run included (`pyproject.toml`, `uv.lock`, extra
> `gpu`; vLLM 0.19.1, transformers 5.14.1, torch 2.10.0+cu128). Nothing outside
> the repository is used.
>
> **Where the old runs are.** Two pairs are superseded and stay on disk as a
> record. **No submitted value comes from any of them.**
> `forecast/runs/2026-08-30_*_v2/` is the temperature-0.85 pair.
> `forecast/runs/2026-08-31_*_t050/` is the temperature-0.5 pair made before the
> repository had its `uv` environment. `raw_data_deposit/` holds the `_uv` pair.
>
> **Re-running the model does NOT reproduce it bit for bit.** The `_t050` and
> `_t050_uv` pairs used the same seed, the same prompts and the same pinned
> versions, and 1,447 of 1,664 arm-answers (87.0 per cent) came out identical.
> vLLM's batching changes the floating-point path, so **the frozen
> `forecast.jsonl` is the reproducible artefact, not the run that made it.** The
> two pairs agree at Pearson r = +0.9974 over the 208 submitted cells, mean
> absolute difference 0.0756, same sign in 207 of 208. Steps 1 and 3 ARE
> deterministic: they rebuild `predictions/` from a frozen `forecast.jsonl` to
> the same sha256 every time, in about 0.12 s.
>
> **Reading the rest of this file.** A reference to `2026-08-30_*_v2` or to
> temperature 0.85 for the SUBMITTED run describes the superseded run. A reference
> to temperature 0.85 in the METHOD SEARCH is correct and unchanged: that search
> really did run at 0.85.

## 0 · Approach identity and output
- **0.1 Team ★** — name, the one or two members (teams are at most two, unless a larger team was approved on request), affiliations, corresponding contact:
  `team_27`. Andrés Laverde Marín, Joint Research Centre of the European Commission; corresponding
  contact andreslaverdemarin@gmail.com. Giordano De Marzo, University of Konstanz, ORCID
  [0000-0002-3127-5336](https://orcid.org/0000-0002-3127-5336).
  The same values appear in `metadata.json` (`team_name`, `contact`, `creators`), which now holds
  the real team and not the template's example.
- **0.2 Plain-language summary ★** — one paragraph, what the approach does (not how):
  We do not build synthetic people. We describe the study to a language model: who took part, what
  they read, which questions they answered, and what number we want. We then show the model **all
  16 intervention texts at the same time** and ask it for one number for each text — how far that
  text moved the average answer, in points of the outcome scale. We ask the same question 8 times,
  with the 16 texts in a new random order each time, and we take the mean. The model never learns
  which study this is.
- **0.3 Submission tier & approach family ★** — tier (1/2/3); family (e.g. per-respondent simulation / agent / direct forecast; single model / ensemble / multi-agent; zero-shot / literature-conditioned):
  **Tier 3.** **Direct effect forecast.** Single model. An ensemble only in the weak sense that the
  **same** prompt is asked 8 times and averaged; there is no second model, no multi-agent scaffold,
  and no ensemble of different prompts. Zero-shot: no fine-tuning, no retrieval, no in-context
  example of any study's results. The model is local open weights on our own hardware.
- **0.4 Pipeline diagram** — ordered steps from raw inputs to submitted file:
  1. `forecast/extract_materials.py` — read the 16 intervention texts from the benchmark's own
     `survey/questionnaire.txt`, and the 13 outcome definitions from `codebook.csv`. Write
     `forecast/materials/stimuli/*.txt`, `outcomes.json` and `stimuli_index.json`. The condition
     order is checked against `scripts/lib/submission_spec.R`.
  2. `forecast/megastudy.py` — fill the six prompt slots for this study. One cell = one outcome.
  3. `forecast/core.py::render` builds one prompt for each of the 13 outcomes. Each prompt holds the
     six sections and all 16 intervention texts, in a random order.
  4. `forecast/core.py::build_work` makes 8 draws for each outcome. Each draw reshuffles the 16 texts
     and uses a new seed. 13 outcomes x 8 draws = **104 calls**.
  5. `forecast/run_vllm.py` runs those 104 prompts on local weights in one vLLM batch, and writes
     `forecast/runs/<run date>_<label>/forecast.jsonl` and `forecast.meta.json`. It ran two times:
     **`2026-08-30_B_pop_on_v2` with the population block, which is submitted**, and
     `2026-08-30_A_pop_off_v2` without it, which is the control.
  6. `forecast/core.py::parse_listwise` reads the `<position>: <number>` lines and maps each position
     back through the recorded arm order.
  7. `forecast/build_predictions.py --out predictions/team_27_T3_primary_v1.csv` takes the mean
     over the draws, writes `condition, outcome, ate` in the template's row order, and prints
     `AUDIT.txt`. Without `--out` it writes no prediction file.
  8. `make manifest`, then `make check`.
  Full detail: [`docs/METHOD.md`](docs/METHOD.md) sections 3 to 8.
- **0.5 Coverage ★** — number of respondents/cells/estimates; mapping to conditions. Full coverage is required: every submission predicts **all 16 interventions and all 13 outcomes** (partial coverage is not accepted). Confirm here:
  **Full coverage, confirmed. 16 interventions x 13 outcomes = 208 estimates, each present exactly
  one time.** No `control` row: Tier 3 reports effects **against** control, and a `control` row is a
  fail (`scripts/lib/check_lib.R:452-453`). No `NA` and no empty `ate`. No respondents: this is a
  direct forecast, so there is no synthetic sample and no per-respondent record. The condition and
  outcome strings come from `scripts/lib/submission_spec.R`; none is typed by hand or written by the
  model. The full contract is in `predictions/SPEC_NOTES.md`.

## A · Scope of LLM use
- **A.1 Purpose** — every workflow stage where LLMs are used:
  **One stage produces submitted values: step 4, the forecast.** Every other step is deterministic
  Python. No language model reads the codebook, builds a prompt, computes a mean, or writes an
  output file.
  Two further models were run **for method selection only**, on public data, and neither contributed
  any submitted value: `qwen/qwen3.8-flash` and `qwen/qwen3.8-27b`, both through OpenRouter. They
  have their own model sections below. Their role is described in J.1 and their cost in K.3.
- **A.2 Degree of automation ★** — confirm fully automated, no human in the loop at prediction time; note any exception:
  **Fully automated at prediction time. No exception.** The prompts are built by code from the
  benchmark materials before any answer exists. No answer is edited, selected, re-asked, or replaced.
  A draw that fails to parse is dropped, not repaired — see G.2.
  Human work was limited to writing the code, reading the code, and reading the aggregate reports.

## B · Model / system details (once per model)

### B — Model 1: the forecasting model (produces every submitted value)
- **B.1 Model name(s)** — exact identifiers incl. provider, size, version/timestamp, source link:
  `Qwen/Qwen3.8-27B` — 27 billion parameters, dense, instruction-tuned. Local weights from the
  Hugging Face Hub, <https://huggingface.co/Qwen/Qwen3.8-27B>. Read from the local cache with
  `HF_HUB_OFFLINE=1`; no hosted endpoint answers any submitted item.
  Recorded by the run itself: `forecast/runs/2026-08-30_B_pop_on_v2/forecast.meta.json`, field
  `model`. **`2026-08-30_B_pop_on_v2` is the submitted run.**
  The same model id is in `metadata.json`, field `models`.
- **B.2 Access & context mode** — API/web/local; API name + version; chat vs stateless; exact call dates:
  Local inference on our own hardware, through the **vLLM offline engine**. No API, no provider, no
  account, no key. The model's own chat template is applied with `enable_thinking=False`, so the
  route is a **single-turn chat message with reasoning off**. Every one of the calls is stateless
  with respect to every other; the model is given one prompt and keeps no history.
  **Call-date window of the SUBMITTED run, from
  `forecast/runs/2026-08-31_B_pop_on_t050_uv/forecast.meta.json`:
  `2026-08-31T13:41:39.792000+00:00` to `2026-08-31T13:43:30.644000+00:00`** — one continuous run of
  1.8 minutes (`wall_clock_s` 110.9). No submitted value was generated outside this window.
  Both values are ISO-8601 UTC and are copied, not rounded and not relabelled.
  The control variant A ran immediately after, from `2026-08-31T13:44:21.855000+00:00` to
  `2026-08-31T13:46:08.589000+00:00`
  (`forecast/runs/2026-08-31_A_pop_off_t050_uv/forecast.meta.json`). **No value from variant A is
  submitted.** The window that covers both runs is `2026-08-31T13:41:39Z` to
  `2026-08-31T13:46:08Z`.
  **The SUPERSEDED temperature-0.85 pair ran on 2026-08-30**, from `16:48:09Z` to `16:50:11Z`
  (variant B) and `16:51:13Z` to `16:53:12Z` (variant A). **No submitted value comes from either.** The superseded first pass ran earlier the same day, from
  `2026-08-30T16:04:04Z` to `2026-08-30T16:09:33Z`; no submitted value comes from it. Every
  measurement run reported in `docs/EVIDENCE.md` ran on 2026-08-29 or 2026-08-30.
- **B.3 Configuration** — temperature, top-p/top-k, max tokens, penalties, stop sequences, seeds, reasoning effort, completions per item:
  `top_p 0.95`, no top-k, no penalties, no stop sequence, `seed 1` with the rule `seed + draw index`
  so the 8 draws differ, `dtype bfloat16`, `max_model_len` set from the longest prompt plus the
  reply. `max_tokens = 40 x (number of arms) + 128` for a listwise call.
  **Reasoning: OFF.** `enable_thinking=False` in the chat template. With thinking on, 88 per cent of
  answers never reach a number (measured 2026-08-30).
  **Completions: 8 draws for each outcome, one completion for each draw.**
  **Temperature 0.85**, from `forecast/runs/2026-08-30_B_pop_on_v2/forecast.meta.json`. Temperature
  is a measured null on both public studies (0 of 46 paired tests significant, `docs/EVIDENCE.md`
  section 5b), so this value was **not** selected on performance. It is the middle of the range that
  keeps the parse rate high on local weights: the submitted run parsed 99.0 per cent of its arms,
  and only 1 call of 104 failed. See G.2.
- **B.4 Customization** — fine-tuning, RAG, prompt optimization, tool use, web search, agentic scaffolds (cross-ref H):
  None. No fine-tuning, no retrieval, no web search, no tool use, no agentic scaffold. The published
  weights are used as they are. The prompt was designed against **public** studies only — see J.1 —
  and never against any outcome of the target study.
- **B.5 Persistent memory** — across interactions? what persisted:
  None. Each call sees one prompt and nothing else. vLLM's prefix cache is a speed optimization over
  identical token prefixes; it changes no output.
- **B.6 Inference stack** — for local models: serving framework + version, quantization, hardware:
  vLLM 0.19.1, offline engine (`vllm.LLM`), torch 2.10.0+cu128, transformers 5.14.1, Python 3.11.
  **No quantization** — the published BF16 weights. Hardware: one NVIDIA H100 80GB HBM3, driver
  550.127.08, CUDA 12.4. `gpu_memory_utilization 0.90`, `max_num_seqs 32` (the default at
  `forecast/run_vllm.py:168`; `forecast.meta.json` does not record it),
  `enable_prefix_caching=True`, `additional_config={"gdn_prefill_backend": "triton"}`.
  **Why the Triton backend.** Qwen3.8-27B has Gated Delta Net layers. vLLM by default picks the
  FlashInfer prefill kernel and JIT-compiles it, which needs `nvcc`. This machine has no CUDA
  toolkit, so the engine dies at the first prefill with
  `RuntimeError: Could not find nvcc`. The Triton kernel needs no compiler.
  **The vLLM SERVER route does not work on this machine for the same reason.** That is why the entry
  uses the offline engine and not an HTTP server.
  Recorded by the submitted run: `max_model_len 16080`, `gpu_memory_utilization 0.9`, longest prompt
  44,401 characters, mean prompt 43,292.3 characters
  (`forecast/runs/2026-08-30_B_pop_on_v2/forecast.meta.json`). The control variant A is 43,737 and
  42,628.3 characters (`forecast/runs/2026-08-30_A_pop_off_v2/forecast.meta.json`); variant B is
  longer because the population block adds about 664 characters.
  **The version strings are read from the interpreter that ran the job**,
  `/home/jovyan/LLMmegastudy/.venv-vllm/bin/python`; `forecast.meta.json` records the engine but not
  the package versions, so they are named here and not copied.
- **B.7 Ensembles** — members + exact aggregation rule:
  **One model. An ensemble of 8 DRAWS of the same prompt, not of different prompts or models.**
  Each draw reshuffles the 16 intervention texts and uses a new seed. The aggregation rule is the
  **unweighted arithmetic mean** over the draws that parsed, computed for each (intervention,
  outcome) pair. No median, no trimming, no weighting, no outlier rule.
  **Why 8 draws and not 1.** At temperature 0 the model does **not** agree with itself when the same
  arms are shown in a different order: measured self-agreement r = +0.5723 (local `Qwen3.8-27B`),
  +0.6151 (hosted 27b), +0.7320 (hosted flash) — `docs/EVIDENCE.md` section 7. The ensemble averages
  that position sensitivity away.
  **Why not an ensemble of 10 framing sentences.** Measured, and rejected: the ranking of the 10
  sentences does not repeat between the two public studies (Pearson -0.2698, p = 0.4509; Spearman
  -0.0909, p = 0.8028) — `docs/EVIDENCE.md` section 5d.

### B — Model 2: `qwen/qwen3.8-flash` (method selection only, no submitted value)
- **B.1–B.7** — `qwen/qwen3.8-flash`, hosted through OpenRouter, `/api/v1/chat/completions`,
  `reasoning: {enabled: false}`, `top_p 0.95`, `seed 1` with the rule `seed + draw index`,
  temperatures 0.0 / 0.5 / 0.85 / 1.0 / 1.6, 8 draws for each cell (2 at temperature 0.0). Call
  window **2026-08-29 to 2026-08-30**. It ran the listwise-against-pointwise comparison, the
  temperature sweep, the demographic-block test, the framing test and the stimulus-provenance test
  on the two **public** studies. **No value it produced reaches the deposited answers.** Its spend is
  in K.3.
- **B.2 note** — This model is the best scorer in our grid on Broockman (+0.4400 within-cell at
  temperature 0.0). **It is not the submission model.** The reasons are in J.1.

### B — Model 3: `qwen/qwen3.8-27b` (method selection only, no submitted value)
- **B.1–B.7** — `qwen/qwen3.8-27b`, hosted through OpenRouter, same route and same settings as
  model 2, same call window. It is the **hosted** counterpart of the submission model. Its purpose
  was to check that the same weights give the same score through a provider and on our own hardware.
  They do: three paired tests, differences -0.0082, -0.0499 and +0.0252, p = 0.7949, 0.2429 and
  0.6643 (`docs/EVIDENCE.md` section 5a). **No value it produced reaches the deposited answers.**

### B — Models 4 to 7: the extended model comparison (no submitted value)
- **B.1–B.7** — Four more models were scored on the public archives on 2026-08-31, at the same
  settings as the entry's own runs (listwise, temperature 0.5, top_p 0.95, 8 draws, seed 1 and
  seed 2, reasoning off unless stated):
  - `google/gemma-4-26B-A4B-it` — local weights, vLLM offline engine, `HF_HUB_OFFLINE=1`. No cost.
  - `google/gemma-4-E4B-it` — local weights, same engine. No cost.
  - `deepseek/deepseek-v4-flash` — hosted through OpenRouter, `/api/v1/chat/completions`.
  - `z-ai/glm-5.3-flash` — hosted through OpenRouter, same route.
  A 12-run arm turned the models' reasoning ON (`Qwen3.8-27B` at `reasoning_effort = xhigh`, the
  Gemma models with `enable_thinking = true`). **No value from any of these models, or from the
  reasoning arm, reaches the deposited answers.** Every run is in
  `raw_data_deposit/method_search/`; the scores are in `docs/EVIDENCE.md` section 14; the spend is
  in K.3.
- **B.2 note** — On the two archives that carry published baselines, the submission model
  `Qwen/Qwen3.8-27B` beats published gpt-4 and the human expert forecasters (Broockman +0.4641
  against +0.2329 and +0.1486; Doell +0.5572 against +0.4374 and +0.4960) and wins two of the three
  archives outright. **It is confirmed as the submission model by this comparison, not displaced by
  it.**

### B — Models 8 and later: the earlier open-weight comparison (no submitted value)
- **B.1–B.7** — Eight open-weight models were scored earlier in the project, on the Ashokkumar
  secondary archive, to choose a model for `team_27`'s **Tier 1** entry. That comparison is
  described in the Tier 1 registration form and is **not** part of this entry's selection. It is
  named here only because it is the reason `Qwen/Qwen3.8-27B` was already on this machine. **None of
  those models produced any value in this entry.**

## C · Prompts
- **C.1 Exact prompts** — verbatim text or link to deposited file; were they iteratively refined? pre-specified vs in response to outputs:
  The prompt is built by `structured_forecast.py::render` from six slots: `TASK`, `STUDY`, `OUTCOME`,
  `ESTIMAND`, `ARMS`, `ASK`. A fully rendered example is in [`docs/METHOD.md`](docs/METHOD.md)
  section 3.1, and the builder prints every prompt with `--print-prompts`, which sends nothing.
  **Refinement, stated honestly.** The prompt WAS refined, twice, and both changes are recorded with
  their dates:
  1. **2026-08-29, before any configuration was scored.** The `Study description:` block, which named
     the study and its authors, was **removed**, and `Answer with a single number and nothing else.`
     was added. Measured on 60 calls: the parse rate rose from 48.3 per cent to 91.7 per cent, and
     the model stopped answering by recall. This change is written into
     `notes/PREREG_broockman_method_search.md` section 7b **before** the first score.
  2. **2026-08-30.** A sign-convention bug was fixed. See G.2 and `docs/EVIDENCE.md` section 6.
  **Neither change was made in response to a score on the target study**, whose outcomes we have
  never seen. Both were made against public data.
- **C.2 System-wide instructions**:
  **None.** There is no system prompt. The whole context is the user message shown in
  `docs/METHOD.md` section 3.1, wrapped in the model's own chat template. The model is not told to
  be helpful, not told it is a language model, and not told anything about the benchmark.
- **C.3 Prompt-design rationale** — brief rationale for the prompt design: why prompts were structured as they were, and the reasoning behind major design choices (recommended, not required):
  *Six sections, in the published order.* All 504,840 prompts deposited by Ashokkumar et al. (2026)
  put the instruction first, the context next, the stimulus late and the answer cue last. We copy
  that order. Ruan et al. (2025) is the one adjacent controlled test of prompt structure on an ATE
  estimate, and it found no effect, so there was no reason to depart from it.
  *All arms in one call (listwise).* Tier 3 is scored on how the predicted effects rank against each
  other. A call that sees one text cannot know the next text is stronger. Measured: listwise beat
  pointwise in all six paired tests, on both studies and all three models (`docs/EVIDENCE.md`
  section 1). One of the six reached p < 0.05.
  *The estimand is stated twice, in plain words and in statistical words.* The quantity is named as
  the OLS coefficient of the condition with the control group as the reference level, which is what
  the archive holds and what the benchmark asks for.
  *No magnitude anchor.* No paper on disk tests a stated range for effect-size forecasting, and an
  anchor can only pull every answer toward one value, which compresses the spread a Pearson
  correlation needs.
  *A population block, kept although it is a measured null.* The `STUDY` slot of the submitted
  prompt carries the benchmark's own recruitment-quota table, projected to N = 18,000
  (`forecast/materials/quotas_18000.csv`). It was tested four times, and it never moved the score:
  on the OLD pointwise prompt +0.0592 (p = 0.5151), -0.1235 (p = 0.6395) and -0.1678 (p = 0.1440);
  on the NEW structured listwise template that this entry uses, -0.0029 (p = 0.8671) on Broockman
  and +0.0024 (p = 0.3910) on Voelkel. **None is significant.** The block is in the submitted prompt
  for consistency with `team_27`'s Tier 1 entry, which describes the same population from the same
  source file, and not because it improves the forecast. The control run without the block is
  deposited, and the two agree at Pearson r = +0.9873 over the 208 cells. See `docs/EVIDENCE.md`
  section 5c.
  *No chain of thought.* No paper on disk measures it on direct effect-size forecasting, the three
  adjacent results are flat or down, and with thinking on the local model's parse rate collapses.
  *The prompt never names the study.* See I.4 and `docs/METHOD.md` section 7.
  The full review behind these choices is `notes/LIT_structured_forecast_prompt.md`.

## D · Persona / profile construction (Tiers 1–2)
- **D.1 Profile source** — source of demographic profiles you constructed: a public survey (e.g. GSS / ANES / Census), other survey, fully synthetic, or none. The benchmark ships no participant pool; report how you built yours, incl. condition assignments:
  **None. N/A for this entry.** No profile, no persona, no synthetic respondent, and no condition
  assignment exists. This is a direct forecast of the effect, not a simulation of people.
  The prompt does hold **one aggregate description of the population**: the benchmark's own
  recruitment-quota table, projected to N = 18,000, in the `STUDY` slot. That is a description of a
  sample, not a set of profiles. No number in it is drawn, sampled or assigned to anybody. Its
  source is `forecast/materials/quotas_18000.csv`, copied from the benchmark preregistration's
  quota table (`forecast/PROVENANCE.json`). It is a measured null — see C.3 and
  `docs/EVIDENCE.md` section 5c.
- **D.2 Profile verbalization** — which variables, rendered how (template vs generated narrative; if generated: model + prompt):
  N/A. No profile is rendered.
- **D.3 Assignment & weighting** — number of personas, assignment to conditions (your responsibility, all 17 conditions), reuse, weighting/matching:
  N/A. No persona, no assignment, no weighting.

## E · Stimulus and survey administration
- **E.1 Stimulus presentation** — verbatim vs paraphrase; how state-contingent content is handled:
  **Verbatim.** The 16 intervention texts are read from the benchmark's own `survey/` directory and
  placed in the prompt unmodified. **We measured why this matters.** On Voelkel, sending a one-line
  paraphrase of each treatment scored +0.2720 and sending the real OSF text scored +0.3101
  (difference +0.0381, t = +0.47, p = 0.6735, n = 4 — not significant, but the paraphrase run could
  not produce a single negative prediction across all 40 arms, and the real-text run could). See
  `docs/EVIDENCE.md` section 9.
  **State-contingent content.** `Extreme weather predictions` is the only state-adaptive arm of the
  16. The benchmark's file for it is a kit for the survey programmer, not one message: its own first
  line says that each participant sees only ONE version, and says not to feed the whole block
  verbatim. The raw block is 11,435 characters and holds authoring scaffolding, a list of 51 states,
  the state-to-case map, all four case texts, and a reference list marked
  "[not displayed to participants]".
  **The first pass sent the whole block, and that was a measurement error.** The 16 arm texts then
  came to 47,032 characters, and this one arm was 24.5 per cent of them. Most of it was instruction
  to the programmer that no participant ever read.
  **We now send what one participant read.** A direct forecast has no respondent and therefore no
  state, so `forecast/extract_materials.py::reduce_state_adaptive` renders the **modal**
  participant: one intro paragraph, then **Case 1**, the flood text, which covers 27 states and the
  District of Columbia — the largest share of the sample. One added line says the message was
  tailored to the reader's home state, and that other readers got a wildfire text or a
  cold-and-snow text. The extracted stimulus file
  `forecast/materials/stimuli/extreme_weather_predictions.txt` is now **2,213 bytes, 9 lines**, or
  5.9 per cent of the 37,722 characters of arm text. The reduction is documented in the comment
  block above `reduce_state_adaptive`, and in `docs/METHOD.md` section 3.4. **Both variants were run
  again after the reduction**; every submitted value comes from a run after it. The 15 other arms
  are sent verbatim and unmodified.
- **E.2 Survey walk-through** — one item/call vs blocks vs whole survey; context carry-over; item/option ordering & randomization; scale display; attention/comprehension handling:
  **One call for each OUTCOME, holding all 16 interventions.** 13 calls make one full draw; 8 draws
  make 104 calls. There is no respondent walking through a survey, so there is no context
  carry-over: each call is stateless.
  **The `OUTCOME` section prints every item of that outcome verbatim, with its scale and BOTH
  anchor labels**, re-pointed so a higher number always means more of the thing the outcome names.
  For a composite outcome it prints all of its items and says that the outcome is their mean.
  **The `ESTIMAND` section states the study's own preregistered analysis**, not a generic one: an
  OLS fit of the post-treatment outcome on condition dummies with control as the omitted reference
  and gender, age and race as covariates, heteroskedasticity-robust standard errors, and a
  Benjamini-Hochberg false-discovery-rate correction **inside** each outcome. `newsletter_signup` is
  described instead as a logistic regression reported as the average difference in predicted
  probability. **The `ASK` section names the units of THAT outcome**, so `donation_ams` is asked in
  dollars on a 0-10 scale and `newsletter_signup` in a change of a 0-1 rate, not in "points of the
  0-100 scale".
  **Randomization.** The 16 interventions are shown in a **new random order in every draw**, drawn
  from `random.Random(seed)`. The order is written into every record as `arm_order`, so position
  bias can be measured afterwards rather than assumed. Item order inside an outcome is codebook
  order and is not randomised.
  **Attention and comprehension items are not forecast.** The benchmark does not score them.
- **E.3 Response elicitation** — free text / constrained choice / structured output / token log-probabilities (if logprobs: normalization & mapping):
  **Free text, then a strict parse.** The model is asked to write exactly n lines of the form
  `<position>: <number>` and nothing else. No JSON mode, no grammar, no constrained decoding, and
  **no log-probabilities**. The parser is described in G.2.

## F · Stochasticity and aggregation
- **F.1 Runs & seeds** — runs per respondent/item/estimate; seeds; reproducibility under identical settings:
  **8 draws for each of the 13 outcomes.** Base seed `1`; the seed sent to the engine is
  `1 + draw index`, so the 8 draws are genuinely different. The arm order of each draw comes from
  `random.Random(1)`, so the 8 orders rebuild byte for byte.
  **Reproducibility.** Every prompt rebuilds exactly from the deposited inputs. The generations
  themselves are sampled, so an identical rerun on identical hardware reproduces them only up to the
  engine's own batching non-determinism. All raw generations are deposited (K.2), so no result
  depends on a rerun.
  Confirmed by the submitted run: `samples 8`, `seed 1`, `seed_rule "seed + sample index"`,
  `framings 1`, `calls 104` (`forecast/runs/2026-08-30_B_pop_on_v2/forecast.meta.json`).
- **F.2 Aggregation rule** — how multiple generations become submitted values (mean/median/mode/first/sampled/…):
  **The unweighted arithmetic mean over the draws that parsed**, computed for each (intervention,
  outcome) pair, by `structured_forecast.py::write_predictions`. No median, no trimming, no
  weighting, no outlier removal. A draw that did not parse for an arm is not counted and is not
  replaced, so different arms may rest on different numbers of draws. The realised count for every
  arm is recoverable from the deposited `forecast.jsonl`.

## G · Validation & post-processing
- **G.1 Human validation** — any human review of outputs (often N/A):
  **No human read, reviewed, edited or selected any forecast value.** Human review was limited to
  the code and to the aggregate reports.
  One exception is worth naming, because it changed the method and not a value: a human read the
  model's **thinking trace** on a public study and found the sign-convention bug described in G.2.
  No output value was altered by that reading; the code was fixed and every affected run was
  re-generated from the start.
- **G.2 Post-processing** — parsing rules; handling of refusals/malformed/missing/out-of-range; exclusions; for approaches that generate individual responses, the resulting effective N per condition (descriptive disclosure, not a scoring input):
  **Parsing.** `structured_forecast.py::parse_listwise` reads `<position>: <number>` lines. It
  accepts `:`, `)`, `]` and `. ` as separators, accepts `,` as a decimal separator, tolerates up to
  12 leading letters (`Message 3: -1.2`), tolerates a missing line, an extra line, and a position
  outside the range. On a repeated position the **first** answer wins. It never assumes the model
  kept the order asked: the position in the reply is mapped back through the recorded `arm_order`.
  **Out of range.** A value outside `[-100, +100]` is dropped.
  **Fallback.** If no labelled line is found and the reply holds exactly n bare in-range numbers,
  they are mapped in the order they appear and the record is stamped
  `parse_mode = "bare numbers, in order"`, so the fallback can be removed from any analysis.
  **Nothing is repaired, imputed, re-asked or interpolated.** No arm is excluded from the submission:
  full coverage is mandatory, and the mean over the surviving draws is submitted.
  **Effective N: not applicable.** This entry generates no individual responses. The analogous
  figure is the number of parsed draws behind each of the 208 values.
  **The sign convention, and the bug that was found in it.** The prompt is always written with
  `100 = the named high end of the scale`, and the number is flipped afterwards where the archive's
  truth points the other way (`structured_forecast.py:1185`, the same operation as
  `codeocean/extracted/code/load_archive1_results.R:104`). An earlier prompt did **not** flip, and
  half of the Broockman cells were scored with the sign reversed. Fixing it moved the score from
  **-0.1355 to +0.1215** (difference +0.2570, t = +2.03, p = 0.0494). The bug never touched a
  submitted value: it was found and fixed on public data, on 2026-08-30, before this entry was
  generated. Full account: `docs/EVIDENCE.md` section 6.
  **Measured on the submitted run: 1,648 of 1,664 arms parsed. Parse rate 99.0 per cent.**
  **Exactly one call of the 104 failed**: the `donation_ams` outcome, draw 4. The model answered
  with prose reasoning and never wrote the 16 required lines, so no labelled line was found and the
  whole call was dropped. The record is in
  `forecast/runs/2026-08-30_B_pop_on_v2/forecast.jsonl` with `parse_mode: unparsed`, `n_parsed 0`,
  and the first 400 characters of the raw reply. **That one failure is the whole of the 16 missing
  arm-answers.** The 16 `donation_ams` cells therefore rest on **7** draws and the other 192 cells
  rest on **8** — minimum 7, maximum 8, mean 7.92
  (`forecast/runs/2026-08-30_B_pop_on_v2/forecast.meta.json` and
  `forecast/runs/2026-08-30_B_pop_on_v2/AUDIT.txt`). The control variant A lost two calls the same
  way, `donation_ams` and `newsletter_signup`, both draw 4: 1,632 of 1,664 arms, 98.1 per cent, mean
  7.85 draws. No cell was filled, no cell was dropped, and no draw was re-asked.
  **The direction rule for this study.** Every prompt is written on the same scale the submission
  uses, so `scale_flip` is `False` for all 13 outcomes and no number is turned. The flag is still
  computed and written into every record, so the claim is auditable and not merely asserted.
  `funding_perceptions` is the case that needs care: the submission defines it as `100 - funding_5`,
  so the prompt prints that item **with its anchors already swapped**, and a positive effect means
  more support for climate research funding.
  **The audit `make check` cannot make.** `forecast/build_predictions.py` prints three checks that
  the organizers' validator does not: the units of `newsletter_signup` (largest |ate| 0.0288, a
  plausible proportion), the units of `donation_ams` (largest |ate| 0.400 dollars on a 0-10 scale),
  and the sign agreement between `trust_post` and `distrust_post` (15 of 16 texts disagree in sign,
  as a trust-building text should; `Social justice` is the one that does not, unchanged from the
  first pass). Source: `forecast/runs/2026-08-30_B_pop_on_v2/AUDIT.txt`.
  **The submitted values, from `predictions/team_27_T3_primary_v1.csv`:** 208 rows, no missing
  value, `ate` from **-5.100 to +4.975**, mean **+1.289**. 27 of the 208 values are negative, 25 of
  them among the 176 slider values. `newsletter_signup` runs from -0.0029 to +0.0288, a change of a
  0-1 proportion. `donation_ams` runs from -0.0640 to +0.4000 dollars.
- **G.3 Calibration corrections** — any post-hoc scaling/shifting/debiasing and exactly what data it was fit on (cross-ref H/I):
  **None.** No scaling, no shifting, no debiasing, no clamping, no rounding beyond the decimal
  precision of the CSV, and no reweighting. The submitted `ate` values are the means of parsed model
  generations.
  A calibration shrink **was preregistered** (`notes/PREREG_broockman_method_search.md` section 8:
  an OLS fit on three donor studies with Broockman excluded, validated leave-one-study-out). **It
  was never fitted and it is not applied.** It is a monotone linear map, so it could not have
  changed a Pearson correlation or any ranking in any case; it would change only the calibration
  slope and the RMSE. No human outcome data, from this study or any other, was used to adjust any
  submitted value.

## H · Learning and conditioning components
- **H.1 Fine-tuning data** — exact corpus (hashes/DOIs), hyperparameters, checkpoints:
  N/A — no fine-tuning. The published weights are used as they are.
- **H.2 Context & retrieval corpora** — exact document set in context / indexed, archived in the deposit:
  **No retrieval and no index.** The entire context of every call is the prompt described in C.1,
  built from two sources, both of which are benchmark materials shipped in this repository:
  1. `survey/` — the 16 intervention texts, verbatim.
  2. `codebook.csv` and `scripts/lib/submission_spec.R` — the 13 outcomes, their items, their
     scales and their anchor labels.
  3. `forecast/materials/quotas_18000.csv` — the benchmark preregistration's recruitment-quota
     table, projected to N = 18,000. It is a **design** document: it says who was to be recruited,
     and it holds no outcome of any kind.
  Nothing else is ever placed in context. No paper, no prior result, no effect size, and no example
  of any study's outcome.

## I · Data inputs, blinding, and competing interests
- **I.1 Competing interests ★** — funding, in-kind compute/model access, relationships with LLM-interested entities:
  **`PENDING (team declaration)`. This item is NOT filled in.** It needs a person, not a run, and
  **only the members named in 0.1 can complete and sign it.** It must be done before the prediction
  lock on 2026-08-31.
  Facts known to the pipeline: the submission model is open weights, downloaded publicly and run on
  the team's own hardware; no compute, credits or model access were granted by any model provider
  for this benchmark; the hosted models used for method selection were paid for out of pocket
  through OpenRouter, at the measured cost in K.3. Institutional affiliations are the Joint Research
  Centre of the European Commission and the University of Konstanz. Any funding source and any
  relationship with an entity with an interest in language-model performance must be listed here by
  the team.
- **I.2 External human data †** — all external human datasets that informed the approach anywhere (training/fine-tuning/retrieval/ICL/calibration):
  **Two. Neither contains any outcome of the target study, and neither is ever placed in context.**
  1. **Broockman et al., 42 cells, 172 arms, 61,869 people.** Our **development set**. It was used to
     compare listwise against pointwise, to sweep temperature, to test the demographic block, and to
     test the framing ensemble. Read from the Ashokkumar et al. (2026) Code Ocean capsule 9843791,
     via `ashokkumar_bench/data/megastudies/`.
  2. **Voelkel et al. (2025), 4 cells, 40 arms, 13,821 public individual responses.** Our
     **confirmation set**. Treatment texts from the study's own OSF materials, doi
     `10.17605/OSF.IO/2MCF8`. It is a different study, on climate attitudes, with no measure of
     trust in climate scientists.
  A third artifact informed the **method** but is not human data: the Ashokkumar capsule's own R
  code, which fixes the sign convention we follow (`load_archive1_results.R:104`) and supplies the
  published gpt-4 and human-expert reference correlations we compare against.
  **No outcome data from the target study, or from any pilot of it, informed any part of this
  entry.**
- **I.3 Blinding attestation ★** — **mandatory.** Signed attestation that no team member accessed, solicited, or was shown any human outcome data from this study, including pilots, before the prediction lock:
  **`PENDING (team signature)`. This attestation is NOT signed.** It needs a person, not a run.
  **The members named in 0.1 must sign it, with a date**, before the prediction lock on 2026-08-31.
  Nobody signed it on the team's behalf.
  Prepared text, to be signed: *"We attest that no member of team_27 accessed, solicited, or was
  shown any human outcome data from the target megastudy, including any pilot of it, at any time
  before the prediction lock."*
  Supporting facts for the signatories: we have never sought, accepted, or looked at any human
  outcome data from the target study; the pipeline reads only the files listed in H.2, all of which
  are benchmark materials that contain no outcome data; the population block in the prompt is the
  benchmark's own **recruitment target** table, which is a design document and holds no outcome; the
  submission model is local, so no network request of any kind is made during generation; and
  `blinding_attestation` in `metadata.json` is `true`.
- **I.4 Contamination note †** — training cutoff of every model vs public release dates of this project's materials; note any known exposure:
  `Qwen/Qwen3.8-27B` publishes no exact training cutoff at the precision this item asks for. The
  same is true of the two hosted models used for selection.
  **The exposure risk we can name.** The benchmark's own materials — the call for participation, the
  preregistration and the survey instrument — are public web pages, so a model with a later cutoff
  may have seen the **design**, including the 16 intervention texts and the outcome items. That is
  not an advantage on the outcomes, which do not exist publicly: the parent megastudy's results are
  unpublished and the human data is sealed. The stimulus texts adapt previously published material,
  so the model may have seen the source articles.
  **A measured contamination event on a PUBLIC study, and what we did about it.** The first version
  of our prompt held a `Study description:` block naming the study and its authors. The model
  answered it by recall: it wrote *"this is a reference to the study by Broockman and Kalla
  (2016)"* (measured 2026-08-29). **The block was removed before any configuration was scored**, and
  the removal is recorded in `notes/PREREG_broockman_method_search.md` section 7b with its date.
  The submitted prompt therefore **never names the target study, its authors, or the benchmark**.
  This is a guard, and it is also a selection safeguard: a method tuned on recall of a published
  result cannot transfer to an unpublished study, so keeping the block would have let us select a
  skill that does not exist on the target.
  **What we did NOT do.** `structured_forecast.py` has a `--contamination-check` mode with two
  probes — author identification and free recall. **It was never run.** No `CONTAMINATION.txt` exists
  in any run directory. We report the qualitative recall event above and rely on the removal of the
  naming block; we did not quantify recall rates.
- **I.5** — not an item of this form.

## J · Internal selection procedure
- **J.1 Design-space search †** — how the final pipeline was chosen: how many configurations tried, internal validation criterion, what data it ran against:
  > **EVERY RESULT IN THIS ITEM IS EXPLORATORY.** Our own preregistration was breached in four
  > ways, so the confirmatory comparison it defined is void by its own terms. **Read the
  > declaration in J.2 first.** The measurements are real and reproducible; the inference is not
  > confirmatory.

  **The rules were fixed in writing before the first score**, in
  `notes/PREREG_broockman_method_search.md`, dated 2026-08-29. **They were then broken. See J.2.** That file names the development set
  (`broockman`), the confirmation set (`voelkel2025`), the primary endpoint (mean within-cell
  `r_raw` over the 42 Broockman cells), the test (a paired comparison over the same 42 cells), and
  the improvement threshold. It also states that the target megastudy is never used for selection.
  **How many configurations were scored: 34 runs, 32 of them in the indexed grid.** Every one is
  listed, winners and losers together, in `docs/EVIDENCE.md` section 11 and in
  `modelbench/output/tier3/index.csv`; the two population-block runs are in
  `modelbench/output/tier3/runs/` and are reported in `docs/EVIDENCE.md` section 5c.
  **The preregistration allowed six on Broockman. We scored 17 on Broockman. See J.2.** The grid is
  3 models x 2 modes x up to 5 temperatures x 2 public studies. A further 9 runs of the earlier
  pointwise-with-personas forecaster are reported in `docs/EVIDENCE.md` sections 5c, 5d, 6 and 9.

  **UPDATE 2026-08-31 — the count is now 74 scored configurations, not 34.** After the runs above,
  the search was extended: four more models, a third public archive (`doell`), a second seed for
  every local run, and a 12-run arm with the models' reasoning turned on. **Every run of the whole
  search is now deposited**, winners and losers together, in
  [`raw_data_deposit/method_search/`](raw_data_deposit/method_search/) — **80 run folders, 74 scored
  configurations and 6 smoke tests**, with an `INDEX.csv` and a sha256 for every file, 1.68 MB
  gzipped. The totals are 7 models, 3 public archives (broockman 34 runs, voelkel2025 34, doell 6),
  2 modes (listwise 68, pointwise 6) and 2 reasoning settings (off 62, on 12). **No value from any
  of them reaches the submitted predictions.** The extension does not change the entry: it scores
  the same pipeline on more data. **It does make the exploratory warning of J.2 stronger, not
  weaker** — more configurations were seen before this form was written, so the true false-positive
  rate of any p value in this item is higher again. The results are in `docs/EVIDENCE.md` section
  14. The added spend is in K.3.

  **UPDATE 2026-08-31 — the search was re-scored with the BENCHMARK's own Tier 3 metrics.** Every
  result above uses the within-cell correlation of Ashokkumar et al. The benchmark does not compute
  that. It pools every intervention x outcome pair and computes ATE recovery (directional
  agreement, Spearman rho, Pearson r, noise-corrected r) and the calibration regression (alpha,
  beta). `docs/EVIDENCE.md` section 14 recomputes the search with the preregistration's own
  formulas. **The conclusions of this item survive the change of metric.** This closes the open
  question of `docs/EVIDENCE.md` section 8.

  **What the search found — the factors that DID matter:**
  - **Listwise beats pointwise. THIS IS THE ONE FINDING THAT HELD EVERYWHERE.** Six paired tests on
    the within-cell metric, all the same sign; one at p = 0.0369. Re-scored on the benchmark's own
    pooled Pearson r, **listwise wins 6 of 6 comparisons** — 3 models x 2 archives, no exception —
    by a mean of **+0.113 on Broockman and +0.071 on Voelkel**. On Broockman it wins EVERY Tier 3
    metric for all three models. Two honest limits: on Voelkel pointwise has the better RMSE in all
    three comparisons and the better Spearman rho in two of three, so listwise improves the LINEAR
    agreement and not the ORDERING. `docs/EVIDENCE.md` section 14.1.
    **This is why the entry is listwise.** It is the only factor of the search whose direction was
    the same for every model and every archive tested. A model ranking was not: `Gemma4-26B` is
    first on Voelkel and next to last on Doell.
  - **The direct forecast beats our own per-respondent simulation** on the same 42 cells:
    +0.4091 against +0.1917, paired t = +2.82, **p = 0.0073**, better in 30 of 42 cells. This is the
    only comparison in the project that reached p < 0.05.
    **EXPLORATORY.** This result was selected after seeing 34 runs. **Its true false-positive rate
    is higher than 0.0073.** It is not a confirmatory result and must not be read as one. The
    preregistered test was a paired bootstrap with a 0.14 minimum difference, and it was never run
    (J.2, breach 3).
  - **Sending the real stimulus text beats sending a paraphrase** (+0.3101 against +0.2720, not
    significant with 4 cells, but the paraphrase run could not produce a negative prediction at all).
  - **A sign-convention bug is worth 0.26 in r.** Fixing it moved the score from -0.1355 to +0.1215.
  **What the search found — the factors that did NOT matter.** These are given equal weight, because
  a null is a result:
  - **Model choice.** 1 of 8 paired tests significant, and that one is the weakest run in the grid.
    The sign reverses across temperatures.
  - **Temperature.** **0 of 46** paired tests significant. Smallest p = 0.0543.
  - **A demographic / population block.** Four tests, none significant. Three used the OLD
    pointwise prompt: +0.0592 (p = 0.5151), -0.1235 (p = 0.6395), -0.1678 (p = 0.1440). The fourth
    used the NEW structured listwise template that this entry actually uses, and is therefore the
    one that counts: **Broockman -0.0029 (p = 0.8671), Voelkel +0.0024 (p = 0.3910)**
    (`modelbench/output/tier3/runs/2026-08-30_Qwen3.8-27B-local_*_listwise_t085_pop/RESULTS.txt`
    against the same runs without `_pop`). The block does not help and it does not hurt.
    **It is in the submitted prompt anyway**, for consistency with `team_27`'s Tier 1 entry, which
    describes the same population from the same quota file. That is a consistency choice, not a
    performance claim. The control run without the block is deposited in `raw_data_deposit/`.
  - **A framing-sentence ensemble.** 0 of 45 pairwise tests significant on Broockman and 6 of 45 on
    Voelkel, but the two studies rank the 10 sentences at Pearson -0.2698 (p = 0.4509) and Spearman
    -0.0909 (p = 0.8028). Choosing a winner would be choosing noise.
  **Why `Qwen/Qwen3.8-27B` on local weights is the submission model, when a hosted model scored
  higher.** `qwen/qwen3.8-flash` scored +0.4400 on Broockman against the local model's +0.3398. We
  did not pick it, for three stated reasons:
  1. **The difference is not significant.** Five of the eight model-choice tests give p > 0.2, and
     the one significant test is the 2-draw temperature-0 run whose parse rate was 95.6 per cent.
     The sign even reverses at temperature 1.0.
  2. **The same weights served two ways give the same score** (three tests, all p > 0.24), so the
     local route costs nothing in accuracy.
  3. **A local run is reproducible by anyone at $0.00 and makes no network request**, which is worth
     more to this benchmark than an unproven 0.10 in a correlation over 42 cells.
  **What we could NOT decide, and did not pretend to.** The three scoring metrics do not rank the
  runs the same way. On mean within-cell r the hosted flash run at temperature 0.5 is best; on
  pooled r over all 172 arms the local 27b run at temperature 1.0 is best. Tier 3 scores 208 rows
  together, which is structurally a pooled correlation, but pooled r on Broockman also rewards
  knowing which policy **issue** moves most — a skill that does not transfer to a one-topic study.
  **This is an open question and we flag it rather than resolve it.** See `docs/EVIDENCE.md`
  section 8.
  **What we have NOT beaten.** On Voelkel — the study that most resembles the target — our best run
  in the whole grid scores **+0.6600** against published gpt-4's **+0.7454**. We are 0.085 below.
  The submitted configuration itself — local `Qwen/Qwen3.8-27B`, listwise, t = 0.85, population
  block on — scores **+0.6509** on Voelkel
  (`modelbench/output/tier3/runs/2026-08-30_Qwen3.8-27B-local_voelkel2025_listwise_t085_pop/RESULTS.txt`),
  which is 0.095 below gpt-4. We report this and do not explain it away. We did not test whether the
  gap is significant; with 4 cells we could not.
- **J.2 Selection blinding †** — confirm no selection used outcome data from this study:
  **Confirmed, for the target study.** No model, prompt, mode, temperature, ensemble size or
  parsing rule was chosen using any outcome data from the target study, or from any pilot of it.
  Every selection used the two public studies named in I.2. That part of the blinding holds without
  qualification.
  We disclose, as the form requires, that selection **did** use visible human outcome data — from
  `broockman` and `voelkel2025`. Both are public, neither is the target, and both are named above.

  ### **DECLARATION: our own preregistration was breached in four ways. Read this before any p value in this form.**

  `notes/PREREG_broockman_method_search.md` was written on 2026-08-29, before any configuration was
  scored. It fixed the development set, the held-out set, the endpoint, the test and the number of
  configurations. **The work that followed broke four of its own rules.** We declare all four. We do
  not soften them.

  | # | The rule, and where it is written | What we actually did |
  |---|---|---|
  | 1 | **"AT MOST SIX configurations may be scored on Broockman... A seventh configuration voids the comparison."** PREREG lines 77-78. | **We scored far more than six.** `modelbench/output/tier3/runs/` holds **34 run directories**, 17 of them on Broockman; `modelbench/output/tier3/index.csv` indexes 32 of them, 16 on Broockman. By the rule's own words, the comparison is void. |
  | 2 | **The held-out set `voelkel2025` "is scored ONE TIME, at the end, on the single winning configuration."** PREREG lines 26-27. | **We scored it 17 times**, on 17 configurations (`modelbench/output/tier3/runs/*voelkel2025*`). It was used as a second development set, not as a held-out set. It is not held out any more. |
  | 3 | **The test is a PAIRED BOOTSTRAP: 10,000 resamples of the 42 cell indices, a 95 per cent percentile interval, and a minimum mean difference of 0.14.** PREREG lines 55-60 and the threshold that follows them. | **We report a paired t-test** (`modelbench/tier3_tests.py:63`, `scipy.stats.ttest_rel`). **No bootstrap interval exists on disk** for any Tier 3 comparison. The preregistered decision rule was never applied, so no configuration was ever formally accepted or rejected by it. |
  | 4 | **Configuration 1, `baseline_seed2`, is the abandonment check.** PREREG section 7 row 1 and section 10: if a second seed of the baseline moves the score by more than 0.14, the noise floor is larger than the effect, and the search stops. | **It was never run.** No `baseline_seed2` run directory exists. **We never measured our own noise floor**, so we cannot say how much of any difference below 0.14 is noise. |

  **The consequence, stated plainly. The preregistered confirmatory comparison is void by its own
  terms.** Every result in `docs/EVIDENCE.md` and in J.1 must be read as **EXPLORATORY**. The
  headline — the direct forecast against our own simulation, +0.2174, t = +2.82, **p = 0.0073** —
  was selected after seeing 34 runs. **Its true false-positive rate is higher than 0.0073.** How
  much higher we cannot say, because the number of comparisons we could have made is not fixed in
  advance. It is **not** a confirmatory result and it must not be presented as one.

  **What is NOT in doubt.** The measurements themselves are real, reproducible and unfabricated.
  Every run directory holds its own prompts, its own raw generations, its own seed and its own
  score. `modelbench/output/tier3/index.csv` lists every run, the losers with the winners. Nothing
  was dropped, re-run to a better number, or reported selectively. **The problem is the inference,
  not the data.**

  **This needs a human decision before the prediction lock**, by the members named in 0.1: whether
  to keep the entry as it is with this declaration attached, or to re-run the preregistered test as
  written. We recommend keeping it with the declaration, because the submitted forecast does not
  depend on the significance test — it depends on the listwise design, which is supported by six
  paired tests all of one sign.

## K · Reproducibility & frozen artifacts
- **K.1 Code & materials** — link/DOI, secrets removed, determinism/seeds documented (also record the link in `metadata.json` → `code_repository` / `code_doi`):
  **What is in this deposit:** the submitted prediction file, its build contract
  (`predictions/SPEC_NOTES.md`), the method in reimplementable detail
  ([`docs/METHOD.md`](docs/METHOD.md)), and every measurement that shaped it
  ([`docs/EVIDENCE.md`](docs/EVIDENCE.md)).
  **The pipeline that produced the submitted values IS in this deposit**, in `forecast/`. It is
  self-contained: it reads only `survey/questionnaire.txt`, `codebook.csv` and
  `scripts/lib/submission_spec.R` of this repository, plus one copied quota file. It makes no
  network call and no paid call. `forecast/PROVENANCE.json` records, for every file, where it was
  copied from, its source SHA-256, what was kept and what was removed.
  `forecast/core.py` and `forecast/run_vllm.py` are adapted copies of
  `modelbench/structured_forecast.py` and `modelbench/structured_forecast_vllm.py`. **One change was
  made to `render`:** the source always asks for "points of the 0-100 scale", but 2 of the 13
  outcomes of this study are not on that scale (`donation_ams` is 0-10 dollars, `newsletter_signup`
  is a rate). The study spec now supplies three more slot functions — `ask_units`, `scale_top` and
  `scale_bottom` — whose default values make the rendered text byte for byte identical to the
  source. `forecast/tests/test_render_parity.py` proves that identity.
  **What is deliberately NOT in this deposit:** the working project `modelbench`, which holds the
  original `structured_forecast.py` and `structured_forecast_vllm.py`, plus `tier3_index.py`,
  `tier3_tests.py`, the Ashokkumar archive loader, the scorer, the OpenRouter transport and all 41
  measurement runs. Those ran against **public** archives only, and this repository has no ground
  truth to score against. No value they produced enters a prediction. `docs/EVIDENCE.md` carries
  their conclusions.
  **No secrets, no credentials and no API keys** are stored in this repository; the submission model
  is local and needs none.
  **Determinism:** base seed `1`; the engine seed is `1 + draw index`; the arm orders come from
  `random.Random(1)` and rebuild byte for byte; every prompt rebuilds byte for byte from the
  benchmark materials in `survey/` and `codebook.csv`.
  **Code repository:** `https://github.com/AndresLaverdeMarin/silicon-sample-submission-tier3`,
  recorded in `metadata.json`, field `code_repository`.
  **`code_doi`: `PENDING (Zenodo deposit)`.** `metadata.json` holds `null` for `code_doi` and for
  `zenodo_doi`. **The members named in 0.1 must set both after the Zenodo release**, and before the
  prediction lock on 2026-08-31. Nobody else can: the deposit is made from the team's own account.
- **K.2 Raw output logs †** — complete unprocessed model responses archived, hashed, time-stamped (required for Tiers 1–2, public or escrowed; Tier 3 where intermediate generations exist; oversized logs may be a separate linked Zenodo upload):
  **Public, not escrowed. Intermediate generations DO exist for this entry**, so this item applies.
  The final run's `forecast.jsonl` holds one record for each call: the study, the outcome, the draw
  index, the seed, the arm order, the parse mode, and every value both **before** and **after** the
  sign flip. Where parsing was not complete, the record also holds the first 400 characters of the
  raw reply.
  **Deposited in this repository.** The run directory
  `forecast/runs/2026-08-30_B_pop_on_v2/` holds the raw log of the submitted run.
  `forecast/runs/2026-08-30_A_pop_off_v2/` holds the raw log of the control.

  | File | Records | Bytes | SHA-256 |
  |---|---|---|---|
  | `forecast/runs/2026-08-31_B_pop_on_t050_uv/forecast.jsonl` — **the submitted run** | 104 | 402,742 | `8a9e664f2c50a45b241f02c24d41f54996183dd1b01e5159667f3bdc8ce41ccd` |
  | `forecast/runs/2026-08-31_B_pop_on_t050_uv/forecast.meta.json` | — | 4,869 | `2646435bef424f7dfc57bb23ead444396dcba493ac91ccedcb4d0c171b78fdc8` |
  | `forecast/runs/2026-08-31_B_pop_on_t050_uv/AUDIT.txt` | — | 2,139 | `c24662fc2ec5d79039bdf52a891da91c961c59480c85f67d03c71a1f4dbd5d38` |
  | `forecast/runs/2026-08-31_A_pop_off_t050_uv/forecast.jsonl` — the control | 104 | 402,830 | `b121f11d2b9ac776fcf00b864ac56cd276a99e649e4c7ad26f99ecf1077c6243` |
  | `forecast/runs/2026-08-31_A_pop_off_t050_uv/forecast.meta.json` | — | 4,870 | `9cbbdee616dc747b79a59de0921bfb074504e7a7151a4def2b4ed16d2c683eaa` |
  | `forecast/runs/2026-08-31_A_pop_off_t050_uv/AUDIT.txt` | — | 2,140 | `0fa9e67e2b389149373d87a0310f873f3a9f077390722e1b6fcd72f7d40422e9` |
  | `raw_data_deposit/variantA_pop_off_t050_uv_T3_ate.csv` — the control's 208 rows | 208 | 8,785 | `cfe90bc70d113f803578b8be45d8fce4ec4a60d3c9899dc8164e233fbc28b858` |
  | `predictions/team_27_T3_primary_v1.csv` — **the submitted values** | 208 | 8,785 | `f9cc1057b8026b66ad0b90d64ab7545877e6e5b90b68096ea9e5c7101e4534a0` |

  **UPDATED 2026-08-31 for the uv-produced temperature-0.5 pair.** The whole pipeline, including
  the model run, now runs inside the repository's own `uv` environment (`pyproject.toml`,
  `uv.lock`, extra `gpu`). The superseded runs stay on disk and no submitted value comes from any
  of them: `forecast/runs/2026-08-30_*_v2/` (temperature 0.85) and
  `forecast/runs/2026-08-31_*_t050/` (temperature 0.5, run before the uv environment existed).

  Every size and hash was read from the file, not copied from a record. The prediction file's hash
  is also in `metadata.json`, field `prediction_files`, written by `make manifest` and checked by
  `make check`.

  **CLOSED 2026-08-31 — `raw_data_deposit/` no longer holds the superseded first pass.** Its six
  stale files (`forecast_primary_B_pop_on.jsonl`, `forecast_variantA_pop_off.jsonl`,
  `forecast.meta.json`, `AUDIT_primary_B_pop_on.txt`, `AUDIT_variantA_pop_off.txt` and
  `COMPARE_A_vs_B.txt`) are **removed**. The folder now holds the pair that produced the submitted
  values and nothing from an earlier pass: `forecast_B_pop_on_t050_uv.jsonl`,
  `forecast_A_pop_off_t050_uv.jsonl`, their two `.meta.json` files,
  `AUDIT_B_pop_on_t050_uv.txt`, `AUDIT_A_pop_off_t050_uv.txt`, `COMPARE_A_vs_B_t050_uv.txt`, and
  `variantA_pop_off_t050_uv_T3_ate.csv` — the control's 208 rows, for comparison only and **not**
  submitted. It also holds `method_search/`, the whole method search (item J.1). The table above
  names every file with its size and sha256.

  **Why the control is deposited and not submitted.** `scripts/lib/check_lib.R` lines 119-124: one
  repository holds one entry. Variant A is the control condition of the population-block test.
- **K.3 Computational resources** — API-call counts, total tokens, cost, compute time:
  **The submitted values cost $0.00 and made 0 API calls.** The model runs on the team's own H100
  80GB, on local weights, with `HF_HUB_OFFLINE=1`.

  **UPDATED 2026-08-31.** The submitted run is now the temperature-0.5 pair. The superseded
  temperature-0.85 pair is in the second table below, kept as a record.

  | Quantity | **Submitted run `2026-08-31_B_pop_on_t050_uv`** | Control variant `2026-08-31_A_pop_off_t050_uv` |
  |---|---|---|
  | temperature | **0.5** | 0.5 |
  | API calls | **0** | 0 |
  | monetary cost | **$0.00** | $0.00 |
  | model calls (13 outcomes x 8 draws) | **104** | 104 |
  | arms asked / arms parsed | **1,664 / 1,664** (100.0 per cent) | 1,664 / 1,664 (100.0 per cent) |
  | draws behind each of the 208 cells | **min 8, max 8, mean 8.00** | min 8, max 8, mean 8.00 |
  | mean prompt size | **43,292.3 characters** | 42,628.3 characters |
  | longest prompt | **44,401 characters** | 43,737 characters |
  | `max_model_len` | **16,080** | 15,859 |
  | wall clock, generation | **110.9 s** (1.8 minutes) | 106.7 s (1.8 minutes) |
  | call-date window | **2026-08-31T13:41:39Z to 13:43:30Z** | 2026-08-31T13:44:21Z to 13:46:08Z |

  The prompt sizes and `max_model_len` are unchanged from the superseded pair, because only the
  temperature changed. **The two temperatures agree at Pearson r = +0.9803 over the 208 submitted
  cells**, mean absolute difference 0.2371, and the same sign in 207 of 208. The control agrees with
  the submitted run at **Pearson r = +0.9941** (`raw_data_deposit/COMPARE_A_vs_B_t050_uv.txt`), against
  +0.9873 for the superseded pair. **The token counts of the new pair were not recounted**; the
  prompts are byte for byte the prompts of the superseded pair, so the input-token figures below
  carry over unchanged.

  **SUPERSEDED — the temperature-0.85 pair.** No submitted value comes from it.

  | Quantity | Superseded run `2026-08-30_B_pop_on_v2` | Its control `2026-08-30_A_pop_off_v2` |
  |---|---|---|
  | temperature | 0.85 | 0.85 |
  | API calls | 0 | 0 |
  | monetary cost | $0.00 | $0.00 |
  | model calls (13 outcomes x 8 draws) | 104 | 104 |
  | arms asked / arms parsed | 1,664 / 1,648 (99.0 per cent) | 1,664 / 1,632 (98.1 per cent) |
  | draws behind each of the 208 cells | min 7, max 8, mean 7.92 | min 7, max 8, mean 7.85 |
  | mean prompt size | 43,292.3 characters | 42,628.3 characters |
  | longest prompt | 44,401 characters | 43,737 characters |
  | `max_model_len` | 16,080 | 15,859 |
  | **input tokens, total** | **1,026,832** | 999,168 |
  | input tokens, mean for each call | **9,873.4** (min 9,737, max 10,154) | 9,607.4 (min 9,471, max 9,888) |
  | output tokens, total | about 12,300 (an estimate) | about 12,300 (an estimate) |
  | wall clock, generation | 122.4 s (2.0 minutes) | 119.1 s (2.0 minutes) |
  | call-date window | 2026-08-30T16:48:09Z to 16:50:11Z | 2026-08-30T16:51:13Z to 16:53:12Z |

  The call counts, prompt sizes, wall clock and windows are copied from
  `forecast/runs/2026-08-30_B_pop_on_v2/forecast.meta.json`,
  `forecast/runs/2026-08-30_A_pop_off_v2/forecast.meta.json` and the `AUDIT.txt` in each of those
  two directories.

  **How the token counts were made.** `forecast.meta.json` records characters, not tokens. The 104
  prompts were rebuilt from the deposited materials with `forecast/core.py::render` under the same
  seed, wrapped in the model's own chat template with `enable_thinking=False`, and counted with the
  `Qwen/Qwen3.8-27B` tokenizer. The rebuild reproduces the recorded `mean_prompt_chars` of 43,292.3
  and `longest_prompt_chars` of 44,401 exactly, which is the check that the counted prompts are the
  prompts that ran. The measured rate is **4.39 characters for each token**, not the 3.79 that
  `forecast/run_vllm.py` uses for its pre-run estimate; the estimate is therefore conservative.
  **The output tokens are an estimate, not a record.** The raw replies are not kept for a call that
  parsed completely, so they cannot be counted. The reply format did not change between the first
  pass and the rerun: 16 lines of `<position>: <number>`. On the first pass, vLLM's own throughput
  line at the end of `forecast/runs_B.log` reported 9,596.16 input tokens/s and 93.09 output
  tokens/s, which gives about 118 output tokens for each call and about **12,300** in total. The
  hard ceiling set by `max_tokens` is 40 x 16 + 128 = 768 for each call, so 79,872 in total.

  Estimated before the run, by `structured_forecast.py --print-prompts` on the 16 real intervention
  texts: one listwise prompt is about 51,210 characters, about 10,451 tokens; 104 calls; the same
  work on the hosted flash route would have cost about $0.174.
  **Cost of the method search, outside the submission.** Measured by summing `spend_usd` over every
  `*.meta.json` under `modelbench/output`: **$4.0108** in OpenRouter charges. 57 files hold a
  `spend_usd` field and **46 of them are non-zero**: 24 paid runs of the 32-run Tier 3 grid, 14
  probe runs, and 8 runs of the earlier forecaster. The 8 local runs of the grid cost $0.00. Of the
  total, **$0.6139** is the 32-run Tier 3 grid (`modelbench/output/tier3/index.csv`, column `spend`,
  which sums to the same figure) and **$2.2821** is the 2026-08-29 flash probe series
  (`modelbench/output/runs/2026-08-29_openrouter_flash_probe/`). No value from any paid call reaches
  the deposited answers.
  **This figure supersedes the $0.203, $2.40 and $3.45 recorded earlier in the project.** Those are
  stale: the grid grew after each was written. $4.0108 is the sum over the files as they now stand.
  Do not carry the older numbers forward.

  **UPDATE 2026-08-31 — the extended model comparison adds $1.6644.** The runs of
  `deepseek/deepseek-v4-flash`, `z-ai/glm-5.3-flash` and the hosted `qwen/qwen3.8-27b` reasoning arm
  cost **$1.6644** through OpenRouter, read by summing `spend_usd` over the 16 `forecast.meta.json`
  files of `raw_data_deposit/method_search/runs/openrouter_glm_deepseek/`. Of that, the two new
  models cost **$0.2507** together (all their runs, reasoning and smoke tests included) and the
  hosted `qwen/qwen3.8-27b` reasoning runs cost **$1.4137** — a reasoning run is expensive because
  the model writes its scratch work before its answer.
  **Cumulative paid spend is therefore $5.6752.** The 30 local runs added on the same date cost
  **$0.00**: they ran on the team's own H100 on local weights, made 0 API calls, and generated
  6,801,093 output tokens in 2.23 hours of engine time. **The declaration below applies to the
  new spend in the same way.** No value from any paid call reaches the deposited answers.

  **Compute of the extended comparison, for the record.** 30 local runs, 3 models, 3 archives, 2
  seeds, plus a 12-run reasoning arm. Reasoning is the whole cost: `Qwen/Qwen3.8-27B` at
  `reasoning_effort = xhigh` wrote 3,900,296 output tokens for 336 Broockman calls in 80.8 minutes,
  against 9,567 tokens in 0.64 minutes for the same calls with reasoning off — **408 times the
  output for a LOWER score** (`docs/EVIDENCE.md` section 14.3). Every run's token counts, wall clock
  and call window are in its own `forecast.meta.json` under
  `raw_data_deposit/method_search/`.

  **DECLARATION: the spend approval gap.** The project's own working rule, in `CLAUDE.md`, is: *"No
  paid LLM API calls without explicit approval from David"* (david.garciabecerra@gmail.com).
  **Cumulative paid spend is $5.6752 ($4.0108 to 2026-08-30, plus $1.6644 on 2026-08-31), and no
  approval from David is recorded anywhere on disk.**
  The runs were directed by the corresponding author in session. We do not claim that an approval
  exists, because we cannot point to one. **The members named in 0.1 must reconcile this before the
  prediction lock.** It affects no submitted value: the submitted values cost $0.00 and made 0 API
  calls, and no output of any paid call reaches `predictions/team_27_T3_primary_v1.csv`.
  **Local compute for the method search:** the 8 local vLLM runs in the Tier 3 grid took 29.7 to
  34.4 seconds of generation each on one H100, plus model load. The 27b local grid is therefore
  about 5 minutes of GPU time in total.

## L · Disclosure class
Each item above is deposited as **public**, **escrowed** (sealed from the public but available to the
core team and auditors under confidentiality, with a public SHA-256 hash + timestamp so the lock is
still verifiable — an embargo with a sunset date is encouraged), or **withheld** (permitted only for
items marked neither ★ nor †). Your entry's class is set by its **most restricted item** and recorded
in `metadata.json` → `disclosure_class` (and `escrow_doi` if anything is escrowed):
- **A · Open** — all items public. Full results-table standing; all features enter the design-choice analysis.
- **B · Escrowed** — some items sealed but every item is available to the core team/auditors under confidentiality. Full standing with an *escrowed* badge; only publicly disclosed features enter the design-choice analysis.
- **C · Sealed** — one or more permitted items withheld even from escrow. Scored and reported with a *not independently verifiable* flag; excluded from the approach catalogue and design-choice analysis.

**This entry is class A · Open.** Every item above is public, including the † items: the prompt
skeleton, the sign rule, the full 32-run design-space search with its losers, the raw generations,
and the external human data used for selection. Nothing is escrowed and nothing is withheld, so
`escrow_doi` in `metadata.json` is `null`. No part of the pipeline is proprietary.

★ items must always be public (never escrowed or withheld); † items must be at minimum escrowed. Full
policy: <https://janpfander.github.io/llm_predictions_megastudy/#disclosure>
