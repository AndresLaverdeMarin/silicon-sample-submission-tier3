# The method

*Written in ASD-STE100 Simplified Technical English.*

This document tells you how to build the entry again from nothing. It gives the
prompt, the sign rule, the ensemble and the parser. Every number in it comes
from a named file. The evidence that this method is the right one is in
[`EVIDENCE.md`](EVIDENCE.md), not here.

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

---

## 1. What the entry is, in one paragraph

This is a **direct effect forecast**. We do not simulate people. We show the
model a description of a study, the outcome items, the estimand, and **all** the
intervention texts of one cell at the same time. The model returns **one number
for each intervention**: the average treatment effect of that text on that
outcome, in points of the outcome scale. We repeat the call 8 times with the
interventions in a new random order each time, and take the mean.

The prompt **never names the target study**, its authors, or the benchmark. This
is deliberate. See section 7.

**Two variants were run. Variant B is submitted.** B puts the benchmark's own
recruitment-quota table into the `STUDY` slot of the prompt; A leaves it out.
The submitted run is `forecast/runs/2026-08-31_B_pop_on_t050_uv/`. Its values are
`predictions/team_27_T3_primary_v1.csv`. The control run is
`forecast/runs/2026-08-31_A_pop_off_t050_uv/`. The two agree at Pearson
r = +0.9941 over the 208 cells. See section 3.3.

**The runs `forecast/runs/B_pop_on/` and `forecast/runs/A_pop_off/` are
SUPERSEDED.** They ran before the `Extreme weather predictions` arm was cut to
what one participant read. They stay on disk as a record of the first pass. **No
submitted value comes from them.** See section 3.4.

---

## 2. Where the code is

**The pipeline that produced the submitted values is deposited, in
`forecast/`.** It reads only files of this repository and makes no network call.

| File | What it does |
|---|---|
| `forecast/extract_materials.py` | Step 1. Reads `survey/questionnaire.txt` and `codebook.csv`; writes the 16 stimuli and the 13 outcome blocks into `forecast/materials/`. Checks the condition order against `scripts/lib/submission_spec.R`. Its `reduce_state_adaptive` cuts the one state-adaptive arm to what one participant read — see section 3.4. |
| `forecast/core.py` | The prompt skeleton, both parsers, the work plan. **Model-free and study-free.** |
| `forecast/megastudy.py` | This study as one spec: the six slot functions, the 16 conditions, the 13 outcomes. |
| `forecast/run_vllm.py` | Step 2. Runs the prompts on local weights with the vLLM offline engine. |
| `forecast/build_predictions.py` | Step 3. Means the draws, writes the 208 rows, prints `AUDIT.txt`. |
| `forecast/tests/test_render_parity.py` | Proves the deposited `render` matches its source byte for byte at default settings. |
| `forecast/PROVENANCE.json` | For every file: where it came from, its source SHA-256, what was kept and what was removed. |

`forecast/core.py` and `forecast/run_vllm.py` are adapted copies of
`forecast/core.py` and `forecast/run_vllm.py`.
The originals stay in the sibling working project `modelbench`, which is **not**
in this deposit, because they carry the OpenRouter transport, the cost model,
the Ashokkumar archive loader and the scorer — and this repository has no ground
truth to score against.

**One change was made to `render`.** The source always asks for "points of the
0-100 scale". Two of the 13 outcomes here are not on that scale: `donation_ams`
is 0-10 dollars and `newsletter_signup` is a rate. So the study spec supplies
three more slot functions — `ask_units`, `scale_top` and `scale_bottom` — whose
**default values reproduce the source text byte for byte**.
`forecast/tests/test_render_parity.py` proves that.

`run_vllm.py` imports `render`, `build_work`, both parsers and `max_tokens_for`
from `core.py`. **No prompt text lives in the runner.** A local run and a hosted
run therefore differ by the model only, never by the prompt.

---

## 3. The prompt: six sections, always in this order

`structured_forecast.py::render` builds one skeleton with six slots. Each study
fills the same six slots. The skeleton never changes.

