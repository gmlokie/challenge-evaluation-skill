# Experiment discipline — pre-registration, baselines, no-peeking

Adapted from simota/agent-skills `experiment` (A/B design, PICOT,
pre-registration, sequential testing, SRM) and currenjin/skillbench
(baseline comparison, medians of 3, hidden tests, aggregate logic).
The upstream A/B machinery assumes web traffic and feature flags; this
file keeps the *discipline* and rewrites the *mechanics* for challenge
entries and skill measurement.

## The four rules

1. **Pre-register before measuring.** Hypothesis, metric, decision rule,
   and sample are written BEFORE any benchmark runs. A rule changed
   after seeing results is not an evaluation.
2. **Baseline first, same week.** Every comparison runs the baseline
   (current entry / no-skill agent) on the same jobs, in the same
   window. A delta against a historical baseline is not a measurement.
3. **Medians of 3.** Single runs lie. Report medians and the range,
   never the best run. Flag tasks whose runs disagree (high variance)
   and investigate instead of averaging them away.
4. **No LLM-as-judge for the headline.** Solved = the check passes
   (test suite, kit check, live status, on-chain read). Judged
   dimensions are secondary columns, clearly marked as judged.

## Pre-registration template (write this first)

```
Hypothesis: <what improves, by how much, on which metric>
Metric: <the official scoring metric — nothing else>
Decision rule: <exact threshold for SUBMIT vs STAND PAT>
Sample: <identical jobs / fresh draws / held-out trials, N, trial count>
Baseline: <current entry / no-skill run, same jobs, same window>
Sanity checks: <split integrity, quota, determinism re-run>
```

Example (markdown-render-speed-02, as it should have been written):
hypothesis "fused single-pass render beats marked"; metric "CPU time on
720 cases"; decision rule "beats marked at 95% one-sided confidence";
sample "720 cases, 5 runs, medians"; baseline "marked 18.1.3, 1.066s".
Recorded result ~1x → the rule returns NO-GO, STAND PAT. The skill's
job is to force that verdict instead of leaving it "awaiting decision".

## No peeking

- A fixed-horizon test is not judged until the horizon is reached.
- Interim looks are allowed ONLY under a pre-specified sequential rule
  (anytime-valid confidence sequences preferred; group-sequential
  α-spending when interim looks are pre-specified). Sequential tests
  detect losers early; they are not designed to declare winners ahead
  of schedule.
- Daily peeking on a fixed test inflates the false-positive rate from
  ~5% to ~30%+. Do not do it.

## Sanity check before analyzing (the SRM rule)

Before trusting any result, check split integrity: did both sides see
the same jobs, the same fixtures, the same quota window? A broken split
invalidates all downstream analysis — halt and investigate, do not
analyze around it. For challenge entries the equivalents are: same job
set, same kit version, same quota day, deterministic re-run passing.

## Sample size and power (practical version)

- For entry comparisons: at least 3 runs per side on identical jobs,
  plus fresh draws / held-out trials for generalization. A strategy
  that wins only on the jobs it was tuned for has not generalized.
- For skill measurement (Part B): 4–8 fixed tasks × 3 runs with the
  skill × 3 runs baseline. Fewer tasks = a noisier verdict; say so.
- When the required sample exceeds what quota/time allows, the MDE is
  probably too small to be practically significant — say so and STAND
  PAT instead of shrinking the sample silently.

## Multiple comparisons

Testing many variants or metrics? Correct for it: Benjamini-Hochberg
FDR for exploratory sweeps across many metrics; Bonferroni/Holm for
confirmatory tests on few primary metrics. A sweep that tries 20
variants and reports the best one without correction is not evidence.

## Guardrail metrics

Define them before the test: primary metric (the decision), secondary
metrics (diagnostics), guardrail metrics (must not regress — e.g.
determinism, kit check 0 failed, quota). A win on the primary that
breaks a guardrail is not a win.

## Skill-bench protocol (Part B, step by step)

1. Fix the task set (4–8 real past tasks, each with a runnable
   pass/fail check). Keep it FIXED — moving tasks invalidates
   comparisons.
2. Run baseline first: 3 runs per task, no skill. Append records to
   `results.jsonl`.
3. Run with the skill: 3 runs per task, same prompt, same checks.
   Append records.
4. Aggregate: `python3 scripts/bench_aggregate.py --log results.jsonl`.
5. Verdict: ADOPT (beats baseline on solve rate without blowing up
   tokens) · ADAPT (helps some tasks — merge the working part) · SKIP
   (does not beat baseline — retire it).
6. Keep the raw log. Disagreements are re-run from the log, not
   re-argued from memory.

## What is NOT adopted from the sources

- Skillbench `run.py` needs Claude Code headless + an API key — not
  available here; the protocol above is the manual equivalent.
- Skillbench's hidden-test fixtures live in a private repo — here the
  "hidden" checks are the platform's own status/grader reads and
  fresh-draw trials.
- Experiment's flag platforms (LaunchDarkly, Statsig, etc.) and
  CUPED/variance-reduction machinery assume web traffic — not
  applicable; the transferable part is the discipline above.
