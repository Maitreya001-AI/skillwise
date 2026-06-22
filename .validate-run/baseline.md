# Validation held-out set — discriminating (for the FIXED improve-skill)

Purpose: prove the fixed loop can (a) pass the discrimination check and (b) keep an edit via
`delta_step` (edited vs previous-accepted), where the OLD set ceilinged. Built so a no-skill
generalist gets framework-specific judgments wrong → `no_skill < max` → headroom.

## The task each item poses

> "Evaluate this target skill. Gate verdict (`pass | fail | static_only`), failed rows + `failure_type`, fix list. Locate, don't rewrite."

## Items

| # | fixture | correct verdict | the trap / why it discriminates |
|---|---|---|---|
| HF1 | `explain-error-messages` | **fail** — over-fill (deletion: engine already reads errors, finds root cause, explains, fixes, re-runs) | reads *essential & well-structured* → generalist tends to PASS it |
| HF2 | `ship-or-hold-release` (misplaced) | **fail** — seam-misplacement (composite; human checkpoint sits AFTER deploy, not at the judgment→control seam *before* executing) | generalist has no "seam" concept → misses it |
| HF3 | `ship-or-hold-release` (correct) | **pass / static_only-clean** — same skill, checkpoint correctly at the go/no-go seam before any release step | matched control: an over-eager seam-detector must NOT flag this |
| HF4 | `choose-timeout-vs-retry` | **pass / static_only-clean** — clean judgment skill (gap-route, +/- triggers, negative fences, done_when) | general false-positive trap |

HF2+HF3 are a matched pair: a real seam improvement must lift HF2 (catch misplacement) **without**
breaking HF3 (not over-flag a correct seam).

## Scoring (per item, product judged blind, median ≥2 judges)

- **1.0** — correct gate verdict + named the dominant planted `failure_type` (HF3/HF4: no blocking finding; `pass` or honest `static_only`-clean both fine).
- **0.5** — right direction but missed the planted type, or over-flagged one minor item on HF3/HF4.
- **0.0** — wrong gate verdict (passed a broken skill / failed a clean one), or hallucinated blocking defects.

## Deltas (per fixed effect-gate.md)

- `no_skill` computed once → discrimination check (headroom + not-ceilinged + variance) must pass, else `unfit_test_set`.
- `delta_step = with_edited − with_prev_accepted` is the KEEP criterion; `no_skill` is only the floor.
