---
name: learning-memory
description: "Capture, recall, consolidate, and forget what the agent learns — with local files only (MEMORY.md, daily notes, AGENTS.md), no vector DB, no server, no paid API. Use after any task, rejection, loss, or unexpected result; at the start of a task to recall relevant lessons; and during periodic memory review. Covers what to record, gated admission, confidence and freshness, promotion to skills, and archiving."
---

# Learning Memory

Memory is a method, not a database. This skill governs how Rahul
remembers: **what** gets recorded, **when**, in **which file**, with
**what confidence**, how it is **recalled**, when it is **promoted**
into a skill or rule, and when it is **forgotten**. Nothing here needs
a vector store, an embedding model, a server, or a paid API — the store
is Markdown files plus `grep`, and the retrieval discipline is what
makes it work.

## When to use

- After any task, rejection, loss, or unexpected result — capture the
  lesson before the session ends (within 48h at the latest; delayed
  capture loses accuracy).
- At the start of a task — recall lessons about the same venue, tool,
  or failure class before acting, so a paid-for mistake is not
  repeated.
- When two notes contradict each other, when a lesson is cited often
  enough to deserve a skill, or when memory feels stale or bloated —
  consolidate, promote, or archive.
- When deciding whether something is worth remembering at all — the
  admission gate (§2) is the default answer.

Route elsewhere: measuring whether a skill helps (`challenge-evaluation`
Part B — fixed-task bench, fitness, Shadow Mode); the pre-submit
acceptance gate (`challenge-evaluation` Part A); the closure report
that hands lessons over (`entry-test-cycle` §7). This skill is the
memory layer those call; it does not re-decide their verdicts.

## 1. The three operations — retain / recall / reflect

Every memory interaction is one of three operations. Name which one
you are doing; they have different rules.

### Retain — store a new record

- Write the record at the moment the lesson is learned, with its
  evidence attached (command + output, file + line, live check,
  timestamp). A record without evidence is a rumour, not a memory.
- One record = one lesson, one decision, or one fact. A record that
  bundles three lessons will be recalled for the wrong one.
- Keep the record in the file it belongs to (§3). Never keep the only
  copy in chat history — chat is not storage.
- **A memory write is not a belief commit.** Recording "X happened"
  does not mean "X is true forever". The record carries its evidence
  and confidence (§5); a later record can contradict it, and the
  contradiction is resolved by re-reading the evidence, not by
  deleting the older record silently.

### Recall — find before you act

- Before starting a task, search memory for the same venue / tool /
  failure class: `grep -ri "<keyword>" ~/MEMORY.md ~/memory/
  ~/AGENTS.md` and the relevant goal's `hidden_files/`.
- Recall is budgeted: read the top matches first, then expand only
  the records you actually need (one `grep` hit list is the index;
  the full record is the expansion). If the hit list is long, narrow
  the query — do not paste the whole memory into context.
- Report what recall returned: "recalled 2 lessons: <ids>, applied
  <n>". If recall returned nothing, say so — "no relevant memory
  found" is a result, not a failure. Never claim a lesson was applied
  when it was never recalled.
- Scope the recall: memory is per-account and per-venue. A lesson
  from lokie.ai or error403.id does not transfer to msbrew.ai unless
  the record says so explicitly (this account works on msbrew.ai
  only). A lesson about make.fun does not transfer to POIDH.

### Reflect — consolidate records into understanding

- Reflection is a separate, deliberate pass over a cluster of related
  records (e.g. all failures on one competition, all cap-raise events
  in a week). It does not happen automatically after every retain.
- An insight produced by reflection must cite **at least two distinct
  source records**. An insight with one citation is an anecdote, not
  an insight. Re-read each cited record before storing the insight;
  if the evidence changed or was deleted, the insight is rejected,
  not stored.
- Record rejected insights too (what was proposed, why it was
  rejected) — a rejected insight that is not recorded will be
  re-proposed next month.
- Reflection output is a standing answer to a standing question
  ("what do we know about X?") kept as a living document — a page
  that is rewritten as the bank learns more, not appended to forever
  (§3, pages).

