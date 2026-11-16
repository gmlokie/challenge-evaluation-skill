---
name: task-analyzer
description: "Front door for any new task, bounty, competition, or job: turn vague or underspecified input into a structured brief with a sealed requirement checklist (REQ IDs + Given/When/Then acceptance criteria), then verify the built artifact against that brief (drift check) before it goes to strategy or submit. Use FIRST when a task arrives vague, when intake is <3 sentences, when requirements must be extracted from a live page/repo/description, or before any submit to catch brief-vs-artifact drift. Routes to precision-task-optimizer for strategy/simulation and to challenge-evaluation for the pre-submit gate."
---

# Task Analyzer

Turn "kerjain ini" into a brief you can verify — before strategy, before
building, before submitting. This skill owns the **intake** stage: vague
input → interview → extracted requirements → sealed checklist → drift
check. It does NOT pick strategies (that is `precision-task-optimizer`
§4), does NOT run simulations (§5), and does NOT issue the submit verdict
(that is `challenge-evaluation` Part A).

## When to use

- A new task, bounty, competition, or job arrives and the input is vague,
  short, or missing objective / scoring / deadline / format.
- Requirements must be extracted from a live page, a repo, a spec doc, or
  a chat description — from more than one source at once.
- Before ANY submit: run the drift check (§6) — brief vs artifact vs live
  platform — even if the entry "feels done".
- When a previous attempt failed on a missed requirement: re-run
  extraction on the same input and diff the checklists.

Route elsewhere: strategy generation, simulation, adversarial review, and
the §11 quality gate live in `precision-task-optimizer`; the pre-submit
acceptance verdict lives in `challenge-evaluation`; the Iron Law (fresh
verification before any completion claim) lives in
`verification-before-completion`; test-writing discipline lives in
`test-driven-development`; root-cause debugging lives in
`systematic-debugging`.

## 1. Intake triage — interview or extract?

Score the input against five questions before doing any other work:

1. Objective — what does "done / win" mean, in one sentence?
2. Scoring — what is the official metric, and what is the cutoff?
3. Deadline — when, in which timezone?
4. Deliverable — what format, where, and what evidence?
5. Constraints — what is forbidden, what costs money, what needs a yes?

- **0–1 missing → extract (§3) directly.** The input is sufficient.
- **≥2 missing, or input <3 sentences → interview (§2) first.** Do not
  guess past the gap: a plausible-but-wrong assumption burns a whole
  build. (Trail of Bits rule, corroborated here: structured upfront
  questions eliminate entire branches of wasted effort.)
- **Input contradicts itself** (e.g. deadline says X, page says Y) →
  interview §2 Phase 4 (conflict resolution) before extraction.

Record the triage verdict in one line: `TRIAGE: interview | extract |
conflict | missing: [list]`.

## 2. Discovery interview — vague input → structured brief

Six phases. Ask at most **5 questions per round**, offer multiple-choice
options with a default where one exists, and **wait for the answers
before doing any work**. Never batch all categories at once.

| Phase | Name | What happens |
|-------|------|--------------|
| 1 | Orientation | 2–3 broad questions: what are we doing, new or existing, who decides |
| 2 | Category deep dive | 8 categories below, 2–4 questions each, adaptive — skip what is already clear, dig where there are gaps |
| 3 | Research loops | Uncertainty found → read the live source first (page, repo, docs, API), return with informed follow-ups |
| 4 | Conflict resolution | Surface contradictions explicitly, ask for a decision — never silently pick a side |
| 5 | Completeness check | Checklist before generating the brief |
| 6 | Brief generation | Write `brief.md` (§4) |

### The 8 categories (garapan-adapted)

| Cat | Name | Focus for Rahul's work |
|-----|------|------------------------|
| A | Objective & reward | What is won, prize, payout wallet/chain, claim deadline |
| B | Rules & eligibility | Who may enter, one-per-wallet, account scope (msbrew.ai only) |
| C | Scoring & judging | Official metric, cutoff/rank, dev vs final phase, judge behavior |
| D | Deliverable & format | Entry format, file/output tree, screenshots, dossier limits |
| E | Deadline & timezone | Open/close/result times — convert to WIB, state both |
| F | Constraints & risks | Free-only, gas cost, key/approval needs, platform quirks |
| G | Resources & tools | Repo, kit level, quota left, scripts, prior entries |
| H | Verification & evidence | How success is checked live, what proof the submit needs |

### Conflict patterns (Phase 4)

- Scope vs time ("full coverage in 2 days") → ask which bends.
- Everything is "critical" → force a rank order, max 3 criticals.
- Unrealistic automation ("auto-submit") → restate the security gate:
  preview + Dhika's yes per action; no standing auto-submit.
- Missing infrastructure (no kit, no quota, no key) → name the blocker
  and stop; do not design around a missing prerequisite.

### Completeness checklist (Phase 5)

- [ ] All 8 categories addressed or explicitly marked N/A with a reason
- [ ] Objective, scoring metric, and deadline each have a source + time
- [ ] Critical paths / happy + unhappy flows named
- [ ] Constraints and approval needs listed (nothing assumed free)
- [ ] No ambiguous or conflicting statement left in the brief
- [ ] Brief is sufficient for `precision-task-optimizer` §2 to run with
      no additional input

