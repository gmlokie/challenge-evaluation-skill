# Skill fitness — measuring the library, not just the entries

Adapted from simota/agent-skills `darwin` (Ecosystem Fitness Score,
Relevance Score, Shadow Mode, bottleneck migration, small mutations),
`lore` (confidence by evidence count, freshness states, domain TTL
multipliers, decay detection), and `gauge` (checklist audit, drift
detection, FP-rate calibration). The upstream versions assume a
90-skill Claude Code ecosystem with journals and dashboards; this file
keeps the *scoring method* and rewrites the *instruments* for a
single-agent Muse workspace (AGENTS.md, MEMORY.md, daily memory logs,
skill files).

## Fitness score (EFS-lite, per skill)

Score each skill across 5 dimensions, 0–20 each, total 0–100:

| Dimension | What it measures |
|-----------|------------------|
| Correctness | Guidance is right; following it produces verified results |
| Freshness | Content reflects current tools, APIs, platform rules |
| Usage | Actually invoked on real work (not shelfware) |
| Overlap | No substantial duplication with another skill |
| Cost | Context cost justified by the benefit (short skills score higher) |

Grades: S(95+) A(85+) B(70+) C(55+) D(40+) F(<40). A drop > 5
points in 7 days → flag for review. A skill that drops twice in a
row → sunset candidate.

## Relevance score (RS, per skill)

RS = recent use × outcome quality × uniqueness. Flag sunset
candidates with evidence: no use in 30 days, full overlap with
another skill, or a stale F grade. Sunset verification requires:
confirm zero active dependents (no skill, cron, or workflow reads
it), then retire — propose, never force; Dhika decides retirements.

## Shadow Mode (after any upgrade)

After any skill change (prompt/model/tool change, or a merge):

- The next 10 uses of that skill are compared against its 30-day
  baseline (success rate on the tasks it serves).
- A drop ≥ 5% → flag and consider rollback to the previous version.
- Keep the previous version (git or a dated copy) until Shadow Mode
  clears. Never overwrite the only copy during an upgrade.

## Confidence by evidence count

Label every lesson, rule, and claim in AGENTS.md / MEMORY.md / skills
with its evidence count:

| Evidence | Confidence |
|----------|------------|
| 1 | Anecdote — do not promote to guidance |
| 2 | Emerging — usable with a caveat |
| 3–5 | Pattern — guidance |
| 6–10 | Established — strong guidance |
| 11+ | Foundational — house rule |

Never promote an Anecdote to guidance. A single fabricated or
unverified "pattern" erodes trust in the whole catalog.

## Freshness states

| State | Age since last evidence | Action |
|-------|-------------------------|--------|
| FRESH | < 30 days | none |
| CURRENT | 30–90 days | monitor |
| AGING | 90–180 days | review |
| STALE | > 180 days | revalidate, archive, or remove |

Domain TTL multipliers (effective STALE threshold = 180 days ×
multiplier): SECURITY 0.5× (stale after 90 days) · INFRA / PERF
0.75× (135 days) · APP / TEST / UX 1.0× (180 days) · DESIGN 1.25×
(225 days) · PROCESS / META 1.5× (270 days).

Exceptions: FAILURE and ANTI patterns are never auto-archived by time
alone — failure modes recur. FOUNDATIONAL-confidence patterns require
an explicit human decision to archive. At catalog time, assign each
pattern an expected-validity window and schedule revalidation at 75%
of it, before it reaches AGING.

## Knowledge capture rules

- Capture within 48 hours of discovery — delayed documentation loses
  accuracy fast.
- Cluster by similarity: ≥ 80% → merge with the existing pattern;
  50–79% → variant; < 50% → new candidate.
- Same insight from 2+ sources in one domain → reinforced domain
  pattern; across domains → cross-cutting pattern.
- Contradictory insights → resolve explicitly; do not keep both
  silently.
- Promotion requires a new context, no active contradiction, and last
  evidence within 90 days.
- Strategic pruning is hygiene, not loss: archive patterns whose
  assumptions were invalidated so outdated knowledge cannot block new
  knowledge.

## Bottleneck migration

When generation gets cheaper or faster (new model, new tool, removed
bottleneck), the binding constraint migrates to judgment (review,
verification, decision). On each fitness check, identify the
currently rate-limiting tier; when the constraint has moved off
generation, reinforce verification/judgment capacity instead of adding
generation. An unmoved bottleneck assumption after a capability shift
is a stale assumption — flag it.

## Small mutations

85% accuracy per step → 5 steps = 44% success. Change one thing,
confirm it holds, then continue. Batch changes without checking impact
in between are forbidden: ~3 changes per session, ~10 per month, each
verified before the next.

## Checklist audit (gauge method, adapted)

Audit each SKILL.md against: frontmatter exactly `name` + `description`;
description carries trigger keywords + primary use in ≤ 2 sentences;
body < 500 lines (detail in references/); imperative form; no README /
CHANGELOG / INSTALLATION_GUIDE clutter; a Workspace adaptation block +
House rules block present; every referenced script exists and runs;
no duplicated content between SKILL.md and references. Classify
violations P0–P3 with concrete fix snippets, never vague
recommendations. Track score deltas between audits: < 10% stable,
10–20% investigate, > 20% intervene. Calibrate any detection rule
whose false-positive rate exceeds 15%.
