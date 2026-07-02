# Ratchet protocol (git ops + decision table)

The ratchet's job: scores rise **versus the skill's own previous accepted version**, never fall, and a version below the no-skill floor or unsafe never lands. The *judgment* is delegated — each round consumes the `gate` object from the shared measurement gate (`../references/effect-gate.md`), read on its **improvement gate** (`delta_step`); the ratchet just turns that into a mechanical git keep/revert. `git checkout` cannot rationalize a regression.

## Per-round git flow

```
git add . && git commit -m "experiment: <hypothesis>"   # snapshot BEFORE the edit
# ... mutate (<=30 changed lines, anywhere inside the skill directory) ...
# ... run ../references/effect-gate.md -> gate object (delta_step vs previous-accepted) ...
# KEEP   -> git commit -m "evolve: <change> (delta_step +N.NN)"   # edited scores become the new previous-accepted
# REVERT -> git checkout -- <skill-dir>                            # the whole directory: SKILL.md + scripts/ + references/
```

The revert target is the **skill directory**, not just `SKILL.md` — the bounded step may legitimately touch `scripts/` (a Capability fix ships as a primitive, THEORY §4) or `references/`, and a revert must undo all of it.

## Decision table (reads the shared gate's improvement gate; first match wins)

| gate output | action |
|---|---|
| `safety_regression`, OR any task whose **median across re-runs** drops below the previous accepted version, OR a floor breach (median `with_edited < no_skill` on any task) | **REVERT** — fatal, overrides everything; the average is void. A single-run dip is not a regression (§8-2); a reproduced one always is. |
| `gate_pass == "unfit_test_set"` — for the improvement loop, the current skill is already maxed on every task with no negative transfer (no headroom); a no-skill baseline at ceiling does **not** trigger this (no-skill is only the floor) | **HALT** — report `already_optimal`, or harden the held-out set (Phase B), then resume. Never keep or revert on a set with no headroom. |
| Tier 1 introduced a new blocking structural finding | **REVERT.** |
| `delta_step > noise_band`, no reproduced per-task regression vs previous, floor intact | **KEEP** → commit; the edited scores become the new previous-accepted. |
| `delta_step` within the noise band — no reproduced per-task regression vs previous, floor intact, safety-clean — AND the edit removes a Tier-1 blocking finding | **KEEP** (lateral; structural repair). |
| `delta_step <= noise_band` with no structural repair, or any reproduced task drop vs previous | **REVERT.** |

The table is **first-match**: the KEEP rows are reached only when the REVERT/HALT rows above did not match, so safety regression, reproduced per-task regression, floor breach, and new blocking findings are already excluded by the time a KEEP row applies. The fatal outcomes are the gate's non-waivable ones — the ratchet has no override for them.

**Terminal check (once, after the last round).** Before reporting `improved`, re-score the surviving version on the **confirmation slice** (`confirm/`, never seen by any round): `delta ≥ 0` vs the entry version there → `improved`; below → `improved (unconfirmed)` and recommend a fresh set (§8-4). The per-set round cap (default 10) is also enforced here: at the cap, rotate or stop.

## Memory update (every decision)

- KEEP → append ≤2 lines to `learnings.md`: what changed + the `delta_step` it produced.
- REVERT → append ≤2 lines to `dead-ends.md`: what was tried + why it regressed. Never re-propose a dead-end; persisting rejected edits is a decisive control ([SkillOpt](https://arxiv.org/abs/2605.23904)).

## Logging (every round)

One row to `experiments.tsv`: round, weakest-dimension targeted, `delta_step`, `delta_exist`, `cost_delta`, `floor_ok`, `regression_count`, `safety_regression`, change summary, kept/reverted, commit hash. `cost_delta` is advisory (§8-5): a persistent cost climb with flat deltas is a signal to stop the loop, not a per-round fatal.

## Anti-cheat

The blind-judge requirement lives in the shared gate (judges never told which run is with-skill, no prior score, no diff — and judges are *decorrelated*: different models or information-isolated contexts). The ratchet only enforces it operationally: never pass that context into a scoring run. Context isolation is the de-bias ([CoEvoSkills](https://arxiv.org/abs/2604.01687)). Because the keep test is `delta_step` against the *fixed* previous-accepted scores on a *fixed* held-out set, the goalposts cannot drift mid-run; the no-skill floor is computed once and never moved. What the fixed set cannot rule out — adaptive overfitting to itself — is the confirmation slice's job (§8-4), not this file's.
