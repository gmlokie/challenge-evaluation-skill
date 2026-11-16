---
name: research-engine
description: "Hypothesis-driven research projects that run over multiple sessions: pre-register the question, form falsifiable hypotheses, run a fast test loop with a periodic synthesis loop, log dead ends, and pass every finding through a 6-dimension rigor review before it is reported as fact or used in a submit. Use when a question needs more than one search — top-10/competitor research, a Synmerco job's evidence base, a new platform or bounty evaluation, or any investigation where claims must survive scrutiny. Routes to deep-research and research-online for the actual searching."
---

# Research Engine

Single-shot search answers one question. This skill runs a **research
project**: a question that survives several rounds of testing, where
hypotheses live or die on evidence, dead ends are logged instead of
retried, and no finding ships until it passes a rigor review. Use it when
the research itself is the work — not when a fact lookup will do.

## When to use

- Top-10 / competitor research for a make.fun entry (what do the leaders
  actually do differently?).
- Evidence base for a Synmerco research job or a Dialectica answer that
  must survive verification.
- Evaluating a new platform, bounty, or garapan: is it real, what does it
  pay, what are the catches?
- Any investigation where an earlier round changed the question, or where
  claims will be submitted, published, or spent on.
- A previous research attempt stalled, looped, or produced confident
  claims from weak evidence — restart it here, with hypotheses.

Route elsewhere: a single question with a direct answer belongs to
`deep-research` (multi-angle method) or `research-online` (search
mechanics, chaining, dead-end protocol, sufficiency rules) — this skill
calls both and adds only project discipline on top. Free reference
sources (Wikipedia, Wikidata, arXiv, CrossRef, PubMed, npm, PyPI) live in
`research-refs`. Web3-specific tools (token/contract/domain checks) live
in `web3-research-toolkit`. Leaderboard benchmarking method lives in
`leaderboard-strategy-optimizer`. Pre-submit evaluation lives in
`challenge-evaluation` Part A — this skill's pre-registration (§2) is
the same discipline, applied to research.

## 1. Bootstrap — state dir first, searching second

Create the state dir before the first search:

```
~/workspace/research/<topic>/
├── question.md      # pre-registered question + stop rule (§2)
├── hypotheses.md    # H1..Hn with prediction + falsifier + status (§3)
├── findings.md      # evolving synthesis, newest at top (§5)
├── literature/      # one file per source: title, author/date, key
│                    # findings, relevance, URL/DOI — never cite a
│                    # source you did not open
├── dead-ends.md     # logged failures (§6)
└── state.md         # status, counts, last run, next step
```

Rules:

- The dir is the project's memory. A later session resumes by reading
  `state.md` + `findings.md` — never by re-searching from scratch.
- Raw numbers go in the files, not in chat memory: exact queries, hit
  counts, dates, values with sources.
