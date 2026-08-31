# The evidence

*Written in ASD-STE100 Simplified Technical English.*

> # EVERY RESULT IN THIS FILE IS EXPLORATORY
>
> Our own preregistration, `notes/PREREG_broockman_method_search.md`, was
> written on 2026-08-29 before any configuration was scored. **The work then
> broke four of its own rules**, so the confirmatory comparison it defined is
> **void by its own terms**. All four breaches are declared in
> `registration.md` item J.2, and are summarised in section 13 below.
>
> The consequence for how you read this file: **the headline result — the
> direct forecast against our own simulation, p = 0.0073 (section 2) — was
> selected after seeing 34 runs. Its true false-positive rate is higher than
> 0.0073.** It is not a confirmatory result and it must not be read as one.
> The same applies to every other p value here.
>
> **The measurements are real, reproducible and unfabricated.** Every run
> directory holds its own prompts, its own raw generations, its own seed and
> its own score. Every run is listed, the losers with the winners. **The
> problem is the inference, not the data.**

This document holds every measurement that shaped the entry. The wins and the
nulls get the same space. Where a result is not significant, the p value is
printed.

**Every number below names the file that produced it.** Three files produce
almost all of them:

| File | Produced by | What it holds |
|---|---|---|
| `modelbench/output/tier3/index.csv` | `modelbench/tier3_index.py` | The 32-run grid, scored three ways. |
| `modelbench/output/tier3/TESTS.txt` | `modelbench/tier3_tests.py` | Every paired significance test. |
| `ashokkumar_bench/output/scorecard_Qwen3.8-27B-v10-broockman.json` | `ashokkumar_bench/bench/task.py score` | Our per-respondent simulation baseline. |
| `modelbench/output/tier3/runs/*/forecast.jsonl` | `modelbench/structured_forecast*.py` | One record for each call, with the truth, the gpt-4 forecast and the expert forecast beside every arm. Sections 5c, 8 and 9 recompute from these. |

Two files of **this** deposit are also cited, and they are here:
`forecast/runs/2026-08-30_B_pop_on_v2/AUDIT.txt` and
`forecast/runs/2026-08-30_A_pop_off_v2/AUDIT.txt`. Section 5c also quotes a
comparison of the two runs. Rebuild it with:

```bash
python forecast/build_predictions.py --compare \
    forecast/runs/2026-08-30_A_pop_off_v2 forecast/runs/2026-08-30_B_pop_on_v2
```

Those files live in the sibling working project `modelbench`, which is **not
part of this deposit**. See registration item K.1. This document is what the
deposit carries forward.

---

## 0. How to read the scores

Three numbers are reported for every run. **They do not agree, and the
disagreement matters.** See section 8.

| Score | What it asks |
|---|---|
| **within-cell r** | Inside one cell, do we rank the arms correctly? Averaged over cells. This is the metric Ashokkumar et al. use. |
| **within-cell r, >=5 arms** | The same, but only for cells with 5 arms or more. |
| **pooled r** | One correlation over ALL arms at one time. |

The two public studies we score against:

| Study | Cells | Arms | People | Why it is used |
|---|---|---|---|---|
| `broockman` | 42 | 172 | 61,869 | The **structural** match to the target: one short text for each arm, one shared control, every arm argues in one direction. It is the only public study with enough cells to separate two methods. |
| `voelkel2025` | 4 | 40 | 13,821 | The **topical** match: climate, 13 items, one "for"-shaped set of texts. |

`broockman` was the development set. `voelkel2025` was the confirmation set.
Both were fixed in `notes/PREREG_broockman_method_search.md` **before the first
score**. The target megastudy was never used for selection.

**A warning about n = 4.** Every Voelkel test below has only 4 cells. A paired
test over 4 cells has almost no power. Read the Voelkel numbers as a direction,
never as a verdict.

---

## 1. EXPLORATORY WIN — listwise beats pointwise

Six paired tests, three models, two studies, temperature 1.0.
Source: `modelbench/output/tier3/TESTS.txt` section 1.

| Study | Model | listwise | pointwise | difference | t | p | wins |
|---|---|---|---|---|---|---|---|
| broockman | `qwen/qwen3.8-27b` | **+0.3468** | +0.1450 | **+0.2018** | +2.16 | **0.0369** | 25/42 |
| broockman | `Qwen/Qwen3.8-27B` local | +0.3430 | +0.2152 | +0.1278 | +1.21 | 0.2327 | 24/41 |
| broockman | `qwen/qwen3.8-flash` | +0.3217 | +0.2501 | +0.0716 | +0.75 | 0.4555 | 24/42 |
| voelkel2025 | `qwen/qwen3.8-27b` | +0.6558 | +0.5795 | +0.0763 | +0.83 | 0.4681 | 3/4 |
| voelkel2025 | `Qwen/Qwen3.8-27B` local | +0.6454 | +0.5916 | +0.0538 | +0.56 | 0.6162 | 3/4 |
| voelkel2025 | `qwen/qwen3.8-flash` | +0.5877 | +0.4151 | +0.1726 | +1.24 | 0.3026 | 3/4 |

**What is true.** The difference points the same way in **all six** tests. That
is the strongest thing we can say about a design choice in this project.

**What is NOT true.** Only **one** of the six passes p < 0.05. Five do not. We
chose listwise because the sign is consistent and because the mechanism is
clear (section 1 of `METHOD.md`), not because six tests were significant.

---

## 2. EXPLORATORY WIN — the structured forecast beats our own simulation

**EXPLORATORY, not confirmatory.** This is the only comparison in the project
that reached p < 0.05, and **it was selected after seeing 34 runs, so its true
false-positive rate is higher than 0.0073.** The preregistered test for this
comparison was a paired bootstrap with a minimum difference of 0.14, and it was
never run (section 13, breach 3). Read the number as a direction, not as a
verdict.

The baseline is our own Tier-1-style per-respondent simulation, run on the same
42 Broockman cells: `ashokkumar_bench/output/RESULTS_Qwen3.8-27B-v10-broockman.txt`,
mean within-cell **r_raw = 0.191694**.

Source: `modelbench/output/tier3/TESTS.txt` section 2.

