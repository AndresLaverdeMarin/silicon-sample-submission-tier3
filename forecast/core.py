#!/usr/bin/env python3
"""
The prompt skeleton, the parsers and the work plan. Model-free and study-free.

PROVENANCE. Copied from
  /home/jovyan/LLMmegastudy/modelbench/structured_forecast.py
  sha256 fe4f71e605409286622a9cddd5e6bb7bbf7ff930488aebe5fec9b7e454728f65
The copy keeps `wrap`, `Opt`, `FRAMINGS`, `render`, `parse_pointwise`,
`parse_listwise`, `build_work`, `max_tokens_for` and `provenance`. It removes
the OpenRouter transport, the cost model, the Ashokkumar archive loader, the
scorer and the contamination probes: this repository has no ground truth to
score against and makes no paid call.

ONE CHANGE TO `render`. The source always asks for "points of the 0-100
scale". Two of the 13 outcomes of this study are not on that scale
(`donation_ams` is 0-10 dollars, `newsletter_signup` is a rate). So the study
spec now supplies three more slot functions: `ask_units`, `scale_top` and
`scale_bottom`. With their default values the rendered text is byte for byte
the same as the source. `forecast/tests/test_render_parity.py` proves that.

SIX SECTIONS, ALWAYS IN THIS ORDER.
    1. TASK      what the model must do, said once.
    2. STUDY     the real study: sample, recruitment, design, N, conditions.
    3. OUTCOME   the exact items, how many, the scale, both anchors.
    4. ESTIMAND  the contrast, in plain words AND in statistical words.
    5. ARMS      the stimulus text of the arms.
    6. ASK       the answer instruction and the sign rule.
All 504,840 deposited Ashokkumar prompts use this order: instruction first,
context next, stimulus late, answer cue last.

**Written in ASD-STE100 Simplified Technical English.**
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def wrap(text: str, indent: str = "  ", width: int = 76) -> str:
    """Fill one paragraph. Keeps the prompt readable when a slot holds a
    long value."""
    return textwrap.fill(" ".join(text.split()), width=width,
                         initial_indent=indent, subsequent_indent=indent) + "\n"


class Opt:
    """The run options that the prompt builders read."""

    population = False       # add the recruitment-target table. Off by default.
    anchor = False           # add the magnitude anchor. Off by default.
    items = "all"            # "all" prints every item; "one" prints one.


# Ten framing openings, kept for `--framings N > 1` only. The DEFAULT is one
# fixed prompt with repeated draws. Measured on the Broockman and Voelkel
# archives (modelbench/output/runs, 2026-08-29): 0 of 45 pairwise framing
# comparisons significant, so repeated sampling replaces a framing ensemble.
FRAMINGS = [
    "You are estimating the result of a randomised survey experiment.",
    "Consider what is known about public opinion from behavioural science.",
    "A survey experiment was run on a large sample of American adults.",
    "Estimate how a persuasive message changes public opinion.",
    "You are asked to forecast the result of an online survey experiment.",
    "Think about how members of the public respond to political arguments.",
    "A nationally diverse sample of American adults took an online survey.",
    "Predict the measured effect of a short persuasive text.",
    "Researchers tested a persuasive message on a general population sample.",
    "Below is a message that was shown to a random half of a survey sample.",
]

# The magnitude anchor. It is OFF by default. An anchor can only pull every
# answer toward one value, which compresses the spread that a correlation
# needs. Use `--anchor` only for a controlled test.
ANCHOR_LINE = ("Most messages of this kind move the average by less than "
               "10 points.")


# --------------------------------------------------------------- render ---
def render(cell: dict, arms: list[dict], mode: str,
           framing: str | None = None, studies: dict | None = None) -> str:
    """Build the whole prompt. Six sections, always in the same order.

    `framing` is passed in, not read from a global, so a thread pool cannot
    race on it.
    """
    spec = (studies or STUDIES)[cell["_study"]]
    thing, things = spec["thing"], spec["things"]
    lo_end, hi_end = spec["ends"](cell)
    # The three scale hooks. Their defaults reproduce the source text.
    units = spec.get("ask_units", lambda c: "in points of the 0-100 scale")(cell)
    top = spec.get("scale_top", lambda c: "100")(cell)
    bottom = spec.get("scale_bottom", lambda c: "0")(cell)
    n = len(arms)

    lead = framing + "\n\n" if framing else ""
    if mode == "listwise":
        task = (f"  You must forecast the result of a randomised experiment.\n"
                f"  Below is the study, its outcome measure, and the {n} "
                f"{things} that\n"
                f"  were tested. Give ONE number for EACH {thing}: the effect "
                f"of that\n"
                f"  {thing} on the outcome.\n")
    else:
        task = (f"  You must forecast the result of a randomised experiment.\n"
                f"  Below is the study, its outcome measure, and ONE {thing} "
                f"that was\n"
                f"  tested. Give ONE number: the effect of that {thing} on "
                f"the outcome.\n")

    # ARMS. The stimulus comes late, immediately before the answer cue.
    if mode == "listwise":
        head = (f"  Each treatment group read ONE of the {n} {things} below. "
                f"A separate\n  control group read no {thing}.\n\n")
        body = []
        for i, arm in enumerate(arms, start=1):
            text = spec["arm_text"](cell, arm)
            body.append(f"  {thing.upper()} {i}:\n  > "
                        + text.replace("\n", "\n  > "))
        arms_block = head + "\n\n".join(body) + "\n"
    else:
        text = spec["arm_text"](cell, arms[0])
        arms_block = (f"  One treatment group read the {thing} below. A "
                      f"control group read\n  no {thing}.\n\n"
                      "  > " + text.replace("\n", "\n  > ") + "\n")

    # ASK. The sign rule is tied to the scale direction, never to the arm.
    anchor = f"\n  {ANCHOR_LINE}\n" if Opt.anchor else ""
    sign = (f"  A POSITIVE number means the {thing} moved the average TOWARD "
            f"{top},\n"
            f"  that is, toward {hi_end}.\n"
            f"  A NEGATIVE number means the {thing} moved the average TOWARD "
            f"{bottom},\n"
            f"  that is, toward {lo_end}.\n")
    if mode == "listwise":
        # The form is shown with a placeholder, never with an example number.
        # An example number is a magnitude anchor.
        form = "\n".join(f"  {i}: <number>" for i in range(1, n + 1))
        ask = (f"  Give the effect of EVERY {thing}, {units}.\n"
               f"{sign}{anchor}\n"
               f"  Write exactly {n} lines and nothing else. Each line is the "
               f"{thing}\n"
               f"  number, then a colon, then the number:\n\n"
               f"{form}\n\n"
               f"  Your estimates:\n")
    else:
        ask = (f"  Give the effect of the {thing}, {units}.\n"
               f"{sign}{anchor}\n"
               f"  Answer with a single number and nothing else.\n\n"
               f"  Your estimate: ")

    return (f"{lead}"
            f"TASK\n{task}\n"
            f"STUDY\n{spec['study'](cell)}\n"
            f"OUTCOME\n{spec['outcome'](cell)}\n"
            f"ESTIMAND\n{spec['estimand'](cell)}\n"
            f"ARMS\n{arms_block}\n"
            f"ASK\n{ask}")


# --------------------------------------------------------------- parsing --
_NUM = re.compile(r"[-+]?\d+(?:[.,]\d+)?")
# `1: -2.4`, `1. -2.4`, `1) -2.4`, `Message 1: -2.4`, `- 1: -2.4`.
# The `.` separator MUST be followed by a space. Without that rule the regex
# reads the bare number `2.4` as position 2 with value 4.
_LINE = re.compile(r"^[\s*\-]*(?:[A-Za-z ]{0,12}?)?(\d{1,2})\s*"
                   r"(?::|\)|\]|\.(?=\s))\s*"
                   r"([-+]?\d+(?:[.,]\d+)?)")


def _num(s: str) -> float:
    return float(s.replace(",", "."))


def parse_pointwise(text: str, lo: float, hi: float) -> dict:
    """Take the first signed number and check it is inside the range."""
    if not text:
        return {"ok": False, "why": "no text", "value": None}
    m = _NUM.search(text)
    if not m:
        return {"ok": False, "why": "no number", "value": None}
    v = _num(m.group())
    if not (lo <= v <= hi):
        return {"ok": False, "why": "out of range", "value": None}
    return {"ok": True, "why": None, "value": v}


def parse_listwise(text: str, n: int, lo: float, hi: float) -> dict:
    """Read `<position>: <number>` lines.

    It returns a dict from POSITION (1..n) to value. It tolerates a missing
    line, an extra line, a position outside 1..n, and a repeated position
    (the FIRST answer wins). It never assumes the model kept the order asked.
    If no labelled line is found, and the reply holds exactly n bare numbers,
    the numbers are mapped in the order they appear. That fallback is
    recorded, so it can be removed from an analysis.
    """
    out: dict[int, float] = {}
    bad = 0
    if not text:
        return {"values": {}, "n_parsed": 0, "n_asked": n, "mode": "no text",
                "n_out_of_range": 0}
    for line in text.splitlines():
        m = _LINE.match(line)
        if not m:
            continue
        pos, v = int(m.group(1)), _num(m.group(2))
        if not (1 <= pos <= n):
            continue
        if not (lo <= v <= hi):
            bad += 1
            continue
        out.setdefault(pos, v)
    mode = "labelled"
    if not out:
        nums = [_num(x) for x in _NUM.findall(text)]
        nums = [v for v in nums if lo <= v <= hi]
        if len(nums) == n:
            out = dict(enumerate(nums, start=1))
            mode = "bare numbers, in order"
        else:
            mode = "unparsed"
    return {"values": out, "n_parsed": len(out), "n_asked": n, "mode": mode,
            "n_out_of_range": bad}


# ------------------------------------------------------------- the work ---
def build_work(cells, mode, framings, samples, rng):
    """One job for each CALL.

    A pointwise job holds one arm. A listwise job holds every arm of the cell,
    IN A RANDOM ORDER. The order is recorded, so position bias is measured
    afterwards and not assumed. The shuffle is load-bearing: at temperature 0
    a reshuffle alone moves the predictions to r = 0.57-0.73 against each
    other, so the many-order ensemble carries real variance.
    """
    work = []
    for cell in cells:
        for f in range(framings):
            for s in range(samples):
                if mode == "listwise":
                    order = list(range(len(cell["arms"])))
                    rng.shuffle(order)
                    work.append({"cell": cell, "order": order,
                                 "framing": f, "sample": s})
                else:
                    for idx in range(len(cell["arms"])):
                        work.append({"cell": cell, "order": [idx],
                                     "framing": f, "sample": s})
    return work


def max_tokens_for(mode: str, n: int) -> int:
    """A listwise reply needs room for n lines. A pointwise reply needs 32.

    The local vLLM run uses `40 * n + 128`, which is wider. Measured
    2026-08-30 on Qwen3.8-27B: a narrower budget truncates the last lines of
    a 16-arm reply.
    """
    return 32 if mode == "pointwise" else 24 * n + 64


# ------------------------------------------------------------ provenance --
def provenance(paths) -> list[dict]:
    """Record every input file: path, size, sha256 and git status."""
    out = []
    for p in paths:
        p = Path(p)
        if not p.exists():
            out.append({"path": str(p), "exists": False})
            continue
        raw = p.read_bytes()
        try:
            subprocess.run(["git", "ls-files", "--error-unmatch", str(p)],
                           cwd=ROOT, check=True, capture_output=True)
            tracked = True
        except Exception:
            tracked = False
        try:
            rel = str(p.relative_to(ROOT))
        except ValueError:
            rel = str(p)
        out.append({"path": rel, "exists": True, "bytes": len(raw),
                    "sha256": hashlib.sha256(raw).hexdigest(),
                    "git_tracked": tracked})
    return out


STUDIES: dict = {}          # filled by forecast/megastudy.py
