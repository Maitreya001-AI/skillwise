# evaluate-delta — the kernel's L2 experiment (design)

**Question.** Does `evaluate-skill` actually improve verdicts about skills — a `delta_exist` beyond the noise band, *for the evaluator itself*? Reading the evaluator and nodding is L1; this is the only experiment that can certify the kernel (`docs/THEORY.md` §7: certification lives at L2 alone).

## Design — with vs without, ground truth from implantation

**Seed set.** N known-good skills (independently vetted, in real use) + N deliberately broken skills, each seeded with **exactly one of the six §6 failure types** — `nogap`, `underfill`, `overfill-order`, `overfill-cost`, `wrong-form`, `no-exit` (optionally also `wrong-route` / `seam-misplacement` from the scorecards). The implantation record *is* the ground-truth label; no judge ever labels the truth. N ≥ 6 per arm, to clear the gate's own power floor (`n_tasks ≥ 6`).

**Two isolated review arms.**
- **Arm A (with):** judges with `evaluate-skill` loaded.
- **Arm B (without):** same base engine, same prompt frame, no skill.

Judges decorrelated per §7 (different base models, or information-isolated contexts); neither arm sees the labels, the other arm's output, or which arm it is in.

**Scoring.** A verdict on a seed skill is correct iff it (a) classifies good/broken correctly and (b) for a broken skill, names the implanted `failure_type`. Per-arm accuracy over the seed set; `delta_exist = acc_with − acc_without`; `noise_band_exist` from **3 fixed re-runs of the no-skill arm** (the gate's §8-1 estimator, `2 × sample SD`). Per-seed scores are medians across re-runs (§8-2).

**Gate.** Read the result through the shared gate's **existence branch** (`shared/effect-gate.md`), fatals included — notably the **inertia-cost fatal**: record `tokens` for both arms; the evaluator must survive its own §6 inertia-cost test (`cost_ratio ≤ 1.5`, or a delta that clears the band).

## The suspended empirical question this settles on the side

Whether a **compiled exit verifier** produces a behavioral difference over prose criteria — the question THEORY §4 prices but leaves empirically open. Tag each broken seed by whether its implanted failure is text-checkable (`wrong-form`, `no-exit`, shuffle's structural half) or L2-native (`nogap`, `underfill`, `overfill-cost`); compare per-class deltas. A with-skill gain concentrated in the text-checkable class and absent in the L2-native class would say the static read predicts only what it can see — exactly what §7 claims.

## Status

**Run — twice, 2026-07-03** (full trace in [`evaluate-delta-run/`](./evaluate-delta-run/), writeup in [`evaluate-delta-run/results.md`](./evaluate-delta-run/results.md)):

- **Round 1** (plainly-written defects, `seed-skills/`): `unfit_test_set` — `no_skill` at ceiling (an unaided sonnet judge aces blatant implants); hardened per the gate's routing.
- **Round 2** (theory-boundary decoys, `seed-skills-r2/`): **`fail` — reproduced negative transfer** (`delta_exist −0.042`; the skill lifts broken-skill detection +0.17 but drops good-skill preservation 1.00 → 0.75; cleanest regression: both with-skill runs mislabeled an honestly-priced prose-rules skill as `wrong-form`). The gap is real (`no_skill` 0.75), so per the sub-floor routing this goes to `improve-skill` — first repair target: the form check must carry its own §4 pricing discipline instead of relying on a nearby paragraph.

The side question came back too: the with-skill gain concentrates in exactly what a static read can see, and the loss concentrates where applying the method needs judgment — §7's claim, observed behaviorally.
