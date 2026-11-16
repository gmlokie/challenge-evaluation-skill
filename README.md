# MUSE UNIVERSAL CHALLENGE & JOB SOLVER

**⚠️ Before you install — read this first:** do not install blindly. Have your agent re-evaluate any skill in this repo against your own setup, and preview what it will change, before installing it. These skills were built and tuned for one agent's workflow — what works there may not fit yours. Evaluate first, preview, then install.

Pre-submit evaluation and post-result review for bounty, competition, and
challenge entries — plus self-measurement of an agent's own skills against a
no-skill baseline. The `challenge-evaluation` skill in this repo is the
universal solver kit: evaluate first, then submit — and measure whether your
own skills actually help.

Built for an AI agent that competes in coding bounties (make.fun, POIDH,
Synmerco, AgentPit, free mints), but the method is generic: evaluate first,
then submit — and measure whether your own skills actually help.

## Install

Copy the `challenge-evaluation/` folder into your agent's skills directory
(e.g. `~/workspace/custom-skills/` for Muse), then load the skill named
`challenge-evaluation`.

No credentials, no paid services, no network calls. The two bundled scripts
run locally:

- `scripts/check_output_tree.py` — flags dotfiles, symlinks, and non-plain
  names in the folders a build copies into its output (catches the exact
  output violation that failed three make.fun rounds on `screenshots/.gitkeep`).
- `scripts/bench_aggregate.py` — aggregates fixed-task benchmark rows into
  solve rate / tokens per solve / vs-baseline, with variance flags.

## What's inside

- `SKILL.md` — Part A: pre-submit entry evaluation (pre-register the
  evaluation, acceptance gate CERTIFIED / CONDITIONAL / REJECTED, independent
  review, pre-mortem, loop discipline, post-result review). Part B: skill
  self-measurement (fixed-task bench vs no-skill baseline, aggregate, library
  fitness audit).
- `references/` — acceptance gate checklist + reason codes, review protocol
  (evidence ladder E0–E6), experiment discipline (pre-registration,
  no-peeking), pre-mortem (FMEA), skill fitness (EFS-lite, Shadow Mode).
- `tests/` — synthetic benchmark rows for `bench_aggregate.py`.

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

## License

MIT — use it, fork it, break it, improve it.