| Forecast run | forecast r | simulation r | difference | t | p | wins |
|---|---|---|---|---|---|---|
| `qwen3.8-flash` listwise, t = 0.5 | **+0.4091** | +0.1917 | **+0.2174** | **+2.82** | **0.0073** | **30/42** |
| `qwen3.8-flash` listwise, t = 0.0 | +0.4400 | +0.1731 | +0.2669 | +2.66 | 0.0113 | 28/41 |
| `qwen3.8-27b` listwise, t = 1.0 | +0.3468 | +0.1917 | +0.1551 | +1.61 | 0.1157 | 26/42 |
| `Qwen3.8-27B` local, t = 0.85 | +0.3398 | +0.1917 | +0.1481 | +1.53 | 0.1340 | 26/42 |
| `Qwen3.8-27B` local, t = 1.0 | +0.3215 | +0.1917 | +0.1298 | +1.26 | 0.2154 | 24/42 |

**What this means.** Asking the model for the effect directly beats building
9,000 synthetic people and computing the effect from their answers — on this
study, on this metric. It also needs about 380 times fewer calls: **336** against
**128,400**
(`modelbench/output/runs/2026-08-30_qwen3.8-flash_broockman_listwise_t05/forecast.meta.json`,
field `calls`, against the line count of
`modelbench/output/runs/2026-08-28_item-mode_v10_broockman/answers_Qwen3.8-27B-v10_broockman.jsonl`).

**What this does NOT mean.** It does not mean simulation is the wrong approach
for the benchmark. Tier 1 is scored on distributional realism as well as on
effects, and a direct forecast produces no distribution at all. The two entries
answer different questions.

---

## 3. Reference points on the same 42 Broockman cells

Both reference values are computed by `modelbench/tier3_index.py` from the same
archive rows as our own score, so they are the same quantity.
Source: `modelbench/output/tier3/index.csv`, columns `gpt4_within` and
`expert_within`.

| Forecaster | within-cell r |
|---|---|
| Our best listwise run (`qwen3.8-flash`, t = 0.0) | +0.4400 |
| Our best local run (`Qwen/Qwen3.8-27B`, t = 0.85) | +0.3398 |
| **Human expert forecasters, published** | **+0.2546** |
| **gpt-4, published** | **+0.1999** |
| Our per-respondent simulation (v10) | +0.1917 |

We are above both reference points on Broockman **on this metric**. Read
section 8 before you use that sentence: on pooled r we are also above both, but
on the 15 cells with 5 arms or more the pointwise run is below both. The three
metrics do not agree about who wins.

---

## 4. EXPLORATORY LOSS — on Voelkel we are still below gpt-4

Say this plainly. **Voelkel is the study that most resembles the target
megastudy**: climate attitudes, a 13-item instrument, and ten texts that all
argue the same way, exactly like the target's 16 interventions. It is the
better guide to how the entry will score.

Source: `modelbench/output/tier3/index.csv`, `study = voelkel2025`.

| Forecaster | within-cell r (4 cells) |
|---|---|
| **gpt-4, published** | **+0.7454** |
| Our best in the whole grid, `qwen/qwen3.8-27b` listwise t = 0.5 | +0.6600 |
| **The submitted configuration**, `Qwen/Qwen3.8-27B` local t = 0.85, block on | **+0.6509** |
| The same, block off | +0.6485 |
| Our worst listwise, t = 1.6 | +0.4086 |

The submitted configuration's own Voelkel score is in
`modelbench/output/tier3/runs/2026-08-30_Qwen3.8-27B-local_voelkel2025_listwise_t085_pop/RESULTS.txt`.

**We are 0.085 below gpt-4 at our best, and 0.095 below in the configuration we
actually submitted.** That is on the study that looks most like the target. We
did not test whether that gap is significant, and with 4 cells we could not.
A larger model would probably close it. We did not use one, because the paid
calls were not approved (registration item I.1) and because a local run is
reproducible for anyone at zero cost.

---

## 5. The nulls

These get the same space as the wins. Four things that we expected to matter,
and that did not.

### 5a. NULL — model choice

`qwen/qwen3.8-flash` against `qwen/qwen3.8-27b`, and hosted against local.
Source: `modelbench/output/tier3/TESTS.txt` section 3.

| Comparison | difference | t | p | wins |
|---|---|---|---|---|
| flash vs 27b, t = 0.0 | +0.1976 | +2.03 | 0.0491 | 23/41 |
| flash vs 27b, t = 0.5 | +0.0681 | +1.25 | 0.2171 | 23/42 |
| flash vs 27b, t = 0.85 | +0.1021 | +1.11 | 0.2739 | 23/42 |
| flash vs 27b, t = 1.0 | -0.0251 | -0.34 | 0.7332 | 19/42 |
| flash vs 27b, t = 1.6 | +0.0734 | +0.48 | 0.6317 | 23/42 |
| 27b hosted vs 27b local, t = 0.0 | -0.0082 | -0.26 | 0.7949 | 8/42 |
| 27b hosted vs 27b local, t = 0.85 | -0.0499 | -1.18 | 0.2429 | 17/42 |
| 27b hosted vs 27b local, t = 1.0 | +0.0252 | +0.44 | 0.6643 | 23/42 |

**One of eight is significant, and it is the weakest run in the grid**: the
t = 0.0 runs used only 2 draws, not 8, and the flash t = 0.0 run parsed only
95.6 per cent of arms. The sign even reverses at t = 1.0. We treat model choice
as a null on this evidence.

**The same weights hosted and served locally give the same answer** (the last
three rows). That is the check that makes the local submission defensible.

### 5b. NULL — temperature

Every pair of temperatures inside one model and one study.
Source: `modelbench/output/tier3/TESTS.txt` section 4.

**0 of 46 paired tests reach p < 0.05.** The smallest p value in the whole
block is 0.0543 (`qwen3.8-27b` broockman, t = 0.5 against t = 1.6).

The only visible pattern is a **parse-rate** effect, not a correlation effect.
At t = 1.6 the parse rate falls to 79.2 per cent for flash and 87.1 per cent
for 27b (`index.csv`, column `parsed_pct`), and the pooled r for
`qwen3.8-27b` broockman collapses to +0.0591. Very high temperature breaks the
output format before it breaks the judgement.

### 5c. NULL — the demographic and population block

An extra prompt block describing the survey population. **The submitted entry keeps this block.**
Read the whole section before you read that as a result: it is a null, and it is
kept for a reason that is not performance.

**The three OLD tests used a different prompt.** They ran on the earlier
pointwise `direct_forecast.py` template, not on the structured listwise
template that this entry uses.
Source: `modelbench/output/tier3/TESTS.txt` section 8.

| Study | with the block | without | difference | t | p |
|---|---|---|---|---|---|
| broockman | +0.1808 | +0.1215 | +0.0592 | +0.66 | 0.5151 |
| voelkel v1 | -0.0447 | +0.0788 | -0.1235 | -0.52 | 0.6395 |
| voelkel v2 | +0.1042 | +0.2720 | -0.1678 | -1.97 | 0.1440 |

