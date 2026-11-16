# MUSE UNIVERSAL CHALLENGE & JOB SOLVER

**⚠️ Before you install — read this first:** do not install blindly. Have your agent re-evaluate any skill in this repo against your own setup, and preview what it will change, before installing it. These skills were built and tuned for one agent's workflow — what works there may not fit yours. Evaluate first, preview, then install.

Pre-submit evaluation and post-result review for bounty, competition, and
challenge entries — plus self-measurement of an agent's own skills against a
no-skill baseline. The skills in this repo form the universal solver kit:
evaluate first, then submit — and measure whether your own skills actually
help.

Built for an AI agent that competes in coding bounties (make.fun, POIDH,
Synmerco, AgentPit, free mints), but the method is generic: evaluate first,
then submit — and measure whether your own skills actually help.

## Install

Do not install blindly — have your agent run this flow first:

1. **Evaluate** — re-evaluate the skill against your own setup: does it fit your runtime, tools, and workflow?
2. **Review** — review what the skill changes and what it assumes.
3. **Preview** — preview the install: which files land where, what gets loaded.
4. **Install** — copy the skill folder(s) you want into your agent's skills directory (e.g. `~/workspace/custom-skills/` for Muse), then load each skill by name.
5. **Develop further** — adapt the skill to your setup and improve it. A skill you never tune to your own work stays generic; the install is the start, not the end.

No credentials, no paid services, no network calls. The bundled scripts
run locally:

- `challenge-evaluation/scripts/check_output_tree.py` — flags dotfiles, symlinks, and non-plain
  names in the folders a build copies into its output (catches the exact
  output violation that failed three make.fun rounds on `screenshots/.gitkeep`).
- `challenge-evaluation/scripts/bench_aggregate.py` — aggregates fixed-task benchmark rows into
  solve rate / tokens per solve / vs-baseline, with variance flags.
- `orchestrated-job-runner/scripts/run_ledger.py` — file-based run ledger: resume after a crash,
  HITL gates, retry with circuit breaker.
- `web-data-extraction/scripts/validate.py` — validates extracted records
  (schema, dedupe, timestamps).

## What's inside

- `challenge-evaluation/` — the evaluation gate: Part A pre-submit entry evaluation (pre-register the
  evaluation, acceptance gate CERTIFIED / CONDITIONAL / REJECTED, independent
  review, pre-mortem, loop discipline, post-result review). Part B skill
  self-measurement (fixed-task bench vs no-skill baseline, aggregate, library
  fitness audit). Includes `references/`, `scripts/`, `tests/` (synthetic benchmark rows).
- `task-analyzer/` — turn vague input into a structured brief: sealed requirement checklist
  (REQ IDs + Given/When/Then), drift check before submit.
- `research-engine/` — hypothesis-driven research over multiple sessions: pre-registration,
  falsifiers, dead-end log, 6-dimension rigor review.
- `orchestrated-job-runner/` — file-based run ledger for multi-step jobs: patterns, HITL gates,
  retry/circuit breaker, resume after crash.
- `web-data-extraction/` — free-source ladder (no-key API → RSS → static HTML → Playwright),
  schema-first, validate + dedupe.
- `entry-test-cycle/` — test campaign before submit: plan → cases → defects → closure,
  plus flaky-pattern handling.
- `learning-memory/` — capture, recall, consolidate, and forget what the agent learns —
  local files only, with an admission gate.
- `EVALUATION-REPORT.md` — evaluation from USING these skills: per-skill verdicts BERGUNA /
  TIDAK PERLU / DITINGKATKAN with real evidence, plus install-flow health. Honest note:
  the 6 new skills are DRAFTS — pilots only, full Part B bench not yet run.

## Proven on real cases

- **best-game-01 (make.fun):** `check_output_tree.py` flags
  `screenshots/.gitkeep` — the exact reason rounds 1–3 were rejected.
  A clean tree passes.
- **markdown-render-speed-02 (make.fun):** applying the pre-registered
  decision rule ("beat marked at 95% one-sided confidence") to the recorded
  numbers (0.97x in-process, slower end-to-end) gives NO-GO / STAND PAT.

## Sources

Method adapted from three repos (evaluate-first discipline, baseline
comparison, meta-skill patterns) and rewritten for an agent workflow:

- https://github.com/BaseIntelligence/agent-challenge
- https://github.com/currenjin/skillbench
- https://github.com/simota/agent-skills

The six solver skills were adapted from 13 further repos — see
`EVALUATION-REPORT.md` for per-skill evidence and verdicts.

## License

MIT — use it, fork it, break it, improve it.
