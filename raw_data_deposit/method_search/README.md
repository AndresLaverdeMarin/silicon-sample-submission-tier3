# The method search — every run, deposited

*Written in ASD-STE100 Simplified Technical English.*

This folder holds **every forecast run of the method search**, winners and
losers together. **No value in this folder reaches the submitted predictions.**
The submitted run is `raw_data_deposit/forecast_B_pop_on_t050_uv.jsonl`, and
it is not here.

It is deposited for one reason: registration item **J.1** asks how many
configurations were tried and against what data. This folder is that answer, in
full, so a reader can check the claim instead of trusting it.

## What is here

**80 runs.** 74 scored configurations and 6 smoke tests (marked `smoke=TRUE`
in `INDEX.csv`; a smoke test is a few calls to prove the plumbing works, not a
scored configuration).

| | |
|---|---|
| Models | 7 — `Qwen/Qwen3.8-27B`, `qwen/qwen3.8-27b`, `qwen/qwen3.8-flash`, `google/gemma-4-26B-A4B-it`, `google/gemma-4-E4B-it`, `deepseek/deepseek-v4-flash`, `z-ai/glm-5.3-flash` |
| Archives | 3 public — `broockman` (34 runs), `voelkel2025` (34), `doell` (6) |
| Modes | `listwise` (68), `pointwise` (6) |
| Reasoning | off (62), on (12) |
| Paid spend | **$2.2783** over the runs in this folder. See K.3 |
| Size | 1.68 MB gzipped |

```
INDEX.csv                       one row for each run, with a sha256
runs/local_slate/               30 runs, local vLLM, no paid call
runs/openrouter_qwen/           34 runs, OpenRouter, $0.6139
runs/openrouter_glm_deepseek/   16 runs, OpenRouter, $1.6644
    <run>/forecast.jsonl.gz     every draw of every arm
    <run>/forecast.meta.json    the exact settings, the call window, the
                                token counts, the spend, and a sha256 for
                                every input file
```

## What each record holds

One record is **one call**. For each arm in that call it holds:

- `value_raw` — the number the model wrote, on the scale of the prompt
- `value` — the same number after the sign flip, where the archive points the
  other way
- `value_truth_units` — the same number in the units of the archive's own
  `estimate.rct`, so it can be compared with the truth directly
- `arm_index` and `position` — which intervention it is, and **where it stood
  in the list the model read**
- `human`, `gpt4`, `expert` — the published values for that arm

The record also holds `arm_order` (the full running order shown to the model),
`parse_mode`, `n_parsed`, `n_asked`, and the sampler `seed`.

**This is enough to rebuild every number of `docs/EVIDENCE.md` from nothing**,
and enough to re-analyse position bias, draw-to-draw spread, or a different
way to combine the draws.

## WHAT IS NOT HERE — read this before you cite the folder

**The verbatim replies are NOT here.** The pipeline parses each reply to
numbers and keeps the text only when the parse was incomplete, cut to 400
characters. Measured over the deposited records:

| run family | records | records holding any raw text |
|---|---|---|
| local slate | 4,512 | 46 (1.0%) |
| OpenRouter, qwen | 9,412 | 179 (1.9%) |
| OpenRouter, glm and deepseek | 1,856 | 3 (0.2%) |

So this folder tells you **what each model answered**, for every arm of every
draw. It does not tell you **what each model said**. To get the replies
themselves, the runs must be made again with the pipeline changed to keep the
text. That would change no submitted value.

## Two warnings about the numbers

**`doell` is a weak reference.** Its human effects have a standard deviation of
1.706 points against a mean standard error of 1.539 points, so the sampling
noise is about twice the true spread. The noise-corrected correlation
`pearson_adj` clips at 1.0000 there. Read the raw correlation only. Its
directional agreement is also empty of information, because all 11 human
effects are positive: an approach that says "everything helps" scores 100 per
cent for free.

**Every result computed from this folder is EXPLORATORY.** Our own
preregistration was breached in four ways (registration item J.2). The
measurements are real and reproducible. The inference is not confirmatory.