Three tests, three different signs, none significant. **But a conclusion
carried across a change of prompt architecture is not evidence.** So the test
was run again, on the template that ships.

**The NEW test, on the submitted template.** Measured 2026-08-30. Local
`Qwen/Qwen3.8-27B`, listwise, temperature 0.85, 8 draws — the exact
configuration of the entry. Paired over the same cells.
Source: `modelbench/output/tier3/runs/2026-08-30_Qwen3.8-27B-local_broockman_listwise_t085_pop/RESULTS.txt`
and `..._voelkel2025_listwise_t085_pop/RESULTS.txt`, each against the same run
without `_pop`.

| Study | with the block | without | difference | t | p | cells |
|---|---|---|---|---|---|---|
| broockman | +0.3369 | +0.3398 | **-0.0029** | -0.17 | **0.8671** | 42 |
| voelkel2025 | +0.6509 | +0.6485 | **+0.0024** | +1.00 | **0.3910** | 4 |

**Neither is significant.** The block does not help and it does not hurt. On
Broockman the effect is -0.0029 in correlation, which is smaller than the
rounding of the numbers around it.

**Why the block is in the submitted prompt anyway.** For consistency with
`team_27`'s **Tier 1** entry, which describes the same population, from the
same source file, to the same model. Two entries from one team should not
disagree about who took part in the study. That is a consistency choice, not a
performance claim, and we state it as such.

**The claim is testable on the target study, and we tested it.** Both variants
were run in full against the target megastudy, back to back:

| Variant | Population block | Submitted? |
|---|---|---|
| `forecast/runs/2026-08-30_B_pop_on_v2/` | yes | **yes**, `predictions/team_27_T3_primary_v1.csv` |
| `forecast/runs/2026-08-30_A_pop_off_v2/` | no | no — the control |

The two agree at **Pearson r = +0.9873** over the 208 cells, with a mean
absolute difference of 0.2044 points. The per-outcome r runs from +0.8884
(`distrust_post`) to +0.9965 (`behavior_mean`). Rebuild those numbers with
`forecast/build_predictions.py --compare` on the two run directories, as shown
at the top of this file. **On the target study the block changes almost
nothing**, which is what the two public studies predicted.

**An earlier pair of runs, `forecast/runs/B_pop_on/` and
`forecast/runs/A_pop_off/`, is SUPERSEDED.** It ran before the
`Extreme weather predictions` arm was cut to what one participant read
(`docs/METHOD.md` section 3.4). Those two runs agreed at r = +0.9864, so the cut
did not change this conclusion. No submitted value comes from them.

### 5d. NULL — the framing-sentence ensemble

Ten different opening sentences, so 45 pairwise comparisons inside one run.
Source: `modelbench/output/tier3/TESTS.txt` section 10.

| Run | best framing | worst framing | pairwise tests at p < 0.05 |
|---|---|---|---|
| broockman | +0.1714 | +0.0150 | **0 of 45** |
| voelkel, real texts | +0.4125 | +0.2349 | **6 of 45** |

**Correction to an earlier note.** An earlier draft said "0 of 45" for both
runs. That is wrong for Voelkel: 6 of 45 pairs are significant there.

But the ranking does not repeat. The two studies rank the same 10 framing
sentences at **Pearson r = -0.2698 (p = 0.4509)** and
**Spearman rho = -0.0909 (p = 0.8028)**. The best sentence on one study is not
the best sentence on the other. Picking a winner would be picking noise. The
entry uses **one fixed sentence and 8 repeated draws** instead.

### 5e. What replaced the framing ensemble

The literature review measured how much variance each prompt slot carries in
the deposited gpt-4 data (`notes/LIT_structured_forecast_prompt.md`
section 6c): the **persona** slot carries excess eta-squared of +0.113 and the
**framing** slot +0.026, so the persona carries about 4.4 times more. A direct
forecast has no persona slot at all. That removes the one slot worth
ensembling over. Repeated sampling of one prompt (Lippert et al. 2024, 50
draws) replaces it.

---

## 6. A bug that cost 0.26 in correlation

**What happened.** An early Broockman prompt asked the model for the effect on
**support** for every cell, including cells whose archive truth is the effect
on **opposition**. The answer was never negated. Half the cells were scored
with the sign reversed.

**What it cost.** Source: `modelbench/output/tier3/TESTS.txt` section 7.

| Run | within-cell r |
|---|---|
| With the bug (2026-08-29) | **-0.1355** |
| Sign fixed (2026-08-30), same prompt, same model, same settings | **+0.1215** |

Difference +0.2570, t = +2.03, p = 0.0494, better in 24 of 42 cells.

**How it was found.** By reading the model's own thinking trace, not by a unit
test and not by the score. The score alone looked like a weak method. The trace
showed the model reasoning correctly and then being marked wrong.

**The lesson we kept.** The sign rule is now written into the prompt builder as
one rule for every cell — *the prompt always names the high end, and the number
is flipped afterwards* — and `--print-prompts` prints a `SIGN CHECK` block
that lists every cell and its flip flag. See `METHOD.md` section 5.

A negative correlation is not a weak method. It is very often a sign error.
Check the sign before you change the method.

---

## 7. Position sensitivity, and why there are 8 draws

At temperature 0, two calls that hold the **same** arms in a **different**
order return different numbers.
Source: `modelbench/output/tier3/TESTS.txt` section 6.

| Run | draw pairs | agreement r |
|---|---|---|
| `Qwen/Qwen3.8-27B` local, t = 0.0 | 1 | +0.5723 |
| `qwen/qwen3.8-27b` hosted, t = 0.0 | 1 | +0.6151 |
| `qwen/qwen3.8-flash` hosted, t = 0.0 | 1 | +0.7320 |
| `Qwen/Qwen3.8-27B` local, t = 1.0 | 28 | +0.1011 to +0.6679 |
| `qwen/qwen3.8-27b` hosted, t = 1.0 | 28 | +0.1405 to +0.5062 |

A model that agreed with itself would score +1.0. At temperature 0 it agrees
with itself at only 0.57 to 0.73. **Temperature 0 does not make a listwise
forecast deterministic**, because the arm order is part of the prompt.

This is the reason for the ensemble. Each of the 8 draws reshuffles the arms,
and the mean averages the position effect away. The order is written into every
record (`arm_order`), so the effect can be measured later rather than assumed.

---

## 8. OPEN QUESTION — which metric matches Tier 3 scoring

