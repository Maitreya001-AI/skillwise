# Round 1 — edit + re-score (KEEP)

**Edit (≤30 lines, one defect):** added a *resolution-precedence* block to `## Converge to one gate`
in `skills/evaluate-skill/SKILL.md`:
> (1) any non-waived blocking structural finding → `fail`, regardless of whether the effect layer
> ran; (2) else effect-layer fatal → `fail`; (3) else effect required-but-unrun → `static_only`;
> (4) else `pass`. `static_only` is ONLY for a structurally-clean skill whose effect layer didn't run.

## Re-score (same held-out set, same 2 blind judges, median)

| task | r0 with-skill | r1 with-skill | what changed |
|---|---|---|---|
| T1 | 1.0 | 1.0 | stayed `fail` (cited precedence (1)) |
| T2 | 0.75 | 1.0 | **`static_only` → `fail`** ("not static_only because structurally broken") |
| T3 | 0.75 | 1.0 | **`static_only` → `fail`** (same) |
| T4 | 1.0 | 1.0 | self-corrected `pass` → `static_only`-clean (precedence stopped the over-claim) |
| **mean** | **0.875** | **1.00** | |

- baseline (fixed, no-skill) = 1.00
- `delta = with − baseline = 0.00` · `regression_count = 0` · `safety_regression = no`
- vs the previous skill state: with-skill **+0.125**, regressions **2 → 0**, both judges now unanimous.

## Decision: KEEP

The strict effect-gate `pass` needs `delta > 0`, which is **unreachable on this set** (baseline
ceilings at 1.00). So this is not a delta-gain KEEP. It is a **negative-transfer repair**: the
shipped skill (r0) scored *below* no-skill (0.875 < 1.00) — the gate's one non-waivable fatal —
and the edit removes it (r1 ties at 1.00) with no new harm. improve-skill's `done_when`: "a version
carrying negative transfer never counts as done — fall back to the last clean KEEP." r0 carried it;
r1 does not → r1 is the clean KEEP.

## Why the loop stops here (plateau at ceiling, no plateau-break)

with-skill is at the test's ceiling (1.00); no edit can raise it further on this set, and a
plateau-break (bigger rewrite) cannot beat a ceiling that lives in the *test*, not the skill — it
could only risk regression. To certify **positive** transfer (delta > 0), the held-out set must be
hardened with cases a strong generalist gets wrong unaided (e.g. seam-misplacement that reads fine;
an over-fill skill that looks essential; a case whose correct verdict is `static_only` where a
generalist would say `pass`). That is the recommended next run, with a fresh set.

## Side finding (about the framework, not this edit)

The framework has an internal edge-case inconsistency this run exposed: `effect-gate.md` defines
`pass` as `delta > 0`, but `ratchet-protocol.md` has a "`delta == 0` → KEEP (lateral rebalance)" row
that presupposes `gate_pass == pass`. On a ceilinged set these can't both hold. Worth reconciling in
the skillwise repo itself (separate from this evaluate-skill edit).
