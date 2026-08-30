#!/usr/bin/env python3
"""
The target megastudy as ONE study spec for `forecast/core.render`.

ONE CELL = ONE OUTCOME. The study has 13 preregistered outcomes and 16 text
interventions. A listwise call therefore asks for 16 numbers at a time, and
13 cells x 8 draws = 104 calls cover the whole 208-cell grid.

THE STUDY IS NEVER NAMED. No prompt holds the name of the study, its authors,
the benchmark, the site or the preregistration. A name is the one feature that
is observed to make a model recall a published result instead of estimate one.

WHAT EACH SLOT HOLDS.
  STUDY     the design and the sample. Variant B adds the recruitment-target
            table of `forecast/materials/quotas_18000.csv`.
  OUTCOME   every item of the composite, with both anchors, re-pointed so a
            HIGHER number is always MORE of the thing that the outcome names.
  ESTIMAND  the OLS coefficient against control, with gender, age and race as
            covariates, and a Benjamini-Hochberg correction inside each
            outcome.
  ARMS      the 16 intervention texts, in a random order for each call.
  ASK       one line for each intervention, with the units of THIS outcome.

THE DIRECTION RULE. Every prompt is written on the SAME scale that the
submission uses. So the returned number needs no turn, and `scale_flip` is
False for all 13 outcomes. The flag is still computed, written into every
record and printed by the dry run, so the claim can be audited and is not just
asserted. `funding_perceptions` is the case that needs care: the submission
defines it as `100 - funding_5` (codebook.csv:53), so the prompt prints the
item WITH ITS ANCHORS ALREADY SWAPPED and a positive effect means more support
for climate research funding.

**Written in ASD-STE100 Simplified Technical English.**
"""
from __future__ import annotations

import csv
import json
import math
import textwrap
from pathlib import Path

import core
from core import wrap, Opt

ROOT = Path(__file__).resolve().parents[1]
MAT = ROOT / "forecast/materials"
STIM_DIR = MAT / "stimuli"
OUTCOMES_JSON = MAT / "outcomes.json"
STIM_INDEX = MAT / "stimuli_index.json"
QUOTAS = MAT / "quotas_18000.csv"

STUDY_KEY = "megastudy"

# The 16 conditions, in the order of scripts/lib/submission_spec.R:14-31.
# `forecast/extract_materials.py` checks this order against that file.
INTERVENTIONS = json.loads(STIM_INDEX.read_text()) if STIM_INDEX.exists() else {}
OUTCOME_BLOCKS = (json.loads(OUTCOMES_JSON.read_text())
                  if OUTCOMES_JSON.exists() else {})

# The units of the submitted `ate` for each answer kind.
#   slider100  the model answers in points of the 0-100 scale, and the
#              submission wants points of the 0-100 scale. Factor 1.
#   dollars    the model answers in dollars, and the submission wants dollars
#              (codebook.csv:25, "$0-$10 in whole-dollar choices"). Factor 1.
#   percent    the model answers in PERCENTAGE POINTS of the sign-up rate, and
#              the submission wants a change of the 0-1 PROPORTION
#              (codebook.csv:54). Factor 0.01.
#              WHY PERCENTAGE POINTS AND NOT A PROPORTION. Both roads end at a
#              proportion. They differ in what a mistake costs. Asked for a
#              proportion, a model that thinks in percent writes `4` and the
#              submitted value is 100x too large. Asked for percentage points,
#              a model that thinks in proportions writes `0.04` and the
#              submitted value is 100x too small, that is, near zero, which
#              scores like a null and not like an absurdity. The one-sided
#              risk decides it. `forecast/build_predictions.py` prints the
#              magnitude audit that finds the failure if it happens.
UNIT_FACTOR = {"slider100": 1.0, "dollars": 1.0, "percent": 0.01}
UNIT_NAME = {"slider100": "points of the 0-100 outcome scale",
             "dollars": "US dollars, on the 0-10 donation scale",
             "percent": "change of the 0-1 sign-up proportion"}
