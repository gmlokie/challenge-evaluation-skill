#!/usr/bin/env python3
"""File-based run ledger for orchestrated-job-runner.

Stdlib only. No network, no credentials. One JSON file per run under
~/workspace/runs/ (or --ledger path). The parent agent owns the ledger;
workers never edit it directly.

Usage:
  run_ledger.py init --job SLUG --goal "..." --steps s1:"Name" s2:"Name" [--expensive s2] [--dir DIR]
  run_ledger.py start --ledger FILE --step s1
  run_ledger.py done --ledger FILE --step s1 --evidence "path|url|hash"
  run_ledger.py fail --ledger FILE --step s1 --note "what happened"
  run_ledger.py gate --ledger FILE --gate g1 --question "..." [--type approve|respond|edit|ignore]
  run_ledger.py answer --ledger FILE --gate g1 --result approved|denied|answered
  run_ledger.py status --ledger FILE
  run_ledger.py resume --ledger FILE
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone

DEFAULT_DIR = os.path.expanduser("~/workspace/runs")


def utcnow():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save(path, data):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, path)  # atomic: a crash mid-write never corrupts the ledger


def find_step(data, step_id):
    for s in data["steps"]:
        if s["id"] == step_id:
            return s
    return None


def log(data, step, event, note=""):
    data.setdefault("log", []).append(
        {"ts": utcnow(), "step": step, "event": event, "note": note})


def cmd_init(args):
    os.makedirs(args.dir, exist_ok=True)
    steps = []
    for spec in args.steps:
        sid, _, name = spec.partition(":")
        if not sid or not name:
            sys.exit(f"bad --steps entry {spec!r}, want id:\"Name\"")
        steps.append({"id": sid, "name": name,
                      "kind": "expensive" if sid in (args.expensive or []) else "cheap",
                      "status": "pending", "attempts": 0,
                      "evidence": None, "ended_utc": None})
    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M")
    path = os.path.join(args.dir, f"{args.job}-{ts}.json")
    data = {"job": args.job, "goal": args.goal, "created_utc": utcnow(),
            "status": "running", "steps": steps, "gates": [], "log": []}
    log(data, None, "init", f"run created, {len(steps)} steps")
    save(path, data)
    print(path)
    return 0


def cmd_start(args):
    data = load(args.ledger)
    step = find_step(data, args.step)
    if step is None:
        sys.exit(f"unknown step {args.step}")
    if step["status"] == "done":
        print(f"step {args.step} already done (evidence: {step['evidence']}) — skip, do not re-run")
        return 0
    step["status"] = "in_progress"
    step["attempts"] += 1
    log(data, args.step, "start", f"attempt {step['attempts']}")
    save(args.ledger, data)
    print(f"started {args.step} ({step['name']})")
    return 0


def cmd_done(args):
    data = load(args.ledger)
    step = find_step(data, args.step)
    if step is None:
        sys.exit(f"unknown step {args.step}")
    step["status"] = "done"
    step["evidence"] = args.evidence
    step["ended_utc"] = utcnow()
    log(data, args.step, "done", f"evidence: {args.evidence}")
    if all(s["status"] in ("done", "skipped") for s in data["steps"]):
        data["status"] = "done"
        log(data, None, "run-done", "all steps done/skipped")
    save(args.ledger, data)
    print(f"done {args.step}")
    return 0


def cmd_fail(args):
    data = load(args.ledger)
    step = find_step(data, args.step)
    if step is None:
        sys.exit(f"unknown step {args.step}")
    step["status"] = "failed"
    step["ended_utc"] = utcnow()
    log(data, args.step, "fail", args.note or "")
    if step["attempts"] >= 3:
        data["status"] = "failed"
        log(data, None, "circuit-open",
            f"step {args.step} failed 3x — stop, re-analyse, escalate")
    save(args.ledger, data)
    print(f"failed {args.step} (attempt {step['attempts']})")
    return 0


def cmd_gate(args):
    data = load(args.ledger)
    data["gates"].append({"id": args.gate, "type": args.type,
                          "question": args.question, "status": "pending"})
    data["status"] = "gated"
    log(data, None, "gate", f"{args.gate} [{args.type}]: {args.question}")
    save(args.ledger, data)
    print(f"gate {args.gate} pending — run is gated, do not proceed past it")
    return 0


def cmd_answer(args):
    data = load(args.ledger)
    for g in data["gates"]:
        if g["id"] == args.gate:
            g["status"] = args.result
            break
    else:
        sys.exit(f"unknown gate {args.gate}")
    if args.result == "denied":
        data["status"] = "aborted"
        log(data, None, "gate-denied", f"{args.gate} denied — run aborted")
    else:
        data["status"] = "running"
        log(data, None, "gate-answered", f"{args.gate} -> {args.result}")
    save(args.ledger, data)
    print(f"gate {args.gate} -> {args.result}")
    return 0


def cmd_status(args):
    data = load(args.ledger)
    print(f"job: {data['job']}  status: {data['status']}  goal: {data['goal']}")
    for s in data["steps"]:
        ev = f" evidence={s['evidence']}" if s["evidence"] else ""
        print(f"  {s['id']} [{s['kind']}] {s['status']} x{s['attempts']} {s['name']}{ev}")
    for g in data["gates"]:
        print(f"  gate {g['id']} [{g['type']}] {g['status']}: {g['question']}")
    return 0


def cmd_resume(args):
    data = load(args.ledger)
    print(f"job: {data['job']}  status: {data['status']}")
    skip, rerun, nxt = [], [], None
    for s in data["steps"]:
        if s["status"] == "done":
            skip.append(f"{s['id']} ({s['kind']}) — SKIP, evidence: {s['evidence']}")
        elif s["status"] == "in_progress":
            action = "re-run (cheap)" if s["kind"] == "cheap" else "VERIFY before re-running (expensive)"
            rerun.append(f"{s['id']} was in_progress — {action}")
            if nxt is None:
                nxt = s["id"]
        elif s["status"] == "pending" and nxt is None:
            nxt = s["id"]
    for line in skip:
        print("  SKIP: " + line)
    for line in rerun:
        print("  RESUME: " + line)
    pending_gate = [g for g in data["gates"] if g["status"] == "pending"]
    if pending_gate:
        print(f"  BLOCKED: gate {pending_gate[0]['id']} pending — ask Dhika, do not proceed past it")
    elif nxt:
        print(f"  NEXT: {nxt}")
    elif data["status"] == "done":
        print("  run is done — nothing to resume")
    return 0


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)
    pi = sub.add_parser("init")
    pi.add_argument("--job", required=True)
    pi.add_argument("--goal", required=True)
    pi.add_argument("--steps", nargs="+", required=True)
    pi.add_argument("--expensive", nargs="*")
    pi.add_argument("--dir", default=DEFAULT_DIR)
    pi.set_defaults(fn=cmd_init)
    for name, fn in [("start", cmd_start), ("done", cmd_done), ("fail", cmd_fail)]:
        ps = sub.add_parser(name)
        ps.add_argument("--ledger", required=True)
        ps.add_argument("--step", required=True)
        if name == "done":
            ps.add_argument("--evidence", required=True)
        if name == "fail":
            ps.add_argument("--note", default="")
        ps.set_defaults(fn=fn)
    pg = sub.add_parser("gate")
    pg.add_argument("--ledger", required=True)
    pg.add_argument("--gate", required=True)
    pg.add_argument("--question", required=True)
    pg.add_argument("--type", default="approve",
                    choices=["approve", "respond", "edit", "ignore"])
    pg.set_defaults(fn=cmd_gate)
    pa = sub.add_parser("answer")
    pa.add_argument("--ledger", required=True)
    pa.add_argument("--gate", required=True)
    pa.add_argument("--result", required=True,
                    choices=["approved", "denied", "answered"])
    pa.set_defaults(fn=cmd_answer)
    for name, fn in [("status", cmd_status), ("resume", cmd_resume)]:
        ps = sub.add_parser(name)
        ps.add_argument("--ledger", required=True)
        ps.set_defaults(fn=fn)
    args = p.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