## 2. Gated admission — not everything deserves to be remembered

Default: **do not record**. A record must pass the gate:

| Question | If no |
|---|---|
| Is it a fact, decision, or lesson — not a transient status? | Skip; status belongs in a run log, not memory. |
| Will it change a future decision? | Skip; trivia is noise that buries real lessons. |
| Is it verified (evidence attached, live-checked)? | Record as UNVERIFIED with the gap named, or skip. |
| Is it free of secrets, keys, wallet material, PII? | **Never record** — see §6. |
| Is it already recorded? | Strengthen the existing record (§4) instead of duplicating it. |

Temporary data (one-off IDs, in-flight run state, session tokens,
prices that change hourly) is never memory. If it is needed for one
task only, it lives in that task's working files and is discarded
with them.

## 3. Record types and where they live (typed multi-store)

One store is not memory. Each type has its own file, its own ID
scheme, and its own archive rule — so `grep` finds the right kind of
record and nothing else.

| Type | Lives in | ID | Archive rule |
|---|---|---|---|
| Durable fact / preference / commitment | `~/MEMORY.md` | — (section) | Never by time; only when superseded (record what replaced it). |
| Daily log (what happened, evidence) | `~/memory/<date>.md` | `claim:` line | Never deleted; superseded claims stay with their replacement noted. |
| Lesson (paid-for mistake / reusable method) | `~/AGENTS.md` or the relevant skill | Lesson line, dated | Never auto-archived — failure modes recur. |
| Bug / defect found in testing | goal `hidden_files/` or `entry-test-cycle` defect log | `BUG-<NNN>` | 50 entries or 6 months old → `_archive/`. |
| Decision (why X, not Y) | `~/memory/` decision note or `GOAL.md` | `ADR-<NNN>` | 30 entries or 12 months old → `_archive/`. |
| Known issue + workaround | relevant skill or `AGENTS.md` | `KI-<NNN>` | 50 entries or resolved > 3 months ago → `_archive/`. |
| Regression (bug that reappeared) | relevant skill | `REG-<NNN>` | 50 entries or 6 months old → `_archive/`. |
| Test / run log | goal `hidden_files/` | `TL-<NNN>` | 50 entries or 3 months old → `_archive/`. |
| Standing page (living answer) | `~/memory/` page or skill | page name | Rewritten in place, never appended to forever. |

- **Index:** each store file starts with a one-line-per-record index
  (ID, date, summary, status, file) so a record is findable by ID,
  keyword, or date without reading the whole file. Newest at the
  bottom; the index is updated when the record is added, not later.