# The parser range for each kind. It rejects a number that cannot be an effect
# on this scale.
VALUE_RANGE = {"slider100": (-100.0, 100.0), "dollars": (-10.0, 10.0),
               "percent": (-100.0, 100.0)}


# ----------------------------------------------------------------- cells --
def load_cells(outcomes: list[str] | None = None) -> list[dict]:
    """One cell for each outcome. Every cell holds the same 16 arms."""
    if not INTERVENTIONS or not OUTCOME_BLOCKS:
        raise SystemExit("run forecast/extract_materials.py first")
    arms = []
    for title, fn in INTERVENTIONS.items():
        arms.append({"text": title,
                     "stimulus": (STIM_DIR / fn).read_text().strip(),
                     "human": math.nan, "gpt4": math.nan,
                     "expert": math.nan})
    cells = []
    for name, block in OUTCOME_BLOCKS.items():
        if outcomes and name not in outcomes:
            continue
        cells.append({"cell_id": f"{STUDY_KEY}/{name}", "_study": STUDY_KEY,
                      "outcome": name, "block": block,
                      "n_conditions": 17, "n_participants": 18000,
                      "arms": arms})
    return cells


# ----------------------------------------------------------------- STUDY --
def _quota_table() -> str:
    """The recruitment targets, from forecast/materials/quotas_18000.csv.

    EVERY NUMBER IN THIS TABLE COMES FROM THAT FILE. Nothing is computed and
    nothing is invented. The file is the benchmark preregistration's own quota
    table, projected to N = 18,000. It was copied from
    /home/jovyan/silicon-sample-submission/population/quotas_18000.csv,
    sha256 1383a768d5f4e3f8a2c22ccf18b1899eb6fbc7c3716cdfd18ccb3befb98e8028.
    Its columns are variable, category, total, male, female.
    """
    rows = list(csv.DictReader(QUOTAS.open()))
    age = [r for r in rows if r["variable"] == "Age"]
    race = [r for r in rows if r["variable"] == "Race / Ethnicity"]
    race.sort(key=lambda r: -int(r["total"]))
    hdr = f"{'total':>7}{'male':>9}{'female':>9}"
    out = ["  The sample was recruited to these targets:", "",
           f"    {'Age band':<26}{hdr}"]
    for r in age:
        out.append(f"      {r['category']:<24}{int(r['total']):>7,}"
                   f"{int(r['male']):>9,}{int(r['female']):>9,}")
    out += ["", f"    {'Race / ethnicity':<26}{hdr}"]
    for r in race:
        out.append(f"      {r['category']:<24}{int(r['total']):>7,}"
                   f"{int(r['male']):>9,}{int(r['female']):>9,}")
    return "\n".join(out) + "\n"


def megastudy_study(cell: dict) -> str:
    """The STUDY slot. The study, its team and the benchmark are NEVER named.

    The design and sample sentences paraphrase the public description of the
    study: a between-subjects experiment of 16 text interventions against a
    control condition, N about 18,000 US adults, 1,000 for each intervention
    plus 2,000 control, an opt-in panel, census-based cross quotas on
    gender x age and gender x race/ethnicity.

    The description also says the interventions are meant to INCREASE TRUST.
    That sentence is left out on purpose. It tells the model that all 16
    effects point the same way, which would flatten the ranking that the
    submission is scored on. The texts speak for themselves.
    """
    pop = "\n" + _quota_table() if Opt.population else ""
    return (
        wrap("A team of researchers ran a randomised controlled experiment on "
             "the public view of climate scientists. The experiment tested 16 "
             "short written texts against a control condition. The design is "
             "between subjects: each participant read ONE text, or read no "
             "text at all.")
        + "\n"
        + wrap("Participants were adults resident in the United States. They "
               "were recruited from a national non-probability opt-in online "
               "panel. Recruitment used census-based cross quotas on gender by "
               "age band and on gender by race and ethnicity. Every "
               "participant passed two attention checks. The checks were made "
               "BEFORE the assignment to a condition, so they cannot be "
               "affected by the text.")
        + pop
        + "\n"
        + wrap("About 18,000 people took part. About 1,000 people were "
               "assigned to each of the 16 texts, and about 2,000 people were "
               "assigned to the control condition. The control group read a "
               "short neutral text on an unrelated subject.")
        + "\n"
        + wrap("Each participant read the text one time only. The outcome was "
               "measured after the text, in the same session."))


