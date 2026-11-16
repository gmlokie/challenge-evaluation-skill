# Evaluation Report — Solver Skills (from USING them)

- Date: 2026-11-16. Study: solver-skills (13 repos, 6 categories).
- Method: `challenge-evaluation` Part B, pilot scale — fixed tasks,
  with-skill vs baseline, 1 run per side unless noted, same agent,
  same checks, solved = the runnable check passes (never LLM-as-judge
  for the headline number). A full Part B bench (4–8 tasks × 3 runs
  per side, independent grading) was NOT run for any skill in this
  study — where that is the case it is written as **belum teruji
  penuh** with exactly what is still needed. Nothing here claims a
  result that was not measured.
- Verdicts: **BERGUNA** (adopt/keep) · **TIDAK PERLU** (skip / do not
  change — with a suggestion: delete, merge, or retire) ·
  **DITINGKATKAN** (useful core, adapted — what changed and why it is
  an improvement).
- Second axis (Dhika's install flow — Evaluate → Review → Preview →
  Install → Develop further): is the skill easy to evaluate, review,
  and develop further by another agent, or too rigid/specific to
  adapt? A skill that cannot be evaluated cannot be trusted, however
  good it reads.
- Companion: `INSTALL-REPORT.md` (same folder) covers per-repo
  verdicts, what was adapted, and what was skipped.

## Summary

| Skill | Verdict | Evidence | Still untested |
|---|---|---|---|
| `task-analyzer` (new) | BERGUNA | Pilot 3/3 vs baseline | Full Part B (3×/side) |
| `research-engine` (new) | BERGUNA | Pilot 3/3 vs baseline | Full Part B (3×/side) |
| `orchestrated-job-runner` (new) | BERGUNA | Mechanism 3/3 + parent re-test | Real-job use + full Part B |
| `web-data-extraction` (new) | BERGUNA | Live CoinGecko + validator | Ladder steps 2–4 + full Part B |
| `entry-test-cycle` (new) | BERGUNA | 7/7 cases, baseline 2/5 reqs | Real entry + full Part B |
| `learning-memory` (new) | BERGUNA | Recall 3/3 vs 0/3 baseline | Precision at scale + full Part B |
| `playwright-skill` | DITINGKATKAN | Bug proven + fixed, 12/12 + smoke | — (verified) |
| `verification-before-completion` | DITINGKATKAN | Method-level (T3 pilot) | Isolated test of merged section |
| `systematic-debugging` | DITINGKATKAN | Method-level, known classes | Isolated test of merged section |
| `challenge-evaluation` | DITINGKATKAN | Formula computable, pointers trivial | — (additive, no gate change) |
| `precision-task-optimizer` | DITINGKATKAN (tiny) | T1 pilot | — (1-line routing) |
| `universal-task-intelligence` | DITINGKATKAN (tiny) | Borderline, hard to bench | Review after 5 uses |
| 14 older skills (see table) | TIDAK PERLU (diubah) | Read, no overlap/gap found | — |
| Upstream source skills not imported | TIDAK PERLU | Duplicates / paid / wrong domain | — |

**No local skill is recommended for retirement.** Every TIDAK PERLU
in this report is either an upstream source skill that was not
imported, or an existing local skill that needs no change. Nothing in
the library was found to be dead weight by this study.

## New skills — full verdicts

### 1. `task-analyzer` — BERGUNA

- **Evidence (pilot, 3 fixed tasks, 1 run/side, evaluator = author):**
  - T1 (vague input "buatin game buat fps-01"): with-skill named 5/5
    gaps and wrote round-1 questions (max 5, with defaults), 0
    assumptions. Baseline (`precision-task-optimizer` §2 alone)
    silently filled 5 gaps from MEMORY (genre, open time, $1,000
    escrow), 0 flagged.
  - T2 (extract requirements, markdown-render-speed-02): 8 REQ items
    (IDs + Given/When/Then + source), 7/7 ground-truth items, and
    surfaced a real close-time conflict (MEMORY says both 03:30 and
    06:00 WIB 17 Nov). Baseline: same 7 facts as flat bullets,
    0 conflicts flagged.
  - T3 (drift check, best-game-01 round-4 tree):
    `check_output_tree.py` → FAIL, 1 violation
    (`screenshots/.gitkeep`, 22 files, exit 1) — the exact failure
    mode of rounds 1–3, caught first run. Baseline by inspection:
    "tree looks clean", violation never looked for. Caveat: the
    flagged tree is the investigation scratch clone, not the
    submitted repo tree / v5 bundle (verified clean 10:24 WIB) —
    the value is the method, the scope must not be exaggerated.