| # | Section | What goes in it |
|---|---|---|
| 1 | `TASK` | What the model must do. Said one time, at the top. |
| 2 | `STUDY` | The real study: who took part, how they were recruited, the design, the N, the number of conditions. |
| 3 | `OUTCOME` | Every item, with its exact wording, the 0-100 scale, and **both** anchor labels. |
| 4 | `ESTIMAND` | The contrast, said two ways: in plain words, then in statistical words. For the target study this is the study's own preregistered analysis — OLS on condition dummies with control as the reference and gender, age and race as covariates, robust standard errors, and a Benjamini-Hochberg correction inside each outcome; `newsletter_signup` is described as a logistic regression reported as an average difference in predicted probability. |
| 5 | `ARMS` | The stimulus text of the interventions. |
| 6 | `ASK` | The answer instruction, the sign rule and the output form. |

**Why this order.** All 504,840 prompts deposited by Ashokkumar et al. (2026)
put the instruction first, the context next, the stimulus late, and the answer
cue last (our prompt literature review, section 0 and section 1).
We copy the published order. Ruan et al. (2025) is the one adjacent controlled
test of prompt structure on an average treatment effect estimate, and it found
no effect. So there is no reason to depart from the published order.

### 3.1 A rendered example

This is the real `ASK` block of a 7-arm Broockman cell. Reproduce it with:

```bash
uv run forecast/run_vllm.py \
    --study broockman --mode listwise --print-prompts
```

```
ARMS
  Each treatment group read ONE of the 7 messages below. A separate
  control group read no message.

  MESSAGE 1:
  > Abortions cause psychological damage. They subject women to increased
  > risk of depression and anxiety.

  ... (messages 2 to 7) ...

ASK
  Give the effect of EVERY message, in points of the 0-100 scale.
  A POSITIVE number means the message moved the average TOWARD 100,
  that is, toward strong support for the policy.
  A NEGATIVE number means the message moved the average TOWARD 0,
  that is, toward strong opposition to the policy.

  Write exactly 7 lines and nothing else. Each line is the message
  number, then a colon, then the number:

  1: <number>
  2: <number>
  ...
  7: <number>

  Your estimates:
```

That prompt is 3,489 characters, about 712 tokens.

### 3.2 What is NOT in the prompt

Three things are left out on purpose. Each one was measured. See
[`EVIDENCE.md`](EVIDENCE.md) sections 5d and 5e.

- **No magnitude anchor.** The prompt never says how big effects usually are.
  An anchor can only pull every answer toward one value. That compresses the
  spread that a Pearson correlation needs.
  `structured_forecast.py:116-124` holds the anchor line, switched off.
- **No magnitude anchor for the population.** The `STUDY` slot **does** carry
  the benchmark's own recruitment-quota table — see section 3.3 — but the
  prompt never says how many people are needed to detect an effect, and never
  names a plausible effect size.
- **No framing-sentence ensemble.** Ten different opening sentences were
  measured. The ranking they produce does not repeat between studies.
- **No chain of thought.** Thinking is off in every run. The hosted route sends
  `reasoning: {enabled: false}`; the local route applies the chat template with
  `enable_thinking=False`. Without that switch the local model writes
  `<think>...` and 88 per cent of answers never reach a number (measured
  2026-08-30, `structured_forecast_vllm.py:130-138`).

### 3.3 What IS in the `STUDY` slot: the population block

The submitted run is **variant B**, and variant B puts the benchmark's own
recruitment-quota table into the `STUDY` slot. This is the whole block, as the
model sees it:

```
  Participants were adults resident in the United States. They were
  recruited from a national non-probability opt-in online panel. Recruitment
  used census-based cross quotas on gender by age band and on gender by race
  and ethnicity. ...

  The sample was recruited to these targets:

    Age band                    total     male   female
      18-29                     3,629    1,848    1,781
      30-44                     4,688    2,365    2,323
      45-59                     4,122    2,048    2,074
      60+                       5,561    2,566    2,995

    Race / ethnicity            total     male   female
      White / Caucasian        10,832    5,332    5,500
      Hispanic / Latino         3,263    1,646    1,617
      Black / African American  2,212    1,042    1,170
      Asian / Asian American    1,201      568      633
      Other                       492      240      252
```

Its only source is `forecast/materials/quotas_18000.csv`, copied from the
benchmark preregistration's quota table
(`forecast/PROVENANCE.json`). It adds about 664 characters to each prompt.

**It is a measured null, and we keep it anyway.** On the template that ships,
the block moves the score by -0.0029 (p = 0.8671) on Broockman and +0.0024
(p = 0.3910) on Voelkel. Neither is significant. It is in the prompt for
consistency with `team_27`'s **Tier 1** entry, which describes the same
population from the same file. Two entries from one team should not disagree
about who took part.

