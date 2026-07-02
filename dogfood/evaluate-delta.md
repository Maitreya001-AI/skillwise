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

Designed, not run. Until it runs, `evaluate-skill`'s row in [`STATUS.md`](./STATUS.md) stays `static_only` and the README claim stays qualified.
