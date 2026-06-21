# Ratchet protocol (git ops + decision table)

The ratchet's job: scores rise, never fall, and a worse-than-nothing or unsafe version never lands. The *judgment* is delegated — each round consumes the `gate` object from the shared measurement gate (`../../../shared/effect-gate.md`); the ratchet just turns `gate_pass` into a mechanical git keep/revert. `git checkout` cannot rationalize a regression.

## Per-round git flow

```
git add . && git commit -m "experiment: <hypothesis>"   # snapshot BEFORE the edit
# ... mutate (<=30 lines) ...
# ... run ../../../shared/effect-gate.md -> gate object ...
# KEEP   -> git commit -m "evolve: <change> (delta +N.NN)"
# REVERT -> git checkout -- <SKILL.md path>
```

## Decision table (reads the shared gate; first match wins)

| gate output | action |
|---|---|
| `gate_pass == "fail"` (any fatal: `regression_count > 0` or `safety_regression`) | **REVERT** — overrides everything; the average is void. |
| `gate_pass == "static_only"` (effect layer required but unrun) | **HOLD** — don't keep; fix the held-out set, then re-score. |
| Tier 1 introduced a new blocking structural finding | **REVERT.** |
| `gate_pass == "pass"` and `delta > 0` and no dimension regressed | **KEEP** → commit, update baseline. |
| `gate_pass == "pass"`, `delta == 0`, a low diagnosis dimension rose, nothing dropped | **KEEP** (lateral rebalance). |
| `delta < 0` or any dimension dropped | **REVERT** (unless a user-approved, logged 1-dim sacrifice for 2-dim gain). |

The fatal outcomes (`regression_count`, `safety_regression`) are the gate's non-waivable ones — the ratchet has no override for them.

## Memory update (every decision)

- KEEP → append ≤2 lines to `learnings.md`: what changed + the delta it produced.
- REVERT → append ≤2 lines to `dead-ends.md`: what was tried + why it regressed. Never re-propose a dead-end; persisting rejected edits is a decisive control ([SkillOpt](https://arxiv.org/abs/2605.23904)).

## Logging (every round)

One row to `experiments.tsv`: round, weakest-dimension targeted, `delta`, `regression_count`, `safety_regression`, change summary, kept/reverted, commit hash.

## Anti-cheat

The blind-judge requirement lives in the shared gate (judges never told which run is with-skill, no prior score, no diff). The ratchet only enforces it operationally: never pass that context into a scoring run. Context isolation is the de-bias ([CoEvoSkills](https://arxiv.org/abs/2604.01687)).