**The control is deposited.** The same run without the block is variant A,
`forecast/runs/2026-08-31_A_pop_off_t050_uv/`. Its 208 rows are also written out as
`raw_data_deposit/variantA_pop_off_t050_uv_T3_ate.csv`. The two variants agree at
Pearson r = +0.9941 over the 208 cells. Full account:
[`EVIDENCE.md`](EVIDENCE.md) section 5c.

**To reproduce either one**, add or remove `--population`:

```bash
python forecast/run_vllm.py --label B_pop_on_v2 --population --go   # submitted
python forecast/run_vllm.py --label A_pop_off_v2             --go   # control
```

Each run writes to `forecast/runs/<run date>_<label>/`.

### 3.4 One arm was cut to what a participant read

`Extreme weather predictions` is the only **state-adaptive** arm of the 16. The
benchmark's file for it is a kit for the survey programmer, not one message. Its
own first line says that each participant sees only ONE version. It says: do
**not** feed the whole block below verbatim.

The raw block is **11,435 characters**. It holds authoring scaffolding, a list
of 51 states, the state-to-case map, **all four** case texts, and a reference
list marked "[not displayed to participants]".

**The first pass sent the whole block. That was a measurement error.** The 16
arm texts then came to 47,032 characters, and this one arm was **24.5 per cent**
of them. Most of that text was instruction to the programmer. No participant
ever read it. One intervention took a quarter of the prompt, and the model spent
that quarter on survey code.

`forecast/extract_materials.py::reduce_state_adaptive` now renders the **modal
participant**. Section II of the source file gives what a participant saw: a
page that asks the home state, then one intro paragraph, then one of four case
texts. The function keeps three things:

1. one intro paragraph;
2. **Case 1**, the flood text. It covers 27 states and the District of Columbia,
   the largest share of the sample;
3. one line that says the message was tailored to the reader's home state, and
   that other readers got a wildfire text or a cold-and-snow text.

The arm is now **2,213 characters**
(`forecast/materials/stimuli/extreme_weather_predictions.txt`). It is **5.9 per
cent** of the 37,722 characters of arm text. The mean prompt fell from 53,058.3
to 43,292.3 characters (`forecast/runs/B_pop_on/forecast.meta.json` against
`forecast/runs/2026-08-31_B_pop_on_t050_uv/forecast.meta.json`).

**Both variants were run again after the cut.** Every submitted value comes from
a run after it.

---

## 4. Listwise, not pointwise

The script has two modes.

| Mode | One call holds | Why it exists |
|---|---|---|
| `pointwise` | ONE intervention | The control. It is the published Ashokkumar format. |
| `listwise` | ALL interventions of one cell | The experiment. |

**The entry uses `listwise`.** The measured reason is in
[`EVIDENCE.md`](EVIDENCE.md) section 1: listwise beat pointwise in all six
paired tests we ran, on both studies and on all three models.

> **All of that evidence is EXPLORATORY, not confirmatory.** Our own
> preregistration was breached in four ways, so the confirmatory comparison it
> defined is void by its own terms. See [`EVIDENCE.md`](EVIDENCE.md)
> section 13 and `registration.md` item J.2. The measurements are real and
> reproducible; the inference is not confirmatory. Listwise is still the best
> supported choice in the file, because all six differences have the same
> sign — that does not depend on any one p value.

**The mechanical reason** is that listwise gives the model the comparison the
score asks for. Tier 3 is scored on how well the predicted effects **rank
against each other**. A pointwise call sees one text and cannot know that the
next text is stronger. A listwise call sees all of them and can order them.

This was the largest open question in the literature review
(our prompt literature review, sections 2 and 9). Lippert et al.
(2024) put all 24 questions in one prompt and reached r = 0.89. Ashokkumar et
al. used one call for each arm and reached r = 0.85. No paper on disk compares
the two directly. So we measured it.

---

## 5. The sign convention

This is the part that broke once and cost 0.26 in correlation. Read it twice.

**Rule: the prompt is ALWAYS written with 100 = the named high end of the
scale. The NUMBER is flipped afterwards, never the prompt.**

For Broockman, the prompt always says `100 = strong support for the policy`.
So the model always returns **the effect on support**.

The Broockman archive is not always on that scale. A cell named `oppose` holds
arguments **against** a policy, and its `estimate.rct` is **the effect on
opposition**. Effect on opposition = minus the effect on support. So the number
is negated at scoring time:

```python
val = None if raw is None else (-raw if flip else raw)   # structured_forecast.py:1185
```

