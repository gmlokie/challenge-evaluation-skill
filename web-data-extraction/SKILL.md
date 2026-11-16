---
name: web-data-extraction
description: Extract structured data from the web with free local tools only — public no-key APIs first, RSS second, static HTML via curl third, Playwright rendering last. Declare the output schema before fetching, validate every record, dedupe, timestamp, and save JSON/CSV under ~/workspace. Use for lead lists, price checks, leaderboard reads, competitor/market research, or any "get me a table of X from the web" task. Never uses paid scrapers or API keys.
---

# Web Data Extraction (Free-Local Pipeline)

One pipeline for every extraction job, cheapest source first. The
method is adapted from Apify's `apify-ultimate-scraper` (actor
selection → schema check → run → poll → dataset) with the paid
platform removed: there are no Actors, no APIFY_TOKEN, no
pay-per-event — the "actors" are `curl`, RSS, and the local
Playwright install.

## 1. Declare the schema BEFORE fetching

Write the output schema first, in the task file or the reply:

```json
{"fields": {"name": "string, required", "price_usd": "number, required",
            "source_url": "string, required", "fetched_utc": "string, required"},
 "dedupe_key": "source_url",
 "max_items": 50}
```

Rules:

- No fetch without a schema. A scrape with no declared fields
  returns a pile of text, not data.
- Every record carries `fetched_utc` and `source_url`. Data with no
  timestamp is stale data waiting to be misread as live.
- `max_items` is a hard cap, declared up front. It is the free
  replacement for Apify's pay-per-event cost estimate: it bounds
  the work before it starts.

## 2. Source ladder — cheapest first, stop at the first that works

| # | Source | When | How |
|---|---|---|---|
| 1 | **Public API, no key** | The site offers one (CoinGecko, GitHub public, FDIC BankFind, public RPCs) | `curl` + `jq`/python; check `~/workspace/data-sources/DATA-SOURCES.md` first — 40 no-key sources are already indexed there |
| 2 | **RSS / Atom feed** | News, blogs, release notes, bounties | `curl` the feed, parse XML with python stdlib |
| 3 | **Static HTML via curl** | Server-rendered pages, tables, lists | `curl -L -A <ua>`; parse with python stdlib (`html.parser`) — never regex the whole page |
| 4 | **Playwright render** | JS-rendered SPA, content only after interaction | `playwright-skill`: headless, wait for a locator (never `networkidle` alone), extract via `locator.allInnerTexts()` / `evaluate()` |

Do not start at step 4. A rendered-browser run costs the most
time and the most bot-detection risk; most extractions end at
step 1 or 2. If step 1 exists, steps 3–4 are waste.

## 3. Run protocol

1. **Check the source's own shape first.** Fetch one sample (or
   the API's schema/docs) and confirm the field names before
   writing the extractor. Field names vary (`maxResults` vs
   `maxItems` vs `resultsLimit` in Apify's gotchas; same problem
   everywhere) — guessing a field name is the #1 cause of empty
   results.
2. **Small batch first.** Fetch 3–5 records, validate them against
   the schema, then run the full batch. Never run the full batch
   on an unvalidated extractor.
3. **Paginate honestly.** Respect the source's page size; cap
   total items at `max_items`; sleep 1–2s between pages.
   A source that returns fewer items than requested is telling
   you something — read it, don't hammer it.
4. **Validate every record** with `scripts/validate.py`:
   required fields present, types correct, dedupe by
   `dedupe_key`, drop empties, report counts (fetched / valid /
   dropped / duplicates). Validation output is part of the
   deliverable, not an afterthought.
5. **Save to `~/workspace/`** as `<yyyymmdd>-<slug>.json`
   (or `.csv`), never `/tmp`. The file + the validation report
   are the result; a chat summary without the file is not a
   delivery.

## 4. Empty results — diagnose before re-running

| Symptom | Likely cause | Fix |
|---|---|---|
| 0 items, HTTP 200 | Wrong field name / too-narrow query | Re-check the schema/sample; broaden the query |
| 0 items, HTTP 403/429 | Rate limit or bot block | Back off, slow down, use the public API/RSS instead |
| 0 items, empty HTML | JS-rendered page | Move up the ladder to Playwright (step 4) |
| Partial items | Pagination cap / page-size limit | Page through; check the source's per-page max |
| Stale numbers | Cached page / wrong endpoint | Re-fetch live; label the timestamp; never present a cached read as live |

## 5. Guardrails (adapted from Apify's gotchas — free-only edition)

- **Free-only gate:** any step that would need an API key, a
  login, a subscription, or a payment STOPS. Report the cost and
  ask Dhika — never pay, never borrow a key, never "just try" a
  paid endpoint. (Apify's rule was "estimate PPE cost, confirm
  above $20" — here the threshold is $0: anything above free
  needs an explicit yes.)
