#!/usr/bin/env python3
"""
Step 1 of the forecast pipeline. Make the materials the prompt needs.

WHAT IT READS. Two files of THIS repository only. The pipeline must run
without any other checkout.
  survey/questionnaire.txt   the instrument, in survey order. Its `### <title>`
                             sections under the CONDITION heading hold the full
                             text of every condition.
  codebook.csv               the item wording, the anchors and the composite
                             rule for each outcome.

WHAT IT WRITES.
  forecast/materials/stimuli/<title>.txt   16 files, one for each intervention.
                                           The control condition is NOT written.
  forecast/materials/outcomes.json         13 outcomes, with the items, the
                                           anchors, the scale and the flip flag.
  forecast/materials/MANIFEST.json         sha256 of every input and output.

THE TITLES ARE THE SUBMISSION STRINGS. The `### ` headings of
questionnaire.txt are the same 16 strings as the `interventions` vector of
scripts/lib/submission_spec.R:14-31. This script checks that, and stops if the
two disagree. So a stimulus file can never be joined to the wrong condition.

    .venv-vllm/bin/python forecast/extract_materials.py

**Written in ASD-STE100 Simplified Technical English.**
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
Q = ROOT / "survey/questionnaire.txt"
CODEBOOK = ROOT / "codebook.csv"
SPEC_R = ROOT / "scripts/lib/submission_spec.R"
OUT = ROOT / "forecast/materials"
STIM = OUT / "stimuli"

# The 16 intervention titles, in the order of scripts/lib/submission_spec.R
# lines 14-31. This copy is checked against that file at run time.
INTERVENTIONS = [
    "Corporate reliance",
    "Social justice",
    "Interview Prof. Maraun",
    "Funding",
    "Oil industry misinformation",
    "Measurement & modeling (1)",
    "Former skeptics",
    "High public trust",
    "Measurement & modeling (2)",
    "Peer-review",
    "Scientist community helpers",
    "Consensus",
    "Portrait Prof. Cherry",
    "Model accuracy",
    "Interview Prof. Sebille",
    "Extreme weather predictions",
]

# The 13 Tier 3 outcomes, in the order of scripts/lib/submission_spec.R
# lines 71-78. This is NOT the section-B list of codebook.csv: `age_band` and
# the four trust subscales are Tier 1 columns, not Tier 3 outcomes.
OUTCOMES = [
    "trust_multidimensional", "trust_post", "distrust_post",
    "funding_perceptions", "policy_role_mean", "inst_trust_mean",
    "belief_post", "concern_mean", "policy_general",
    "policy_specific_mean", "behavior_mean", "donation_ams",
    "newsletter_signup",
]

# The composite rule of each outcome. `items` holds `target_label` values of
# codebook.csv. The rules come from codebook.csv section B, lines 53-64, and
# from the `target_label` column of section A.
#   mean        the arithmetic mean of the listed items
#   copy        the single item, as measured
#   reverse100  100 minus the single item (codebook.csv:53)
COMPOSITION = {
    "trust_multidimensional": ("mean", [
        f"trust_{d}_{i}" for d in
        ("competence", "integrity", "benevolence", "openness")
        for i in (1, 2, 3)]),
    "trust_post": ("copy", ["trust_post"]),
    "distrust_post": ("copy", ["distrust_post"]),
    "funding_perceptions": ("reverse100", ["funding_perceptions"]),
    "policy_role_mean": ("mean", [f"policy_role_{i}" for i in range(1, 5)]),
    "inst_trust_mean": ("mean", [
        "inst_trust_epa", "inst_trust_nasa", "inst_trust_noaa",
        "inst_trust_universities", "inst_trust_federal_gov"]),
    "belief_post": ("copy", ["belief_post"]),
    "concern_mean": ("mean", [f"concern_{i}" for i in range(1, 4)]),
    "policy_general": ("copy", ["policy_general"]),
    "policy_specific_mean": ("mean",
                             [f"policy_specific_{i}" for i in range(1, 8)]),
    "behavior_mean": ("mean", [
        "behavior_meat", "behavior_transport", "behavior_solar",
        "behavior_fly", "behavior_talk", "behavior_donate"]),
    "donation_ams": ("copy", ["donation_ams"]),
    "newsletter_signup": ("copy", ["newsletter_signup"]),
}

# The plain name of each outcome, and the two ends of its scale. The wording
# always makes 100 (or the top of the scale) MORE of the thing that the
# outcome name says. Source of every anchor: the `response_options` column of
# codebook.csv, and codebook.csv:53 for the reverse coding of
# `funding_perceptions`.
ENDS = {
    "trust_multidimensional": (
        "trust in climate scientists",
        "no trust in climate scientists at all",
        "the highest possible trust in climate scientists"),
    "trust_post": (
        "trust in climate scientists",
        "no trust in climate scientists at all",
        "very strong trust in climate scientists"),
    "distrust_post": (
        "distrust of climate scientists",
        "no distrust of climate scientists at all",
        "very strong distrust of climate scientists"),
    "funding_perceptions": (
        "the belief that the government spends too little on climate research",
        "the belief that the government spends far too much on climate "
        "research",
        "the belief that the government spends far too little on climate "
        "research"),
    "policy_role_mean": (
        "agreement that climate scientists should take a role in policy",
        "complete disagreement that climate scientists should take a role in "
        "policy",
        "complete agreement that climate scientists should take a role in "
        "policy"),
    "inst_trust_mean": (
        "trust in public institutions",
        "no trust in these institutions at all",
        "very strong trust in these institutions"),
    "belief_post": (
        "belief that human activities cause climate change",
        "the belief that the statement is not accurate at all",
        "the belief that the statement is extremely accurate"),
    "concern_mean": (
        "concern about climate change",
        "no concern about climate change at all",
        "extreme concern about climate change"),
    "policy_general": (
        "support for government action on global warming",
        "strong opposition to more government action on global warming",
        "strong support for more government action on global warming"),
    "policy_specific_mean": (
        "support for specific climate policies",
        "strong opposition to these climate policies",
        "strong support for these climate policies"),
    "behavior_mean": (
        "the stated intention to act for the climate",
        "no intention at all to do these things",
        "an extremely likely intention to do these things"),
    "donation_ams": (
        "the amount donated to a scientific society",
        "no donation at all",
        "the whole 10 dollar bonus donated"),
    "newsletter_signup": (
        "the rate of sign-up to a climate science newsletter",
        "nobody in the group signs up",
        "everybody in the group signs up"),
}

# The answer scale of each outcome. It is NOT the same for all 13.
#   slider100   the outcome is a 0-100 slider, or the mean of 0-100 sliders.
#               The effect is in points of that scale.
#   dollars     `donation_ams` is whole dollars, 0 to 10 (codebook.csv:25).
#               The effect is in dollars.
#   percent     `newsletter_signup` is a 0/1 answer (codebook.csv:54). The
#               submitted effect is a change of the PROPORTION. The model is
#               asked in PERCENTAGE POINTS and the answer is divided by 100.
#               Reason: a model writes a readable number in percentage points
#               and writes 0.02 badly. `forecast/megastudy.py` holds the
#               divisor, so the units can be audited in one place.
KIND = {o: "slider100" for o in OUTCOMES}
KIND["donation_ams"] = "dollars"
KIND["newsletter_signup"] = "percent"

# Every outcome is asked on its OWN scale, the same scale the submission uses.
# So no outcome needs its number turned round at scoring time. The flag is
# kept, written into every record, and printed by the dry run, so the claim is
# auditable and not just asserted. See forecast/megastudy.py `megastudy_flip`.
FLIP = {o: False for o in OUTCOMES}


def sha(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


# ------------------------------------------------------------- stimuli ----
def extract_stimuli() -> dict:
    """Cut the 16 intervention texts out of survey/questionnaire.txt."""
    text = Q.read_text()
    head = "CONDITION  (each respondent sees exactly ONE"
    tail = "POST-TREATMENT OUTCOMES"
    section = text.split(head)[1].split(tail)[0]
    out = {}
    for part in re.split(r"^### ", section, flags=re.M)[1:]:
        title = part.split("\n")[0].strip()
        body = "\n".join(part.split("\n")[1:]).strip()
        body = re.sub(r"\n=+\s*$", "", body).strip()
        if title.startswith("control"):
            continue                     # the control group reads no message
        if title == "Extreme weather predictions":
            body = reduce_state_adaptive(body)
        out[title] = body
    missing = [t for t in INTERVENTIONS if t not in out]
    extra = [t for t in out if t not in INTERVENTIONS]
    if missing or extra:
        raise SystemExit(f"title mismatch. missing={missing} extra={extra}")
    return out


# ------------------------------------------------- state-adaptive arm ----
# `Extreme weather predictions` is the ONLY state-adaptive arm. Its own first
# line says: "each participant sees only ONE version ... do NOT feed the whole
# block below verbatim." The raw block is 11,435 chars and holds authoring
# scaffolding, a 51-state list, a state-to-case mapping, all FOUR case texts
# and a reference list marked "[not displayed to participants]".
#
# Sent whole, this one arm was 24.5% of all arm text, and most of it was text
# that no participant ever read. That is a measurement error, not a style
# problem: it gives one intervention a quarter of the prompt and fills it with
# instructions to the survey programmer.
#
# What a participant actually saw, from section II of the file:
#   page 1  a question asking their home state
#   page 2  ONE intro paragraph
#   page 3  ONE of four case texts, chosen by their state
#
# We render the MODAL participant. Case 1 (flood) covers 27 states and D.C.,
# the largest share of the US adult population. The other cases are named in
# one line, so the model knows the arm was tailored, without reading three
# texts that most participants never saw.
def reduce_state_adaptive(body: str) -> str:
    """Give the text ONE participant read, not the programmer's whole block."""
    lines = body.splitlines()
    def find(pat, start=0):
        for i in range(start, len(lines)):
            if re.match(pat, lines[i].strip()):
                return i
        raise SystemExit(f"extreme weather arm: no line matches {pat!r}")
    c1 = find(r"^Case 1$", find(r"^Intervention page 3"))
    c2 = find(r"^Case 2$", c1 + 1)
    case1 = "\n".join(l for l in lines[c1 + 1:c2] if l.strip())
    intro = ("You reported that you are currently living in a state with high "
             "or recurrent flood risk. Please read the text on the following "
             "page carefully. It describes a real project in the U.S., working "
             "particularly on reducing the risks from these hazards by helping "
             "communities prepare for extreme weather.")
    note = ("(This message was tailored to the reader's home state. Readers in "
            "states with high wildfire risk, or with severe cold and snow, read "
            "a parallel text about that hazard instead.)")
    return f"{intro}\n\n{case1}\n\n{note}"