`flip` is `True` when `cell["side"] == "oppose"` (`broockman_flip`,
`structured_forecast.py:409-431`).

**This is the same operation as the capsule's own R code.**
`codeocean/extracted/code/load_archive1_results.R:104` reads:

```r
mutate(expectation = ifelse(scale_flip,
                            outcome_scale_max - (expectation - outcome_scale_min),
                            expectation))
```

That line flips a **level** on a bounded scale. Our answer is a **difference**
of two levels, so the same flip becomes a change of sign:

```
(max - (a - min)) - (max - (b - min)) = -(a - b)
```

**Check it before you run.** `--print-prompts` prints a `SIGN CHECK` block that
names every cell and its `scale_flip` value.

**For Voelkel there is no flip.** All four outcomes already point the
pro-climate way and all ten texts push the same way
(`voelkel_flip`, `structured_forecast.py:434-438`; source
the Voelkel 2025 questionnaire (OSF 10.17605/OSF.IO/2MCF8), field `scale_note`).

**For the target megastudy there is NO flip at all.** Every prompt is written
on the same scale that the submission uses, so `scale_flip` is `False` for all
13 outcomes and no number is turned. The flag is still computed and written into
every record, so the claim is auditable and not merely asserted.

Two outcomes still need care, and both are handled inside the prompt:

- **`funding_perceptions`** is defined as `100 - funding_5` (`codebook.csv:53`).
  The prompt therefore prints that item **with its anchors already swapped**, so
  a positive effect means more support for climate research funding.
- **`distrust_post`** is not reversed. A higher value means more distrust. A
  trust-building text should give a **negative** ATE there and a positive ATE on
  `trust_post`. `forecast/build_predictions.py` audits that sign agreement for
  all 16 texts and prints the result in `AUDIT.txt`.

Both are also set out in `predictions/SPEC_NOTES.md` section 7.

---

## 6. The 8-draw ensemble and the arm-order randomisation

### 6.1 Why an ensemble at all

**The model is sensitive to the position of an arm in the list.** At
temperature 0, two calls that hold the same arms in a **different order**
return different numbers. Measured over the 42 Broockman cells
(the method-search test report section 6):

| Model | Self-agreement, r |
|---|---|
| `Qwen/Qwen3.8-27B`, local vLLM | +0.5723 |
| `qwen/qwen3.8-27b`, hosted | +0.6151 |
| `qwen/qwen3.8-flash`, hosted | +0.7320 |

A model that agreed with itself would score +1.0. It does not. The ensemble
averages that position noise away.

### 6.2 How the draws are built

`build_work` (`structured_forecast.py:971-992`) makes one job for each call:

```python
for cell in cells:
    for f in range(framings):
        for s in range(samples):
            order = list(range(len(cell["arms"])))
            rng.shuffle(order)                 # a NEW arm order for each draw
            work.append({"cell": cell, "order": order, ...})
```

- `samples = 8`. Eight draws for each cell.
- `framings = 1`. **One fixed opening sentence, not an ensemble of ten.**
- `rng` is `random.Random(seed)` with `seed = 1`, so the 8 orders rebuild
  exactly.
- The seed sent to the model is `seed + sample index`
  (`structured_forecast.py:1153`). Without that, a provider that honours
  `seed` returns the same text 8 times and the ensemble does nothing.
- **`arm_order` is written into every record.** The order is recorded, so
  position bias can be measured afterwards instead of assumed.

### 6.3 How the draws become one number

The mean, over the draws, of the parsed value for each arm
(`collect` and `write_predictions`, `structured_forecast.py:825-945`).
No median, no trimming, no weighting. A draw that failed to parse is not
counted; it is not replaced.

---

## 7. Why the prompt never names the study

The first version of the prompt held a `Study description:` block that named
the study and its authors, copied from the Ashokkumar format. The model
answered it with recall, not with reasoning: it wrote *"this is a reference to
the study by Broockman and Kalla (2016)"* (measured 2026-08-29,
the method-search preregistration, section 7b).

A method tuned on **recall of a published result cannot transfer to the target
megastudy**, because that study is not published. Removing the block is not
only a contamination guard. It stops us from selecting a skill that does not
exist on the target.

The block was removed before any configuration was scored. That decision is
written into the preregistration, section 7b, with its date and its
justification.

---

## 8. Parsing

`parse_listwise` (`structured_forecast.py:612-647`) reads
`<position>: <number>` lines. It tolerates:

