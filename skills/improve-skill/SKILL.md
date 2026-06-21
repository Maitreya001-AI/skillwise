---
name: improve-skill
description: Iteratively improve an existing skill so it gets monotonically better without degrading or drifting. Use this when a skill isn't triggering, is over-engineered, produces weak output, or fails on some cases, or when asked to make a skill better, optimize it, or evolve it from failure traces. Also use it to push a draft from "runs" to "ships". This runs a propose-test-accept loop where every edit must beat a no-skill baseline before it lands; it does not freely rewrite. Use seek-skill instead to create a brand-new skill from a corpus.
license: MIT
---

# Improve a Skill

This is a **control** skill (composite: control + judgment + capability). It puts a gap-classification front-end in front of a ratchet-and-gate evolution loop. The derivation and citations are in the skillwise repo's `docs/THEORY.md` (§5, §8); read it on first activation, along with `references/rubric.md`, `references/ratchet-protocol.md`, and `references/failure-driven.md`.

The core move turns unconditional self-editing into propose-and-test: **no edit lands unless it provably beats the current version on a held-out set** ([SkillOpt](https://arxiv.org/abs/2605.23904)). That is the only source of monotone, non-degrading improvement.

> **A theory refinement this skill embodies.** A control skill leaves *task* iteration to the engine — but the **gate protocol must be concrete and non-skippable**, because the failure being prevented is the engine skipping its own gate. So the loop below is a *measurement protocol* (change → measure → keep/revert): its order is epistemic, not task-flow, and that is the legitimate exception to the shuffle test.

## Phase A — Classify the target first

Name the gap the target skill fills (Knowledge / Capability / Judgment / Control, or a composite). Skipping this lets a hill-climb push a knowledge/judgment skill into a procedural shape that scores higher but is worse. The classification selects the type-aware rubric weighting (`references/rubric.md`): workflow-clarity is N/A for Knowledge and Judgment skills; executable-specificity relaxes for Judgment skills. Run `evaluate-skill` once for the baseline verdict.

## Phase B — Set up the harness

- Confirm the target holds a `SKILL.md` and the git tree is clean (the ratchet reverts via `git checkout`).
- Create a working dir for logs and rolling memory: `learnings.md` (verified wins) and `dead-ends.md` (falsified edits, never retried).
- **Test-prompt gate.** Draft 3 happy-path prompts + 1 edge prompt, write them to `baseline.md`, and show the user for confirmation before scoring. Weak tests inflate scores. If subagents are unavailable, fall back to dry-run and flag it.

## Phase C — The loop (default-deny gate)

Each round is atomic edit + independent re-score + forced keep/revert.

1. **Diagnose** the single weakest dimension. If you have execution traces with outcome labels, switch the diagnosis source to failure-driven mode (`references/failure-driven.md`): pair each failure with a neighboring success and extract the missing-behavior signature, instead of reading the rubric. Read `learnings.md` + `dead-ends.md` first; never re-walk a falsified edit. Write a one-line hypothesis. **One defect per edit.**
2. **Mutate.** Snapshot via commit, then edit. **Bounded step: ≤30 changed lines per round** ([SkillOpt](https://arxiv.org/abs/2605.23904)'s textual learning rate). More → split into rounds.
3. **Re-evaluate.** Spawn independent judges (default 2, take the median) in a fresh context. The judge prompt must not reveal "this is the improved version", the prior score, or a diff — context isolation is the de-bias ([CoEvoSkills](https://arxiv.org/abs/2604.01687)). Each test prompt runs twice — with-skill and no-skill — to detect negative transfer.
4. **Ratchet** (`references/ratchet-protocol.md`). Default is revert.

## The gate — default deny, priority order

1. **Negative-transfer gate (overrides all).** If any test's with-skill output is worse than the no-skill baseline → revert, regardless of total. A skill worse than no skill never lands.
2. **Safety gate.** Refusal rate, attack-success, and scope-creep into judgment the engine should own — any regression fails the gate even if task score rose ([Skill-Inject](https://arxiv.org/abs/2602.20156)).
3. **Correctness gate.** Re-run `evaluate-skill`; no new scorecard failure.
4. **No-regress + improvement.** Accept iff total strictly improved (or a low dim rose with no dimension dropping). Else revert.

After deciding: KEEP → distil the win into `learnings.md`; REVERT → distil the failure into `dead-ends.md` so it is never retried.

## Plateau-break

When N rounds pass with no KEEP, do one larger exploratory rewrite that may exceed the step budget (snapshot a branch first; never introduce negative transfer; consult `dead-ends.md`). Better and clean → adopt and reset the counter; else return to the snapshot. One per skill.

## done_when

Stop when total ≥ target **and** negative_transfer is false **and** the safety gate is clean; or the held-out score plateaus within bounded-step noise for N rounds (after one plateau-break); or max rounds; or the user stops it. A version carrying negative transfer or a safety regression never counts as done — fall back to the last clean KEEP.

## What this is not

Generation (0→1) is `seek-skill` (from a corpus) or `write-skill` (by hand). A one-shot verdict with no loop is `evaluate-skill`. This skill only evolves an existing SKILL.md. It does not rename `name`, does not mutate two places at once, and does not optimize non-SKILL.md files.
