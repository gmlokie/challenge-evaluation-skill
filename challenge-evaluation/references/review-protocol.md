# Review protocol — concurrence, grounding, evidence ladder

Adapted from simota/agent-skills `judge` (tri-engine review, concurrence
scoring, grounding, severity vs blocking) and `attest` (evidence ladder,
circular verification, traceability). The upstream tri-engine fan-out needs
Codex/Claude/agy CLIs — this workspace replaces it with: a fresh
reviewer subagent + scripted checks + live-data verification. The
*method* (independent passes, concurrence labels, grounding before
shipping) is kept intact.

## The rule that matters most

**Generator never grades its own work.** The agent that built the entry
does not review it. Review runs as: (1) a fresh subagent with no shared
context, (2) scripted checks (kit check, `check_output_tree.py`, live
status reads), (3) the parent re-verifying the reviewer's claims against
the actual artifact. A subagent's "success" report is its own claim —
re-run the receipt before repeating it.

## Concurrence labels

| Label | Meaning | Ship it? |
|-------|---------|----------|
| CONFIRMED | Found by 2+ independent passes (different reviewers/checks) | Yes, with evidence |
| LIKELY | Found by 1 pass, grounded in code/data (file:line or live output cited) | Yes, with the grounding cited |
| CANDIDATE | Found by 1 pass, ungrounded | NO — verify against the actual artifact first; it becomes VERIFIED, REJECTED, or NEEDS-INFO |

Never ship an ungrounded CANDIDATE in the main findings list. Keep a
condensed rejection ledger (counts per category) so dropped findings are
visible, not silently lost.

## Severity vs blocking (separate axes)

- Severity ranks findings against each other: CRITICAL / HIGH / MEDIUM /
  LOW / INFO.
- Blocking is a separate axis: every shipped finding carries
  `blocking: yes | no` + the reason. A HIGH on a path the change does
  not enable can be non-blocking; a MEDIUM that breaks a published
  contract blocks. Blocking states the resolution level required, not the
  implementation — fix the mechanism, do not dictate the patch.
- Non-blocking findings that must not be lost carry an owner and a
  tracking route, never a bare "consider…".

## Intent alignment

Emit an `intent_alignment` verdict per review: PASS (the entry matches
the competition's stated task) · FAIL (scope creep or contradiction) ·
NOT_CHECKED. Absent intent is never PASS. A FAIL blocks the submit
regardless of check scores.

## Evidence ladder (E0–E6)

How independent of the implementation's own assumptions is the evidence?

| Level | Evidence | Example |
|-------|----------|---------|
| E0 | Assertion only | "It works" |
| E1 | Read the implementation | Code review of main.ts |
| E2 | Static check | Kit check, lint, typecheck |
| E3 | Automated test, same session | Local grade run by the builder |
| E4 | Property / differential / fresh-draw check | Same entry on unseen jobs; two independent runs agree |
| E5 | Independent reproduction | A fresh agent reproduces the result from a clean checkout |
| E6 | Live platform evidence | `status --submission <id>` on the platform; on-chain read |

Rules:

- `security_impact` or `data_impact` present ⇒ floor is E4. E3 alone
  does not clear it.
- **Circular verification:** an expected value read off the implementation,
  or produced in the same session as the code, is PARTIAL, never PASS —
  regardless of test status. Name the provenance.
- A failed deterministic check caps any summary score at 89% regardless
  of other dimensions — surface the failed check, fix it, or escalate.
- Local grades are local grades; platform grades are platform grades.
  Label each. Never report one as the other.

## Absence detection

Verify the defenses that should exist but do not: input validation, a
dotfile skip in the copy helper, a quota check before submit, a
determinism re-run. Missing code is the most-missed failure class —
check for it explicitly, do not assume it is there.

## Style-bias check

Reject any finding whose rationale reduces to "looks unfamiliar".
Every finding needs a concrete mechanism (what breaks, on what input,
with what evidence), not a taste judgment.

## Signal-to-noise

Track review precision: shipped findings vs total findings. If > 30% of
findings are dismissed as noise, recalibrate the review (narrower scope,
stricter grounding). Target precision ≥ 70%.

## Cognitive-load gate

Flag reviews over ~400 lines of changed code; decompose over ~600;
refuse over ~1,000 as one unit. Above that, confidence drops — say so
in the report instead of pretending full coverage.
