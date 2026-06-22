---
name: improve-skill
description: Iteratively improve an existing skill so it gets monotonically better without degrading or drifting. Use this when a skill isn't triggering, is over-engineered, produces weak output, or fails on some cases, or when asked to make a skill better, optimize it, or evolve it from failure traces. Also use it to push a draft from "runs" to "ships". This runs a propose-test-accept loop where every edit must beat the skill's own previous version (and never fall below a no-skill floor) before it lands; it does not freely rewrite. Use seek-skill instead to create a brand-new skill from a corpus.
license: MIT
---

# Improve a Skill

This is a **control** skill (composite: control + judgment + capability): a gap-classification front-end in front of a ratchet-and-gate loop. The derivation is in the skillwise repo's `docs/THEORY.md` (§5, §8). On first activation also read `references/rubric.md` (the *diagnosis* rubric — which dimension is weakest), `references/ratchet-protocol.md`, and `references/failure-driven.md`.

The keep/revert decision is **not** re-implemented here. Every edit is judged by the **shared measurement gate** in `../../shared/effect-gate.md` — but on its **improvement gate** (`delta_step`: the edited version vs the last accepted version), *not* the **existence gate** `evaluate-skill` uses (`delta_exist`: vs no-skill). These are different questions: `evaluate-skill` asks *should this skill exist?*; `improve-skill` asks *did this edit make it better?* Conflating them is the failure that makes "improve" change nothing — when the base model is already strong, no-skill ceilings and *no* version can beat it, so a loop keyed on `delta_exist` rejects every edit. The no-skill score stays a **floor/guard**, never the bar each round must clear.

> **A theory refinement this skill embodies.** A control skill leaves *task* iteration to the engine, but the **gate protocol must be concrete and non-skippable** — the failure being prevented is the engine skipping its own gate. The loop below is a *measurement protocol* (change → measure → keep/revert): its order is epistemic, the legitimate exception to the shuffle test.

## Phase A — Classify the target

Name the gap the target fills (Knowledge / Capability / Judgment / Control / composite) and its **tier** (scaffold vs production/library — this decides whether the effect layer is mandatory; see `effect-gate.md`). Classification selects the type-aware diagnosis weighting in `references/rubric.md`: workflow-clarity is N/A for Knowledge/Judgment skills; executable-specificity relaxes for Judgment. Run `evaluate-skill` once as the **entry check**: the existence floor (`delta_exist` vs no-skill) and the current structural findings. If the skill already loses to no-skill, that negative transfer is the first thing to fix; if it is already strong, that is fine — improvement is still measured each round against the skill's *own previous version*, not the floor.

## Phase B — Set up the harness

- Confirm the target holds a `SKILL.md` and the git tree is clean (the ratchet reverts via `git checkout`).
- Create a working dir with rolling memory: `learnings.md` (verified wins) and `dead-ends.md` (falsified edits, never retried).
- **Assemble the held-out set per `../../shared/effect-gate.md`**: caller-supplied tasks, or draft 3 happy-path + 1 edge into `baseline.md` and confirm with the user before scoring.
- **Calibrate the set for discrimination (mandatory, before any round).** Compute the once-only `no_skill` baseline *and* the current skill's scores, and run the gate's **discrimination check**: headroom (some task below max for the current skill), `no_skill` not at ceiling, and variance across tasks. If the set ceilings → `unfit_test_set`: **halt and harden the fixtures** (cases the base model gets wrong unaided) before iterating. Weak tests inflate everything; **ceilinged tests hide every gain** — a set where no-skill already maxes out cannot show improvement, and running the loop on it is exactly the failure that makes "improve" change nothing.

## Phase C — The loop

Each round is propose candidates → pick the best vs the current version → independent re-score through the gate's **improvement** gate → forced keep/revert.