- **Useful for:** Rahul, every vague task intake (Dhika's short
  commands are the norm, not the exception); before every submit
  (drift check §6); after any failure on a missed requirement.
- **Install-flow:** easy to evaluate — bench tasks T1–T3 are concrete
  and countable (gaps named, REQ recall vs ground truth, drift
  findings). Easy to review (phases + checklists, no hidden
  machinery) and to develop (categories are adaptive, skip-if-clear).
  Not rigid.
- **Belum teruji penuh:** pilot only (n=1, single run, author-graded).
  Full Part B needs T1–T3 × 3 runs/side with independent grading.
  T1's interview was simulated — a real interview round with Dhika
  is the true test of §2.

### 2. `research-engine` — BERGUNA

- **Evidence (pilot, 3 fixed tasks, 1 run/side, evaluator = author):**
  - R1 (token-radar v4 vs round-4 rank 47): state dir + 2 hypotheses
    with falsifiers; rigor review REJECTED "v4 ready to submit"
    (D1/D3/D6 ≤2: local grade 7/7 ≠ judge win; submit blocked on
    cap/quota, not quality). Baseline: "v4 looks ready, submit when
    quota resets" — no falsifier, no cap check.
  - R2 (POIDH 1553, fund 0.005/0.01 ETH?): cost bounded live
    (0.005 ETH × $1,806.54 = **$9.03**, 0.01 ETH = **$18.07**,
    usd_value.py, CoinGecko 16 Nov 10:56 UTC); rigor review REJECTED
    "fund it, it's cheap" — joiner probability has no base rate;
    also caught MEMORY's stale price (0.028 ETH = $63.02 at ETH
    ~$2,251 then vs $50.58 now). Baseline: "0.005 ETH is only ~$9,
    worth trying" — cost treated as the decision, joiner question
    never asked.
  - R3 (Synmerco 50% price eval): pre-registered question +
    falsifier; current evidence recorded (2 bids open at 50%, 0/10
    wins, scout 0 bids); rigor review STRONG ACCEPT for "eval is
    running correctly" (all D ≥4). Baseline: "eval started, keep
    watching" — no falsifier, scout signal unflagged.
  - Pilot 3/3; 2 of 3 baseline answers would have shipped an
    over-claim.
- **Useful for:** Rahul, multi-session research (top-10/competitor
  research, a Synmerco job's evidence base, new-platform/bounty
  evaluation), any investigation whose claims feed a submit.
- **Install-flow:** easy to evaluate — hypotheses + falsifiers +
  D1–D6 grades are all countable; state dirs are inspectable files.
  Not rigid: the two loops are a rhythm, pivots explicitly allowed.
- **Belum teruji penuh:** pilot only (n=1, single run, author-graded).
  Full Part B needs R1–R3 × 3 runs/side with independent grading.

### 3. `orchestrated-job-runner` — BERGUNA

- **Evidence (mechanism tests, 16 Nov):** resume after simulated
  crash (s1/s2 done, s3 in progress → resume prints SKIP s1, SKIP
  s2 with evidence, NEXT s3) — PASS; gate `approve` → denied → run
  `aborted` — PASS; same step failing 3× → circuit open, run
  `failed` — PASS. Script stdlib-only, no network.
  Parent independently re-ran the resume scenario (init → s1 done →
  s2 done → resume) → `SKIP s1, SKIP s2 (evidence), NEXT s3` — PASS.
- **Useful for:** any job with 3+ steps, subagent fan-out, or work
  that must survive interruption (make.fun builds, Synmerco
  deliveries, POIDH claims, free-mint attempts). Not useful for
  1–2-step tasks (ledger overhead exceeds the benefit).
