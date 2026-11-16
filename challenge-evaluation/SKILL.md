---
name: challenge-evaluation
description: "Pre-submit evaluation and post-result review for bounty, competition, and challenge entries, plus self-measurement of the agent's own skills against a no-skill baseline. Use before any submit (make.fun, POIDH, Synmerco, AgentPit, free mints), after any rejection or loss, and whenever a skill is created or changed."
---

# Challenge Evaluation

Evaluate first, then submit — and measure whether your own skills actually help.
Two halves: **Part A** evaluates a challenge entry before it ships;
**Part B** measures your skills against a no-skill baseline so a skill that
cannot beat "no skill" does not keep taking up context.

## When to use

- Before ANY submit: make.fun entry, POIDH claim, Synmerco bid strategy
  change, AgentPit strategy change, free-mint attempt.
- After ANY rejection, loss, or unexpected result — run the post-result
  review before the next attempt.
- When a skill is created, expanded, or changed — measure it (Part B)
  before trusting it.
- When two strategies compete — evaluate on identical jobs, never on vibes.

Route elsewhere: requirement extraction and strategy generation live in
`precision-task-optimizer`; leaderboard benchmarking in
`leaderboard-strategy-optimizer`; the Iron Law (fresh verification before
any completion claim) in `verification-before-completion`. This skill is the
evaluation gate those skills call, not a replacement for them.

## Part A — Pre-submit entry evaluation

Run in order. A gate that fails stops the submit; fix it, re-run, do not
route around it.

### A1. Pre-register the evaluation (before measuring anything)

Write the evaluation plan BEFORE running benchmarks or simulations:

- Hypothesis: what the entry does better than the current entry / Top 1,
  and by how much.
- Metric: the official scoring metric, nothing else (local grade is a
  backtest, never the platform result).
- Decision rule: the exact threshold that means SUBMIT vs STAND PAT
  (e.g. "beats marked at 95% one-sided confidence on 720 cases").
- Sample: identical jobs / fresh draws / held-out trials for both sides;
  medians of 3 runs — a single run lies, report the range, never the best.
- Sanity check before analyzing: split integrity (both sides saw the same
  jobs), no peeking (no interim verdicts on a fixed-horizon test).

No peeking: once the plan is written, do not change the metric, the
threshold, or the sample because the numbers look bad. A changed rule after
seeing results is not an evaluation. Full method:
`references/experiment-discipline.md`.

### A2. Acceptance gate — verdict before submit

Score the entry against the acceptance checklist and issue one verdict:

| Verdict | Meaning |
|---------|---------|
| CERTIFIED | Every checklist item passes on fresh evidence. Submit. |
| CONDITIONAL | Passes except named, owned, non-blocking gaps. Submit only with the gaps listed in the report. |
| REJECTED | Any blocking item fails. Do not submit. Fix and re-run. |

Checklist (full text + reason codes in `references/acceptance-gate.md`):

1. The behavior is implemented in the source, not only described in prose.
2. Targeted tests / checks pass and match the expected outcome — on the
   EXACT artifact the grader sees (bundle contents, output tree), not the
   repo tree. Run `scripts/check_output_tree.py <entry-dir>`.
3. The solution solves generally: no tailoring to visible tests, no
   special-casing of the competition/task, no reading of grading internals.
4. Packaging, imports, and entry points are valid; new files are in the
   paths the task expects.
5. The final state is deterministic enough to reproduce from a clean
   checkout (same inputs → same outputs, twice).
6. No security violation: no secret/token exfiltration, no credential
   material in the entry, no sandbox escape, no hidden network callbacks.
7. Every requirement from `precision-task-optimizer` §2 is met, with
   evidence cited per item — never "should pass".

**Read the live check reason FIRST.** When a platform check fails, open
the live status/reason on the platform before theorizing any cause. A
theory formed before reading the reason is a guess, not a diagnosis.

### A3. Independent review — generator never grades its own work

- The builder (or the agent that wrote the entry) never grades it. Review
  is done by a fresh reviewer: a subagent with no shared context, plus
  scripted checks, plus live-data verification.
- Label every finding by concurrence: CONFIRMED (found by 2+ independent
  passes) · LIKELY (found by 1 pass, grounded in code/data) · CANDIDATE
  (found by 1 pass, ungrounded — must be verified against the actual
  artifact before shipping, never shipped as-is).
- Severity and blocking are separate axes: a HIGH on a path the change
  does not enable can be non-blocking; a MEDIUM that breaks a published
  contract blocks. Every shipped finding carries `blocking: yes | no` + reason.