- **No WAF/CAPTCHA bypass.** Cloudflare Turnstile, DataDome,
  login walls, and CAPTCHAs are stop signs, not obstacles to
  route around. No residential proxies, no fingerprint rotation,
  no session-cookie reuse from Dhika's browser. If the public
  path is blocked, say so and use another source.
- **No credential material.** Scrapers never touch cookies,
  sessions, or tokens belonging to Dhika. Test credentials only,
  dummy values only.
- **Respect the source.** 1–2s between requests, honour
  `robots.txt` for bulk crawls, never scrape a site in a way
  that could get Dhika's IP or account flagged. If a source
  says no (403/429/toS), stop.
- **Live data only.** Every deliverable states when it was
  fetched (UTC). A price, rank, or listing from an hour ago is
  reported with its timestamp, never as "current".

## 6. Output format (every delivery)

- File path + record count + validation counts
  (fetched / valid / dropped / duplicates).
- Fetch timestamp (UTC) + source(s) used + ladder step reached.
- Top 5 records inline (or all, if ≤ 5).
- What was NOT found / what is uncertain — never silently
  omit a missing field.

## 7. What this skill does NOT do

- Choosing which data matters / strategy: `precision-task-optimizer`.
- Keeping a catalogue of sources: `~/workspace/data-sources/DATA-SOURCES.md`
  (crypto-market-data, news-rss-feeds, onchain-reads, public-records-geo,
  research-refs, prediction-markets skills own their sources).
- Browser automation mechanics: `playwright-skill` (this skill
  decides *when* to render; playwright-skill decides *how*).
- Acting on the data (bid, submit, trade): the job's own skill
  + `challenge-evaluation` gate. Extraction is read-only.

## 8. Evaluate, review, develop further (mandatory, not optional)

This skill is a draft method, not a fixed law. It must be measured
and revised like any other skill:

- **Measure (Part B, `challenge-evaluation`):** fixed task set
  (4–8 real extractions with a runnable pass/fail check: the
  output file exists, `validate.py` passes, record count is
  within the expected range, every record has `fetched_utc` +
  `source_url`). Run each 3× WITH this skill and 3× WITHOUT it
  (baseline: ad-hoc curl/grep), same model, same prompt. Solved
  = the check passes, never LLM-as-judge for the headline number.
  Aggregate with `challenge-evaluation/scripts/bench_aggregate.py`.
  Verdict: ADOPT / ADAPT / SKIP.
- **Review:** after every real use, note what the ladder got
  wrong (started too high? field name guessed? source blocked?).
  Promote recurring notes into this SKILL.md within 48h.
- **Develop further:** new sources come from real jobs, not from
  a vendor catalogue. If a job needs a source that is not in
  DATA-SOURCES.md, add it there (free, no-key) with the
  verification date — never add a paid source without Dhika's yes.
- **Fitness signals:** validation pass rate, share of jobs that
  end at ladder step 1–2 (cheap), zero paid/blocked incidents.
  If most jobs still end at step 4, the ladder is not being
  followed — fix the skill, not the jobs.

## Workspace adaptation

- Source methods: Apify `apify-ultimate-scraper` SKILL.md +
  `references/gotchas.md` + `references/actor-index.md`
  (actor selection, dynamic schema fetch, run/poll/dataset,
  pricing models, cost-estimation protocol, empty-result and
  rate-limit playbooks). Studied 2026-11-16; report:
  `~/workspace/research/solver-skills/group-B-eval.md`.
- Adapted for Muse/Rahul: the Apify platform is NOT adopted —
  no CLI, no token, no Actors, no pay-per-event. The *method*
  (select source → check schema → small batch → validate →
  structured dataset) is re-implemented on free local tools
  (curl, RSS, stdlib python, Playwright). The actor index
  (100+ platform Actors) is replaced by DATA-SOURCES.md + the
  source ladder. The PPE cost protocol becomes the free-only
  gate ($0 threshold). The proxy/fingerprint sections of the
  gotchas are explicitly REJECTED (anti-bot bypass).
- NOT adapted: `apify-actor-development`, `apify-actorization`,
  `apify-integration-development`, `apify-generate-output-schema`
  — all build/deploy for the paid Apify platform (Docker,
  Actor SDK, `apify push`); no free-local equivalent is needed.

## House rules (Rahul — msbrew.ai)

- Every sign, transaction, or approval needs a preview + Dhika's explicit yes per action. Never auto-execute on-chain or account actions.
- Never request, show, or send seed phrases or private keys.
- Free-only: no capital, stake, deposit, or paid API/key without Dhika's explicit yes per action. Credentials live in the Secure Vault or a registered connector — never in files.
- Use `curl`, not Python `urllib` (urllib fails with IncompleteRead on some hosts).
- Dollar values only via `~/workspace/tools/usd_value.py`, with formula + price sources shown.
- Live data only — never present a stale snapshot as current.
- Deliverables in `~/workspace/`, never `/tmp` (/tmp is wiped on VM replacement). VM clock is UTC; Node 22.
