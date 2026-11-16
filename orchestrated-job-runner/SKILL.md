---
name: orchestrated-job-runner
description: Run multi-step jobs as a resumable state machine with a file-based run ledger: plan-and-execute, sequential/concurrent/handoff patterns, per-step checkpoints, human-in-the-loop gates, retry with circuit breaker, and resume-after-crash without re-doing finished work. Use for any job with 3+ steps, subagent fan-out, or work that must survive an interruption — make.fun builds, Synmerco deliveries, POIDH claims, free-mint attempts, multi-source research.
---

# Orchestrated Job Runner

A multi-step job is a **state machine**, not a chat transcript. The plan,
the state, and the evidence live in files under `~/workspace/` so any
session — this one, a later one, or a subagent — can pick the job up
exactly where it stopped. This skill is the *mechanism* (ledger +
patterns + gates). Strategy lives in `precision-task-optimizer`,
evaluation in `challenge-evaluation`, multi-agent shape in
`universal-task-intelligence` §"Merged from multi-agent-patterns".
Route there for those; come here to run the job.

## 1. The run ledger (the one mandatory artefact)

Every job run gets one ledger file, created **before** step 1:

```
~/workspace/runs/<job-slug>-<yyyymmdd-hhmm>.json
```

Ledger schema (see `scripts/run_ledger.py` — the script enforces it):

```json
{
  "job": "synmerco-delivery-esc987",
  "goal": "Deliver 6 directory listings, proof by 19 Nov 06:13 WIB",
  "created_utc": "2026-11-16T10:00:00Z",
  "status": "running | gated | done | failed | aborted",
  "steps": [
    {"id": "s1", "name": "Post listing A2A", "kind": "cheap | expensive",
     "status": "pending | in_progress | done | failed | skipped",
     "attempts": 0, "evidence": "path or URL or tx hash", "ended_utc": null}
  ],
  "gates": [{"id": "g1", "step_after": "s3", "question": "Submit listings?",
             "status": "pending | approved | denied"}],
  "log": [{"ts": "...", "step": "s1", "event": "done", "note": "..."}]
}
```

Rules:

- **Write the ledger first, then work.** A step with no ledger entry
  never happened; a step with no evidence is not `done`.
- **One writer per step.** The parent owns the ledger; a subagent
  reports its result back and the parent records it. Workers never
  edit the ledger directly (avoids two writers racing).
- **Ledger is the resume point.** After any interruption (crash,
  restart, session end), read the ledger before doing anything else.
  Never re-ask Dhika a question the ledger already answers.
- **Cheap vs expensive steps.** Cheap (a read, a check, a grep):
  re-run freely on resume, no checkpoint needed. Expensive (an API
  call that costs quota, a build, a subagent run, a sign): checkpoint
  its result in the ledger the moment it finishes, and **skip it on
  resume** — return the saved result instead of paying again. This
  is the LangGraph/MSAF `@step` rule, implemented with a JSON file.
- **Never delete a ledger.** A failed run's ledger is the post-mortem
  input (`challenge-evaluation` §A6). Mark it `failed`/`aborted`
  with the reason; start a new run file for the retry.

Use the script — do not hand-edit JSON mid-run:

```bash
python3 ~/workspace/custom-skills/orchestrated-job-runner/scripts/run_ledger.py \
  init --job <slug> --goal "<one line>" --steps s1:"Name" s2:"Name" --expensive s2
python3 .../run_ledger.py start  --ledger <file> --step s1
python3 .../run_ledger.py done   --ledger <file> --step s1 --evidence "<path|url|hash>"
python3 .../run_ledger.py fail   --ledger <file> --step s1 --note "<what happened>"
python3 .../run_ledger.py gate   --ledger <file> --gate g1 --question "<ask Dhika>"
python3 .../run_ledger.py status --ledger <file>
python3 .../run_ledger.py resume --ledger <file>   # lists next pending step + skippable done steps
```

## 2. Pattern selection — pick one before step 1