- Evidence ladder: a claim whose expected value was read off the
  implementation, or produced in the same session as the code, is Circular
  Verification — verdict PARTIAL, never PASS. Full ladder E0–E6 and the
  grounding protocol: `references/review-protocol.md`.
- Absence detection: verify the defenses that should exist but do not
  (input validation, dotfile skip, quota check) — missing code is the
  most-missed failure class.
- Style-bias check: reject any finding whose rationale reduces to "looks
  unfamiliar".

### A4. Pre-mortem — assume it already failed

Before submitting, assume the entry failed and reverse-engineer why
(prospective hindsight finds ~30% more causes than forward brainstorming):

- Enumerate at least 5 failure modes (3 for a rapid pass).
- Score each: RPN = Severity × Occurrence × Detection (1–10 each).
  Severity ≥ 9 is critical regardless of RPN — catastrophic severity is
  never offset by low occurrence.
- For each mode above threshold: mitigations in three layers —
  Detection, Prevention, Recovery — plus what would falsify it.
- Failure taxonomy to check first (loop/eval failures):
  CONTRACT_MISSING · STATE_DRIFT · VERIFY_GAP · TOOL_FAILURE ·
  CIRCUIT_OPEN · CONVERGENCE_STALL · OSCILLATION_LOOP · CONTEXT_OVERFLOW ·
  VALIDATOR_GAP · REWARD_HACK · GOAL_DRIFT · BURN_RATE_ANOMALY.
  Full method + scoring scales: `references/pre-mortem.md`.

### A5. Loop discipline (evaluation runs are loops too)

- Operation contract: every evaluation run declares 3–6 measurable
  acceptance criteria up front, in writing.
- Circuit breaker: 3 iterations on the same failing area → stop,
  re-analyse the root cause, replan once or escalate. Never loop the
  same failing action.
- Convergence: repeated signatures or A→B→A→B oscillation is NOT
  progress — it is a stall. Stop and re-analyse.
- Never declare DONE without artifact evidence; a verify PASS alone is
  never enough — pair it with a second, independent check (placeholder
  grep, mutation, a critic pass).
- Termination is enforced externally (iteration cap / timeout / budget),
  never by the agent's self-assessment.
- Cost metric: cost-per-completed-task (calls + tool runs + escalations),
  not cost-per-token.
- Parameter changes need ≥ 3 data points; roll back if the metric drops.

### A6. Post-result review (after the result lands)

For every rejection, loss, or unexpected result, before the next attempt:

1. Classify the failure stage and root cause: strategic (wrong
   approach) · operational (bug, misconfiguration) · platform (the
   grading environment, not the entry).
2. A platform fault is not a code defect — do not "fix" the entry for
   it. Re-submit the same entry unchanged when the platform was at
   fault; a rewrite is the wrong fix.
3. Record: selected strategy, predicted result, actual result, errors
   and missed requirements, time spent, what worked, what failed.
   Promote the lesson to `AGENTS.md` / `MEMORY.md` / the relevant skill
   within 48 hours — delayed capture loses accuracy.
4. Feed the failure back into the evaluation baseline: a drift that
   escapes detection becomes the new normal.

## Part B — Skill self-measurement

A skill that cannot beat "no skill" should not take up context.

### B1. Fixed-task bench protocol

1. Fix a small task set (4–8 tasks) drawn from real past work, each with
   a runnable pass/fail check (a test command, a script, a live status
   read). Keep the set FIXED across measurements — moving tasks invalidate
   comparisons.
2. Run each task 3 times WITH the skill and 3 times WITHOUT it
   (baseline), same model, same prompt, same checks. Record one JSON
   record per run in `results.jsonl`:
   `{"skill": "<name>|baseline", "task": "<id>", "run": 1, "solved": true,
   "tokens_in": N, "tokens_out": N, "cache_read": N, "duration_s": N,
   "ts": "<iso>"}`.
3. Never grade with LLM-as-judge for the headline number: solved =
   the check passes. Judged dimensions are secondary columns, marked
   as judged.
4. Baseline runs FIRST, same week as the skill runs. A delta against a
   historical baseline is not a measurement.

### B2. Aggregate

```bash
python3 scripts/bench_aggregate.py --log results.jsonl [--prev older.jsonl]
```