**We do not resolve this. It changes which configuration looks best.**

**The problem with within-cell r on Broockman.** 27 of the 42 cells hold only 3
or 4 arms (`index.csv`, `cells` 42 against `cells5` 15). A Pearson correlation
over 3 points is nearly always close to +1 or -1. Those cells carry almost no
information, and they dominate the average.

**Measured: the score falls as the cell gets larger.** Mean |r| for each cell
size, over the 42 Broockman cells of the `qwen3.8-27b` pointwise run
(`modelbench/output/tier3/runs/2026-08-30_qwen3.8-27b_broockman_pointwise_t10/forecast.jsonl`,
fields `value_truth_units` and `human`):

| Arms in the cell | Cells | Mean \|r\| |
|---|---|---|
| 3 | 16 | **0.830** |
| 4 | 11 | 0.612 |
| 5 | 12 | **0.441** |
| 6 | 1 | 0.590 |
| 7 | 2 | **0.248** |

That is a property of the metric, not of the forecaster. Three points fit a
line almost perfectly whatever the three points are.

**The three metrics rank the three PREDICTORS in three different orders.** This
is the sharpest form of the problem. The same three sets of predictions, scored
three ways, give three different winners. All from the same file as the table
above; `gpt4` and `expert` are the published gpt-4 and human-expert forecasts
that the archive carries for the same 172 arms.

| Predictor | within-cell | within, >= 5 arms | pooled over 172 arms |
|---|---|---|---|
| ours, `qwen3.8-27b` pointwise | +0.1450 (3rd) | -0.0360 (3rd) | **+0.3237 (1st)** |
| gpt-4, published | +0.1999 (2nd) | +0.0246 (2nd) | +0.2329 (2nd) |
| human experts, published | **+0.2546 (1st)** | **+0.2008 (1st)** | +0.1486 (3rd) |

Read the columns. On within-cell r the human experts win and we come last. On
pooled r we win and the human experts come last. **Nothing about the
predictions changed between those two columns.** Only the metric changed.

**Why this is not academic.** `docs/EVIDENCE.md` section 3 says "we are above
both reference points on Broockman". That claim is true on within-cell r. It is
also true on pooled r. It is **not** true of the pointwise run on the cells
that carry information, where we are below both. Which sentence is the honest
summary depends on a metric choice we have not been able to make.

**Restricting to cells with 5 arms or more changes the picture.**
Source: `modelbench/output/tier3/TESTS.txt` section 5, 15 cells.

| Model | listwise | pointwise | difference | t | p | wins |
|---|---|---|---|---|---|---|
| `qwen/qwen3.8-27b` | **+0.2855** | **-0.0360** | +0.3216 | +2.43 | **0.0293** | 11/15 |
| `qwen/qwen3.8-flash` | +0.3157 | +0.1013 | +0.2143 | +1.23 | 0.2402 | 9/15 |
| `Qwen/Qwen3.8-27B` local | +0.2499 | +0.0189 | +0.2311 | +1.37 | 0.1922 | 9/15 |

On the cells that carry information, the pointwise mode is **at or below
zero** for the 27b models. The listwise gain gets larger, not smaller.

**Pooled r is a different number again.** One correlation over all 172 arms at
one time. Source: `index.csv`, column `pooled`.

| Run | within-cell r | pooled r |
|---|---|---|
| `Qwen3.8-27B` local, t = 1.0 | +0.3215 | **+0.5076** |
| `Qwen3.8-27B` local, t = 0.85 | +0.3398 | +0.4900 |
| `qwen3.8-27b`, t = 1.0 | +0.3468 | +0.4620 |
| `qwen3.8-flash`, t = 0.85 | +0.3920 | +0.4423 |
| `qwen3.8-flash`, t = 1.0 | +0.3217 | +0.4226 |
| `qwen3.8-flash`, t = 0.5 | +0.4091 | +0.4178 |
| `qwen3.8-27b`, t = 0.5 | +0.3410 | +0.3586 |

**The two metrics do not rank the runs the same way.** `qwen3.8-flash` t = 0.5
is the best run on within-cell r and the sixth of seven on pooled r. The local
27b run at t = 1.0 is the reverse.

**Why this is unresolved.** Tier 3 asks for 208 rows — 16 interventions by 13
outcomes — and scores them together. That is structurally a **pooled**
correlation, not a mean of within-cell correlations. If pooled r is the right
match, the local 27b run at t = 1.0 is the best configuration in the grid, not
the flash run.

**But pooled r also rewards the wrong skill on Broockman.** Broockman's cells
are different policy issues. A pooled correlation over 172 arms rewards knowing
which **issue** moves most, not only which **message** moves most. The target
megastudy has one topic, so that part of the skill does not transfer.

**OPEN QUESTION, stated plainly. Do not resolve this from the numbers
alone.** Tier 3 submits 208 rows and they are scored together, which is
structurally a pooled correlation, not a mean of within-cell correlations.
Every method choice in this project was made on **within-cell r**, because that
is the metric Ashokkumar et al. use. **If pooled r is the scored quantity, the
project optimised the wrong metric all along**, and the local 27b run at
t = 1.0 — pooled r +0.5076, the best in the grid — is the configuration that
should have been submitted, not the t = 0.85 run.

**What must happen next.** Read the benchmark preregistration and find the
exact scored quantity, before any method choice rests on either metric. We do
not have that answer and we do not guess at it. This is also flagged in
`modelbench/tier3_index.py` lines 15-20.

**What this does NOT change.** The submitted file is fixed and the lock is
2026-08-31. The two configurations are close: the submitted run scores +0.3398
within-cell and +0.4900 pooled; the t = 1.0 run scores +0.3215 and +0.5076
(`index.csv`). No paired test separates them (0 of 46 temperature tests, 5b).
So the metric question changes which run *looks* best; on this evidence it does
not change which run *is* best.

---

## 9. Stimulus provenance changes the answer

**What happened.** The first Voelkel runs sent one-line paraphrases of each
treatment, taken from Table 2 of the paper. The real treatment texts are on the
study's own OSF page, doi `10.17605/OSF.IO/2MCF8`, and were already on disk at
`ashokkumar_bench/data/osf/materials/`.

Source: `modelbench/output/tier3/TESTS.txt` section 9.

| Stimulus sent | within-cell r (4 cells) |
|---|---|
| One-line paraphrase, from the paper's Table 2 | +0.2720 |
| The real treatment text, from OSF | **+0.3101** |

Difference +0.0381, t = +0.47, p = 0.6735. **Not significant with 4 cells.**