def check_spec_r() -> None:
    """Stop if this file's copy of the titles or outcomes is stale."""
    src = SPEC_R.read_text()
    for t in INTERVENTIONS:
        if f'"{t}"' not in src:
            raise SystemExit(f"{SPEC_R} does not hold the title {t!r}")
    for o in OUTCOMES:
        if f'"{o}"' not in src:
            raise SystemExit(f"{SPEC_R} does not hold the outcome {o!r}")


# ------------------------------------------------------------ outcomes ----
# The three items whose `response_options` cell is not a simple
# "0 = low ... 100 = high" pair. They are written out by hand, from the same
# cell of codebook.csv.
SPECIAL_ANCHORS = {
    # codebook.csv:22. The composite reverses it, so the anchors below are
    # ALREADY re-pointed: 100 = "far too little". See codebook.csv:53.
    "funding_perceptions": ("the government spends far too MUCH money on "
                            "climate change research",
                            "the government spends far too LITTLE money on "
                            "climate change research"),
    "donation_ams": ("0 dollars donated", "10 dollars donated"),
    "newsletter_signup": ("did not subscribe", "subscribed"),
}


def parse_anchor(target: str, options: str) -> tuple[str, str]:
    """Read the two ends out of the `response_options` cell of codebook.csv."""
    if target in SPECIAL_ANCHORS:
        return SPECIAL_ANCHORS[target]
    for sep in ("…", "..."):
        if sep in options:
            lo, hi = options.split(sep, 1)
            lo = re.sub(r"^\s*0\s*=\s*", "", lo).strip(" ,")
            hi = re.sub(r"^\s*100\s*=\s*", "", hi).strip(" ,")
            return lo, hi
    raise SystemExit(f"cannot read the anchors of {target!r}: {options!r}")