A task counts as solved when the MAJORITY of its runs pass. Report:
solve rate, tokens per solve (median over solved runs), vs baseline,
and high-variance tasks (runs disagree — investigate, do not average
away). Verdict: ADOPT (beats baseline on solve rate without blowing
up tokens) · ADAPT (helps some tasks, merge the working part) ·
SKIP (does not beat baseline — retire it, do not keep it "just in
case"). Full protocol: `references/experiment-discipline.md`.

### B3. Skill-library fitness (periodic audit)

After any skill change, and at least monthly, audit the library:

- Fitness per skill across 5 dimensions (correctness of guidance,
  freshness, usage, overlap, cost) — grade S(95+) A(85+) B(70+) C(55+)
  D(40+) F(<40). A drop > 5 points in 7 days → flag for review.
- Shadow Mode after any upgrade (prompt/model/tool change): the next 10
  uses are compared against the 30-day baseline; a drop ≥ 5% → flag
  and consider rollback.
- Confidence by evidence count: 1 Anecdote · 2 Emerging · 3–5 Pattern ·
  6–10 Established · 11+ Foundational. Never promote an Anecdote to
  guidance.
- Freshness: FRESH <30d · CURRENT 30–90d · AGING 90–180d · STALE >180d
  since last evidence (SECURITY knowledge stales 2× faster;
  PROCESS/META 1.5× slower). FAILURE/ANTI patterns are never
  auto-archived by time — failure modes recur.
- Sunset candidates: skills with no use, full overlap with another
  skill, or a stale F grade — propose, never force; verify zero active
  dependents before retiring.
- Bottleneck check: when generation gets cheaper/faster, judgment
  becomes the constraint — reinforce verification capacity instead of
  adding generation.
- Small mutations over big rewrites: 85% accuracy per step → 5 steps =
  44% success. Change one thing, confirm it holds, then continue.
  Full method: `references/skill-fitness.md`.

## Evaluation report (every run produces one)

1. Pre-registered plan (hypothesis, metric, decision rule, sample).
2. Acceptance verdict (CERTIFIED / CONDITIONAL / REJECTED) + reason codes.
3. Review findings (concurrence tags, severity, blocking, evidence).
4. Pre-mortem table (failure modes, RPN, mitigations).
5. Numbers (before/after, trial counts, medians, range — never best run).
6. Decision (SUBMIT with change list, or STAND PAT with evidence).
7. Lessons recorded (where: file + line, confidence by evidence count).

## Workspace adaptation

- Source methods: BaseIntelligence/agent-challenge `.rules/` (acceptance,
  anti-cheat, hardcoding, security) and `docs/evaluation.md` (lifecycle,
  scoring, fail-closed gates); currenjin/skillbench harness (baseline
  comparison, medians of 3, hidden tests, aggregate logic);
  simota/agent-skills `darwin` (fitness, Shadow Mode, bottleneck
  migration), `lore` (confidence, freshness, decay), `orbit` (operation
  contract, failure taxonomy, circuit breaker), `judge` (concurrence,
  grounding, severity vs blocking), `attest` (evidence ladder, circular
  verification), `experiment` (pre-registration, no-peeking, SRM),
  `omen` (pre-mortem, FMEA/RPN), `compete` (sourced claims,
  disconfirming evidence), `gauge` (checklist audit, drift detection).
  Studied 2026-11-16; report:
  `~/workspace/research/challenge-eval-skills/INSTALL-REPORT.md`.
- Adapted for Muse/Rahul: the agent-challenge production path (Phala TDX
  CVMs, paid cloud, baseagent runtime) is NOT adopted — only its review
  method. Skillbench's `run.py` needs Claude Code headless + an API key —
  NOT adopted; only its method + aggregate logic (re-implemented in
  `scripts/bench_aggregate.py`). The simota tri-engine fan-out needs
  Codex/Claude/agy CLIs — replaced by fresh-subagent review + scripted
  checks + live-data verification. The 90 generic simota skills were NOT
  imported (wrong runtime, duplicates existing skills).
- Scripts are read-only checks + aggregation. No network, no credentials,
  no submission. `check_output_tree.py` mirrors exactly what a
  make.fun `main.ts` copies into `/output` (game/, screenshots/).

## House rules (Rahul — msbrew.ai)

- Every sign, transaction, or approval needs a preview + Dhika's explicit
  yes per action. Never auto-execute on-chain or account actions.
- Never request, show, or send seed phrases or private keys.
- Free-only: no capital, stake, deposit, or paid API/key without Dhika's
  explicit yes per action. Credentials live in the Secure Vault or a
  registered connector — never in files.
- Use `curl`, not Python `urllib` (urllib fails with IncompleteRead on
  some hosts).
- Dollar values only via `~/workspace/tools/usd_value.py`, with formula +
  price sources shown.
- Live data only — never present a stale snapshot as current. Read the
  live platform reason before theorizing any failure.
- Deliverables in `~/workspace/`, never `/tmp` (/tmp is wiped on VM
  replacement). VM clock is UTC; Node 22.
