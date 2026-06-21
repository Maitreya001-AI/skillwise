---
name: improve-skill
description: Iteratively improve an existing skill so it gets monotonically better without degrading or drifting. Use this when a skill isn't triggering, is over-engineered, produces weak output, or fails on some cases, or when asked to make a skill better, optimize it, or evolve it from failure traces. Also use it to push a draft from "runs" to "ships". This runs a propose-test-accept loop where every edit must beat a no-skill baseline before it lands; it does not freely rewrite. Use seek-skill instead to create a brand-new skill from a corpus.
license: MIT
---

# Improve a Skill

This is a **control** skill (composite: control + judgment + capability): a gap-classification front-end in front of a ratchet-and-gate loop. The derivation is in the skillwise repo's `docs/THEORY.md` (§5, §8). On first activation also read `references/rubric.md` (the *diagnosis* rubric — which dimension is weakest), `references/ratchet-protocol.md`, and `references/failure-driven.md`.

The keep/revert decision is **not** re-implemented here. Every edit is judged by the **shared measurement gate** in `../../shared/effect-gate.md` — the same gate `evaluate-skill` uses as its second tier, so a kept edit means exactly what an evaluate pass means. The loop's only job is to propose bounded edits and let that gate accept or reject them.

> **A theory refinement this skill embodies.** A control skill leaves *task* iteration to the engine, but the **gate protocol must be concrete and non-skippable** — the failure being prevented is the engine skipping its own gate. The loop below is a *measurement protocol* (change → measure → keep/revert): its order is epistemic, the legitimate exception to the shuffle test.

## Phase A — Classify the target

Name the gap the target fills (Knowledge / Capability / Judgment / Control / composite) and its **tier** (scaffold vs production/library — this decides whether the effect layer is mandatory; see `effect-gate.md`). Classification selects the type-aware diagnosis weighting in `references/rubric.md`: workflow-clarity is N/A for Knowledge/Judgment skills; executable-specificity relaxes for Judgment. Run `evaluate-skill` once for the baseline gate.

## Phase B — Set up the harness

- Confirm the target holds a `SKILL.md` and the git tree is clean (the ratchet reverts via `git checkout`).
- Create a working dir with rolling memory: `learnings.md` (verified wins) and `dead-ends.md` (falsified edits, never retried).
- **Assemble the held-out set per `../../shared/effect-gate.md`**: caller-supplied tasks, or draft 3 happy-path + 1 edge into `baseline.md` and confirm with the user before scoring. Weak tests inflate everything downstream.

## Phase C — The loop

Each round is atomic edit + independent re-score through the shared gate + forced keep/revert.

1. **Diagnose** the single weakest dimension via `references/rubric.md`. If you have execution traces with outcome labels, switch the diagnosis source to failure-driven mode (`references/failure-driven.md`): pair each failure with a neighboring success and extract the missing-behavior signature. Read `learnings.md` + `dead-ends.md` first; never re-walk a falsified edit. One-line hypothesis. **One defect per edit.**
2. **Mutate.** Snapshot via commit, then edit. **Bounded step: ≤30 changed lines per round** ([SkillOpt](https://arxiv.org/abs/2605.23904)'s textual learning rate). More → split into rounds.
3. **Re-score through the shared gate.** Run `../../shared/effect-gate.md` on the edited skill: held-out with-skill vs no-skill, judges blind to which run is which, median of ≥2. This yields the `gate` object (`gate_pass`, `delta`, `regression_count`, `safety_regression`).
4. **Ratchet** (`references/ratchet-protocol.md`) on the gate's output. Default is revert.

## The decision (delegated to the shared gate)

Keep/revert reads the shared gate, it is not re-derived here:

- **Keep** iff `gate_pass == "pass"` and `delta > 0` — and, additionally, `evaluate-skill`'s Tier 1 introduced no new blocking structural finding.
- **Revert** on `gate_pass == "fail"`, or any `regression_count > 0`, or `safety_regression` — these are the gate's fatal, non-waivable outcomes. A skill worse than no skill, or less safe, never lands, whatever the average.
- **`static_only`** (effect layer required but unrunnable) is not a keep — fix the held-out set first.

After deciding: KEEP → distil the win into `learnings.md`; REVERT → distil the failure into `dead-ends.md` so it is never retried.

## Plateau-break

When N rounds pass with no KEEP, do one larger exploratory rewrite that may exceed the step budget (branch first; consult `dead-ends.md`; the gate's fatals still apply). Clears the gate → adopt and reset the counter; else return to the snapshot. One per skill.

## done_when

Stop when the gate reports `pass` with `delta` at/above target **and** `regression_count == 0` **and** safety clean; or the held-out score plateaus within bounded-step noise for N rounds (after one plateau-break); or max rounds; or the user stops it. A version carrying negative transfer or a safety regression never counts as done — fall back to the last clean KEEP.

## What this is not

Generation (0→1) is `seek-skill` (from a corpus) or `write-skill` (by hand). A one-shot verdict with no loop is `evaluate-skill`. This skill only evolves an existing SKILL.md; it does not rename `name`, mutate two places at once, or optimize non-SKILL.md files. When distributed standalone, ship `shared/effect-gate.md` alongside it.
