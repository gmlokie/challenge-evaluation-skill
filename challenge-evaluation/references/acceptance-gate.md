# Acceptance gate — checklist, reason codes, self-checks

Adapted from BaseIntelligence/agent-challenge `.rules/acceptance.md`,
`.rules/anti-cheat.md`, `.rules/hardcoding.md`, `.rules/security.md`
(studied 2026-11-16). The upstream policies gate SWE-agent submissions
on a TEE benchmark; this file keeps the *method* — evidence-based
acceptance with reason codes — and rewrites the *targets* for this
workspace's competitions (make.fun entries, POIDH claims, Synmerco bids,
AgentPit strategies, free mints). The upstream production path (Phala TDX
CVMs, paid cloud, baseagent runtime) is NOT adopted.

## The checklist (all must pass for CERTIFIED)

| # | Check | Evidence that passes it |
|---|-------|-------------------------|
| 1 | Behavior implemented, not described | The capability exists in source files; a diff shows it |
| 2 | Targeted checks pass on the EXACT artifact the grader sees | Kit check / bundle contents / output tree, fresh run, exit 0 — never the repo tree alone |
| 3 | Solves generally (see anti-cheat below) | Works on fresh draws / unseen inputs, not only the visible cases |
| 4 | Packaging / imports / entry points valid | Build passes; new files in the paths the task expects |
| 5 | Deterministic + reproducible from clean checkout | Same inputs → same outputs, run twice |
| 6 | No security violation (see security below) | No secret material, no exfiltration, no sandbox escape |
| 7 | Every requirement met, with evidence per item | Requirement checklist from precision-task-optimizer §2, each item cited |

## Reason codes (use these verbatim in the verdict)

| Code | Meaning | Example in this workspace |
|------|---------|---------------------------|
| `reads_hidden_tests` | Reads/inspects grading internals to match the expected result | Reading kit internals or the grader's hidden checks to hardcode the pass |
| `tailors_to_tests` | Static / test-specific output that satisfies visible checks without solving generally | Tuning only to the kit check while the entry fails fresh draws |
| `branches_on_task_identity` | Behavior changes by task id, test name, fixture, directory, or host | Special-casing one competition slug instead of solving the task |
| `partial_or_stub` | Partially implemented, stubbed, or left as TODO | A feature named in the dossier but not in the code |
| `tests_weakened` | Tests removed, weakened, skipped, or changed to hide a failure | Dropping a failing case from the local grade instead of fixing it |
| `unreproducible` | Depends on manual steps, local paths, unpublished services, files outside the workspace | An entry that only builds on one machine |
| `claims_without_evidence` | Claims completion without matching code, tests, logs, or artifacts | "Should pass" with no fresh run |
| `secret_material` | Embeds, requests, or forwards credentials / keys / tokens | An API key pasted into the entry or a log |
| `output_not_plain` | Output tree holds a non-plain relative name (dotfile, symlink, absolute path) | `screenshots/.gitkeep` copied into /output — the best-game-01 rounds 1–3 failure |

## Anti-cheat self-check (run before every submit)

Ask, with evidence, not vibes:

- Did any part of the build read the grading harness, hidden tests, or
  kit internals to discover the expected result? If yes → REJECTED.
- Does the entry produce static or pre-baked output that only satisfies
  the visible checks? If yes → REJECTED (`tailors_to_tests`).
- Does any branch key on task identity (slug, test name, directory,
  host)? If yes → REJECTED (`branches_on_task_identity`).
- Would the entry still pass on unseen inputs? If untested → run fresh
  draws first; "probably" is not evidence.

Evidence standard: flag cheating/hardcoding only when code, config, or
artifacts show a concrete shortcut. Prefer SUSPICIOUS over REJECTED when
a read or branch is plausibly benign and there is no direct proof of
intent. Never reject only because a solution is small or uses constants:
constants documenting stable behavior, public protocol values, or
task-requested configuration are fine, and heuristics are fine when
explained by the task domain and validated on more than one input shape.

## Security self-check

Prohibited in any entry: exfiltrating secrets, tokens, keys, cookies,
env vars, or private files; embedding or requesting credential material;
disabling sandboxing or escaping containers; hidden network callbacks or
telemetry; credential prompts or phishing flows; destructive filesystem
behavior outside the workspace; weakening auth, signatures, or auditability
without a direct task requirement. Security findings must cite observable
code, config, command output, or file behavior. If evidence is
incomplete, mark the finding uncertain instead of overstating it.

## Verdict rules

- CERTIFIED: all 7 checklist items pass on fresh evidence.
- CONDITIONAL: all blocking items pass; only named, owned, non-blocking
  gaps remain — list them in the report.
- REJECTED: any blocking item fails, or any `reads_hidden_tests` /
  `tailors_to_tests` / `branches_on_task_identity` / `secret_material`
  finding is confirmed.
- A timed-out evaluation is terminal, score 0, counted once — it is not
  "inconclusive, retry silently".
- Only a CERTIFIED or CONDITIONAL verdict authorizes a submit. A REJECTED
  verdict means fix and re-run the gate; routing around the gate is
  forbidden.
