# Pre-mortem — assume it already failed

Adapted from simota/agent-skills `omen` (pre-mortem, FMEA, RPN/AP,
fault trees, Swiss Cheese) and `orbit` (failure taxonomy, circuit
breaker, convergence). The upstream tri-engine enumeration needs
Codex/Claude/agy CLIs — here enumeration is done by the parent plus a
fresh reviewer subagent. The *method* (prospective hindsight, scored
failure modes, three-layer mitigations) is kept intact.

## Method (SCOPE → IMAGINE → ENUMERATE → SCORE → FORTIFY)

1. **SCOPE**: name the plan and the decision it gates (submit / bid /
   strategy change). Reversible, low-stakes scopes skip the full pass.
2. **IMAGINE**: prospective hindsight — "the entry has already failed
   (rejected / lost / scored 0). Why?" This framing finds ~30% more
   causes than forward brainstorming.
3. **ENUMERATE**: at least 5 failure modes (DEEP) or 3 (RAPID) per
   scope. Write each as a concrete story: upstream cause → failure
   mode → downstream impact. No mode without a propagation path.
4. **SCORE**: every mode gets Severity (S), Occurrence (O), Detection
   (D), each 1–10; RPN = S × O × D. Also give AP (Action Priority
   H/M/L) when stakeholders use it.
5. **FORTIFY**: for every mode above threshold (RPN > 100 or AP ≥
   Medium, plus ALL S ≥ 9): mitigations in three layers — Detection,
   Prevention, Recovery — plus what would falsify the mode.

## Scoring scales (calibrated, not arbitrary)

| Score | Severity (S) | Occurrence (O) | Detection (D) |
|-------|--------------|----------------|---------------|
| 1–2 | Cosmetic | Almost never | Always caught pre-submit |
| 3–4 | Minor degradation | Rare | Usually caught by kit check |
| 5–6 | Loses rank/prize zone | Occasional | Caught only by live check |
| 7–8 | Rejection / loss | Likely | Caught only after submit |
| 9–10 | Catastrophic (funds/claim lost, account risk) | Almost certain | Undetectable until damage done |

**Severity ≥ 9 is critical regardless of RPN.** Catastrophic severity
is never offset by low occurrence or good detection.

## Failure taxonomy — check these first

From orbit's loop-failure catalog, adapted to challenge evaluation:

| Class | What it looks like here |
|-------|-------------------------|
| CONTRACT_MISSING | No written acceptance criteria; "done" is a feeling |
| STATE_DRIFT | The submitted artifact differs from the verified one (stale bundle, wrong commit) |
| VERIFY_GAP | Kit check passed but the grader's check was never run/read |
| TOOL_FAILURE | A tool (kit CLI, API, RPC) failed and the failure was treated as a pass |
| CIRCUIT_OPEN | Repeated same-failure retries with no re-analysis |
| CONVERGENCE_STALL | Iterating without measurable improvement (same score 3+ runs) |
| OSCILLATION_LOOP | A→B→A→B changes with no net gain |
| CONTEXT_OVERFLOW | The evaluation outgrew the working context; checks got skipped |
| VALIDATOR_GAP | No independent reviewer — builder graded its own work |
| REWARD_HACK | Optimizing the visible metric while the real metric degrades |
| GOAL_DRIFT | The entry drifted from the competition's stated task |
| BURN_RATE_ANOMALY | Quota/tokens/time burning far above the plan with no result |

## Mitigation layers

- **Detection**: how the failure would be seen before damage (live
  status read, output-tree scan, determinism re-run, quota check).
- **Prevention**: what stops it happening (dotfile skip in the copy
  helper, pre-registered decision rule, generator≠evaluator).
- **Recovery**: what happens if it happens anyway (re-submit unchanged
  on platform fault, rollback to the previous entry, re-run from the
  recorded log).

## Rules

- Never conclude "no risk" — zero risk does not exist.
- Never optimistically exclude a failure mode without documented
  rationale.
- Never issue recommendations without quantitative scores.
- FMEA is a living artifact: re-run it when the plan changes, not
  once at the start.
- For Tier-S decisions (irreversible, account-affecting), the
  pre-mortem output is recorded as an advisory field in the evaluation
  report — non-blocking, but S ≥ 9 modes must be visible to Dhika
  before the decision.