1. **Diagnose** the single weakest dimension via `references/rubric.md`. If you have execution traces with outcome labels, switch the diagnosis source to failure-driven mode (`references/failure-driven.md`): pair each failure with a neighboring success and extract the missing-behavior signature. Read `learnings.md` + `dead-ends.md` first; never re-walk a falsified edit. **One defect per edit.**
2. **Generate ≥3 diverse candidate edits**, not a single bet — the lone-diagnosis guess is often wrong (it was, in this skill's own dogfood run). Spread them across dimensions/mechanisms. Each respects the **bounded step: ≤30 changed lines** ([SkillOpt](https://arxiv.org/abs/2605.23904)'s textual learning rate).
3. **Score the candidates against the current accepted version** (`delta_step`), keep only the single best; snapshot via commit, then apply it.
4. **Re-score through the shared gate.** Run `../../shared/effect-gate.md` on the chosen edit: held-out **edited vs previous-accepted** (`delta_step`), reusing the once-computed `no_skill` only for the floor check; ≥2 re-runs per condition for the noise band; judges blind to which run is which, median of ≥2. This yields the `gate` object (`gate_pass`, `delta_step`, `delta_exist`, `floor_ok`, `regression_count`, `safety_regression`).
5. **Ratchet** (`references/ratchet-protocol.md`) on the gate's output. Default is revert.

## The decision (delegated to the shared gate's improvement gate)

Keep/revert reads the shared gate, it is not re-derived here:

- **Keep** iff `delta_step > noise_band` **and** no per-task regression vs the previous accepted version **and** `with_edited ≥ no_skill` on every task (floor intact) **and** no safety regression **and** `evaluate-skill`'s Tier 1 introduced no new blocking structural finding.
- **Lateral keep** (`delta_step` within the noise band, nothing dropped) only if the edit *removes* a Tier-1 blocking finding; otherwise a within-noise change is a revert.
- **Revert** on any per-task regression vs the previous version, any floor breach (`with_edited < no_skill` on a task), any `safety_regression`, or a new blocking structural finding — the gate's fatal, non-waivable outcomes. A skill worse than its previous version or below the floor, or less safe, never lands, whatever the average.
- **`unfit_test_set`** is neither keep nor revert — **halt**, harden the held-out set (Phase B), then resume. Never keep on a set that cannot measure a gain.

After deciding: KEEP → distil the win into `learnings.md` and make the edited scores the new previous-accepted; REVERT → distil the failure into `dead-ends.md` so it is never retried.

## Plateau-break

When N rounds pass with no KEEP, do one larger exploratory rewrite that may exceed the step budget (branch first; consult `dead-ends.md`; the gate's fatals still apply). Clears the improvement gate → adopt and reset the counter; else return to the snapshot. One per skill. (A plateau cannot be broken by a bigger edit when the ceiling lives in the *test set* — that is `unfit_test_set`, handled in Phase B, not here.)

## done_when — terminate into one honest state, named explicitly

The user asked for improvement, so a near-zero-change run must resolve to a real verdict, never silently to "done":

- **`improved`** — ≥1 edit kept, each beating the previous version on a confirmed-discriminating set; report the cumulative `delta_step` gain.
- **`already_optimal`** — edits were tried but none beat the current version, **and the set was confirmed discriminating** (it had headroom). Only then is "barely changed" a true verdict about the *skill*.
- **`cannot_measure`** — the set ceilinged / was `unfit_test_set` / nothing could be scored. The null result is the **harness's** fault, not the skill's: do **not** report success. Escalate with the concrete remedy — harden the held-out set, widen the edit budget, or route to `seek-skill` for a structural rethink.

Stop also on max rounds or user stop. A version carrying negative transfer (floor breach) or a safety regression never counts as done — fall back to the last clean KEEP. **A run the user asked to improve that ends with ~0 change must resolve to `already_optimal` or `cannot_measure`, with evidence for which — never an unqualified "done".**

## What this is not

Generation (0→1) is `seek-skill` (from a corpus) or `write-skill` (by hand). A one-shot verdict with no loop is `evaluate-skill`. This skill only evolves an existing SKILL.md; it does not rename `name`, mutate two places at once, or optimize non-SKILL.md files. When distributed standalone, ship `shared/effect-gate.md` alongside it.