# --------------------------------------------------------------- OUTCOME --
def megastudy_outcome(cell: dict) -> str:
    """The OUTCOME slot. It prints the items with both anchors.

    An item that the submission reverse-codes is printed WITH ITS ANCHORS
    SWAPPED. That is the published rule: re-point every scale so that a HIGHER
    number always means MORE of the thing named. Never ask the model to hold a
    negative direction in its head. `funding_perceptions` is the only item of
    this study that needs it (codebook.csv:53).
    """
    b = cell["block"]
    n, kind = b["n_items"], b["kind"]
    lines = [f"  After reading, everyone answered {n} "
             + ("item." if n == 1 else "items."), ""]

    if kind == "slider100":
        if b["rule"] == "mean":
            lines.append(f'  The outcome is "{b["label"]}". It is the MEAN of '
                         f"the {n} items.")
        elif b["rule"] == "reverse100":
            lines.append(f'  The outcome is "{b["label"]}". It is that one '
                         f"item, turned round so that a higher number means "
                         f"more of it.")
        else:
            lines.append(f'  The outcome is "{b["label"]}". It is that one '
                         f"item.")
        lines.append("  Every item is a slider from 0 to 100.")
    elif kind == "dollars":
        lines.append(f'  The outcome is "{b["label"]}". It is a whole number '
                     f"of US dollars, from 0 to 10.")
        lines.append("  The group score is the MEAN donation of the group, in "
                     "dollars.")
    else:
        lines.append(f'  The outcome is "{b["label"]}". Each participant '
                     f"either subscribed or did not.")
        lines.append("  The group score is the PERCENTAGE of the group that "
                     "subscribed. It runs")
        lines.append("  from 0% to 100%.")
    lines.append("")

    items = b["items"] if Opt.items == "all" else b["items"][:1]
    if Opt.items != "all" and n > 1:
        lines.append(f"  One of the {n} items, as an example:")
        lines.append("")
    for i, it in enumerate(items, start=1):
        q = textwrap.fill(" ".join(it["question"].split()), width=76,
                          initial_indent=f"    Item {i}. ",
                          subsequent_indent="            ")
        lines.append(q)
        if kind == "slider100":
            lines.append(f"            0 = {it['anchor_low']}")
            lines.append(f"            100 = {it['anchor_high']}")
        elif kind == "dollars":
            lines.append("            0 = keeps the whole bonus")
            lines.append("            10 = donates the whole bonus")
        else:
            lines.append("            The answer is yes or no.")

    top = "100" if kind == "slider100" else ("10 dollars" if kind == "dollars"
                                             else "100%")
    lines += ["",
              f"  The outcome score runs from 0 to {top}.",
              f"  0 is {b['low_end']}.",
              f"  {top} is {b['high_end']}.",
              f"  A HIGHER number always means MORE "
              f'"{b["label"]}".',
              ""]
    return "\n".join(lines)


# -------------------------------------------------------------- ESTIMAND --
def megastudy_estimand(cell: dict) -> str:
    """The estimand of the study's own preregistered analysis plan.

    Continuous outcomes: an OLS fit of the post-treatment outcome on a set of
    condition dummies, with the control condition as the omitted reference,
    and gender, age and race as covariates. Heteroskedasticity-robust standard
    errors. p-values corrected by the Benjamini-Hochberg false discovery rate
    procedure inside each outcome, not across outcomes.
    The binary sign-up outcome is fitted by logistic regression and reported
    as the average difference in the predicted probability.
    """
    b = cell["block"]
    if b["kind"] == "percent":
        stat = (
        "  In statistical words: the quantity is the average treatment effect\n"
        "  of the text on the sign-up rate. The model is a logistic regression\n"
        "  of the sign-up on the assigned condition, with the control\n"
        "  condition as the omitted reference level, and with gender, age and\n"
        "  race as covariates. The reported quantity is the average difference\n"
        "  in the predicted sign-up probability between the text group and the\n"
        "  control group. Standard errors are heteroskedasticity robust, and\n"
        "  p-values are corrected for multiple comparisons by the\n"
        "  Benjamini-Hochberg false discovery rate procedure inside this one\n"
        "  outcome.\n")
    else:
        stat = (
        "  In statistical words: the quantity is the average treatment effect\n"
        "  of the text on the outcome. It is the coefficient of the text in an\n"
        "  ordinary least squares regression of the outcome on the assigned\n"
        "  condition, with the control condition as the omitted reference\n"
        "  level, and with gender, age and race as covariates. Standard errors\n"
        "  are heteroskedasticity robust, and p-values are corrected for\n"
        "  multiple comparisons by the Benjamini-Hochberg false discovery rate\n"
        "  procedure inside this one outcome.\n")
    return (
        "  In plain words: how far did the text move the average answer of the\n"
        "  group that read it, compared with the control group that read no\n"
        "  text on this subject?\n"
        "\n" + stat)


