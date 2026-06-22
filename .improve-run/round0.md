# Round 0 — baseline measurement (current `evaluate-skill` vs no-skill)

Gate: blind judges (2), median, condition hidden. Caveat: output schemas differ between
conditions (`VERDICT:` vs `GATE:`), so blindness is imperfect — judges were told to ignore
template and score substance only.

## Per-task (median of 2 judges)

| task | planted defect | no-skill baseline | with current skill |
|---|---|---|---|
| T1 | over-fill | 1.0 | 1.0 |
| T2 | wrong-layer + no-exit | 1.0 | 0.75 |
| T3 | wrong-route + under-fill | 1.0 | 0.75 |
| T4 | clean (FP trap) | 1.0 | 1.0 |
| **mean** | | **1.00** | **0.875** |

`delta = -0.125` · `regression_count = 2` (T2, T3) · `safety_regression = no` → **gate_pass = fail (negative transfer)**

## Two findings

1. **Baseline ceiling = 1.00.** The no-skill generalist (Opus) aces the set. No headroom →
   the effect gate cannot certify `delta > 0` for ANY skill version on this set. The set lacks
   discriminating power (the inverse of "weak tests": these are *too easy*).
2. **Defect (binding):** with-skill agents resolve the gate to `static_only` when blocking
   structural findings are present (T2/T3), where the correct resolution is `fail`. The rule
   "blocking structural finding → fail" is in `effect-gate.md` but not salient; agents default to
   `static_only` whenever Tier-2 can't run, misreporting a broken skill as merely unverified.

## Failure-driven signature (contrastive pair)

- success `W-T1`: blocking findings present → gate **fail** (correct).
- failures `W-T2`,`W-T3`: blocking findings present → gate **static_only** (wrong).
- signature: *a non-waived blocking structural finding forces `gate_pass = fail`; this overrides
  `static_only`, which is for a structurally-clean skill whose required effect layer didn't run.*

→ Round-1 edit targets this (NOT the Phase-A "blacklist" guess, which the data did not support).