- **Install-flow:** easy to evaluate — the ledger script is testable
  without an LLM (resume/gate/circuit scenarios are runnable
  commands); §9 names Part B bench tasks explicitly. Easy to review
  (patterns + thresholds, not framework code) and to develop (new
  patterns only from real failures, per §9).
- **Belum teruji penuh:** mechanism only — no real-job use yet and
  no Part B bench. First real use (e.g. the fps-01 build or the
  Synmerco delivery) should run with a ledger in `~/workspace/runs/`
  and its outcome recorded in §9.

### 4. `web-data-extraction` — BERGUNA

- **Evidence (live test, 16 Nov 10:59 UTC):** CoinGecko public API
  no-key (`/simple/price`, BTC/ETH/SOL) → BTC $64,470, ETH $1,806.54,
  SOL $71.56. `validate.py` over 5 records (3 valid + 1 duplicate +
  1 wrong type) → `fetched=5 valid=3 dropped_invalid=1
  dropped_duplicate=1`, exit 1 (correct — invalid records present),
  cleaned file saved. Mini-bench 1×: baseline ad-hoc (curl + eyeball)
  scored 0/3 checks vs with-skill 3/3 (schema, dedupe, timestamp) —
  indicative, not conclusive. Parent verified `validate.py --help`
  runs clean.
- **Useful for:** any "get me a table of X from the web" task (lead
  lists, price checks, leaderboard reads, competitor/market research,
  data for a Synmerco bid). It is also the skill that STOPS a job
  whose source needs a login/key/payment — that refusal is a feature.
- **Install-flow:** easy to evaluate — `validate.py` pass rate, share
  of jobs ending at ladder steps 1–2, zero paid/blocked incidents
  are all countable; §8 names the Part B bench. Easy to review and
  develop (new sources come from real jobs).
- **Belum teruji penuh:** ladder steps 2–4 (RSS, static HTML,
  Playwright render) were not executed in the pilot — only the no-key
  API path ran live. Full Part B (4–8 extractions × 3 runs/side)
  not run.

### 5. `entry-test-cycle` — BERGUNA

- **Evidence (real test, target
  `challenge-evaluation/scripts/check_output_tree.py`, 87 lines,
  known behaviour):** with-skill: plan (5 requirements from the
  docstring) → 5 scenarios → 7 cases (clean, dotfile, dot-dir,
  symlink, missing folder, nested dotfile, backslash) → execution +
  traceability + closure → **7/7 matched expected** (TC-1 PASS;
  TC-2/3/4/6/7 FAIL with the exact violation; TC-5 PASS + WARN
  "folder missing"). Baseline (no skill): 2 runs (clean PASS, dirty
  FAIL), covered 2/5 requirements, no plan/scenarios/traceability/
  closure. The method caught **1 error in the evaluator's own test
  design** (TC-5 first built an empty `screenshots/` instead of a
  missing one; traceability flagged R4 untested, fixed, re-run
  proved the WARN) — the baseline would never have caught it.
- **Useful for:** every entry before submit (make.fun bundle, POIDH
  artifact, Synmerco deliverable, AgentPit strategy change,
  free-mint script); after any fix (regression selection); whenever
  asked "what is tested / what is not".
- **Install-flow:** easy to evaluate — bench is direct (fixed tasks +
  runnable checks; "defects found / P0 untested" countable). Easy to
  review (phases + templates) and develop (§Evaluate names what to
  cut: any phase that produces only paperwork).
- **Belum teruji penuh:** 1 target, 1 run per case (not 3× as Part B
  requires), not yet tested on a real game entry (e.g. the fps-01
  bundle). The claim is only: the method works end-to-end on a small
  target and found a test-design error. Full Part B bench is
  follow-up work, not a claim made here.

### 6. `learning-memory` — BERGUNA

