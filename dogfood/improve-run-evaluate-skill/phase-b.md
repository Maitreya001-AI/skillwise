# Phase B — harness

- Target: skills/evaluate-skill (composite: Judgment + Capability; production tier).
- Entry state (Phase A): existence gate FAIL on r2 hardened set — reproduced negative transfer
  (see dogfood/evaluate-delta-run/results.md). Sub-floor routing: gap real -> negative transfer
  is the first repair target. Diagnosed single weakest defect: **form-check precision** — the
  §4 pricing clause does not transmit; carriers emit wrong-form on good skills (r2: skill-02
  both runs, skill-06 one run).
- Held-out set: dogfood/seed-skills-r3 (24 fresh seeds authored for this loop; never used for
  diagnosis). Working slice: skill-01..18 (9 good / 9 broken). **Confirmation slice: skill-19..24
  (3 good / 3 broken), invisible to all rounds** — read only at the terminal check.
- Power (working slice): n_tasks=18, resolution=0.056, adequate=true (>=6).
- Screening substrate: dogfood/seed-skills-r2 (burned by diagnosis; never authoritative again).
- Conditions on the working slice: no_skill 2x (floor, per-task medians); previous-accepted 3x
  (reference — band = 2 x SD of the 3 aggregates); edited 2x. Judges: sonnet, fresh isolated
  contexts, variant paths name-neutral (variants/a = previous-accepted, variants/b = edited);
  no judge is told which variant is which or that an improvement loop is running.
- Round cap: 10 (default). Bounded step: <=30 changed lines inside skills/evaluate-skill/.
- Cost: sub-agent token counts not exposed by the harness -> cost_delta recorded as n/a (advisory).

## Amendment 3 (logged 2026-07-06, after the Amendment-2 calibration runs, BEFORE any candidate was gated)

**Calibration verdict on the 23-seed slice: `unfit_test_set` for the improvement question — halt and harden (gate rule, §8-3).**
The Amendment-2 conditions ran as declared (no-skill ×2; previous-accepted ×3 fresh). Three findings, recorded before any edit was applied or screened against this set:

1. **The r2-diagnosed defect does not express here.** Zero `wrong-form` false positives on the four implicit repair-class seeds (25–28) across all three reference runs (12/12 preserved). The r2 negative transfer appears narrower than diagnosed: its expression class is "mechanically-checkable-*looking* rule grammars" (r2's skill-02 was an org SQL bar), not prose-rules-with-manual-exit in general — tone/register/email/visual seeds do not bait the FP.
2. **The live defect on this set is the leniency face**: reference per-seed medians fall below the no-skill floor on task-02 (nogap in team costume) and task-23 (welded march with fake-dependency rhetoric) — the same two failure shapes as round-1's REVERT fatals.
3. **Structural unfitness**: reference run aggregates 0.957 / 0.826 / 0.913 → noise band 0.133, while the max showable `delta_step` (2 headroom tasks / 23) is 0.087 — no candidate can mathematically KEEP. Same shape as the r2 run's limitation #3.

**Hardening (this amendment):** six seeds added to `seed-skills-r4/` — skill-31/32 (broken, nogap in org costume: generic Python error-handling / REST pagination wisdom in team dress), skill-33/34 (broken, overfill-order with fake-dependency rhetoric: "the discipline is the sequence" / "visual thinking contaminates query thinking"), skill-35/36 (good, the *actual* r2 FP-expression class: SQL review bar / Terraform naming grammar — mechanically-checkable-looking, implicit pricing, manual review exit, no guarantee claim). Working slice: **29 seeds (14 good / 15 broken)**, resolution 0.0345, adequate. Confirmation slice untouched. All conditions re-run fresh on the 29-seed slice (no-skill ×2, previous-accepted ×3, edited ×3); the 23-seed calibration runs are archived as `calibration-23/`, not authoritative. Round-2 diagnosis updates to the **decoy-leniency mechanism** (self-justifying rhetoric accepted as evidence); the wrong-form-FP scoped candidates (c4/c5/c6, screened on burned r2) are recorded but not selected — their target does not express on the authoritative set.

## Amendment 2 (logged 2026-07-06, BEFORE any round-2 run)

**Working set hardened for the diagnosed defect (per round-1's prescription in dead-ends.md).**
Round 1 established the r3 working slice never expresses the wrong-form-FP defect: its
repair-class seeds (03, 09) recite their §4 pricing in-text. Per the gate ("the remedy is
harder or more numerous fixtures"), six fresh seeds were authored into `dogfood/seed-skills-r4/`:

- skill-25..28 — **good, repair-class, implicit pricing**: prose rules + honest manual exit
  where the *context* (human-read artifact, loud cheap failure, or an honestly-manual visual
  dimension) makes declarative form rational, but the justification is never recited in-text.
  Judging them correctly requires applying the pricing clause, not quoting the seed.
- skill-29..30 — **broken, wrong-form with a guarantee claim**: machine-parsed downstream,
  silent drops, scale, a claimed guarantee their prose form cannot deliver, no
  validator/builder. These punish the leniency direction round-1's c1 died on.

Working slice for round 2: r3 {01..10, 12..18} + r4 {25..30} = **23 seeds (12 good / 11 broken)**;
power: n_tasks=23, resolution=0.0435, adequate. Confirmation slice unchanged (r3 skill-19..24,
still untouched, labels still outside the repo). For the runs, seeds are copied to a session
workspace under neutral names task-01..task-23 (interleaved mapping, recorded) so the r4
additions are not identifiable as a block; labels-r4 stay outside the repo until runs complete.
All conditions re-run fresh on the 23-seed slice this round: no-skill ×2, previous-accepted
(= entry version @HEAD, round 1 reverted) ×3, edited ×3 — the tested condition moves to 3 runs
per round-1's protocol note on the weak n=2 median filter.

## Amendment (logged 2026-07-03, after gate run ns-2 arrived, BEFORE any a/b result)

**skill-11 excluded from scoring (working n: 18 -> 17; resolution 0.0588, still adequate).**
Reason: seed-authoring error — its SKILL.md references `scripts/pii_fields.yaml`, which was
never created. The dangling reference is an objective, judgment-free defect (file existence),
so the seed's ground-truth label ("good") is contaminated: careful judges who check the
reference are penalized by the label, careless ones rewarded. Exclusion applies identically
to all conditions (ns / a / b). Decision recorded before any variant-arm result was received.

## Amendment 4 (logged 2026-07-06, after Phase-A behavioral labeling, BEFORE any round-5 run)

**Scoring key for round 5 onward: `labels-behavioral.json`** (working set) and
`labels-r2-behavioral.json` (screening substrate) — six labels overturned by the pre-registered
behavioral procedure in `behavioral-labels.md` (task-03/14/24 and r2 skill-03 → good;
task-05/17 → broken/nogap). Stored reference (a-1..3) and floor (ns-1..2) runs are re-scored
under the new key without re-running (verdicts are data; the key was wrong): reference
aggregates 0.828 · 0.828 · 0.793 → band 0.0398, median aggregate 0.828; no-skill median
aggregate 0.724; reproducibly-failed reference tasks {02, 05, 17, 24, 29} → max showable
delta_step 0.172. Headroom/power: fit. All four prior REVERTs stand under the new key (their
deciding fatals were on labels the procedure confirmed). Round 5 proceeds as the sanctioned
**plateau-break** (4 rounds, no KEEP): one larger rewrite — `scripts/deletion_probe.py` as a
compiled Capability primitive plus SKILL.md wiring — branch first, gate fatals unchanged.