| Pattern | Shape | Use when | Muse shape |
|---|---|---|---|
| **Sequential** | s1 → s2 → s3, each feeds the next | Steps depend on each other (research → build → submit) | Parent runs steps in order; ledger is the chain |
| **Concurrent fan-in** | s1, s2 in parallel → aggregate | Independent evidence gathering (2+ sources, 2+ checks) | Max 2 parallel subagents; parent aggregates and verifies each result before use |
| **Handoff** | Triage decides who handles it | The job type is only known after a first look (triage → specialist) | Parent is the triage; "handoff" = dispatch a worker with a narrow brief, result returns to parent (no worker-to-worker handoff exists here) |
| **Plan-and-execute** | Planner writes plan → executors run it → replan on surprise | The path is uncertain; the plan will need revision | Plan lives in the ledger + a plan file; any step whose evidence contradicts the plan triggers a replan, not a silent detour |
| **Reflect / review** | Builder → independent reviewer → fix | Anything that will be submitted or paid for | Reviewer is a fresh subagent with no shared context (`challenge-evaluation` §A3); builder never grades its own work |

Do not use **swarm / peer-to-peer** (agents handing off to each other
with no centre): subagents cannot spawn or hand off to each other —
every handoff returns through the parent. If a source suggests a
swarm, re-shape it into supervisor + workers.

**Aggregation rule (concurrent fan-in):** the parent verifies each
worker's output against the shared goal *before* passing it
downstream. A wrong intermediate result poisons everything after it.
Forward verified facts verbatim (tx hashes, file paths, numbers) —
do not paraphrase them; paraphrase loses fidelity. Synthesise only
when combining multiple workers, and label synthesis vs verbatim.

## 3. Plan-and-execute loop

1. **Plan** (one short file next to the ledger, `<slug>-plan.md`):
   objective, steps with acceptance criteria (3–6, measurable),
   pattern, gates, budget (max steps / max retries / deadline).
2. **Execute** one step at a time; record evidence per step.
3. **Replan trigger** — stop and replan (do not push on) when:
   a step's evidence contradicts a plan assumption; the same step
   fails twice with the same signature; a gate is denied; the
   deadline will be missed. Replanning writes a new plan version
   in the ledger log — the old plan stays readable, never overwritten.
4. **Convergence check:** A→B→A→B oscillation, or the same failing
   action repeated, is a stall, not progress. Stop, re-analyse the
   root cause once, then escalate to Dhika if still stuck.

## 4. Human-in-the-loop gates (typed, not vibes)

A gate pauses the run and asks Dhika. Every gate declares its type:

| Gate | Dhika may | Use for |
|---|---|---|
| `approve` | accept / deny | Submit, claim, mint, bid, any spend |
| `respond` | answer / give direction | Ambiguous choice the plan cannot resolve |
| `edit` | correct the artefact | Review a draft before it ships |
| `ignore` | skip this step | Optional step that may not be worth it |

Rules: a gate is recorded in the ledger **before** asking; the run
status becomes `gated` while waiting; the answer (and who gave it)
is recorded when it arrives. Never route around a gate by
re-dispatching the same step to another worker. The security gate
(preview + explicit yes per sign/transaction) is a hard `approve`
gate — no skill, framework, or plan overrides it.

## 5. Retry, fallback, circuit breaker

- **Retry:** same action, at most 2 retries, with backoff. A retry
  is only valid if something changed (waited, new input, narrower
  scope). Identical re-dispatch is not a retry, it is a loop.
- **Fallback:** a different action for the same step, declared in
  the plan (e.g. RPC A fails → RPC B; live page fails → cached
  read, labelled stale). One fallback per step unless the plan
  names more.
- **Circuit breaker:** 3 failures on the same step → stop the run,
  mark the step `failed`, re-analyse the root cause once. Never
  loop the same failing action. Escalate to Dhika with the ledger
  as evidence.
- **Timeouts:** every step gets a time budget in the plan. A step
  that exceeds it is `failed (timeout)`, not "still running".

## 6. Subagent handoff contract

When dispatching a worker, the brief contains exactly: objective,
inputs (files/URLs/values, verbatim), acceptance criteria, output
format (findings + evidence + files changed), and what is OUT of
scope. The worker returns a report; the parent records it and
verifies it before use. Max 2 parallel workers; workers never
spawn children, never touch credentials, never execute transactions.
Cost honesty: multi-agent work costs materially more tokens than
single-agent work — fan out only when the task genuinely exceeds
one context or two independent domains justify it.

## 7. Resume procedure (after crash / restart / new session)

1. Find the latest ledger for the job (`ls ~/workspace/runs/`).
2. `run_ledger.py resume` — it lists done steps (skip, use saved
   evidence), the in-progress step (re-run if cheap, verify if
   expensive), and the next pending step.