- Keep it small: one topic per dir, archive (don't delete) when done.

## 2. Pre-register — write the plan before measuring anything

Before the first search, write `question.md`:

- **Question:** one sentence, falsifiable where possible.
- **Metric:** what would count as an answer (official metric, number,
  named fact — not "understand X better").
- **Sources:** which sources will be consulted, in which order
  (official docs first, then primary data, then secondary).
- **Inclusion criteria:** what counts as evidence (live data only?
  dated? primary source required?).
- **Stop rule:** when to stop (convergent evidence, official source,
  all sub-questions covered — see §8).
- **Decision rule:** what the answer changes (submit / stand pat /
  escalate / abandon) and at what threshold.

No peeking: once written, do not change the metric, the threshold, or
the sources because the numbers look bad. A changed rule after seeing
results is not research. (Same discipline as `challenge-evaluation` A1;
the PRISMA lesson: an audit trail retrofitted at the end is how reviews
fail — record queries, dates, and hit counts as you go.)

## 3. Hypotheses — every claim carries its own falsifier

Each hypothesis in `hypotheses.md`:

```markdown
## H1 — <claim in one sentence>
- Prediction: <observable outcome if H1 is true>
- Falsifier: <what observation would kill H1>
- Test: <search / simulation / measurement that decides it>
- Status: open | confirmed | refuted | abandoned (why)
- Evidence: <source + date + value>
```

Rules:

- A hypothesis without a falsifier is a guess — do not test it, rewrite
  it until it has one.
- One test decides one hypothesis. A test that "supports everything"
  supports nothing.
- Refuted hypotheses stay in the file with their evidence. Deleting a
  dead end is how the next session re-runs it.
- Start with 2–4 hypotheses, not 20. New ones come from the outer loop
  (§5), not from upfront brainstorming.

## 4. Inner loop — fast, tight, recorded

Repeat: pick one open hypothesis → run its test → record the result →
next. One cycle, one hypothesis.

- **Search tests** use `deep-research` / `research-online` method
  (multi-angle, fetch full sources, never snippets alone) and
  `research-refs` free sources.
- **Numeric tests** report medians of 3 runs with the range, never the
  best run. A single run lies.
- **Live-data tests** re-check the live source at test time; a stale
  snapshot is not evidence.
- Record immediately in `hypotheses.md`: status, evidence (source +
  date + value), and the raw numbers. Unrecorded results did not happen.

## 5. Outer loop — synthesize, then steer

Every 5–10 inner-loop tests, or when progress stalls, or when a pattern
appears — stop testing and synthesize:

1. Read all hypothesis outcomes + `literature/` + `dead-ends.md`.
2. Update `findings.md` (newest at top): what is now known, what changed
   since the last synthesis, what is still open.
3. Ask: what patterns emerge? What does this mean for the decision rule
   (§2)? New hypotheses? Pivot the question entirely?
4. Decide: continue inner loop, pivot, or stop (§8). Record the decision
   in `state.md` with the reason.

Research is non-linear: returning to the literature mid-project is
normal, not failure. Most real investigations loop back 1–3 times and
generate new hypotheses mid-stream. The two loops are a rhythm, not a
railroad — agent judgment sets the pace.

## 6. Dead-end log — log it once, never re-run it blind

When 2–3 query reformulations still return poor results, stop searching
and log in `dead-ends.md` (method: `research-online` dead-end protocol):

1. **Classify:** too niche (not publicly documented) · too new (not
   published yet) · too ambiguous (broaden, then narrow) · language
   barrier (try translated keywords).
2. **Switch strategy, not tool:** if the query is the problem, another
   search backend with the same query will fail the same way. Try
   site-qualified search (`site:docs.example.com <topic>`),
   version-qualified search (`"<library> <version>" <feature>`), or an
   exact error-quote search first.
3. **Document:** what was searched, what failed, which queries returned
   poor results. Mark the gap explicitly: "No authoritative source found
   for [topic]."
4. **Escalate rather than extrapolate:** never fabricate an answer from
   weak evidence. Partial information ships with confidence qualifiers;
   no information ships as an honest "I don't know" — better than a
   confident wrong answer.

A dead end already in the log is never re-searched in the same project
without a new strategy noted first.

## 7. Rigor review — no finding ships unreviewed

Before any finding is reported as fact, published, or used in a submit,
score it on six dimensions (1–5 each). Adapted from peer-review practice:
the review is constructive — strengths, weaknesses, and fixes — not a
bug hunt.

| Dim | What it evaluates | 1 = | 5 = |
|-----|-------------------|---|-----|
| D1 Evidence relevance | Does the cited evidence support the claim in substance, not just by reference? | Citation exists but says something else | Evidence directly entails the claim |
| D2 Falsifiability | Are the falsification criteria meaningful, actionable, well-scoped? | Unfalsifiable ("probably the best") | A named observation would kill it |
| D3 Scope calibration | Does the claim assert exactly what the evidence supports? | Over-claims (one example → "always") | Claim matches evidence, no more |
| D4 Argument coherence | Does the narrative follow from problem to evidence to conclusion? | Jumps, gaps, circular reasoning | Each step follows from the last |
| D5 Exploration integrity | Does the record document genuine process, including failures? | Only successes shown | Dead ends + refuted hypotheses logged |
| D6 Methodological rigor | Are tests well-designed: baselines, held-out data, medians of 3? | Single run, cherry-picked | Pre-registered, replicated, controlled |

Grade: **Strong accept** (all ≥4) · **Accept with fixes** (any 3,
with named fixes) · **Reject** (any ≤2 — rework, do not ship the
finding). Record the scores + grade in `findings.md` next to the finding.
A finding whose expected value was read off the same session's work
without an independent check is circular — verdict PARTIAL, never PASS
(`challenge-evaluation` evidence ladder E0–E6).

## 8. Sufficiency & stop rules

Stop researching when any of these holds — over-research wastes context,
under-research yields unreliable syntheses:

- **Convergent evidence:** 2+ independent sources agree. One source is
  a hint; two is a signal; three is confirmation.
- **Official source:** official docs / the live platform / the contract
  directly answer the question. Stop; no secondary confirmation needed
  unless the official source is outdated.
- **All sub-questions covered:** the question had 3 aspects and all 3
  are answered — stop, even if more could be found on aspect 1.
- **Decision rule met:** the §2 threshold is reached (submit / stand
  pat / abandon). Further research does not change the decision.

Keep researching when: sources contradict each other (resolve, don't
average); the only sources are forums, blogs, or AI-generated content
(find official or primary); the answer is version-dependent and no
version is cited; only indirect evidence exists.

Practical stop rules by query type (from `research-online`): simple fact
— 1 authoritative source; version-qualified — 1 official source with
version; how-to — 1 official doc + 1 working example; comparison — 2+
sources with different perspectives; error diagnosis — 1 confirmed,
version-matched fix.

## 9. Evaluate, review, preview, install, develop further

This skill is a draft input, not a fixed law — Dhika's flow applies:
**Evaluate → Review → Preview → Install → Develop further.**

- **Evaluate it:** measure with `challenge-evaluation` Part B. Fixed
  bench (run 3× with skill, 3× baseline = `deep-research` alone, same
  tasks, same checks):
  - R1 — token-radar v4 vs round-4 rank 47: hypothesis + falsifier
    written? decision (submit/stand pat) tied to a threshold?
  - R2 — POIDH 1553 (create our own bounty): cost/benefit hypothesis
    with a falsifier, dead ends logged?
  - R3 — Synmerco 50% price eval: hypothesis "win rate rises >1.5×
    vs 75%" with falsifier + what evidence would refute it?
  A task counts as solved when the majority of its runs pass. Verdict:
  ADOPT (beats baseline) · ADAPT (merge the working part) · SKIP.
- **Review it:** a fresh reviewer (subagent, no shared context) checks
  this SKILL.md for overreach — anything that duplicates
  `deep-research` phases or `research-online` mechanics belongs there,
  not here. This skill must stay project discipline only.
- **Preview it:** before installing, run it once on a live open question
  (§9 bench) and read the state dir it produces end-to-end.
- **Develop further:** after each real use, record what worked/failed,
  what source was missed, whether the method is reusable — in
  `AGENTS.md` / `MEMORY.md` / this skill. Small mutations over big
  rewrites: change one thing, confirm it holds, then continue. Never
  promote an anecdote (1 use) to guidance; 3–5 uses = pattern.

## Workspace adaptation

- Source methods: Kalaris Labs `research-agent-skills` (studied
  2026-11-16, sample only — 281 skills, full eval in
  `~/workspace/research/solver-skills/group-A-eval.md`): `autoresearch`
  (two-loop architecture, workspace state files, bootstrap, "research
  is non-linear"), `ara-rigor-reviewer` (6-dimension epistemic review,
  1–5 scoring, Strong Accept → Reject), `systematic-review-prisma`
  (pre-registration, audit trail of exact queries/dates/hit counts,
  PICO framing), `hypothesis-generation` /
  `brainstorming-research-ideas` (testable hypotheses with predictions).
  `research-online` (already installed) supplies the dead-end protocol
  and sufficiency/stop rules referenced in §6 and §8 — not duplicated
  here.
- Adapted for Muse/Rahul: the academic output (paper, PROSPERO/OSF
  registration, PubMed/Embase/Scopus searches, ARA artifact format
  `PAPER.md`/`logic/`/`trace/`) is NOT adopted — the question is a
  garapan decision, the "paper" is `findings.md`, the registry is the
  state dir. Paid/keyed tools named upstream (Exa MCP, Firecrawl,
  Semantic Scholar API) are replaced by free sources: `browser.search`,
  `research-refs` endpoints, `~/workspace/data-sources/DATA-SOURCES.md`.
  The "run fully autonomously, do not ask permission" posture is
  REJECTED — the security gate stands: research runs ahead freely, but
  any submit/spend/sign still needs preview + Dhika's yes per action.
  State files use plain Markdown (`state.md`, `findings.md`) instead of
  `research-state.yaml` — grep-able, no parser needed. Claude Code
  `/loop` and OpenClaw heartbeat continuity are replaced by the state
  dir itself (a later session resumes from files).
- Not adopted from the same repo: the ~275 domain skills (biology,
  chemistry, physics, ML training, clinical, academic publishing) —
  wrong domain for garapan work; `ara-research-manager` (ARA artifact
  format, academic publishing); `literature-review` as a standalone
  (its survey structure is folded into `literature/` here);
  `citation-management` / `bibtex-hygiene` (no BibTeX use here).

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