**RETRACTED: "the real stimulus texts unlocked backfire prediction."** An
earlier note said that. It is wrong, and we withdraw it. The counts matched by
coincidence. **The r gain of +0.0381 still stands. The interpretation does
not.**

A *backfire* is an arm whose true effect goes the **wrong** way: a message
meant to raise belief that lowers it. Voelkel has four such arm-outcome pairs.
Here is what each run actually predicted, from
`modelbench/output/runs/2026-08-30_flash_direct_voelkel_v3_fulltext/forecast.jsonl`
(fields `value` and `human`, meaned over the 50 draws of each arm):

| Cell | Arm | True effect | Predicted, real texts |
|---|---|---|---|
| belief | `Warmth Framing` | **-0.307** | **+2.91** |
| concern | `Warmth Framing` | **-0.779** | **+4.14** |
| policies | `Warmth Framing` | **-0.765** | **+4.20** |
| policies | `Consensus Framing 1` | **-0.513** | **+4.57** |

**Every real backfire was predicted strongly positive.** Not one was found.

And the negative predictions the run did make were all on the wrong arm:

- The paraphrase run predicted a **positive** effect for every one of the 40
  arms. It could not produce a negative number at all.
- The real-text run predicted **one negative effect in each of the four
  cells** — four negatives in all.
- **All four fell on `Binding Framing`**, whose true effect is **positive** in
  every outcome: +0.258 on belief, +0.458 on concern, +1.525 on intent,
  +0.038 on policies.

So the real text changed *whether* the model can write a negative number. It
did not change *which* arm the model puts it on. Four negative predictions and
four true backfires, and the overlap is zero.

**The lesson that survives.** Send the real stimulus, because sending a
paraphrase removes the model's ability to predict a negative effect at all, and
because it scores +0.0381 higher. Do **not** claim it predicts backfires. The
target megastudy's 16 texts are shipped verbatim in `survey/`, so sending the
real text costs nothing to get right.

---

## 10. What we did NOT measure

Say this plainly too.

- **We did not run a contamination probe.** `structured_forecast.py` has a
  `--contamination-check` mode with two probes (author identification and free
  recall). No `CONTAMINATION.txt` exists in any run directory. The prompt does
  not name the study, which is the guard we rely on instead
  (`METHOD.md` section 7). Registration item I.4 says this.
- **We did not test whether the Voelkel gap against gpt-4 is significant.**
  With 4 cells we could not.
- **We did not fit a calibration shrink.** The preregistration
  (`notes/PREREG_broockman_method_search.md` section 8) specifies one, fitted
  on the three donor studies with Broockman excluded. It was never fitted. It
  is a monotone linear map, so it cannot change a Pearson correlation or any
  ranking; it changes only the calibration slope and the RMSE. Registration
  item G.3 records that no calibration was applied.
- **We did not test a larger model.** No paid call outside the measured spend
  was approved.
- **We ran no more configurations than we scored.** All 32 runs are in
  `index.csv`, winners and losers together.

---

## 11. The full grid, all 32 runs

Source: `modelbench/output/tier3/index.csv`, produced by
`modelbench/tier3_index.py`. `spend` is in United States dollars.
`Qwen3.8-27B-local` is `Qwen/Qwen3.8-27B` on local weights and always costs
$0.00.

```
            model       study      mode    temp  arms  cells  within  within5  pooled  parsed_pct   spend
Qwen3.8-27B-local   broockman  listwise +0.0000   172     42 +0.2657  +0.1839 +0.3886       100.0 +0.0000
Qwen3.8-27B-local   broockman  listwise +0.8500   172     42 +0.3398  +0.2153 +0.4900       100.0 +0.0000
Qwen3.8-27B-local   broockman  listwise +1.0000   172     42 +0.3215  +0.2499 +0.5076        99.6 +0.0000
      qwen3.8-27b   broockman  listwise +0.0000   172     42 +0.2575  +0.1883 +0.4568       100.0 +0.0106
      qwen3.8-27b   broockman  listwise +0.5000   172     42 +0.3410  +0.3040 +0.3586       100.0 +0.0439
      qwen3.8-27b   broockman  listwise +0.8500   172     42 +0.2899  +0.2080 +0.3911        99.6 +0.0401
      qwen3.8-27b   broockman  listwise +1.0000   172     42 +0.3468  +0.2855 +0.4620        97.2 +0.0457
      qwen3.8-27b   broockman  listwise +1.6000   172     42 +0.1544  +0.2429 +0.0591        87.1 +0.0437
    qwen3.8-flash   broockman  listwise +0.0000   172     41 +0.4400  +0.4138 +0.4049        95.6 +0.0054
    qwen3.8-flash   broockman  listwise +0.5000   172     42 +0.4091  +0.4310 +0.4178        99.7 +0.0238
    qwen3.8-flash   broockman  listwise +0.8500   172     42 +0.3920  +0.2553 +0.4423        98.9 +0.0140
    qwen3.8-flash   broockman  listwise +1.0000   172     42 +0.3217  +0.3157 +0.4226        93.8 +0.0285
    qwen3.8-flash   broockman  listwise +1.6000   172     42 +0.2278  +0.0945 +0.2436        79.2 +0.0165
Qwen3.8-27B-local   broockman pointwise +1.0000   172     41 +0.2152  +0.0189 +0.3585       100.0 +0.0000
      qwen3.8-27b   broockman pointwise +1.0000   172     42 +0.1450  -0.0360 +0.3237       100.0 +0.1001
    qwen3.8-flash   broockman pointwise +1.0000   172     42 +0.2501  +0.1013 +0.3713        92.6 +0.0343
Qwen3.8-27B-local voelkel2025  listwise +0.0000    40      4 +0.5952  +0.5952 +0.5252       100.0 +0.0000
Qwen3.8-27B-local voelkel2025  listwise +0.8500    40      4 +0.6485  +0.6485 +0.5363       100.0 +0.0000
Qwen3.8-27B-local voelkel2025  listwise +1.0000    40      4 +0.6454  +0.6454 +0.5359       100.0 +0.0000
      qwen3.8-27b voelkel2025  listwise +0.0000    40      4 +0.5803  +0.5803 +0.4560       100.0 +0.0062
      qwen3.8-27b voelkel2025  listwise +0.5000    40      4 +0.6600  +0.6600 +0.5579       100.0 +0.0278
      qwen3.8-27b voelkel2025  listwise +0.8500    40      4 +0.6596  +0.6596 +0.5331        96.9 +0.0249
      qwen3.8-27b voelkel2025  listwise +1.0000    40      4 +0.6558  +0.6558 +0.5516        96.9 +0.0280
      qwen3.8-27b voelkel2025  listwise +1.6000    40      4 +0.4086  +0.4086 +0.1877        90.6 +0.0283
    qwen3.8-flash voelkel2025  listwise +0.0000    40      4 +0.6560  +0.6560 +0.5905       100.0 +0.0049
    qwen3.8-flash voelkel2025  listwise +0.5000    40      4 +0.6527  +0.6527 +0.5539        93.8 +0.0061
    qwen3.8-flash voelkel2025  listwise +0.8500    40      4 +0.6385  +0.6385 +0.5608        87.5 +0.0047
    qwen3.8-flash voelkel2025  listwise +1.0000    40      4 +0.5877  +0.5877 +0.4409        71.9 +0.0229
    qwen3.8-flash voelkel2025  listwise +1.6000    40      4 +0.5203  +0.5203 +0.4512        81.6 +0.0050
Qwen3.8-27B-local voelkel2025 pointwise +1.0000    40      4 +0.5916  +0.5916 +0.4878       100.0 +0.0000
      qwen3.8-27b voelkel2025 pointwise +1.0000    40      4 +0.5795  +0.5795 +0.4515       100.0 +0.0337
    qwen3.8-flash voelkel2025 pointwise +1.0000    40      4 +0.4151  +0.4151 +0.3774        95.6 +0.0148
```

