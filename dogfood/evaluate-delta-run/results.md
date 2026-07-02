# evaluate-delta — first execution (2026-07-03)

Two rounds. Engine under measurement: **claude-sonnet** judges in fresh, information-isolated contexts (labels never in the repo during runs; judges barred from reading anything but the seed folders — plus, in Arm A only, `skills/evaluate-skill/`). Both arms received the identical prompt frame including one-line glosses of the six `failure_type` options (the *answer format*); Arm A additionally loaded and applied `evaluate-skill`. Scoring is mechanical (`score.py` vs implantation labels): a verdict is correct iff good/broken matches, and for broken seeds the `primary_defect` token matches exactly.

## Round 1 — `unfit_test_set` (no_skill at ceiling)

Seed set: `../seed-skills/` (6 good + 6 broken, one §6 failure each, written *plainly*). Labels: `labels.json`, report: `round1-report.json`.

- no-skill run accuracies: **1.0, 1.0, 0.917** → per-seed medians all 1.0 → `no_skill` at ceiling.
- `delta_exist = 0.0`, `noise_band_exist = 0.096`, regressions 0.
- **Gate: `unfit_test_set`** — the set cannot show existence value; per the gate, harden and re-run, conclude nothing about the skill. (The implanted defects were too blatant: an unaided mid-tier judge with the answer sheet aces them.)

## Round 2 — hardened set → **`fail` (reproduced negative transfer)**

Seed set: `../seed-skills-r2/` — discrimination moved onto the theory's *distinctive* content: goods that look broken (external-mandate order; explicitly **priced** declarative form; heavy protocol priced by irreversibility; thin-but-complete + compiled verifier) and brokens that look good (fake-specificity `nogap`; one buried improvisation point; fake-dependency rhetoric; unpriced cost; a **fake verifier**; an aspirational "Quality" section that checks nothing). Labels: `labels-r2.json`, report: `round2-report.json`.

| | run accuracies | aggregate (per-seed medians) |
|---|---|---|
| Arm B (no skill) ×3 | 0.75 · **1.0** · 0.75 | **0.75** |
| Arm A (with evaluate-skill) ×2 | 0.833 · 0.583 | **0.708** |

- `delta_exist = −0.042` · `noise_band_exist = 0.289` · power `{n_tasks: 12, resolution: 0.083, adequate: true}`
- `regression_count = 3` (per-seed medians): `skill-02`, `skill-06`, `skill-07`
- **Resolution order → `fail` at step 4 (reproduced negative transfer), before any band or headroom question.**

### Where the delta lives (the side question, answered)

| slice | no skill | with skill | Δ |
|---|---|---|---|
| broken, text-checkable failures (overfill-order / wrong-form / no-exit) | 0.667 | 0.833 | **+0.17** |
| broken, L2-native failures (nogap / underfill / overfill-cost) | 0.333 | 0.50 | **+0.17** |
| **good-skill preservation** (n=6) | **1.00** | **0.75** | **−0.25** |

The skill *does* transmit detection ability: Arm A was the only condition to reliably catch the disguised `no-exit` (skill-12: B median 0, A median 1) and it half-caught the buried `underfill` (skill-05). All of the damage is concentrated on **good skills**: the method makes its carrier trigger-happy.

### The reproduced failure, precisely

- **skill-02** (good: org SQL review bar, honest manual exit, no machine-guarantee claim) — **both** Arm A runs judged it `wrong-form` ("mechanically checkable rules left as prose, no linter"). The evaluate-skill text contains exactly the clause that forbids this ("price the trade-off before writing the finding … word as an unpriced trade-off, not a defect, unless the skill claims a guarantee its form cannot deliver") — and it transmitted only where the seed *recited* it (skill-04, which both A runs correctly passed) and failed where applying it required judgment. A fully reproduced negative transfer.
- **skill-06 / skill-07** (1-of-2 A runs each): the same over-eager form check fired on the irreversibility-priced deletion protocol, and one A run traded a correct `overfill-order` for `nogap`. With only 2 with-skill runs, the median filter is weak (see limitations); skill-02 alone is enough for the fatal.

### Routing (the gate's own sub-floor rule, applied to ourselves)

`no_skill` does **not** pass the typical tasks (0.75 — unaided judges miss buried underfill, disguised no-exit, and fake-specificity nogap): **the gap evaluate-skill targets is real.** `with_skill < no_skill` → **negative transfer, not `nogap`**: route to `improve-skill`, first repair target named by the contrastive evidence — *the form check ships without its own pricing discipline welded in; the trade-off clause must become part of the check (e.g. "before emitting `wrong-form`, verify the skill claims a machine guarantee its form cannot deliver; an honest manual exit on low-stakes rules is at most an advisory compile-candidate, mirroring the linter's non-blocking `form.hint`"), not a paragraph nearby.* Retirement is not the routing — and this run is itself the evidence for why the two must not be conflated.

## Limitations (read before quoting the numbers)

1. **Cost not instrumented.** The sub-agent harness didn't expose per-run token counts, so `cost_ratio` and the inertia-cost fatal were not evaluated. Qualitative: Arm A reads ~9k extra words per run; the verdict (`fail`) is unaffected (it fires earlier in the resolution order).
2. **Arm A ran 2×** (the gate's minimum). At n=2 the "reproduced" filter is weak for the 0.5-median seeds; only skill-02 (0-of-2) is a fully reproduced regression. A repair-then-remeasure should run the tested condition 3×.
3. **Reference variance is huge** (one lucky 12/12 run): `noise_band_exist` (0.289) exceeds the maximum showable delta on this set (0.25) — *even a perfect skill could not have passed round 2*. Any future certifying attempt needs a larger set (≥24 seeds) to stabilize run accuracies. The `fail` is untouched by this (fatals precede the band in the resolution order), but a future `pass` claim on a 12-seed set would be structurally impossible.
4. **Label provenance.** Labels are by-construction (implantation records), but the boundary-case labels (02, 04, 06) encode the theory author's reading of §4's pricing clause. The two decoy labels that Arm A got right (04) and wrong (02, 06) differ exactly in whether the pricing was recited in the seed — which is itself the finding.
5. Engine = sonnet. The result certifies (negatively) *for that consumer engine*; a stronger engine may need the skill less and be damaged by it less — or more.

## Verdict line for STATUS.md

> evaluate-skill · existence gate · hardened 12-seed set · sonnet judges: **fail — reproduced negative transfer** (`delta_exist −0.042`, 3 regressions, cleanest: skill-02). Gap confirmed real (no-skill 0.75). Routed to improve-skill; repair target: weld the §4 pricing discipline into the form check.
