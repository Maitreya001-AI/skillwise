# Round 1 — REVERT (2026-07-03)

**Target defect** (from `../evaluate-delta-run/results.md`): form-check precision — `wrong-form` false positives on good skills; the §4 pricing clause doesn't transmit where applying it requires judgment.

## What ran

- **Candidates**: 3 mechanisms for the same defect (c1 default-deny rule gate / c2 three-question protocol / c3 contrast pair), each ≤30 lines, all lint-clean. Screened non-blind on the burned r2 set: c1 10/12, c2 9/12, c3 10/12; **c1 picked** over c3 (c3's exemplars near-verbatim describe the screening seeds — inflated by construction).
- **Snapshot** `7eca923` → applied c1 (+6/−1) → **authoritative improvement gate** on the fresh r3 working slice (18 authored seeds; **skill-11 excluded pre-registered** — my authoring bug: dangling `pii_fields.yaml` reference contaminated its label; n=17, resolution 0.059, adequate). Conditions: no-skill ×2, previous-accepted ×3 (band), edited ×2; sonnet judges, isolated, variant paths name-neutral.

## The numbers

| | run aggregates | per-seed-median aggregate |
|---|---|---|
| no-skill ×2 | 0.824 · 0.941 | 0.882 |
| previous-accepted ×3 | 0.882 · **1.0** · 0.941 | 0.941 (band = 2×SD = **0.118**) |
| edited (c1) ×2 | 0.941 · 0.941 | 0.941 |

`delta_step = 0.000` ≤ band; **median regressions vs previous: skill-02** (nogap costume judged "good" by one edited run — a *leniency* error, also a floor breach vs no-skill) **and skill-18** (overfill-order missed by one edited run). Ratchet first-match row: fatal → **REVERT** (`git checkout 7eca923 -- skills/evaluate-skill`). Improvements the edit *did* show (skill-04: median 0 → 1; skill-16: 1, ns 0.5) don't average away fatals — by design.

## Why the null delta (the diagnosis for round 2)

The reference arm produced **zero** wrong-form false positives on r3 — seeds 03/09 (the repair-class) were authored with their pricing **recited in-text**, which is exactly the condition where the old paragraph already works (the r2 finding). The working set never expressed the diagnosed defect, so the fix had nothing to show; meanwhile ordinary judge noise produced two 1-of-2 median regressions. Two prescriptions, logged in `dead-ends.md`:

1. **Fixture-harden for the question**: round 2 needs repair-class seeds whose pricing is *implicit* (requires judgment, not quotation) — otherwise the set is unfit for this defect and no candidate can land.
2. **Scope the next candidate tighter**: "burden of proof is on the finding" may induce leniency beyond `wrong-form` (the skill-02 miss was a leniency error). The next edit should gate only the wrong-form verdict sentence.

## Protocol notes

- With the tested condition at n=2, a single dip becomes a 0.5 median — the "reproduced" filter is weak exactly where the charter warns (§8-2); the gate still behaved correctly (default deny).
- Cost not instrumented (harness doesn't expose sub-agent tokens); `cost_delta = n/a` in `experiments.tsv`.
- Entry version's own thin sub-floor signal on skill-04 (median 0 vs ns 0.5) is consistent with the r2 verdict: evaluate-skill remains **in repair**; the r2 `fail` stands.

**State after round 1**: tree reverted to entry; no KEEP; confirmation slice (skill-19..24) untouched and its labels still outside the repo. Loop paused (round cap 10 far away) — resume by authoring defect-expressing fixtures first.