`gpt4_within` is +0.1999 on every Broockman row and +0.7454 on every Voelkel
row. `expert_within` is +0.2546 on every Broockman row and is empty on Voelkel,
because that archive holds no expert forecast.

The t = 0.0 runs used **2 draws**, not 8. Every other run used 8.

---

## 12. What the evidence supports, and what it does not

**Supported — as EXPLORATORY evidence only.** Every item below was selected
after seeing 34 runs. None of it is confirmatory. See section 13.

1. Listwise beats pointwise. Six tests, one sign, one of them at p < 0.05. This
   is the strongest evidence in the file, because it does not rest on one test:
   all six differences have the same sign, on three models and two studies.
2. The direct forecast beats our own per-respondent simulation on Broockman.
   p = 0.0073, wins 30 of 42 cells. **The true false-positive rate is higher
   than 0.0073.**
3. We are above published gpt-4 and above human expert forecasters on
   Broockman **on within-cell r and on pooled r**. Not on the 15 large cells,
   for the pointwise run (section 8).
4. Sending the real stimulus text is better than sending a paraphrase.
5. The same weights served locally and served through a provider give the same
   score.

**Not supported.**

1. Any claim that a particular model is better. flash and 27b are not
   separable (5a).
2. Any claim that a particular temperature is better. 0 of 46 tests (5b).
3. Any claim that a demographic block helps (5c).
4. Any claim that a framing ensemble helps (5d).
5. Any claim that we will beat gpt-4 on the target. On the study that most
   resembles it, we do not (section 4).
6. Any claim about backfire prediction. **Retracted** (section 9). All four
   true Voelkel backfires were predicted strongly positive.
7. Any claim that the population block helps. Four tests, none significant, and
   the one on the shipped template gives -0.0029 (p = 0.8671) and +0.0024
   (p = 0.3910). It is in the submitted prompt for consistency with our Tier 1
   entry, not for accuracy (section 5c).

**Unresolved, and it needs a human.** The four preregistration breaches in
section 13, and the spend approval gap in `registration.md` item K.3.

**Unresolved.** Which metric matches Tier 3 scoring (section 8). Tier 3 scores
208 rows together, which is structurally a **pooled** correlation, and every
choice in this project was made on **within-cell** r. The three metrics rank
the three predictors — us, gpt-4 and the human experts — in three different
orders. **Check this against the benchmark preregistration.** We flag it and do
not resolve it.

---

## 13. The preregistration breaches

**This section exists because the honest report of a result includes how it was
selected.** `notes/PREREG_broockman_method_search.md` was written on
2026-08-29, before any configuration was scored. It fixed the development set,
the held-out set, the endpoint, the statistical test and the number of
configurations we were allowed to try. **The work then broke four of its own
rules.**

| # | The rule, and where it is written | What we actually did | The cost |
|---|---|---|---|
| 1 | "AT MOST SIX configurations may be scored on Broockman. A seventh configuration voids the comparison." PREREG lines 77-78. | `modelbench/output/tier3/runs/` holds **34 run directories, 17 of them on Broockman**. `index.csv` indexes 32, 16 on Broockman. | By the rule's own words the comparison is **void**. Any p value below is a p value chosen from many. |
| 2 | The held-out set `voelkel2025` "is scored ONE TIME, at the end, on the single winning configuration." PREREG lines 26-27. | **Scored 17 times**, on 17 configurations (`modelbench/output/tier3/runs/*voelkel2025*`). | **We have no held-out set.** Voelkel became a second development set. Section 4's Voelkel numbers cannot confirm anything selected on Broockman. |
| 3 | The test is a **paired bootstrap**: 10,000 resamples of the 42 cell indices, a 95 per cent percentile interval, and a minimum mean difference of **0.14**. PREREG lines 55-60. | We report a **paired t-test** (`modelbench/tier3_tests.py:63`, `scipy.stats.ttest_rel`). **No bootstrap interval for any Tier 3 comparison exists on disk.** | The preregistered decision rule was never applied. **No configuration was ever formally accepted or rejected.** Note that the headline difference, +0.2174, would have cleared the 0.14 threshold; the interval was never computed, so we cannot say whether it would have cleared the interval. |
| 4 | Configuration 1, `baseline_seed2`, is the abandonment check: if a second seed of the baseline moves the score by more than 0.14, the noise floor is larger than the effect and the search stops. PREREG section 7 row 1 and section 10. | **Never run.** No `baseline_seed2` run directory exists. | **We never measured our own noise floor.** For any difference smaller than 0.14 we cannot say how much is signal. That covers every null in section 5 and the model-choice differences in 5a. |

### What this changes, and what it does not

**It changes the inference.** Every result in this file is **EXPLORATORY**. The
p values are real arithmetic on real data, but they are not the false-positive
rates of a preregistered test, because the number of comparisons available was
not fixed in advance. **The p = 0.0073 headline was selected after seeing 34
runs, so its true false-positive rate is higher than 0.0073.** We cannot say
how much higher.

**It does not change the data.** Every measurement in this file is real,
reproducible and unfabricated. Every run directory holds its own prompts, its
own raw generations, its own seed and its own score. `index.csv` lists every
run, the losers with the winners. No run was dropped, no run was repeated to a
better number, and no result was reported selectively.

