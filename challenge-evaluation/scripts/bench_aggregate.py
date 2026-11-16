#!/usr/bin/env python3
"""Aggregate a skill-bench results log into a leaderboard table.

Adapted from currenjin/skillbench harness/aggregate.py (MIT): same
semantics — a task counts as solved for a skill when the MAJORITY of its
runs pass; tokens-per-solve is the median of (in + out + cache_read) over
solved runs only; tasks whose runs disagree are flagged as high-variance.

Differences from upstream: reads one results JSONL log (any path) instead of
a runs/<week>/ tree, because this workspace has no Claude Code headless
runner — the bench protocol is manual (see challenge-evaluation SKILL.md,
Part B): run fixed tasks with the skill ON and with the skill OFF (baseline),
append one JSON record per run, then aggregate here.

Record format (one JSON object per line):
  {"skill": "my-skill" | "baseline", "task": "task-id", "run": 1,
   "solved": true, "tokens_in": 1234, "tokens_out": 5678,
   "cache_read": 0, "duration_s": 12.3, "ts": "2026-11-16T10:00:00+00:00"}

Usage:
  python3 bench_aggregate.py --log results.jsonl [--prev older.jsonl]

Prints a GitHub-flavoured markdown leaderboard. Exit 0 on success.
"""
import argparse
import json
import statistics
import sys
from collections import defaultdict


def load_log(path):
    """-> {skill: {task: [records]}}"""
    data = defaultdict(lambda: defaultdict(list))
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            data[r["skill"]][r["task"]].append(r)
    return data


def summarize(by_task):
    tasks = solved = 0
    token_costs = []
    for records in by_task.values():
        tasks += 1
        wins = [r for r in records if r["solved"]]
        if len(wins) * 2 > len(records):
            solved += 1
            costs = [r.get("tokens_in", 0) + r.get("tokens_out", 0)
                     + (r.get("cache_read") or 0)
                     for r in wins
                     if r.get("tokens_in") is not None]
            if costs:
                token_costs.append(statistics.median(costs))
    variance = sum(1 for records in by_task.values()
                   if len({r["solved"] for r in records}) > 1)
    return {
        "tasks": tasks,
        "solve_rate": solved / tasks if tasks else 0.0,
        "tokens_per_solve": statistics.median(token_costs) if token_costs else None,
        "high_variance_tasks": variance,
    }


def fmt_tokens(n):
    return f"{round(n / 1000)}k" if n else "—"


def main():
    p = argparse.ArgumentParser(description="Aggregate a skill-bench results log.")
    p.add_argument("--log", required=True, help="results JSONL log")
    p.add_argument("--prev", help="older results JSONL log, for the Δ column")
    args = p.parse_args()

    stats = {s: summarize(t) for s, t in load_log(args.log).items()}
    base = stats.pop("baseline", None)

    prev_rank = {}
    if args.prev:
        prev = {s: summarize(t) for s, t in load_log(args.prev).items()
                if s != "baseline"}
        ordered = sorted(prev, key=lambda s: -prev[s]["solve_rate"])
        prev_rank = {s: i + 1 for i, s in enumerate(ordered)}

    print("| # | Skill / Setup | Solve rate | Δ | Tokens per solve | vs baseline |")
    print("|---|---|---|---|---|---|")
    if base:
        print(f"| — | *baseline · no skill* | *{base['solve_rate']:.0%}* | — "
              f"| *{fmt_tokens(base['tokens_per_solve'])}* | — |")
    ranked = sorted(stats, key=lambda s: -stats[s]["solve_rate"])
    for i, skill in enumerate(ranked, 1):
        s = stats[skill]
        if skill in prev_rank:
            d = prev_rank[skill] - i
            delta = f"▲{d}" if d > 0 else f"▼{-d}" if d < 0 else "—"
        else:
            delta = "new"
        vs = f"{(s['solve_rate'] - base['solve_rate']) * 100:+.0f}pt" if base else "—"
        note = f" ⚠{s['high_variance_tasks']}" if s["high_variance_tasks"] else ""
        print(f"| {i} | {skill} | {s['solve_rate']:.0%}{note} "
              f"| {delta} | {fmt_tokens(s['tokens_per_solve'])} | {vs} |")
    return 0


if __name__ == "__main__":
    sys.exit(main())