- a missing line;
- an extra line;
- a position outside 1..n;
- a repeated position (the **first** answer wins);
- `,` as a decimal separator;
- the separators `:`, `)`, `]` and `. ` (a full stop **must** be followed by a
  space, or the bare number `2.4` reads as position 2 with value 4);
- up to 12 leading letters, so `Message 3: -1.2` parses.

**It never assumes the model kept the order asked.** The position in the reply
is mapped back through the recorded `arm_order` to the real arm.

A number outside `[-100, +100]` is dropped. If **no** labelled line is found,
and the reply holds exactly n bare in-range numbers, they are mapped in the
order they appear, and the record is stamped `parse_mode = "bare numbers, in
order"` so the fallback can be removed from an analysis.

**Nothing is repaired, imputed or re-asked.** A cell with no parsed value in a
given draw simply has fewer draws in its mean.

---

## 9. Running it

Nothing is sent without `--go`. `--max-spend` is a hard stop.

Run everything from the repository root.

```bash
# 1. Extract the materials from the benchmark's own files.
#    This step also cuts the state-adaptive arm. See section 3.4.
python forecast/extract_materials.py

# 2. Render every prompt and the scale_flip table. Runs NOTHING.
python forecast/run_vllm.py --model Qwen/Qwen3.8-27B \
    --population --print-prompts

# 3. The real run. It costs $0.00. --population makes the SUBMITTED variant B.
python forecast/run_vllm.py --model Qwen/Qwen3.8-27B \
    --temperature 0.5 --samples 8 --population --go \
    --label B_pop_on_v2

# 3b. The control variant A. The same, without the population block.
python forecast/run_vllm.py --model Qwen/Qwen3.8-27B \
    --temperature 0.5 --samples 8 --go \
    --label A_pop_off_v2

# 4. Build the 208 rows and print the audits make check cannot make.
#    WITHOUT --out this writes AUDIT.txt only. It writes NO prediction file.
python forecast/build_predictions.py forecast/runs/2026-08-31_B_pop_on_t050_uv \
    --out predictions/team_27_T3_primary_v1.csv

# 5. Fingerprint and validate.
make manifest
make check
```

Step 3 writes to `forecast/runs/<run date>_<label>/`, so a rerun on another day
makes a directory with that day's date.

The measurements behind the design ran in the sibling project `modelbench` and
are **not** reproducible from this deposit. Their scripts are
the method-search scorer (the 32-run grid) and the method-search test script
(every paired test). Their outputs are quoted in full in
[`EVIDENCE.md`](EVIDENCE.md).

Each run directory holds three files:

| File | Content |
|---|---|
| `forecast.jsonl` | One record for each CALL. Holds the raw text when parsing was not complete, the arm order, the seed, the flip flag, and every parsed value both before and after the flip. |
| `forecast.meta.json` | The exact model id, the call-date window, the sampling settings, the call count, the parse rate, the spend, the wall clock, and the SHA-256 of every stimulus and material file. |
| `AUDIT.txt` | The unit and sign checks, and the number of draws behind each of the 208 cells. |

`forecast.meta.json` is the source for registration items B.1, B.2, B.3 and
K.3. Do not retype its values.

---

## 10. The local inference stack

The **server** route fails on this machine. vLLM 0.19.1 asks FlashInfer to
build a kernel at the first generation, and FlashInfer needs `nvcc`, which this
machine does not have:

```
RuntimeError: Could not find nvcc and default cuda_home='/usr/local/cuda'
doesn't exist
```

The **offline engine** works. Two settings make it work:

1. `additional_config={"gdn_prefill_backend": "triton"}`. Qwen3.8-27B is a
   hybrid model with Gated Delta Net layers. By default vLLM picks the
   FlashInfer prefill kernel and JIT-compiles it. The Triton version of the
   same kernel needs no compiler. `gdn_linear_attn.py:133` is the switch.
2. `tok.apply_chat_template(..., enable_thinking=False)`. Without it the model
   writes a thinking trace and 88 per cent of answers never reach a number.

`max_model_len` is set from the longest prompt plus the reply, so it is small
(2,056 tokens for the Broockman grid) and the engine schedules many sequences
at once.

---

## 11. Cost and size of the target run

