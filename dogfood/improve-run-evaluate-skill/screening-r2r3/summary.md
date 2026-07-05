# Round-2 candidate screening (burned r2 set, 12 seeds, 1 cheap non-blind pass each; sonnet)

Two candidate families, one per diagnosed mechanism; the c-family was screened first, then
Phase-B calibration (23-seed) showed its target defect does not express on the authoritative
set — recorded here, not selected. The d-family targets the calibration-confirmed defect
(decoy leniency: self-justifying rhetoric accepted as evidence).

| candidate | mechanism (all ≤30 changed lines, lint-clean) | score | misses |
|---|---|---|---|
| c4 | wrong-form verdict gated by two priced questions | 10/12 | 02 (FP persists), 03 (decoy) |
| c5 | wrong-form decision table (first match wins) | 10/12 | 03 (decoy), 05 |
| c6 | negative fences appended to pricing paragraph | 10/12 | 02 (FP persists), 03 (decoy) |
| **d1** | **"self-description is a claim, never evidence" — fake-specificity + fake-dependency rules, FP-guard clause** | **12/12** | — |
| d2 | decoy table inside deletion/shuffle tests | 9/12 | 03, 05, 12 |
| d3 | minimal-contrast mental ablation before passing a suspect | 10/12 | 03, 05 |

**Selected: d1** — the only candidate to fix both directions on r2 (preserved the unrecited SQL/warehouse
bar good seeds AND caught the fake-specificity nogap decoy) while keeping full recall on the
true brokens. Note the c-family's uniform failure on skill-03 (the decoy class) corroborates the
Phase-B re-diagnosis. Screening is a selection heuristic only; KEEP/REVERT belongs to the
authoritative 29-seed improvement gate (per-task medians, band, floor).
