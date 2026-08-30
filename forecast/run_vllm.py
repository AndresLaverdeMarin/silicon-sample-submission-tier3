#!/usr/bin/env python3
"""
Run the structured forecast on a LOCAL model, with the vLLM offline engine.

PROVENANCE. Copied and adapted from
  /home/jovyan/LLMmegastudy/modelbench/structured_forecast_vllm.py
  sha256 56886d2dc5ccc1d839bef6c641119919ead1b4282de8070ce702fcc2ba8eb79c
The engine settings are unchanged. The scorer is removed, because the target
study has no ground truth in this repository. A local run makes NO paid call:
`spend_usd` is 0.00.

THREE ENGINE FACTS, MEASURED ON THIS MACHINE 2026-08-30. Do not remove them.
  1. `additional_config={"gdn_prefill_backend": "triton"}` is necessary.
     Qwen3.8-27B is a hybrid model with Gated Delta Net layers. vLLM picks the
     FlashInfer GDN prefill kernel by default and builds it just in time. The
     build needs `nvcc`, and this machine has no CUDA toolkit, so the engine
     dies at the first prefill.
  2. The tokenizer chat template must be applied with `enable_thinking=False`.
     Without it the model writes `<think>...` and 88% of the answers never
     reach a number.
  3. A listwise reply needs about `40 * n_arms + 128` output tokens. A
     narrower budget truncates the last lines of a 16-arm reply.

WHY THESE RUN OPTIONS. All three were measured, not chosen.
  listwise      beats pointwise. Qwen3.8-27B on the Broockman archive:
                +0.3468 against +0.1450 in Pearson r. On the Voelkel archive:
                +0.6558 against +0.5795.
  temperature   0.85 with 8 draws. 0 of 20 paired tests separated the
                temperatures, so the choice is free. The 8-draw ensemble is
                load-bearing: at temperature 0, a reshuffle of the arm order
                alone moves the predictions to r = 0.57-0.73 against each
                other, so one call is not a stable estimate.
  population    OFF is the control. Three earlier tests found the demographic
                block did not help (+0.059, -0.124, -0.168 in Pearson r). This
                run makes both variants and reports how far apart they land.

    P=/home/jovyan/LLMmegastudy/.venv-vllm/bin/python
    $P forecast/run_vllm.py --print-prompts
    $P forecast/run_vllm.py --label A_pop_off
    $P forecast/run_vllm.py --label B_pop_on --population --go

**Written in ASD-STE100 Simplified Technical English.**
"""
from __future__ import annotations

import argparse
import json
import os
import random
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("VLLM_LOGGING_LEVEL", "WARNING")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

import core                                                     # noqa: E402
import megastudy                                                # noqa: E402
from core import Opt                                            # noqa: E402

STUDY = megastudy.STUDY_KEY
SPEC = megastudy.SPEC

# Characters for each token, measured with the Qwen3.8-27B tokenizer on
# 12,929,556 characters of probe prompts, 2026-08-29. Source:
# /home/jovyan/LLMmegastudy/modelbench/output/runs/
# 2026-08-29_openrouter_flash_probe/probe_openrouter.py
CHARS_PER_TOKEN = 3.79


def build(args):
    """Make the cells, the work plan and every prompt, and send nothing."""
    cells = megastudy.load_cells(args.outcomes)
    rng = random.Random(args.seed)
    work = core.build_work(cells, args.mode, args.framings, args.samples, rng)
    if args.limit:
        work = work[: args.limit]
    prompts, jobs = [], []
    for job in work:
        cell = job["cell"]
        arms = [cell["arms"][i] for i in job["order"]]
        framing = (core.FRAMINGS[job["framing"] % len(core.FRAMINGS)]
                   if args.framings > 1 else None)
        prompts.append(core.render(cell, arms, args.mode, framing))
        jobs.append(job)
    return cells, work, prompts, jobs