# The two behavioural items refer back to an earlier survey page. The codebook
# cell alone is not answerable, so the offer page is folded into the question.
# Source: survey/questionnaire.txt lines 819-856, the verbatim offer page and
# the scored item.
QUESTION_OVERRIDE = {
    "newsletter_signup":
        "Earlier in the survey you were offered a free subscription to the "
        "newsletter \"Talking Climate\" by climate scientist Katharine "
        "Hayhoe. It gives short, accessible updates on climate science and "
        "climate solutions for a general audience. Signing up takes less than "
        "a minute and is optional. Did you subscribe?",
    # The codebook question_text ends "(reverse-coded in cleaning)". That note
    # is about the cleaning script, not about what the respondent read, and it
    # contradicts the already-swapped anchors. Source: codebook.csv:22.
    "funding_perceptions":
        "Do you think the federal government is spending too much, too little "
        "or about the right amount of money on climate change research?",
    "donation_ams":
        "You were given a $10 bonus. Of the $10 bonus, how much would you "
        "like to donate to the American Meteorological Society (AMS)? "
        "(Whole dollars, $0 to $10.)",
}


def extract_outcomes() -> dict:
    """Build the 13 outcome blocks from codebook.csv."""
    items = {}
    for row in csv.DictReader(CODEBOOK.open()):
        key = row["target_label"]
        # codebook.csv holds TWO rows for a constructed outcome: the measured
        # item in section A, and the cleaning rule in section B. Keep the
        # section A row. Without this rule `newsletter_signup` takes the text
        # "Recode of newsletter: Yes->1, No->0" as its question, which no
        # respondent ever saw.
        if key in items and not row["section"].startswith("A."):
            continue
        items[key] = {
            "question": " ".join(row["question_text"].split()),
            "options": " ".join(row["response_options"].split()),
            "section": row["section"],
        }
    out = {}
    for name in OUTCOMES:
        rule, keys = COMPOSITION[name]
        label, lo_end, hi_end = ENDS[name]
        block = []
        for k in keys:
            if k not in items:
                raise SystemExit(f"{CODEBOOK} has no item {k!r}")
            lo, hi = parse_anchor(k, items[k]["options"])
            block.append({"key": k,
                          "question": QUESTION_OVERRIDE.get(
                              k, items[k]["question"]),
                          "anchor_low": lo, "anchor_high": hi})
        out[name] = {"outcome": name, "label": label, "rule": rule,
                     "n_items": len(block), "items": block,
                     "kind": KIND[name], "flip": FLIP[name],
                     "low_end": lo_end, "high_end": hi_end}
    return out


