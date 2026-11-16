---
name: entry-test-cycle
description: "Run a full test cycle on a challenge entry before submit: test plan from requirements, scenarios and cases, execution tracking, defect triage, coverage traceability, regression selection after a fix, and a closure verdict. Use when an entry (make.fun game, POIDH claim artifact, Synmerco deliverable, AgentPit strategy change, free-mint script) is ready to test, after a fix that needs re-verification, or when a lead asks what is tested and what is not."
---

# Entry Test Cycle

A test cycle for one entry, from plan to closure verdict. Unit-test
discipline lives in `test-driven-development`; root-cause analysis of a
found defect lives in `systematic-debugging`; the pre-submit acceptance
gate lives in `challenge-evaluation` Part A. This skill is the campaign
between them: **what** gets tested, **in what order**, **what failed**,
and **what is still untested** when the cycle closes.

## When to use

- An entry is built and needs testing before the acceptance gate runs.
- A fix landed and you must decide what to re-run (regression selection).
- Someone asks "what did we test / what is still untested" — answer with
  the traceability matrix, not from memory.
- A defect was found during testing and needs a structured report +
  triage before the next cycle.

Route elsewhere: writing the unit tests themselves (`test-driven-development`);
debugging a failure to its root cause (`systematic-debugging`); the final
submit decision (`challenge-evaluation` A2). This skill feeds those, it
does not replace them.

## The cycle (in order — do not skip a phase)

### 1. Plan — from requirements, not from the code

Write the plan BEFORE writing cases. Source of truth is the
requirement set from `precision-task-optimizer` §2 (or the competition
page / task brief). Never derive requirements from the implementation.

- Scope: what is in / out of this cycle. Out-of-scope is a decision,
  written down — never silent.
- Gaps & questions: every requirement that is ambiguous, missing an
  acceptance criterion, or untestable as written goes in the gaps table
  with a question for the owner (Dhika). A missing AC is a finding,
  not a blank to fill in yourself.
- Scenarios, prioritised P0 / P1 / P2. P0 = the entry fails / is
  rejected without it. Every scenario maps to one requirement or one
  gap — an unmapped scenario is scope creep, an unmapped requirement
  is a hole.
- Test data & environment: exact data sets, flags, accounts, VM facts
  (UTC clock, Node 22, network). Reference data sets by name; never
  invent concrete values inline.
- Entry / exit criteria: entry = build exists + requirements frozen
  for this cycle; exit = all P0 cases executed + every failure has a
  defect record + coverage matrix complete.
- **Review gate.** The plan is a draft until Dhika (or the cycle
  owner) approves or edits it. In this workspace that gate is Dhika's
  explicit yes; for a solo cycle, record "self-approved, <time>" and
  the assumptions made.

Template: `references/test-plan-template.md`.

### 2. Design — scenarios to cases

- One case per scenario variant: positive, negative, and boundary
  paths each get their own case. Never collapse them into one
  multi-branch case — a collapsed case hides which path failed.
- Every case carries: unique ID, title, preconditions, test-data
  reference, numbered steps (one action per step), and a specific
  expected result per step. "Verify it works" is not an expected
  result; the observable outcome is.
- Trace every case to its scenario ID and requirement. Flag any
  scenario with no case and any case that maps to nothing.
- Never invent an expected result you cannot justify from a
  requirement or the scenario — mark it "expected result to confirm"
  instead of guessing.

### 3. Execute — track, do not just run

- Run cases in priority order (all P0 first). Record every run in the
  execution log: case ID, result (PASS / FAIL / BLOCKED / SKIP with
  reason), evidence (command + output, file path, screenshot), time.
- A FAIL without a defect record is an unrecorded failure: file the
  defect in the same pass (see §4), do not batch it for later.
- BLOCKED is not SKIP: a blocked case (missing data, broken env) stays
  open and blocks the exit criteria until resolved or explicitly
  waived by the owner.
- Never report "tested" from a run you did not execute, and never
  imply a case passed because a neighbouring case passed.

### 4. Defect report + triage

Report (one per defect, filed at discovery time):