def print_prompts(args) -> int:
    """Render one prompt for each named outcome and print it with its size."""
    show = args.show or ["trust_multidimensional", "donation_ams",
                         "newsletter_signup", "funding_perceptions",
                         "distrust_post"]
    cells = {c["outcome"]: c for c in megastudy.load_cells(None)}
    rng = random.Random(args.seed)
    sizes = []
    for name in show:
        cell = cells[name]
        order = list(range(len(cell["arms"])))
        rng.shuffle(order)
        arms = ([cell["arms"][i] for i in order] if args.mode == "listwise"
                else [cell["arms"][order[0]]])
        p = core.render(cell, arms, args.mode)
        print("=" * 78)
        print(f"OUTCOME {name}   mode {args.mode}   arms {len(arms)}   "
              f"population {Opt.population}")
        print("=" * 78)
        print(p)
        print("-" * 78)
        print(f"chars {len(p):,}   ~tokens {len(p) / CHARS_PER_TOKEN:,.0f}\n")
        sizes.append((name, len(p)))

    print("=" * 78)
    print(f"PROMPT SIZES   mode {args.mode}   population {Opt.population}")
    print("=" * 78)
    print(f"{'outcome':<26}{'kind':<11}{'items':>6}{'chars':>9}{'~tokens':>10}"
          f"{'flip':>7}")
    for name, cell in cells.items():
        order = list(range(len(cell["arms"])))
        rng.shuffle(order)
        arms = ([cell["arms"][i] for i in order] if args.mode == "listwise"
                else [cell["arms"][order[0]]])
        p = core.render(cell, arms, args.mode)
        print(f"{name:<26}{cell['block']['kind']:<11}"
              f"{cell['block']['n_items']:>6}{len(p):>9,}"
              f"{len(p) / CHARS_PER_TOKEN:>10,.0f}"
              f"{str(SPEC['flip'](cell)):>7}")
    print("\nSIGN CHECK. Every prompt is written on the SAME scale as the")
    print("submission, so scale_flip is False everywhere. The two cases that")
    print("need care are printed in full:")
    for name in ("distrust_post", "funding_perceptions"):
        b = cells[name]["block"]
        print(f"  {name:<22} 0 = {b['low_end']}")
        print(f"  {'':<22} {'100' if b['kind'] == 'slider100' else 'top'} "
              f"= {b['high_end']}")
    print("\nUNITS OF THE SUBMITTED ate")
    for name, cell in cells.items():
        k = cell["block"]["kind"]
        print(f"  {name:<26} answer x {megastudy.UNIT_FACTOR[k]:<6} -> "
              f"{megastudy.UNIT_NAME[k]}")
    print("\nNothing was sent.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="Qwen/Qwen3.8-27B")
    ap.add_argument("--label", default=None)
    ap.add_argument("--mode", default="listwise",
                    choices=["pointwise", "listwise"])
    ap.add_argument("--framings", type=int, default=1)
    ap.add_argument("--samples", type=int, default=8)
    ap.add_argument("--temperature", type=float, default=0.85)
    ap.add_argument("--top-p", type=float, default=0.95)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--outcomes", nargs="*", default=None)
    ap.add_argument("--show", nargs="*", default=None)
    ap.add_argument("--population", action="store_true",
                    help="add the recruitment-target table to STUDY.")
    ap.add_argument("--items", default="all", choices=["all", "one"])
    ap.add_argument("--gpu-memory-utilization", type=float, default=0.90)
    ap.add_argument("--max-num-seqs", type=int, default=32)
    ap.add_argument("--max-tokens", type=int, default=None)
    ap.add_argument("--gdn-backend", default="triton",
                    choices=["triton", "flashinfer", "auto"])
    ap.add_argument("--out-dir", default=None)
    ap.add_argument("--print-prompts", action="store_true")
    ap.add_argument("--go", action="store_true")
    args = ap.parse_args()

    Opt.population = args.population
    Opt.items = args.items

    if args.print_prompts:
        return print_prompts(args)

    cells, work, prompts, jobs = build(args)
    longest = max(len(p) for p in prompts)
    mean = sum(len(p) for p in prompts) / len(prompts)
    n_out = max(40 * len(j["order"]) + 128 for j in jobs)
    label = args.label or (args.model.split("/")[-1]
                           + ("_pop_on" if args.population else "_pop_off"))
    print(f"model          {args.model}")
    print(f"mode           {args.mode}   population {args.population}   "
          f"items {args.items}")
    print(f"cells          {len(cells)} outcomes   arms "
          f"{len(cells[0]['arms'])} interventions")
    print(f"samples        {args.samples}   temperature {args.temperature}   "
          f"top_p {args.top_p}")
    print(f"calls          {len(prompts):,}")
    print(f"arms asked     {sum(len(j['order']) for j in jobs):,}")
    print(f"mean prompt    {mean:,.0f} chars  "
          f"~{mean / CHARS_PER_TOKEN:,.0f} tokens")
    print(f"longest prompt {longest:,} chars  "
          f"~{longest / CHARS_PER_TOKEN:,.0f} tokens")
    print(f"max_tokens     {n_out}")
    print(f"cost           $0.00  (local weights, no paid call)")
    if not args.go:
        print("\nDRY RUN. Nothing ran. Add --go.")
        return 0

    from vllm import LLM, SamplingParams                        # noqa: E402
    from transformers import AutoTokenizer                      # noqa: E402

    max_len = min(32768, (longest // 3) + n_out + 512)
    t_load = time.time()
    # See engine fact 1 in the module docstring.
    llm = LLM(model=args.model, dtype="bfloat16",
              gpu_memory_utilization=args.gpu_memory_utilization,
              max_model_len=max_len, max_num_seqs=args.max_num_seqs,
              enable_prefix_caching=True, trust_remote_code=True,
              additional_config={"gdn_prefill_backend": args.gdn_backend})
    print(f"loaded in      {time.time() - t_load:.1f} s")

    # See engine fact 2 in the module docstring.
    tok = AutoTokenizer.from_pretrained(args.model, trust_remote_code=True)
    chat = [tok.apply_chat_template([{"role": "user", "content": t}],
                                    tokenize=False, add_generation_prompt=True,
                                    enable_thinking=False) for t in prompts]

    started = datetime.now(timezone.utc)
    t0 = time.time()
    # See engine fact 3 in the module docstring.
    params = [SamplingParams(n=1, temperature=args.temperature,
                             top_p=args.top_p,
                             max_tokens=args.max_tokens
                             or (48 if args.mode == "pointwise"
                                 else 40 * len(j["order"]) + 128),
                             seed=args.seed + j["sample"])
              for j in jobs]
    outs = llm.generate(chat, params)
    wall = time.time() - t0
    ended = datetime.now(timezone.utc)

    out_dir = Path(args.out_dir) if args.out_dir else (
        ROOT / "forecast/runs" / f"{started.date()}_{label}")
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "forecast.jsonl"

    ok_n = asked_n = 0
    with path.open("w") as fh:
        for job, out in zip(jobs, outs):
            cell, order = job["cell"], job["order"]
            text = out.outputs[0].text if out.outputs else ""
            n = len(order)
            flip = SPEC["flip"](cell)
            factor = SPEC["unit_factor"](cell)
            lo, hi = SPEC["value_range"](cell)
            if args.mode == "listwise":
                p = core.parse_listwise(text, n, lo, hi)
                values, pmode, n_parsed = p["values"], p["mode"], p["n_parsed"]
            else:
                p = core.parse_pointwise(text, lo, hi)
                values = {1: p["value"]} if p["ok"] else {}
                pmode = "single" if p["ok"] else (p["why"] or "unparsed")
                n_parsed = len(values)
            answers = []
            for pos in range(1, n + 1):
                idx = order[pos - 1]
                arm = cell["arms"][idx]
                raw = values.get(pos)
                val = None if raw is None else (-raw if flip else raw)
                answers.append({
                    "position": pos, "arm_index": idx,
                    "condition": arm["text"],
                    "value_raw": raw,        # as given, on the prompt's scale
                    "scale_flip": flip,      # TRUE: the submission points back
                    "value": val,            # after the flip
                    "ate": None if val is None else val * factor,
                    "ate_units": megastudy.UNIT_NAME[cell["block"]["kind"]],
                    "unit_factor": factor,
                    "ok": raw is not None})
            ok_n += n_parsed
            asked_n += n
            fh.write(json.dumps({
                "study": STUDY, "mode": args.mode,
                "cell_id": cell["cell_id"], "outcome": cell["outcome"],
                "kind": cell["block"]["kind"],
                "population_block": args.population,
                "framing": job["framing"], "sample": job["sample"],
                "seed": args.seed + job["sample"], "n_arms": n,
                "arm_order": order, "parse_mode": pmode,
                "n_parsed": n_parsed, "n_asked": n, "answers": answers,
                "error": None,
                "raw": None if n_parsed == n else (text or "")[:400]}) + "\n")

    meta = {
        "method": "structured_forecast, listwise",
        "model": args.model,
        "served_by": "local vLLM offline engine",
        "study": STUDY, "mode": args.mode,
        "population_block": args.population, "items": args.items,
        "anchor_line": Opt.anchor,
        "framings": args.framings, "samples": args.samples,
        "temperature": args.temperature, "top_p": args.top_p,
        "seed": args.seed, "seed_rule": "seed + sample index",
        "thinking": False,
        "call_window_start": started.isoformat(),
        "call_window_end": ended.isoformat(),
        "calls": len(prompts), "arms_asked": asked_n, "arms_parsed": ok_n,
        "parse_rate": round(ok_n / max(asked_n, 1), 4),
        "spend_usd": 0.00,
        "price_table": None,
        "price_table_source": "not applicable: local weights, no paid call",
        "wall_clock_s": round(wall, 1),
        "max_model_len": max_len,
        "gpu_memory_utilization": args.gpu_memory_utilization,
        "mean_prompt_chars": round(mean, 1),
        "longest_prompt_chars": longest,
        "stimulus_provenance": core.provenance(
            [megastudy.STIM_DIR / f for f in
             sorted(megastudy.INTERVENTIONS.values())]
            + list(SPEC["stimulus_files"])),
    }
    (out_dir / "forecast.meta.json").write_text(json.dumps(meta, indent=1))
    print(f"\ncalls {len(prompts):,}   arms parsed {ok_n}/{asked_n} "
          f"({100 * ok_n / max(asked_n, 1):.1f}%)   {wall / 60:.1f} min")
    print(f"wrote {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