def main() -> int:
    check_spec_r()
    STIM.mkdir(parents=True, exist_ok=True)
    stim = extract_stimuli()
    files = {}
    for title in INTERVENTIONS:
        fn = re.sub(r"[^a-z0-9]+", "_", title.lower()).strip("_") + ".txt"
        (STIM / fn).write_text(stim[title] + "\n")
        files[title] = fn
    (OUT / "stimuli_index.json").write_text(json.dumps(files, indent=1))

    outcomes = extract_outcomes()
    (OUT / "outcomes.json").write_text(json.dumps(outcomes, indent=1))

    manifest = {
        "made_by": "forecast/extract_materials.py",
        "inputs": [{"path": str(p.relative_to(ROOT)), "sha256": sha(p),
                    "bytes": p.stat().st_size}
                   for p in (Q, CODEBOOK, SPEC_R)],
        "outputs": [{"path": str(p.relative_to(ROOT)), "sha256": sha(p),
                     "bytes": p.stat().st_size}
                    for p in sorted(OUT.rglob("*"))
                    if p.is_file() and p.name != "MANIFEST.json"],
    }
    (OUT / "MANIFEST.json").write_text(json.dumps(manifest, indent=1))

    total = sum((STIM / f).stat().st_size for f in files.values())
    print(f"stimuli    {len(files)} files, {total:,} chars, in {STIM}")
    for title in INTERVENTIONS:
        n = len((STIM / files[title]).read_text())
        print(f"  {title:<32} {files[title]:<34} {n:>6,} chars")
    print(f"\noutcomes   {len(outcomes)} blocks in {OUT / 'outcomes.json'}")
    for name in OUTCOMES:
        b = outcomes[name]
        print(f"  {name:<24} {b['rule']:<11} {b['n_items']:>2} item(s)  "
              f"{b['kind']:<10} flip={b['flip']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
