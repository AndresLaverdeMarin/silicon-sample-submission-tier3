#!/usr/bin/env python3
"""
Prove that `forecast/core.render` did not change the validated prompt.

WHY THIS TEST EXISTS. `forecast/core.py` is a copy of
/home/jovyan/LLMmegastudy/modelbench/structured_forecast.py, sha256
fe4f71e605409286622a9cddd5e6bb7bbf7ff930488aebe5fec9b7e454728f65. That file's
listwise prompt was measured against two archives with known human effects
(Broockman r = +0.3468, Voelkel r = +0.6558, Qwen3.8-27B, 2026-08-29). The
copy adds three scale hooks so that `donation_ams` and `newsletter_signup` can
be asked in their own units. This test proves the hooks change NOTHING for the
11 outcomes on a 0-100 slider.

It also proves the two dangerous units, and the direction rule.

    .venv-vllm/bin/python forecast/tests/test_render_parity.py

**Written in ASD-STE100 Simplified Technical English.**
"""
from __future__ import annotations

import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import core                                                     # noqa: E402
import megastudy                                                # noqa: E402

SRC = Path("/home/jovyan/LLMmegastudy/modelbench/structured_forecast.py")
fails = []


def check(ok: bool, what: str) -> None:
    print(f"  {'PASS' if ok else 'FAIL'}  {what}")
    if not ok:
        fails.append(what)


def main() -> int:
    cells = {c["outcome"]: c for c in megastudy.load_cells(None)}
    rng = random.Random(0)

    def render(name):
        cell = cells[name]
        order = list(range(len(cell["arms"])))
        rng.shuffle(order)
        return core.render(cell, [cell["arms"][i] for i in order], "listwise")

    print("\n1. The 0-100 slider path is the validated text, word for word.")
    p = render("trust_post")
    check("  Give the effect of EVERY text, in points of the 0-100 scale.\n"
          in p, "ASK line reads 'in points of the 0-100 scale'")
    check("  A POSITIVE number means the text moved the average TOWARD 100,\n"
          in p, "POSITIVE line names 100")
    check("  A NEGATIVE number means the text moved the average TOWARD 0,\n"
          in p, "NEGATIVE line names 0")
    check("  Write exactly 16 lines and nothing else." in p,
          "the form asks for exactly 16 lines")
    pos = [p.index(h) for h in
           ("TASK\n", "\nSTUDY\n", "\nOUTCOME\n", "\nESTIMAND\n",
            "\nARMS\n", "\nASK\n")]
    check(pos == sorted(pos),
          "the six sections are in the published order")

    if SRC.exists():
        print("\n1b. The ASK skeleton is byte for byte the source's skeleton.")
        src = SRC.read_text()
        for line in ('f"  Give the effect of EVERY {thing}, in points of the 0-100 "',
                     'f"  A POSITIVE number means the {thing} moved the average TOWARD "',
                     'f"  Write exactly {n} lines and nothing else. Each line is the "'):
            check(line in src, f"source still holds {line[:44]}...")
    else:
        print("\n1b. SKIP. The source file is not on this machine.")

    print("\n2. The two outcomes that are NOT on a 0-100 slider ask in their "
          "own units.")
    p = render("donation_ams")
    check("  Give the effect of EVERY text, in US dollars.\n" in p,
          "donation_ams asks in US dollars")
    check("moved the average TOWARD 10 dollars," in p,
          "donation_ams names 10 dollars as the top of the scale")
    p = render("newsletter_signup")
    check("  Give the effect of EVERY text, in percentage points of the "
          "sign-up rate.\n" in p,
          "newsletter_signup asks in percentage points")
    check("moved the average TOWARD 100%," in p,
          "newsletter_signup names 100% as the top of the scale")
    check(megastudy.UNIT_FACTOR["percent"] == 0.01,
          "a newsletter_signup answer is divided by 100 to give a proportion")
    check(megastudy.UNIT_FACTOR["dollars"] == 1.0,
          "a donation_ams answer is submitted in dollars, unchanged")

    print("\n3. The direction rule.")
    for name in cells:
        check(megastudy.SPEC["flip"](cells[name]) is False,
              f"{name}: scale_flip is False, so the prompt scale is the "
              f"submitted scale")
    p = render("distrust_post")
    check("  100 is very strong distrust of climate scientists." in p,
          "distrust_post: 100 is MORE distrust, so a trust-building text is "
          "negative here")
    p = render("funding_perceptions")
    check("100 = the government spends far too LITTLE money on climate change "
          "research" in p,
          "funding_perceptions: the anchors are already swapped, so a "
          "positive number is more support for funding")

    print("\n4. The parsers.")
    r = core.parse_listwise("\n".join(f"{i}: {i - 8}" for i in range(1, 17)),
                            16, -100, 100)
    check(r["n_parsed"] == 16 and r["mode"] == "labelled",
          "16 labelled lines parse to 16 values")
    r = core.parse_listwise("1: 2.4\n2: -3\n", 16, -100, 100)
    check(r["values"] == {1: 2.4, 2: -3.0},
          "a decimal and a negative number parse correctly")
    r = core.parse_listwise("1: 250\n", 16, -100, 100)
    check(r["n_parsed"] == 0 and r["n_out_of_range"] == 1,
          "a value outside the range is refused, not clipped")
    r = core.parse_listwise("1: 9\n", 16, -10, 10)
    check(r["values"] == {1: 9.0},
          "the dollar range accepts 9 and the caller sets the range")

    print(f"\n{len(fails)} failed.")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
