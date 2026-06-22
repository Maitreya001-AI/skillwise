# Validation of the fixed improve-skill

Goal: prove the fixed loop (a) no longer fakes "done" on an unmeasurable set, and (b) keeps an
edit via `delta_step` where the old `delta_exist` gate could not.

## Re-run on a deliberately harder, discriminating set (4 fixtures)

Sealed isolated agents (no tools); blind scoring. Built so a no-skill generalist *should* miss
framework-specific judgments (over-fill-that-reads-essential, composite seam-misplacement, a matched
correct-seam control, a clean judgment skill).

| fixture | correct | no-skill (Opus) | with current evaluate-skill |
|---|---|---|---|
| HF1 over-fill-reads-essential | fail | **fail** (caught over-fill + scope creep) | fail |
| HF2 seam **misplaced** | fail | **fail** ("post-mortem, not a gate") | fail |
| HF3 seam **correct** | pass | pass | static_only-clean (no over-flag) |
| HF4 clean judgment | pass | pass | pass |
| **mean** | | **1.00** | **1.00** |

**Finding:** a frontier base model is already an expert skill-reviewer — it caught over-fill *and*
seam-misplacement from first principles, with no framework vocabulary. So evaluate-skill has **no
measurable headroom** against this model: both no-skill and with-skill ceiling at 1.00.

## What the re-run validated

1. **Fix C (honest terminal state).** The correct verdict here is `already_optimal` (current skill
   maxed on every task), NOT a faked "done, barely changed." The fixed loop names it.
2. **Fix B was wrong as written — and the dogfood caught it.** My first cut gated discrimination on
   "`no_skill` not at ceiling." But that is the *existence* question's concern. The improvement loop
   only needs the **current skill** to have headroom. Under the buggy check, the *original*
   evaluate-skill run (no_skill=1.0 but current skill=0.875) would have been wrongly rejected as
   `unfit_test_set` — yet it produced a real KEEP. **Corrected:** headroom keys on the current skill
   (below max, or below no-skill); no-skill is only the floor and may sit at ceiling.

## The KEEP demonstration (Fix A), on real measured data

The original evaluate-skill run is the pure case the fix unlocks — `delta_exist = 0` (ceiling) but a
genuine improvement vs the previous version:

| | no_skill | r0 (current) | r1 (edited) |
|---|---|---|---|
| mean | 1.00 | 0.875 | 1.00 |
| `delta_exist` (vs no-skill) | — | −0.125 | **0.00** |
| `delta_step` (vs previous) | — | — | **+0.125** |

- **Old gate** (`delta_exist > 0`): r1 fails → no KEEP possible (ceiling) → "changed nothing." This
  was the bug.
- **New gate** (`delta_step > noise`, floor intact, no per-task regression): r1 KEEPS cleanly →
  terminal `improved (+0.125)`. No hand-waving. Corrected headroom check confirms the set was *fit*
  (current skill below max + negative transfer to repair).

## Conclusion

The fix is correct and self-corrected once under its own dogfood. On the specific target the user
asked about (evaluate-skill), the honest result against a frontier model is `already_optimal` — there
is no headroom to improve its *measured effect*, which is exactly the truth the old loop hid behind a
2-line non-change. A fresh live KEEP on a target with genuine current-skill headroom can be run on
request.