# ------------------------------------------------------------ other slots --
def megastudy_arm_text(cell: dict, arm: dict) -> str:
    """The stimulus. The full text of the intervention, as the study shows it."""
    return arm["stimulus"]


def megastudy_ends(cell: dict) -> tuple[str, str]:
    return cell["block"]["low_end"], cell["block"]["high_end"]


def megastudy_flip(cell: dict) -> bool:
    """TRUE when the submitted `ate` points the other way from the prompt.

    It is False for all 13 outcomes, because every prompt is written on the
    same scale that the submission uses. Two cases were checked by hand:

      distrust_post       The item asks how much the person DISTRUSTS climate
                          scientists, 0 = not at all, 100 = very strongly
                          (codebook.csv:21). The submission does not reverse
                          it. The prompt therefore says 100 = very strong
                          distrust, and a text that builds trust gets a
                          NEGATIVE number here and a POSITIVE number on
                          trust_post. `forecast/build_predictions.py` tests
                          that sign disagreement on the finished values.
      funding_perceptions The submission defines it as 100 - funding_5
                          (codebook.csv:53), so the prompt prints the item
                          with the anchors ALREADY swapped: 100 = "the
                          government spends far too little". A positive number
                          is therefore more support for climate research
                          funding, which is what the submission wants.

    If a future outcome ever needs a turn, set it here. The value is written
    into every record of forecast.jsonl and the number is negated at scoring,
    never the anchors in the prompt.
    """
    return bool(cell["block"]["flip"])


def megastudy_units(cell: dict) -> str:
    """The phrase that ends the ASK line, for THIS outcome's scale."""
    kind = cell["block"]["kind"]
    if kind == "dollars":
        return "in US dollars"
    if kind == "percent":
        return "in percentage points of the sign-up rate"
    return "in points of the 0-100 scale"


def megastudy_top(cell: dict) -> str:
    kind = cell["block"]["kind"]
    return {"dollars": "10 dollars", "percent": "100%"}.get(kind, "100")


def megastudy_bottom(cell: dict) -> str:
    kind = cell["block"]["kind"]
    return {"dollars": "0 dollars", "percent": "0%"}.get(kind, "0")


def unit_factor(cell: dict) -> float:
    """Multiply the model's number by this to get the submitted `ate`."""
    return UNIT_FACTOR[cell["block"]["kind"]]


def value_range(cell: dict) -> tuple[float, float]:
    return VALUE_RANGE[cell["block"]["kind"]]


SPEC = {
    "study": megastudy_study,
    "outcome": megastudy_outcome,
    "estimand": megastudy_estimand,
    "arm_text": megastudy_arm_text,
    "ends": megastudy_ends,
    "flip": megastudy_flip,
    "ask_units": megastudy_units,
    "scale_top": megastudy_top,
    "scale_bottom": megastudy_bottom,
    "unit_factor": unit_factor,
    "value_range": value_range,
    "thing": "text", "things": "texts",
    "stimulus_files": [OUTCOMES_JSON, STIM_INDEX, QUOTAS],
}

core.STUDIES[STUDY_KEY] = SPEC
