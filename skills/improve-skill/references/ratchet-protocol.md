# Ratchet protocol (git ops + decision table)

The ratchet's only job: scores can rise, never fall, and a worse-than-nothing or unsafe version can never land. Decisions are mechanical — `git checkout` cannot rationalize a regression.

## Per-round git flow

```
git add . && git commit -m "experiment: <hypothesis>"   # snapshot BEFORE the edit
# ... mutate (<=30 lines) ...
# ... independent re-score (2 judges, median) + no-skill baseline ...
# KEEP   -> git commit -m "evolve: <change> (+N: A->B)"
# REVERT -> git checkout -- <SKILL.md path>
```

## Decision table (priority order — first match wins)

| condition | action |
|---|---|
| `negative_transfer == true` | **REVERT** (overrides all). With-skill worse than no-skill; the total is void. |
| `safety_regression == true` | **REVERT.** Refusal / attack-success / scope-creep regressed; task gain is irrelevant. |
| new `evaluate-skill` scorecard failure introduced | **REVERT.** |
| `new_total > old_total` and no dimension dropped | **KEEP** -> commit, update baseline. |
| `new_total == old_total`, a low dim rose, no dimension dropped | **KEEP** (lateral rebalance). |
| `new_total < old_total` or any dimension dropped | **REVERT** (unless user-approved sacrifice). |
| deliberate 1-dim sacrifice for 2-dim gain | **KEEP only with explicit user approval**, logged. |
| score crash / judge failure | **SKIP**, log, next round. |

## Memory update (every decision)

- KEEP -> append <=2 lines to `learnings.md`: what changed + why it rose.
- REVERT -> append <=2 lines to `dead-ends.md`: what was tried + why it regressed. Never re-propose a dead-end direction; persisting rejected edits is a decisive control ([SkillOpt](https://arxiv.org/abs/2605.23904)).

## Logging (every round)

One row to `experiments.tsv`: round, dim scores, total, negative_transfer, safety_regression, change summary, kept/reverted, flags, commit hash. Failures fill the dead-end buffer and are worth recording.

## Anti-cheat (judge prompts)

Never include in a judge prompt: "improved version", "new", "better", "updated", the prior score, or a diff. Context isolation is the de-bias; a verifier blind to the generator's reasoning sidesteps confirmation bias ([CoEvoSkills](https://arxiv.org/abs/2604.01687)).