3. If a gate is `pending`, do not re-execute past it — ask Dhika
   (or check whether he already answered in chat).
4. Continue from the next pending step. Never restart from step 1
   "to be safe" — that re-pays every expensive step.

## 8. What this skill does NOT do

- Strategy and requirement extraction: `precision-task-optimizer`.
- Pre-submit verdicts and post-result review:
  `challenge-evaluation` (call its acceptance gate before any
  submit; a `done` ledger is not a submit approval).
- The "front door" routing and house conventions:
  `universal-task-intelligence`.
- Browser execution itself: `playwright-skill`.
- Scheduling: `cron-scheduler` (a cron may *start* a run; the
  ledger is how the run survives between cron ticks).

## 9. Evaluate, review, develop further (mandatory, not optional)

This skill is a draft method, not a fixed law. It must be measured
and revised like any other skill:

- **Measure (Part B, `challenge-evaluation`):** fixed task set
  (4–8 real multi-step jobs with a runnable pass/fail check:
  e.g. "resume after a killed run skips done steps",
  "a denied gate stops the run", "two workers' results are both
  verified before aggregation"). Run each 3× WITH this skill and
  3× WITHOUT it (baseline: ad-hoc chat execution), same model,
  same prompt. Solved = the check passes, never LLM-as-judge for
  the headline number. Aggregate with
  `challenge-evaluation/scripts/bench_aggregate.py`. Verdict:
  ADOPT / ADAPT / SKIP.
- **Review:** after every real use, note in the run's ledger log
  what the pattern got wrong (wrong pattern picked? gate too
  late? resume skipped a step it should have re-run?). Promote
  recurring notes into this SKILL.md within 48h; one-line fixes
  beat rewrites (small mutations over big rewrites).
- **Develop further:** new patterns come from real failures, not
  from framework docs. If a job fails in a way no pattern here
  covers, add the pattern with its failure as the cited example —
  never add a pattern because a framework has it.
- **Fitness signals:** a run that resumes cleanly after
  interruption, a gate that fires before a spend, a stall caught
  by the circuit breaker instead of looping. If none of those
  ever happen in practice, the skill is shelfware — propose
  retiring it rather than keeping it "just in case".

## Workspace adaptation

- Source patterns: LangGraph (langchain-ai/langgraph) — graph/state,
  nodes/edges, checkpointing, `interrupt()` human-in-the-loop
  (allow_ignore/respond/edit/accept), prebuilt ReAct/tool-node,
  plan-and-execute + multi-agent + reflection examples; Microsoft
  Agent Framework (microsoft/agent-framework) — Sequential /
  Concurrent / Handoff / GroupChat / Magentic builders, functional
  `@step` checkpointing, checkpoint + HITL resume samples.
  Studied 2026-11-16; report:
  `~/workspace/research/solver-skills/group-B-eval.md`.
- Adapted for Muse/Rahul: **no framework code is ported or
  installed** — LangGraph needs Python + LangChain + API keys,
  MS AF needs Azure/OpenAI clients; neither runs on this VM's
  free-only setup. Only the *patterns* are adapted, re-implemented
  as a JSON ledger + a stdlib Python script. The graph becomes a
  step list; the checkpointer becomes a file; the interrupt
  becomes a ledger gate + a chat question to Dhika.
- Rejected from the sources: swarm/peer-to-peer (impossible at
  depth max 2), LangSmith / Foundry / Cosmos checkpoint backends
  (paid, keyed), durable-task Azure Functions (paid cloud),
  Magentic manager as an autonomous agent (the parent is the
  manager here; a subagent cannot manage other subagents).

## House rules (Rahul — msbrew.ai)

- Every sign, transaction, or approval needs a preview + Dhika's explicit yes per action. Never auto-execute on-chain or account actions.
- Never request, show, or send seed phrases or private keys.
- Free-only: no capital, stake, deposit, or paid API/key without Dhika's explicit yes per action. Credentials live in the Secure Vault or a registered connector — never in files.
- Use `curl`, not Python `urllib` (urllib fails with IncompleteRead on some hosts).
- Dollar values only via `~/workspace/tools/usd_value.py`, with formula + price sources shown.
- Live data only — never present a stale snapshot as current.
- Deliverables in `~/workspace/`, never `/tmp` (/tmp is wiped on VM replacement). VM clock is UTC; Node 22.