- **Evidence (real test, 3 lessons from MEMORY.md):** store with
  IDs, dates, evidence, confidence, applies-to + index vs baseline
  free-text notes of the same 3 lessons. Recall (grep, 3 queries):
  row precision 100% on both sides (store too small to discriminate
  — recorded honestly). The measurable difference: **actionable-rule
  recall 3/3 (with skill) vs 0/3 (baseline)** — the baseline lost
  the exact rules ("plain relative name", "-K vs -H", "live header
  PNL"); the store kept them with evidence + confidence. Admission
  gate: a fake secret (`mf_live_FAKESECRET123`) and unverified
  trivia were both refused. Reflect: an insight citing 2 sources
  accepted; a 1-source insight rejected as anecdote — per §1.
- **Useful for:** after every task/rejection/loss (capture ≤48h);
  at the start of a task (recall before acting); monthly review.
  For Rahul first, for any future agent that inherits this memory
  second.
- **Install-flow:** easy to evaluate — recall bench with ground
  truth + evidence files; precision and "repeated mistakes" are
  countable. Easy to review (files + grep, no hidden machinery)
  and develop (admission gate + sunset review prevent bloat).
  Risk noted in the skill itself: record accumulation — mitigated
  by the gate + §7 review.
- **Belum teruji penuh:** a 3-record store is too small to measure
  recall precision meaningfully. Full Part B needs 4–8 recall tasks
  with ground truth in a larger store. The gate test shows gate
  decisions, not automated enforcement (the gate is a procedure).

## Merged older skills — verdicts (DITINGKATKAN)

### `playwright-skill` — DITINGKATKAN (merge applied + verified)

- **What changed:** `run.js` replaced with the upstream v5
  child-process executor (caller cwd preserved, `-e`, `PW_SCRIPT_DIR`,
  signal forwarding); local compat kept (bare-arg inline, stdin,
  wrapping of code without `require()`; temps under
  `~/workspace/playwright/.tmp/`). `lib/helpers.js`: env-driven
  `launchBrowser()`, `--no-sandbox` only as root, `createContext()`
  drops `mobile`, `takeScreenshot()` accepts `PW_ARTIFACT_DIR`,
  locator-based cookie banner, parallel dev-server detection.
  SKILL.md: "Current Playwright patterns" (accessible locators first,
  `locator.waitFor()` over `waitForSelector`/`networkidle`) +
  "Reconnaissance before action" (Anthropic webapp-testing) +
  "Merged from upstream v5.0.0" note. Tests ported (`tests/`,
  fixtures). Playwright `^1.57.0` → `^1.62.0` (installed 1.65.1),
  version 4.1.0 → 5.0.0.
- **Why it is an improvement:** the v4.1.0 executor had a real bug
  (proven twice, independently): `process.chdir(__dirname)` turned a
  relative script path into inline code (`ReferenceError: exit3 is
  not defined`, exit 1) and misdirected relative artifact paths into
  the skill dir. Exit codes are what `challenge-evaluation` uses as
  pass/fail — a wrong exit code is a wrong verdict. The merge fixes
  that and modernizes the waiting guidance (`networkidle` as default
  hangs on polling/SSE pages).
- **Evidence:** parent re-confirmed the bug pre-merge and the fix
  post-merge (exit 3); `node --test tests/*.test.js` → **12/12 pass**
  (also post-upgrade), `node tests/smoke.js` → **PASS**; bare inline,
  stdin, wrapped chromium-launch snippet all verified individually.
- **Useful for:** all browser work (entry verification, live checks,
  repo About setup). **Install-flow:** easy — the test suite now
  lives in the skill; every merge item has test evidence.
- **Note:** SKILL.md is now 675 lines (was 630), over the 500-line
  guideline — pre-existing condition, candidate for a future split
  into `references/`.

### `verification-before-completion` — DITINGKATKAN

- **What changed:** new section "Merged from qa-spec-auditor /
  qa-coverage-analyzer" (lines 209–241): 4-dimension drift check
  (brief↔artifact, brief↔live platform, brief↔checks,
  docs↔implementation) + read-the-live-reason-first rule +
  `check_output_tree.py` + regression-set rotation; RTM coverage
  (every requirement ≥1 evidence check; untested requirements and
  orphan checks both flagged).
- **Why it is an improvement:** the Iron Law verifies a claim; it
  never asked whether the claim covers the *brief*. The exact
  failure class that killed best-game-01 rounds 1–3 (brief↔artifact
  drift — a `.gitkeep` the brief never mentioned, in the output the
  gate never checked) now has a named check at the gate. RTM closes
  the "untested requirement" hole the gate previously could not see.
- **Evidence:** method-level. The drift method itself was
  pilot-tested (task-analyzer T3: caught `screenshots/.gitkeep`
  first run). No isolated test run of the merged section itself —
  honest gap, not a claim.
- **Useful for:** every pre-submit gate. **Install-flow:** easy —
  the section is self-contained and reviewable; its checks are
  countable (drift findings, RTM gaps).

### `systematic-debugging` — DITINGKATKAN

- **What changed:** Phase 1 gains a fishbone check (line 120: 5
  bones — People / Process / Tooling / Data / Environment, one
  candidate per bone before theorizing); the root-cause section gains
  an explicit **escape point** (line 357: which check should have
  caught this and why it did not) and a **flaky failure patterns**
  table (line 362: race / shared state / time dependency / external
  dependency with typical causes + first fixes); Fix verification
  gains **corrective vs preventive** (line 394: the preventive action
  fixes the escape point, with owner + verification).
- **Why it is an improvement:** Phase 1 had no structured way to
  enumerate causes (it jumped to tracing); RCA never asked why
  testing/review missed the bug — so the same escape recurred; flaky
  failures had no pattern table (the symptom table mentioned them
  in one line). These three additions close those gaps without
  touching the four-phase structure.
- **Evidence:** method-level — the patterns map to known failure
  classes (race/shared-state/time/external are the standard flaky
  causes; escape-point analysis is the standard post-incident
  question). No isolated test run of the merged additions.
- **Useful for:** all debugging, especially post-incident RCA
  (grader rejections, escape analysis). **Install-flow:** easy —
  the skill already carries a "Merged from …" + "Skipped … and why"
  pattern; additions follow it.
- **Note:** SKILL.md is now 578 lines (was 553), over the 500-line
  guideline — same pre-existing condition as playwright-skill.

### `challenge-evaluation` — DITINGKATKAN

- **What changed:** A4 pre-mortem gains a risk-ranked verification
  aid (line 118: Risk = Complexity × ChangeFrequency ×
  (1 − Coverage), verify High → Low); A2 checklist item 2 now routes
  to `entry-test-cycle` for the full test campaign (line 70); A6
  step 3 now routes lesson capture/promotion through
  `learning-memory` (line 163).
- **Why it is an improvement:** RPN alone ranks failure modes, not
  what to verify first when time is limited — the risk formula is
  computable from git log + coverage and fills that gap. The two
  routing pointers stop the gate from being used as a substitute for
  a test campaign (A2) and from promoting lessons without the memory
  method (A6).
- **Evidence:** the formula is computable (inputs defined); the
  pointers are trivially verifiable by reading. Additive only — the
  gate's verdicts and checklist are unchanged.
- **Useful for:** every pre-submit gate and post-result review.
  **Install-flow:** easy — small, reviewable, no behaviour change
  to the gate itself.

### `precision-task-optimizer` — DITINGKATKAN (tiny)

- **What changed:** one routing line (§1, line 16): vague input
  (<3 sentences, or ≥2 of the 5 intake questions unanswered) goes to
  `task-analyzer` first — interview + sealed brief — before §2.
- **Why it is an improvement:** §1 previously had no intake routing;
  vague input entered §2 directly, and the T1 pilot showed the cost
  (5 gaps silently filled from MEMORY, 0 flagged). One line routes
  around that.
- **Evidence:** T1 pilot (see `task-analyzer` above). **Install-flow:**
  trivially reviewable.

### `universal-task-intelligence` — DITINGKATKAN (tiny)

- **What changed:** §11 Communication gains the discernment-nudge
  habit (line 238): after a substantive answer Dhika may act on,
  append 2–3 short follow-up questions tied to specific claims —
  max once per conversation.
- **Why it is (probably) an improvement:** reports Dhika acts on
  previously had no check-questions habit; a wrong claim acted on
  costs real money or a submit. The cost is ~3 lines per report.
- **Evidence:** borderline — the effect is on Dhika's checking, not
  on a runnable check, so it is hard to bench. Group A flags this
  honestly. **Install-flow:** easy to review, hard to measure.
- **Suggestion:** keep it small; review after 5 uses — if no
  follow-up question ever catches anything, cut it.

## Evaluated but unchanged — TIDAK PERLU (diubah)

Read and checked for overlap/gaps against the studied repos; no change
needed. Keep as-is.

| Skill | Why no change |
|---|---|
| `deep-research` | Single-shot multi-angle search; `research-engine` routes to it, does not duplicate it. |
| `research-online` | Search mechanics + dead-end protocol + sufficiency rules; referenced, not duplicated. |
| `research-refs` | Free reference sources catalogue; `research-engine` §4 calls it. |
| `web3-research-toolkit` | Web3-specific checks; no studied repo covers them. |
| `leaderboard-strategy-optimizer` | Leaderboard benchmarking method; untouched by this study. |
| `optimize-approach` | Approach judging; no overlap found. |
| `token-saver` | Context/cost discipline (incl. the max-2 subagent cap); untouched. |
| `test-driven-development` | Unit-test discipline (contract-first, table-driven, coverage floor); STLC-level work went to `entry-test-cycle`, not here. |
| `ai-engineering` | LLM-app engineering (prompts, RAG, evals); no overlap found. |
| `mcp-builder` | MCP server building; untouched by this study. |
| `cron-scheduler` | Cron expressions; untouched. |
| `security-audit` | Contract audit workflow; untouched by this study. |
| `threat-modeler` | STRIDE modelling; untouched. |
| `bug-bounty` | Bounty workflow (1,647 lines); not a QA STLC — untouched. |

## Upstream source skills — TIDAK PERLU (not imported)

For the record: the TIDAK PERLU verdicts on the source side are
duplicates of local skills (16 AZANIR framework test writers,
`qa-orchestrator`, `qa-test-strategy`/`qa-test-reviewer`,
`qa-project-memory`, `automation-script-generator`, `pw-locator-fixer`
as a skill), paid/keyed products (6 tracker integrations, Jira
fetching, Exa/Firecrawl, LangSmith, Foundry, Cosmos DB, Apify
platform + 4 Actor skills, Hindsight server/Cloud, agent-memory
daemon), wrong-domain mass (~275 Kalaris academic skills, Anthropic
docx/pdf/pptx/xlsx + design + comms + `academy-guide`), or
methods that conflict with the verification gate (`qa-test-healer`
auto-fix). Detail per repo: `INSTALL-REPORT.md`. None of these is
proposed for a future import.

## Final suggestions

1. **Adopt the 6 new skills as DRAFTS** (they are already installed
   in `~/workspace/custom-skills/`), then run each skill's named
   Part B bench (4–8 tasks × 3 runs/side, independent grading)
   before ADOPT. The bench tasks are written into each skill's
   §Evaluate section — no new design needed, just the runs.
2. **First real uses to watch:** `orchestrated-job-runner` on the
   fps-01 build (ledger in `~/workspace/runs/`); `entry-test-cycle`
   on the fps-01 bundle before its round-1 submit; `task-analyzer`
   on the next vague Dhika command (real interview, not simulated);
   `learning-memory` on the next rejection/loss (capture ≤48h).
3. **Keep the merged skills as they are.** The only behaviour change
   is the playwright executor (verified 12/12 + smoke); the rest are
   additive guidance.
4. **Do not retire any local skill** on the basis of this study.
5. **Install-flow health:** all 6 new skills are easy to evaluate,
   review, and develop further (explicit §Evaluate with countable
   bench tasks, testable scripts where bundled, no rigid
   prescriptions). The one hard-to-measure item is the UTI
   discernment-nudge — review after 5 uses. Nothing in this batch
   is too rigid or too specific to adapt; every skill states what
   it does NOT do and where to route instead.
