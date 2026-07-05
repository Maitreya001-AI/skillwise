# wise-eval — evaluate-skill · existence gate · **pass (certifying)** · 2026-07-06

**Verdict.** `evaluate-skill` beats the no-skill baseline beyond the noise band on a 29-seed
held-out set with zero reproduced per-task regressions:

| | value |
|---|---|
| no-skill pass rate (medians, ×3 runs) | 0.724 |
| with-skill pass rate (medians, ×3 runs) | 0.828 |
| `delta_exist` | **+0.103** |
| `noise_band_exist` (2×SD of 3 no-skill aggregates) | 0.080 |
| reproduced regressions / floor breaches | **0** |
| power | n=29, resolution 0.034, adequate → **certifying** |

**Scope (read before quoting).** Existence branch; the dogfood r3/r4 29-seed working set under
the **pre-registered behavioral label key** (labels established by actually running unaided
engines — `dogfood/improve-run-evaluate-skill/behavioral-labels.md`); consumer engine =
claude-sonnet judges in isolated, name-blind contexts. Cost is not instrumented (standing debt)
— the inertia-cost fatal is structurally inapplicable here because the delta clears the band.
The 2026-07-03 r2 run's `fail` (12-seed set, by-construction labels) remains on record; this run
is the current best-grounded reading, not an erasure of that one.

**Where the value comes from** (per-task medians): the entire delta is the wrong-form class —
unaided judges reliably miss all three silent-drop-pipeline seeds and the skill flips every one
of them (08/15/16: 0 → 1). That is precisely the text-checkable failure class THEORY §7 predicts
a static method *can* transmit — the r2 run observed the same asymmetry from the losing side.
Both arms are matched (at 0) on the decoy-boundary conventions (02/05/17/24) and the
narrative-justified order (29); the skill never falls below the baseline on any task.

**Advisory fix list** (no blocking findings): (1) decoy-boundary conventions (behaviorally-nogap
seeds 02/05/17) sit at 0 for both arms — headroom that five prompt-layer repair mechanisms could
not claim (all mechanically REVERTed; see `dead-ends.md`); the next viable form is an
orchestrator-run deletion probe that does not compete with the judge's read. (2) wrong-form ↔
no-exit token confusion on silent-drop seeds. (3) plausible-narrative order acquittals.

Full machine object: `wise-eval.json`. Run trail: `dogfood/improve-run-evaluate-skill/`
(rounds 1–5, behavioral labeling, all run JSONs).
