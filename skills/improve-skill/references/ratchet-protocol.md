# Ratchet protocol (git ops + decision table)

The ratchet's job: scores rise **versus the skill's own previous accepted version**, never fall, and a version below the no-skill floor or unsafe never lands. The *judgment* is delegated — each round consumes the `gate` object from the shared measurement gate (`../../../shared/effect-gate.md`), read on its **improvement gate** (`delta_step`); the ratchet just turns that into a mechanical git keep/revert. `git checkout` cannot rationalize a regression.

## Per-round git flow

```
git add . && git commit -m "experiment: <hypothesis>"   # snapshot BEFORE the edit
# ... mutate (<=30 lines) ...
# ... run ../../../shared/effect-gate.md -> gate object (delta_step vs previous-accepted) ...
# KEEP   -> git commit -m "evolve: <change> (delta_step +N.NN)"   # edited scores become the new previous-accepted
# REVERT -> git checkout -- <SKILL.md path>
```

## Decision table (reads the shared gate's improvement gate; first match wins)

| gate output | action |
|---|---|
| `safety_regression`, OR a per-task regression vs the previous accepted version, OR a floor breach (`with_edited < no_skill` on any task) | **REVERT** — fatal, overrides everything; the average is void. |
| `gate_pass == "unfit_test_set"` — for the improvement loop, the current skill is already maxed on every task with no negative transfer (no headroom); a no-skill baseline at ceiling does **not** trigger this (no-skill is only the floor) | **HALT** — report `already_optimal`, or harden the held-out set (Phase B), then resume. Never keep or revert on a set with no headroom. |
| Tier 1 introduced a new blocking structural finding | **REVERT.** |
| `delta_step > noise_band`, no per-task regression vs previous, floor intact | **KEEP** → commit; the edited scores become the new previous-accepted. |
| `delta_step` within the noise band — no per-task regression vs previous, floor intact, safety-clean — AND the edit removes a Tier-1 blocking finding | **KEEP** (lateral; structural repair). |
| `delta_step <= noise_band` with no structural repair, or any task dropped vs previous | **REVERT.** |

The table is **first-match**: the KEEP rows are reached only when the REVERT/HALT rows above did not match, so safety regression, per-task regression, floor breach, and new blocking findings are already excluded by the time a KEEP row applies. The fatal outcomes (per-task regression, floor breach, `safety_regression`) are the gate's non-waivable ones — the ratchet has no override for them.

## Memory update (every decision)

- KEEP → append ≤2 lines to `learnings.md`: what changed + the `delta_step` it produced.
- REVERT → append ≤2 lines to `dead-ends.md`: what was tried + why it regressed. Never re-propose a dead-end; persisting rejected edits is a decisive control ([SkillOpt](https://arxiv.org/abs/2605.23904)).

## Logging (every round)

One row to `experiments.tsv`: round, weakest-dimension targeted, `delta_step`, `delta_exist`, `floor_ok`, `regression_count`, `safety_regression`, change summary, kept/reverted, commit hash.

## Anti-cheat

The blind-judge requirement lives in the shared gate (judges never told which run is with-skill, no prior score, no diff). The ratchet only enforces it operationally: never pass that context into a scoring run. Context isolation is the de-bias ([CoEvoSkills](https://arxiv.org/abs/2604.01687)). Because the keep test is `delta_step` against the *fixed* previous-accepted scores on a *fixed* held-out set, the goalposts cannot drift mid-run; the no-skill floor is computed once and never moved.
