#!/usr/bin/env python3
"""
Turn a run's `forecast.jsonl` into the Tier 3 prediction file, and audit it.

WHAT IT DOES.
  1. Read every record of forecast.jsonl.
  2. For each (condition, outcome) pair, take the MEAN of the parsed draws.
     One call gives one draw for each of the 16 conditions, and there are 8
     calls for each outcome, so a full cell has 8 draws.
  3. Write the 208 rows in the row order of the template file, so a human can
     read a diff. The row SET comes from the template and is never changed.
  4. Print the audits that `make check` cannot make. `scripts/lib/check_lib.R`
     lines 378-381 say the Tier 3 `ate` is NOT range-checked, on purpose. So
     a units error passes validation in silence and only shows up in the
     score. These audits are the only guard.

THE AUDITS.
  units       `newsletter_signup` must be a change of a 0-1 proportion and
              `donation_ams` must be dollars on a 0-10 scale. Both are printed
              apart from the 11 slider outcomes.
  proportion  If every `newsletter_signup` value is smaller than 0.001, the
              model probably answered in proportions where percentage points
              were asked, and the values are 100 times too small.
  direction   `distrust_post` is NOT reverse-coded, and `trust_post` is. So a
              text that builds trust must give a NEGATIVE number on
              distrust_post and a POSITIVE number on trust_post. The two must
              DISAGREE in sign for most of the 16 texts. If they agree, the
              sign convention is wrong somewhere.
  coverage    208 rows, 16 conditions x 13 outcomes, no control row, no
              duplicate, no empty value.

    P=/home/jovyan/LLMmegastudy/.venv-vllm/bin/python
    $P forecast/build_predictions.py forecast/runs/B_pop_on \
        --out predictions/team_27_T3_primary_v1.csv
    $P forecast/build_predictions.py --compare forecast/runs/A_pop_off \
        forecast/runs/B_pop_on

**Written in ASD-STE100 Simplified Technical English.**
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "predictions/team_27_T3_primary_v1.csv"

# The 11 slider outcomes get 3 decimal places, `donation_ams` gets 3, and
# `newsletter_signup` gets 4 because its whole scale is only 0-1.
# Source: predictions/SPEC_NOTES.md section 8.
DECIMALS = {"newsletter_signup": 4}


def collect(run_dir: Path) -> dict:
    """(condition, outcome) -> the list of parsed draws, in submitted units."""
    by: dict[tuple, list[float]] = {}
    kinds: dict[str, str] = {}
    for line in (run_dir / "forecast.jsonl").open():
        rec = json.loads(line)
        kinds[rec["outcome"]] = rec["kind"]
        for a in rec["answers"]:
            if not a["ok"]:
                continue
            by.setdefault((a["condition"], rec["outcome"]), []).append(a["ate"])
    return {"by": by, "kinds": kinds}


def template_rows() -> list[tuple[str, str]]:
    """The row set and the row order of the shipped template file."""
    rows = []
    for r in csv.DictReader(TEMPLATE.open()):
        rows.append((r["condition"], r["outcome"]))
    return rows


def fmt(outcome: str, v: float) -> str:
    return f"{v:.{DECIMALS.get(outcome, 3)}f}"


def audit(values: dict, kinds: dict, name: str) -> str:
    """Print the checks that `make check` does not make."""
    out, w = [], lambda s: out.append(s)
    slider = [v for (c, o), v in values.items()
              if kinds.get(o) == "slider100"]
    don = [v for (c, o), v in values.items() if o == "donation_ams"]
    news = [v for (c, o), v in values.items() if o == "newsletter_signup"]

    w("")
    w(f"AUDIT  {name}")
    w("-" * 72)
    w(f"rows                     {len(values)}")
    w(f"conditions               "
      f"{len({c for c, o in values})}")
    w(f"outcomes                 {len({o for c, o in values})}")
    w(f"missing value            "
      f"{sum(1 for v in values.values() if v is None or v != v)}")
    w("")
    w("                          n      min      max     mean   mean|x|  neg")
    for label, xs in (("11 slider outcomes, points", slider),
                      ("donation_ams, dollars", don),
                      ("newsletter_signup, proportion", news)):
        if not xs:
            continue
        w(f"  {label:<28}{len(xs):>4}{min(xs):>9.4f}{max(xs):>9.4f}"
          f"{statistics.mean(xs):>9.4f}"
          f"{statistics.mean(abs(x) for x in xs):>9.4f}"
          f"{sum(1 for x in xs if x < 0):>5}")
    w("")
    # The proportion guard. See the module docstring.
    if news:
        big = max(abs(x) for x in news)
        if big > 1.0:
            w(f"  FAIL  newsletter_signup reaches {big:.3f}. A proportion "
              f"cannot pass 1.0.")
        elif big < 0.001:
            w(f"  WARN  newsletter_signup never reaches 0.001. The model may "
              f"have answered in proportions where percentage points were "
              f"asked, so the values may be 100 times too small.")
        else:
            w(f"  ok    newsletter_signup largest |ate| = {big:.4f}, which is "
              f"a plausible proportion.")
    if don:
        big = max(abs(x) for x in don)
        if big > 2.0:
            w(f"  WARN  donation_ams reaches {big:.3f} dollars on a 0-10 "
              f"scale. Check the units.")
        else:
            w(f"  ok    donation_ams largest |ate| = {big:.3f} dollars on a "
              f"0-10 scale.")

    # The direction guard. See the module docstring.
    conds = sorted({c for c, o in values})
    pairs = [(values.get((c, "trust_post")), values.get((c, "distrust_post")))
             for c in conds]
    pairs = [(a, b) for a, b in pairs if a is not None and b is not None]
    disagree = sum(1 for a, b in pairs if a * b < 0)
    w("")
    w(f"  trust_post vs distrust_post, sign DISAGREES for "
      f"{disagree}/{len(pairs)} texts")
    w("     A trust-building text must raise trust_post and lower "
      "distrust_post.")
    w("     Most of the 16 texts should therefore disagree in sign.")
    for c in conds:
        a, b = values.get((c, "trust_post")), values.get((c, "distrust_post"))
        if a is None or b is None:
            continue
        mark = "ok " if a * b < 0 else "SAME"
        w(f"       {mark}  {c:<30} trust {a:+7.3f}   distrust {b:+7.3f}")
    return "\n".join(out) + "\n"


def pearson(x, y) -> float:
    if len(x) < 3:
        return float("nan")
    mx, my = statistics.mean(x), statistics.mean(y)
    num = sum((a - mx) * (b - my) for a, b in zip(x, y))
    dx = sum((a - mx) ** 2 for a in x) ** 0.5
    dy = sum((b - my) ** 2 for b in y) ** 0.5
    return num / (dx * dy) if dx and dy else float("nan")


def compare(a_dir: Path, b_dir: Path) -> str:
    """How far apart do the two variants land, over the 208 cells?

    There is no ground truth for this study, so agreement between the two
    variants is the only evidence this repository can make.
    """
    A, B = collect(a_dir), collect(b_dir)
    keys = sorted(set(A["by"]) & set(B["by"]))
    xa = [statistics.mean(A["by"][k]) for k in keys]
    xb = [statistics.mean(B["by"][k]) for k in keys]
    out = ["", f"COMPARE  A={a_dir.name}  B={b_dir.name}", "-" * 72,
           f"cells in both            {len(keys)}",
           f"Pearson r, all cells     {pearson(xa, xb):+.4f}",
           f"mean |A - B|             "
           f"{statistics.mean(abs(p - q) for p, q in zip(xa, xb)):.4f}"]
    out.append("")
    out.append("per outcome              r        mean|A-B|   mean A   mean B")
    for o in dict.fromkeys(o for c, o in keys):
        idx = [i for i, k in enumerate(keys) if k[1] == o]
        pa = [xa[i] for i in idx]
        pb = [xb[i] for i in idx]
        out.append(f"  {o:<22}{pearson(pa, pb):+7.4f}"
                   f"{statistics.mean(abs(p - q) for p, q in zip(pa, pb)):>12.4f}"
                   f"{statistics.mean(pa):>9.3f}{statistics.mean(pb):>9.3f}")
    # The units of the three groups differ, so the overall mean |A - B| mixes
    # points, dollars and proportions. The per-outcome rows are the readable
    # version.
    return "\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir", nargs="?")
    ap.add_argument("--out", default=None)
    ap.add_argument("--compare", nargs=2, default=None)
    args = ap.parse_args()

    if args.compare:
        txt = compare(Path(args.compare[0]), Path(args.compare[1]))
        print(txt)
        return 0

    run_dir = Path(args.run_dir)
    got = collect(run_dir)
    values = {k: statistics.mean(v) for k, v in got["by"].items()}
    rows = template_rows()
    missing = [k for k in rows if k not in values]
    if missing:
        raise SystemExit(f"{len(missing)} cells have no parsed draw: "
                         f"{missing[:5]}")
    extra = [k for k in values if k not in rows]
    if extra:
        raise SystemExit(f"{len(extra)} cells are not in the template: "
                         f"{extra[:5]}")

    draws = {k: len(v) for k, v in got["by"].items()}
    txt = audit(values, got["kinds"], run_dir.name)
    txt += (f"\n  draws for each cell      min {min(draws.values())}  "
            f"max {max(draws.values())}  "
            f"mean {statistics.mean(draws.values()):.2f}\n")
    print(txt)
    (run_dir / "AUDIT.txt").write_text(txt)

    if args.out:
        out = Path(args.out)
        with out.open("w", newline="\n") as fh:
            fh.write("condition,outcome,ate\n")
            for cond, o in rows:
                fh.write(f"{cond},{o},{fmt(o, values[(cond, o)])}\n")
        print(f"wrote {out}   {len(rows)} rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