```
## Defect — <area>: <what fails> when <condition>
Environment: build <ver> | env <name> | role/account | VM facts
Severity: S? (impact)   Priority: P? (urgency)   Suspected area: <component>
Steps to reproduce: 1. ... 2. ... (minimal, from a known starting state)
Expected: <what should happen>
Actual:   <what happened>   Frequency: always / n of m
Evidence: <links to logs / screenshots / trace>
```

- Severity is impact, priority is urgency — rate each with a one-line
  justification. Suspected area is a hypothesis, not a verdict.
- Never fabricate a repro step, log line, error message, or evidence
  link. If it does not reliably reproduce, report the frequency
  honestly instead of inventing a clean repro.
- Triage the batch, don't grind one by one: cluster likely duplicates
  (same symptom, same signal) and present them as **suggested
  duplicates for confirmation** — never merge or close silently.
  Route each defect to a component/owner as a suggestion; flag ones
  you cannot confidently route and reports missing repro/env/evidence
  (send back before triage, don't guess the missing fields).
- After triage, the fix goes through `systematic-debugging` (root
  cause first, no symptom fixes). A defect whose fix is verified
  moves to §5; a defect deferred is recorded with reason + owner.

### 5. Regression selection — after any fix

A fix changes the code; the question is what to re-run. Never default
to "run everything" (wastes quota/time) or "run the one failing case"
(hides blast radius).

1. Take the diff / changed files / modules. If the scope is unclear,
   ask — do not guess which areas moved.
2. Map impact: changed areas → features, endpoints, shared components,
   likely downstream effects.
3. Select: **Must-run** (directly exercises the change),
   **Should-run** (shared / adjacent), **Skip-with-reason**. Always
   include a smoke / critical-path safety net regardless of the change.
4. State the trade-off in writing: what the selected set does NOT
   cover, so the risk of skipping is visible.
5. If a mapping is uncertain, lean toward including the test. Never
   present the subset as risk-free.

### 6. Coverage — the traceability matrix

Build it from real artifacts only: requirements/ACs on one axis,
executed cases on the other.

| Requirement / AC | Cases | Status | Gap |
| AC-1 | TC-1, TC-2 | covered + passing | — |
| AC-2 | TC-4 (happy only) | thin | no negative / boundary |
| AC-3 | — | UNTESTED | high risk |

- Surface: untested ACs (no case at all), thin coverage (happy path
  only), executed-but-failing coverage, orphan cases (map to no
  requirement).
- Rank gaps by risk, not by count. Distinguish "covered" from
  "covered and passing" — a failing case is not coverage.
- Never assume coverage exists without a case to point to. Do not
  fabricate case or requirement IDs to make the matrix look complete.

### 7. Closure — verdict, not a summary

Close the cycle with a verdict, owned by the cycle owner:

- **GO** — all P0 cases executed and passing, no open S1/S2 defect,
  coverage matrix complete, known gaps listed with risk.
- **GO WITH GAPS** — passes except named, owned, non-blocking gaps
  (list them; each carries risk + owner).
- **NO-GO** — any P0 failure, open S1/S2, or untested P0 requirement.
  Fix and run a new cycle; do not re-open this one silently.
- Closure report: plan version, cases executed (n PASS / n FAIL /
  n BLOCKED / n SKIP), defects found / fixed / deferred, top coverage
  gaps by risk, and the lessons to hand to `learning-memory` (what
  escaped, what check caught it, what to add next cycle).
- A closed cycle is frozen: later fixes start a new cycle with a new
  plan version, so the history stays auditable.

## Flaky and intermittent failures

- A case that passes sometimes is a defect in the test or the entry,
  not a pass. Record frequency (n of m runs), conditions, and the
  exact failing run's evidence.
- Before re-running a flaky case, change one thing: isolate shared
  state, remove fixed sleeps, pin data, or scope the check. Re-running
  the same flaky case unchanged and hoping is not a fix — after 3
  identical re-runs, stop and analyse (see `challenge-evaluation` A5
  circuit breaker).
- Never "fix" flakiness by broadening an assertion or a locator
  (`.first()`, regex-anything, looser match) — that hides the failure
  instead of removing it. For Playwright locators specifically, prefer
  `getByRole` / `getByLabel` over XPath, class, or index selectors,
  verify each replacement resolves to exactly one element, and mark
  any swap made without live-DOM evidence UNVERIFIED (see
  `playwright-skill`).

## Guardrails

- The plan, cases, and closure report are drafts until the owner
  approves them; you do not sign off your own testing.
- A test that cannot fail (passes by construction, asserts nothing)
  is not a test — prove it can fail before counting it (mutation
  sanity check: break the thing under test, watch the case go red).
- Determinism: same inputs → same result, twice. A case whose result
  depends on wall-clock time, network, or leftover state is a case
  that needs fixing, not a result to report.
- Cost: a full cycle costs runs, not just tokens. Prefer the smallest
  case set that covers the P0 requirements; expand only on a gap the
  matrix names.

## Evaluate, review, develop further

This skill is a draft to be measured, not a fixed ritual. Evaluate it
the `challenge-evaluation` Part B way before trusting it:

- Fixed-task bench: 4–8 real past entries (e.g. a make.fun bundle
  check, a POIDH claim dry-run, a Synmerco deliverable check), each
  with a runnable pass/fail check. Run each task 3× WITH this skill
  and 3× WITHOUT (baseline), same prompt, same checks; record
  `results.jsonl` and aggregate with
  `challenge-evaluation/scripts/bench_aggregate.py`.
- What counts as "helps": more real defects found before submit,
  fewer untested P0 requirements at closure, no blow-up in runs per
  cycle. A skill that adds paperwork without finding defects is
  ADAPT (keep the working part) or SKIP — retire it, don't keep it
  "just in case".
- Review after every real cycle: which phase found the defect that
  mattered, which phase produced only paperwork, what to cut. Change
  one thing, confirm it holds, then continue (small mutations over
  big rewrites). Report the change and its evidence in the skill's
  next review; do not silently rewrite the cycle.

## Workspace adaptation

- Source methods: PramodDutta/agentskills STLC pack (14 skills, 7
  phases), studied 2026-11-16; report:
  `~/workspace/research/solver-skills/group-C-eval.md`. Adapted:
  test-plan shape + gaps table + template, scenario/case writing
  (atomic steps, expected result per step, traceability), defect
  report shape + triage (suggested duplicates, severity vs priority,
  send-back for missing info), regression selection (Must/Should/
  Skip + safety net), coverage traceability matrix, closure verdict.
  The pw-locator-fixer method is NOT duplicated here — it lives in
  `playwright-skill`, which already covers role/label locators and
  flaky-test debugging; this skill only states the rule.
- Adapted for Muse/Rahul: the source's Jira dependency is dropped —
  there is no Jira here; requirements come from
  `precision-task-optimizer` §2 and the competition/task page, fetched
  with `curl`. The source's "HUMAN REVIEW GATE" becomes Dhika's
  explicit yes per the house security gate (or a recorded
  self-approval with assumptions for solo cycles). Jira ticket IDs
  become entry/requirement IDs. The 14 one-skill-per-phase split is
  collapsed into one skill: a single entry cycle does not need 14
  triggers, and 14 near-identical 55-line skills would bloat the
  library (see `challenge-evaluation` B3 overlap rule).
- Not adopted: Jira REST fetching (`fetch_jira.sh`, ROVO/Atlassian
  MCP), Copilot prompt-file duplicates, the runnable Playwright demo
  project (VWO login spec — demo data, not a method).

## House rules (Rahul — msbrew.ai)

- Every sign, transaction, or approval needs a preview + Dhika's
  explicit yes per action. Never auto-execute on-chain or account
  actions. A test cycle never submits, claims, or files anything —
  it only produces the plan, cases, log, and closure verdict.
- Never request, show, or send seed phrases or private keys.
- Free-only: no capital, stake, deposit, or paid API/key without
  Dhika's explicit yes per action. Credentials live in the Secure
  Vault or a registered connector — never in files, test data, or
  defect reports.
- Use `curl`, not Python `urllib` (urllib fails with IncompleteRead
  on some hosts).
- Dollar values only via `~/workspace/tools/usd_value.py`, with
  formula + price sources shown.
- Live data only — never present a stale snapshot as current. Test
  against the exact artifact the grader sees (bundle contents,
  output tree), not the repo tree.
- Deliverables in `~/workspace/`, never `/tmp` (/tmp is wiped on VM
  replacement). VM clock is UTC; Node 22.