**It does not change the submitted forecast.** The submitted file rests on the
**listwise design**, and the evidence for listwise is not one p value: six
paired tests, on three models and two studies, all of the same sign
(section 1). It does not rest on the p = 0.0073 comparison, which measures the
direct forecast against our own Tier 1 method and decides nothing about the
prompt that shipped.

**A human must decide what to do about this before the lock**, and the choice
is stated in `registration.md` item J.2: keep the entry with the declaration
attached, or re-run the preregistered test as written.

---

## 14. The benchmark's own Tier 3 metrics — how you ask, and which model

*Added 2026-08-31. Every number here comes from
`raw_data_deposit/method_search/`, which holds all 80 runs. It answers the
OPEN QUESTION of section 8.*

Sections 1 to 13 score with the **within-cell** correlation of Ashokkumar et
al. **That is not what this benchmark computes.** A Tier 3 entry is eligible
for exactly two preregistered analyses, and both **pool** every intervention x
outcome pair into one number:

> "Tier 3 - Average treatment effect predictions. Eligible for ATE recovery and
> the calibration regression. *Grain: 1 row = 1 intervention x outcome
> estimate.*" - benchmark preregistration, *Analysis eligibility by tier*

Section 14 computes those two analyses with the preregistration's own formulas
(`pooled_metrics()`, `adjusted_metrics()`, `run_calibration_pooled()`). Every
estimate is first put into **percentage points (pp) of its outcome's scale
range**, as the benchmark requires.

**The six metrics.** `dir %` is the share of pairs where the predicted effect
has the same SIGN as the human effect. `Spearman rho` is the rank correlation.
**`Pearson r` is the benchmark's key metric.** `r adj` corrects it for the
sampling noise in the human effects. `RMSE` is the average size of the errors
in pp; read it against the "no effect anywhere" null. `alpha` and `beta` are
the calibration intercept and slope, perfect at 0 and 1.

---

### 14.1 THE MAIN FINDING — how you ASK beats which model you ask

Same model, same temperature (1.0), same 8 draws, same six-slot prompt. The
only thing that changes is whether the model sees **all arms of a cell in one
call** (`listwise`) or **one arm for each call** (`pointwise`).

| archive | model | mode | dir % | Spearman rho | **Pearson r** | r adj | RMSE pp |
|---|---|---|---|---|---|---|---|
| broockman | Qwen3.8-27B | **listwise** | **80.8** | **+0.5640** | **+0.5076** | **+0.6083** | **5.208** |
| | | pointwise | 77.9 | +0.3430 | +0.3585 | +0.4297 | 5.579 |
| broockman | qwen3.8-27b | **listwise** | **82.0** | **+0.5155** | **+0.4620** | **+0.5537** | **5.320** |
| | | pointwise | 79.1 | +0.3512 | +0.3237 | +0.3879 | 5.650 |
| broockman | qwen3.8-flash | **listwise** | **80.8** | **+0.4878** | **+0.4226** | **+0.5065** | **5.838** |
| | | pointwise | 77.3 | +0.4665 | +0.3713 | +0.4450 | 7.808 |
| voelkel2025 | Qwen3.8-27B | **listwise** | 85.0 | +0.4968 | **+0.5359** | **+0.5824** | 1.175 |
| | | pointwise | 85.0 | +0.5052 | +0.4878 | +0.5302 | **1.052** |
| voelkel2025 | qwen3.8-27b | **listwise** | 85.0 | **+0.5193** | **+0.5516** | **+0.5995** | 1.168 |
| | | pointwise | 85.0 | +0.4474 | +0.4515 | +0.4907 | **1.090** |
| voelkel2025 | qwen3.8-flash | **listwise** | **82.5** | +0.4432 | **+0.4409** | **+0.4792** | 1.393 |
| | | pointwise | 80.0 | +0.5539 | +0.3774 | +0.4102 | **1.311** |

**Listwise wins Pearson r in 6 of 6 comparisons.** Three models, two archives,
no exception. The mean gain is **+0.113 on Broockman and +0.071 on Voelkel**,
**+0.092 over all six.** On Broockman listwise wins EVERY metric for all three
models.

**Two honest limits.** On Voelkel, pointwise has the better RMSE in all three
comparisons: asking about one arm at a time gives better-SIZED effects.
Pointwise also wins Spearman rho in 2 of 3 there. So listwise improves the
LINEAR agreement and does not improve the ORDERING.

**Why this is the finding, and the model ranking is not.** The direction of the
listwise effect is the same in every comparison we made. The direction of the
model effect is not: `Gemma4-26B` wins Voelkel and loses both Doell and
Broockman (section 14.2). A design choice that points the same way across every
model and every archive is a result. A model ranking that reverses by archive
is a local fact about that archive.

**This is why the entry is listwise.** It is the one factor of the search that
behaved the same way everywhere.

---

### 14.2 The models — all seven, on three public archives

All runs below are `listwise`, temperature 0.5, 8 draws, seed 1, reasoning off.
The submission model is marked.

**voelkel2025 - 10 interventions x 4 outcomes = 40 pairs**
*(human effect SD 1.020 pp, mean human standard error 0.397 pp)*

| model | served by | dir % | Spearman rho | Pearson r | r adj | RMSE pp | alpha | beta |
|---|---|---|---|---|---|---|---|---|
| Gemma4-26B | local vLLM | 80.0 | **+0.6310** | **+0.5898** | **+0.6410** | **0.888** | +0.343 | +0.647 |
| **Qwen3.8-27B** *(submitted)* | local vLLM | 85.0 | +0.5832 | +0.5884 | +0.6395 | 1.111 | +0.551 | +0.456 |
| qwen3.8-flash | OpenRouter | 80.0 | +0.5975 | +0.5539 | +0.6020 | 1.386 | +0.627 | +0.358 |
| deepseek-v4-flash | OpenRouter | 85.0 | +0.4914 | +0.4571 | +0.4968 | 0.937 | +0.476 | **+0.756** |
| glm-5.3-flash | OpenRouter | **87.5** | +0.4727 | +0.4434 | +0.4819 | 0.942 | +0.467 | +0.623 |
| Gemma4-E4B | local vLLM | 82.5 | +0.4021 | +0.4242 | +0.4611 | 9.585 | +0.619 | +0.070 |
| mean of 3 local models | — | 80.0 | +0.5217 | +0.4949 | +0.5379 | 3.541 | +0.494 | +0.190 |
| gpt-4, published | — | — | +0.6615 | +0.6957 | +0.7561 | — | — | — |
| **null: no effect anywhere** | — | 0.0 | — | — | — | **1.597** | — | — |