## 3. Requirement extraction — sources → sealed checklist

### Modes (pick all that apply; `full-audit` = all of them)

| Mode | Source | How |
|------|--------|-----|
| `from-url` | Live competition/job page | Read the live page + status API first; extract flows, fields, validation rules, endpoints, deadlines |
| `from-code` | Repo / entry tree | Scan structure, entry points, configs; derive what the artifact must contain |
| `from-description` | Chat / brief text | Parse actors, actions, outcomes; decompose into atomic items |
| `from-docs` | README / rules / DESIGN.md | Extract stated rules, limits, formats |
| `full-audit` | All of the above | Cross-check modes against each other; conflicts go to §2 Phase 4 |

**Never extract from memory or from a stale snapshot.** The live page is
the source; a search snippet is not. When the first source fails (403,
timeout, empty API), try a relevant alternative and record the failure
separately — a blocked page is a source failure, not evidence the
requirement does not exist.

### Requirement format

Every requirement gets an ID and is written once, sealed:

- **ID:** `REQ-FN-001` (functional), `REQ-NFR-001` (non-functional),
  `REQ-CX-001` (constraint / compliance — e.g. free-only, no secrets,
  deterministic output)
- **Title + statement:** one unambiguous sentence, no "should / may /
  might".
- **Priority:** Critical / High / Medium / Low (business value, not
  effort).
- **Acceptance criteria:** Given / When / Then, measurable.
- **Source:** URL / file + line / message — with a timestamp for live
  sources.
- **Status:** Draft / Reviewed / Approved (only Dhika approves scope
  changes).

### Requirement patterns (check each task against them)

CRUD, auth/login, search/filter, pagination, file upload, error handling,
payment/claim, deadline/window, output-tree shape, determinism,
screenshot/dossier gates. A pattern the task needs but the brief never
mentions is a gap — flag it, do not silently add it.

### Quality checklist

- [ ] Every requirement has a unique ID and a source
- [ ] No ambiguous language; every item is testable (measurable AC)
- [ ] Mandatory vs bonus vs recommendation distinguished
- [ ] Dependencies explicitly linked (REQ-X blocks REQ-Y)
- [ ] No duplicates, no conflicts
- [ ] Hidden conditions named (quota, kit level, sealed transcripts,
      one-per-wallet, output-tree rules)

## 4. Brief output — `brief.md`

Save in `~/workspace/<task>/brief.md` (never `/tmp`). Contents:

```markdown
# Brief — <task>
- Objective: …
- Scoring: <official metric + cutoff> (source + time)
- Deadline: <UTC + WIB> (source)
- Deliverable: <format + location>
- Constraints: …
## Requirements
| ID | Statement | Priority | Acceptance (G/W/T) | Source |
## Open questions / blockers
## Handoff
- Next: precision-task-optimizer §2 checklist ← this file; §13 plan
  brief AC-{n} ← REQ IDs above (one check per AC, sealed once written)
```

The brief is the handoff document. `precision-task-optimizer` §13
Step 2 builds its plan brief from these REQ IDs — one acceptance
criterion per requirement, sealed once written.

## 5. NFR lens — non-functional requirements, garapan edition

Run `qa-nfr-analyst`-style analysis (ISO 25010, adapted — no enterprise
baggage) on every build task. Ask per dimension; anything unanswered
becomes a REQ-NFR item:

| Dimension | Garapan translation |
|-----------|---------------------|
| Performance | Grader time/memory limits (e.g. 120 s wall, 1 CPU, 1024 MB); screenshot dimensions; CPU-time race |
| Determinism | Same inputs → byte-identical outputs, twice; no network at grade time; no timestamps/randomness in output |
| Reliability | Concurrent grader runs (2× into one /output); atomic install; no delete-then-copy |
| Security | No secret/token/credential in the entry; no hidden network callbacks; no sandbox escape |
| Compatibility | Vendored deps only; pinned versions (three r187); kit level current |

## 6. Drift check — brief vs artifact vs live platform

Run before ANY submit, and after any rejection. Compare four dimensions;
a finding in any dimension blocks the submit until fixed or explicitly
accepted by Dhika.

| Dimension | A | B | Detects |
|-----------|---|---|---------|
| Brief ↔ artifact | `brief.md` REQ list | Built entry / bundle | Requirement not implemented; extra behavior not in brief |
| Brief ↔ live platform | REQ list | Live status / check reason | Rule changed; quota/kit level moved; deadline moved |
| Brief ↔ checks | REQ list | Test results / kit checks / `check_output_tree.py` | Untested requirement; orphan check; output-tree violation |
| Docs ↔ implementation | README / DESIGN.md | Code / bundle | Outdated docs; undocumented behavior |

Procedure:

1. **Read the live check reason FIRST** when a platform check failed —
   before theorizing any cause. (best-game-01 rounds 1–3: the cause was
   `screenshots/.gitkeep` in the output, not the pid-1 theory.)