- **Pages:** a standing page answers one question ("what is the
  Synmerco 50% price evaluation?"). Define the question once; rewrite
  the answer as new evidence arrives. Reading a page is a file read —
  no search, no synthesis — so a session can boot with settled
  knowledge instead of rediscovering it every time.
- **Environment / identity facts** (wallet addresses, account IDs,
  tool versions) are updated in place, never archived — they are
  always current or they are wrong.

## 4. Consolidation — records evolve, they are not overwritten

- Related records consolidate into **observations**: deduplicated
  beliefs with their supporting evidence and a proof count. New
  evidence **refines** an observation (strengthens, weakens, or
  extends it) — it never silently replaces it. Keep the exact quotes
  / evidence links on the observation; an observation without
  evidence is an opinion.
- When two records conflict, do not delete either. Write the
  conflict down (both claims, both evidences, date) and resolve by
  re-checking the live source. The resolution is itself a record.
- **Promotion (memory → skill → rule):** a lesson becomes skill
  guidance only when it has earned it — see §5 confidence. The
  compression spectrum is: raw log → observation → lesson →
  skill guidance → house rule. Each step up throws away detail and
  raises the bar for change. A house rule changes only on Dhika's
  say-so or on evidence that the old rule caused a loss.
- **Curate at read time, not write time** — with one caveat: the
  admission gate (§2) is the write-time filter, but ranking and
  filtering of recalled records happens at recall, against the
  current task. Do not pre-filter records for a future you cannot
  predict; do record them with enough context (venue, date,
  evidence) that future recall can judge them.

## 5. Confidence and freshness

Confidence is by evidence count, never by feeling:

| Evidence count | Label | May become |
|---|---|---|
| 1 | Anecdote | A log entry only. Never guidance. |
| 2 | Emerging | An observation. |
| 3–5 | Pattern | A lesson in `AGENTS.md` / a skill. |
| 6–10 | Established | Skill guidance, cited in reviews. |
| 11+ | Foundational | House rule candidate (Dhika decides). |

- Freshness: FRESH <30d · CURRENT 30–90d · AGING 90–180d · STALE
  >180d since last evidence. Security knowledge stales 2× faster;
  process/meta knowledge 1.5× slower. A STALE record is not deleted
  — it is flagged on recall ("last evidence <date>") so the reader
  re-verifies it before acting on it.
- **Authority is separate from content.** Who said it (Dhika,
  a live platform check, a subagent report, an upstream repo) is
  recorded on the record. Consolidation must not destroy authority:
  a lesson that came from Dhika's explicit instruction keeps that
  authority when promoted; a lesson from an unverified web page does
  not gain authority by being consolidated.
- Never promote an Anecdote to guidance. If a single incident
  demands a rule, the rule is "watch for X", not "X is always true".

## 6. Forgetting, archiving, and defense

- **Forgetting is a feature.** Archive (move to `_archive/`, never
  delete silently) when a store hits its threshold (§3), when a
  record is superseded (note the replacement), or when a periodic
  review finds a record that no longer changes any decision. A
  memory that cannot change a decision is clutter.
- **Never auto-archive failure / anti-pattern records by time.**
  Failure modes recur; a 6-month-old lesson about a grader quirk is
  still live if the grader still behaves that way.
- **Memory defense (mandatory):** every retain is scanned for
  secrets and PII before it reaches storage — API keys, tokens,
  seed phrases, private keys, passwords, wallet secrets, personal
  data. A match is **redacted** (`[REDACTED:api_key]`) or the record
  is **blocked** outright. No credential material ever enters
  `MEMORY.md`, daily notes, `AGENTS.md`, or a skill. Credentials
  live in the Secure Vault or a registered connector — never in
  files, never in memory.
- Deletion (not archiving) is only for: a record that contains a
  secret/PII (remove + note the removal), or a record Dhika
  explicitly asks to forget (see the `forget` skill). Deletion is
  recorded: what was removed, when, why — otherwise the gap looks
  like a missing record.
- Multi-agent caution: memory is per-agent. A lesson learned by
  another agent (or a subagent) is not trusted until its evidence
  is re-read here. Subagent reports are data, not memory, until
  verified and retained through this skill.

## 7. Periodic review (monthly, or after any skill change)

1. **Fitness per record type** — correctness, freshness, usage,
   overlap, cost (see `challenge-evaluation` B3 for the grading
   scale; this skill does not re-define it).
2. **Shadow check after any promotion:** the next 10 uses of the
   promoted lesson are compared against the pre-promotion baseline;
   a drop ≥ 5% → flag and consider rollback.
3. **Sunset candidates:** records with no use, full overlap with
   another record, or a stale F grade — propose, never force;
   verify zero active dependents before archiving.
4. **Small mutations over big rewrites:** one change, confirm it
   holds, then continue. A memory rewrite that changes 50 records
   at once cannot be verified.
5. **Bottleneck check:** when generation gets cheaper, judgment
   becomes the constraint — reinforce verification (recall +
   evidence re-read) instead of adding more records.

## Evaluate, review, develop further

This skill is a draft to be measured, not a fixed ritual. Evaluate it
the `challenge-evaluation` Part B way before trusting it:

- Fixed-task bench: 4–8 real recall tasks (e.g. "what do we know
  about the make.fun dotfile rejection?", "what is the Synmerco
  50% price evaluation?", "why did the Flint rank report go wrong?").
  Each has a ground-truth answer + the evidence file it lives in.
  Run each task 3× WITH this skill (retain/recall/reflect as
  written) and 3× WITHOUT (free-text notes, plain grep), same
  prompts; record `results.jsonl` and aggregate with
  `challenge-evaluation/scripts/bench_aggregate.py`.
- What counts as "helps": higher recall precision (relevant records
  / returned records), fewer repeated mistakes (a lesson recalled
  and applied before the same error recurs), no secret ever retained,
  no blow-up in records per task. A skill that adds records without
  improving recall is ADAPT (keep the working part) or SKIP.
- Review after every real use: which records were actually recalled,
  which were never recalled (sunset candidates), which recall missed
  a record that mattered (indexing gap). Change one thing, confirm
  it holds, then continue. Report the change and its evidence in
  the skill's next review; do not silently rewrite the memory rules.

## Workspace adaptation

- Source methods: vectorize-io/hindsight (retain / recall / reflect,
  observations with evidence + proof count, mental models / pages,
  Memory Defense, banks), bigrzz/agent-memory (memory vs observation
  layers, lessons, insights citing ≥2 sources with evidence re-read,
  budgeted recall, keyless local BM25 mode), tfatykhov/
  awesome-agent-memory (gated admission, typed multi-store,
  consolidation loops, forgetting as a feature, memory↔skills↔rules
  compression spectrum, curate at read time, authority separate from
  content, memory write ≠ belief commit), AZANIR/qa-skills
  `docs/qa-memory/` (file-based typed stores with ID formats,
  archive thresholds, grep index), simota/agent-skills `lore`
  (confidence by evidence count, freshness, decay) via
  `challenge-evaluation` B3. Studied 2026-11-16; report:
  `~/workspace/research/solver-skills/group-C-eval.md`.
- Adapted for Muse/Rahul: **method only — no infrastructure.**
  Hindsight needs an LLM API key + a server (Docker/Postgres) or
  paid Cloud; agent-memory needs a pinned iii-engine binary + a
  local MCP/REST daemon on fixed ports. Neither is adopted: the
  store here is `MEMORY.md` + daily notes + `AGENTS.md` + `grep`,
  and the "BM25" in the keyless mode is exactly what `grep -ri`
  already does. Banks become per-account/per-venue scoping
  (msbrew.ai only — no cross-account memory). Decision models,
  rerankers, and embedding models are not adopted; ranking at
  recall is by recency + evidence count + explicit relevance to
  the task, done by the agent.
- The existing memory files already follow most of this method
  informally (dated lessons in `AGENTS.md`, claim lines in daily
  notes, 48h promotion rule in `challenge-evaluation` A6). This
  skill makes the method explicit, adds the parts that were missing
  (admission gate, typed stores + archive rules, confidence ladder,
  insight citation rule, memory defense, forgetting), and gives
  the whole thing a measurement method. It does not replace
  `MEMORY.md` or `AGENTS.md` — it governs how they are written.
- Not adopted: any vector DB, embedding provider, cloud service,
  hosted inference, or background daemon. If a future task genuinely
  needs semantic search over a large corpus, that is a new proposal
  for Dhika — not something this skill smuggles in.

## House rules (Rahul — msbrew.ai)

- Every sign, transaction, or approval needs a preview + Dhika's
  explicit yes per action. Never auto-execute on-chain or account
  actions. Memory work is read-only against accounts and wallets:
  it never touches credentials, never executes a transaction, never
  changes a cron or goal.
- Never request, show, or send seed phrases or private keys.
- Free-only: no capital, stake, deposit, or paid API/key without
  Dhika's explicit yes per action. Credentials live in the Secure
  Vault or a registered connector — never in files, never in memory.
- Use `curl`, not Python `urllib` (urllib fails with IncompleteRead
  on some hosts).
- Dollar values only via `~/workspace/tools/usd_value.py`, with
  formula + price sources shown.
- Live data only — never present a stale snapshot as current. A
  recalled record is a lead to re-verify, not a current fact, until
  its evidence is re-checked.
- Deliverables in `~/workspace/`, never `/tmp` (/tmp is wiped on VM
  replacement). VM clock is UTC; Node 22.