**doell - 11 interventions x 2 outcomes = 22 pairs**
*(human effect SD 1.706 pp, mean human standard error 1.539 pp)*

| model | dir % | Spearman rho | Pearson r | r adj | RMSE pp | alpha | beta |
|---|---|---|---|---|---|---|---|
| **Qwen3.8-27B** *(submitted)* | 100.0 | **+0.5280** | **+0.5572** | *1.0000* | 2.376 | +1.800 | **+1.065** |
| mean of 3 local models | 100.0 | +0.4478 | +0.4972 | *1.0000* | 2.260 | +1.731 | +1.003 |
| Gemma4-E4B | 100.0 | +0.2897 | +0.3296 | *0.7836* | **1.937** | +2.717 | +0.381 |
| Gemma4-26B | 95.5 | +0.2885 | +0.3082 | *0.7327* | 3.057 | +3.160 | +0.584 |
| gpt-4, published | — | +0.3992 | +0.4374 | *1.0000* | — | — | — |
| human experts, published | — | +0.4692 | +0.4960 | *1.0000* | — | — | — |
| **null: no effect anywhere** | 0.0 | — | — | — | **4.299** | — | — |

*No hosted-model run exists on Doell. `r adj` is in italics because it is
DEGENERATE here, not excellent: Doell's sampling noise is 2.09 times its true
signal, so the correction divides by a nearly vanished variance and clips at
1.0000. Read the raw correlation only. Doell's `dir %` is also empty of
information: all 11 human effects are positive, so "everything helps" scores
100 per cent for free.*

**broockman - 172 messages x 1 outcome = 172 pairs**
*(human effect SD 5.900 pp, mean human standard error 3.229 pp)*

| model | served by | dir % | Spearman rho | Pearson r | r adj | RMSE pp | alpha | beta |
|---|---|---|---|---|---|---|---|---|
| **Qwen3.8-27B** *(submitted)* | local vLLM | 79.7 | +0.4678 | **+0.4641** | **+0.5562** | **5.373** | −1.956 | +1.798 |
| glm-5.3-flash | OpenRouter | 79.7 | +0.3978 | +0.4280 | +0.5130 | 5.484 | −1.798 | **+1.097** |
| qwen3.8-flash | OpenRouter | **80.2** | **+0.4876** | +0.4178 | +0.5007 | 5.854 | **−0.947** | +0.773 |
| deepseek-v4-flash | OpenRouter | 79.7 | +0.3207 | +0.3596 | +0.4310 | 5.527 | −1.664 | +1.321 |
| Gemma4-26B | local vLLM | 75.0 | +0.3659 | +0.2919 | +0.3498 | 6.137 | +1.178 | +0.471 |
| mean of 3 local models | — | 72.7 | +0.2482 | +0.2184 | +0.2617 | 6.481 | +1.991 | +0.323 |
| Gemma4-E4B | local vLLM | 69.8 | +0.1742 | +0.0946 | +0.1134 | 10.602 | +3.163 | +0.063 |
| gpt-4, published | — | — | +0.2816 | +0.2329 | +0.2791 | — | — | — |
| human experts, published | — | — | +0.1253 | +0.1486 | +0.1780 | — | — | — |
| **null: no effect anywhere** | — | 0.0 | — | — | — | **6.884** | — | — |

**What the model table says.**

1. **The submission model wins two of the three archives** and is second on
   the third by 0.0014, which is a tie.
2. **It beats published gpt-4 and the human expert forecasters on both
   archives where those baselines exist.** Broockman: +0.4641 against +0.2329
   and +0.1486. Doell: +0.5572 against +0.4374 and +0.4960. On Voelkel it is
   behind gpt-4 (+0.6957).
3. **No model wins everywhere.** `Gemma4-26B` is first on Voelkel and next to
   last on Doell. That reversal is the reason we do not read a model ranking
   as a finding.
4. **The mean of three models is never the best on any archive**, and on
   Voelkel its RMSE (3.541 pp) is worse than predicting no effect at all
   (1.597 pp). One model in that average, `Gemma4-E4B`, overshoots by about 14
   times, and a plain mean gives it a third of the weight. **We do not submit
   an ensemble.**
5. **A second seed does not change the winner** on any archive. The second
   seed of every local run is in `raw_data_deposit/method_search/`.

---

### 14.3 Reasoning ON — 12 runs, and why it is not used

`Qwen3.8-27B` at `reasoning_effort = xhigh` (its highest; its ladder is `low`,
`medium`, `xhigh`, and there is no `high`) and both Gemma models with
`enable_thinking = true`.

**It improved the calibration of every model on every archive**, with no
exception: every `alpha` moved toward 0 and every `beta` toward 1.
`Gemma4-26B` with reasoning is the only configuration we have measured whose
`alpha` interval contains 0 AND whose `beta` interval contains 1, on both
archives.

**It produced no new best score on either archive.** The best Pearson r on
Voelkel (+0.6439) and on Broockman (+0.4706) both come from runs with
reasoning OFF.

**Its effect on accuracy reverses by archive for the same model.** Reasoning
lifts `Qwen3.8-27B` on all six Voelkel metrics and lowers it on all six
Broockman metrics.

**It is not affordable.** `Qwen3.8-27B` wrote 3,900,296 output tokens for 336
Broockman calls, **408 times** the 9,567 of the same calls without reasoning,
in 80.8 minutes against 0.64. 7 of 32 Voelkel calls ran past a 20,480-token
budget and are recorded unparsed, a 78.1 per cent parse rate, the worst in the
project.

**Reasoning is a calibration fix, and calibration is the cheaper problem.** A
linear rescale does the same work for nothing and cannot change a correlation.
Its catch is that a rescale needs the human answers, and the target study is
sealed.

---

### 14.4 What is deposited, and what is not

`raw_data_deposit/method_search/` holds **all 80 runs** — 74 scored
configurations and 6 smoke tests — with an `INDEX.csv` and a sha256 for each
file. 1.68 MB gzipped. Its `README.md` states the one important limit:
**the verbatim replies were not kept.** The pipeline parses each reply to
numbers and stores the text only when the parse was incomplete, cut to 400
characters — 1.0 to 1.9 per cent of records. The deposit says what each model
ANSWERED for every arm of every draw. It does not say what each model SAID.

**Everything in section 14 is EXPLORATORY.** See item J.2 of the registration
form. The measurements are real and reproducible. The inference is not
confirmatory.