2. For make.fun entries run
   `python3 ~/workspace/custom-skills/challenge-evaluation/scripts/check_output_tree.py <entry-dir>`
   — it mirrors exactly what `main.ts` copies into `/output`.
3. Per finding: severity (Critical/High/Medium/Low), affected artifact,
   action (update docs / fix implementation / create check).
4. Regression-set note: checks that always pass and cover stable code are
   "worn out" — rotate them out, prioritize checks on changed/high-risk
   areas (§7).

Output: a drift report (findings by dimension + action items). No drift
report, no submit.

## 7. Risk-ranked verification — check the riskiest first

When verification time is limited, order the checks by risk, not by
checklist order:

```
Risk = Complexity × ChangeFrequency × (1 − Coverage)
```

- **Complexity:** how intricate the requirement/area is (logic, edge
  cases, concurrency) — H/M/L → 3/2/1.
- **ChangeFrequency:** how often this area changed (git log, recent
  fixes) — H/M/L → 3/2/1. New files with no history: use complexity +
  criticality only, flag as "new".
- **Coverage:** 0–1, fraction of the requirement's acceptance criteria
  with a passing evidence check. 1 = fully covered.
- **Adjust:** defect history and business criticality move an item up
  one rank (payment, auth, claim, submit path).

Rank all REQ items, verify High → Low, and record the ranking in the
drift report. If scores tie or cluster, normalize to relative ranking —
identical scores mean the factors were not discriminating, not that
everything is equally risky.

## 8. Evaluate, review, preview, install, develop further

This skill is a draft input, not a fixed law — Dhika's flow applies:
**Evaluate → Review → Preview → Install → Develop further.**

- **Evaluate it:** measure with `challenge-evaluation` Part B. Fixed
  bench (run 3× with skill, 3× baseline = `precision-task-optimizer`
  §2 alone, same tasks, same checks):
  - T1 — vague input ("buatin game buat fps-01", <3 sentences):
    interview triggered? brief written with gaps flagged?
  - T2 — extract requirements for markdown-render-speed-02 from its
    brief: all of byte-identical / 720 cases / CPU-time race / sealed
    transcripts captured as REQ items?
  - T3 — drift check on the best-game-01 round-4 bundle: output-tree
    clean? dotfile risk flagged (copyEntryFolder copies dotfiles)?
  A task counts as solved when the majority of its runs pass. Verdict:
  ADOPT (beats baseline) · ADAPT (merge the working part) · SKIP.
- **Review it:** a fresh reviewer (subagent, no shared context) checks
  this SKILL.md for overreach — anything that duplicates
  `precision-task-optimizer` §2 or `challenge-evaluation` A2 belongs
  there, not here.
- **Preview it:** before installing, read the draft end-to-end and check
  the routing table (§When to use) against a real incoming task.
- **Develop further:** after each real use, record what worked/failed,
  what source was missed, whether the method is reusable — in
  `AGENTS.md` / `MEMORY.md` / this skill. Small mutations over big
  rewrites: change one thing, confirm it holds, then continue. Never
  promote an anecdote (1 use) to guidance; 3–5 uses = pattern.

## Workspace adaptation

- Source methods: AZANIR `qa-skills` (studied 2026-11-16, full eval in
  `~/workspace/research/solver-skills/group-A-eval.md`):
  `qa-discovery-interview` (6 phases, 8 categories, embedded trigger,
  conflict resolution, completeness check, brief output),
  `qa-requirements-generator` (from-url/from-code/from-description/
  full-audit modes, ISO 29148 structure, REQ IDs, Given/When/Then),
  `qa-spec-auditor` (4-dimension drift comparison, regression-set
  optimization), `qa-risk-analyzer` (Risk = Complexity ×
  ChangeFrequency × (1 − Coverage)), `qa-nfr-analyst` (ISO 25010 NFR
  lens). Trail of Bits `ask-questions-if-underspecified` (via
  whatif-dev awesome list, verified 2026-11-16): max 5 targeted
  questions per round, multiple-choice with defaults, wait for answers.
- Adapted for Muse/Rahul: the 8 QA categories re-mapped to garapan
  intake (objective/reward, rules, scoring, deliverable, deadline,
  constraints, resources, verification); ISO 29148 SRS full structure
  dropped — only REQ IDs + Given/When/Then kept; Cursor/MCP tooling
  (Playwright MCP, Sequential Thinking MCP, Memory MCP, GitHub MCP)
  replaced by this VM's tools (browser search/fetch, exec, git,
  connectors); `output_dir: docs/briefs` replaced by
  `~/workspace/<task>/brief.md`; Figma mode dropped (no Figma use);
  Jira/Linear/ClickUp/Qase integrations NOT adopted (paid keys, unused
  here).
- Not adopted from the same repo: the 16 framework test writers
  (Jest/Vitest/Cypress/Selenium/pytest/… — `test-driven-development` +
  `playwright-skill` already cover test discipline), the 6 tracker
  integrations, `qa-playswag` (needs OpenAPI specs), `qa-test-healer`
  auto-fix (conflicts with the verification gate — fixes are reviewed,
  never silent).

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