**`2026-08-31_B_pop_on_t050_uv` is the submitted run.** `2026-08-31_A_pop_off_t050_uv` is
the control. Measured on the runs themselves:
`forecast/runs/2026-08-31_B_pop_on_t050_uv/forecast.meta.json`,
`forecast/runs/2026-08-31_A_pop_off_t050_uv/forecast.meta.json` and the `AUDIT.txt`
in each of those two directories.

| Quantity | `2026-08-31_B_pop_on_t050_uv` — SUBMITTED | `2026-08-31_A_pop_off_t050_uv` — control |
|---|---|---|
| model | `Qwen/Qwen3.8-27B`, local vLLM offline engine | the same |
| mode / temperature / draws | listwise / **0.5** / 8 | the same |
| population block | **yes** | no |
| calls: 13 outcomes x 8 draws | **104** | 104 |
| arms asked / parsed | **1,664 / 1,664 — 100.0 per cent** | 1,664 / 1,664 — 100.0 per cent |
| draws behind each of the 208 cells | **min 8, max 8, mean 8.00** | min 8, max 8, mean 8.00 |
| mean prompt | **43,292.3 characters** | 42,628.3 characters |
| longest prompt | **44,401 characters** | 43,737 characters |
| input tokens, total | **1,026,832** (carried over; the prompts are unchanged) | 999,168 |
| `max_model_len` | 16,080 | 15,859 |
| wall clock, generation | **110.9 s — 1.8 minutes** | 106.7 s — 1.8 minutes |
| call window | **2026-08-31T13:41:39Z to 13:43:30Z** | 2026-08-31T13:44:21Z to 13:46:08Z |
| API calls | **0** | 0 |
| **monetary cost** | **$0.00** | $0.00 |

**The output tokens are no longer estimated**, because the new pair parsed every
call; the earlier estimate of about 12,300 applied to the superseded run.

**The parse rate is 100 per cent.** All 104 calls of the submitted run, and all
104 of the control, wrote the 16 required lines. **Every one of the 208 cells
rests on 8 draws.** Nothing was repaired, imputed or asked again; the pipeline
drops a failed draw and does not replace it, so a 100 per cent rate is a
property of the run and not of any repair.

**The superseded temperature-0.85 run lost one call**, `donation_ams` draw 4,
where the model answered with prose and never wrote the 16 lines. Its 16
`donation_ams` cells rested on 7 draws and the other 192 on 8, giving 1,648
parsed arm-answers and a mean of 7.92. Its control lost two calls the same way.
**Lowering the temperature from 0.85 to 0.5 removed the failure.**

**The output of the submitted run**, from
`predictions/team_27_T3_primary_v1.csv` and
`forecast/runs/2026-08-31_B_pop_on_t050_uv/AUDIT.txt`: 208 rows, no missing value,
`ate` from **-6.250 to +4.750**, mean **+1.329**. 27 of the 208 values are
negative, 25 of them among the 176 slider values. `newsletter_signup` runs from
-0.0081 to +0.0310, which is a change of a 0-1 proportion. `donation_ams` runs
from -0.110 to +0.454 dollars on a 0-10 scale. `trust_post` and
`distrust_post` disagree in sign for 15 of the 16 texts, which is what a
trust-building text should do; `Social justice` is the one that does not.

**Where the token counts come from.** `forecast.meta.json` records characters,
not tokens. The 104 prompts were rebuilt with `forecast/core.py::render` under
the same seed, wrapped in the model's own chat template with
`enable_thinking=False`, and counted with the `Qwen/Qwen3.8-27B` tokenizer. The
rebuild reproduces the recorded 43,292.3 mean characters and 44,401 longest
characters exactly. The measured rate is 4.39 characters for each token. The
input tokens are 9,873.4 for each call on average, with a minimum of 9,737 and a
maximum of 10,154.

**The output count is an estimate, not a record.** The raw reply is not kept for
a call that parsed completely, so the output tokens cannot be counted. The reply
format did not change between the first pass and the rerun: it is 16 lines of
`<position>: <number>`. The first pass measured about 118 output tokens for each
call, from vLLM's own throughput line at the end of `forecast/runs_B.log` —
9,596.16 input tokens/s and 93.09 output tokens/s. 104 calls at that size give
about 12,300 output tokens. The hard ceiling set by `max_tokens` is
40 x 16 + 128 = 768 for each call, so 79,872 in total.

The same 16 texts repeat in all 13 outcome calls, so prompt caching would pay
for itself on a hosted route. The submission does not need it, because the
submission runs locally. The same work on the hosted `qwen3.8-flash` route was
estimated at about $0.174.
