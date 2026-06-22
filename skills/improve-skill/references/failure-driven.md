# Failure-driven evolution mode

The default loop diagnoses from the rubric's weakest dimension. **Failure-driven mode** swaps the diagnosis *source*: instead of "which dimension is lowest", it asks "what does the failure corpus say is missing". Everything downstream (mutate ≤30 lines → independent re-score → ratchet → memory) is unchanged. Use this when you have execution traces with outcome labels, not just a static skill to grade.

## The unit of learning is the contrastive pair, not the lone failure

A single failure carries almost no signal — you cannot tell whether the skill, the engine, or the task was at fault, and an all-failure pool produces the worst skills, since failures have no anchor ([SkillLens](https://dev.to/wonderlab/is-your-agent-skill-actually-good-microsofts-dual-paper-deep-dive-into-skill-evaluation-and-28b7)). The signal lives in the contrast:

> Pair each failure with its *neighboring success* — the most similar trajectory that succeeded — and locate the behavior **present in the success and absent or wrong in the failure** ([SkillGen](https://arxiv.org/abs/2605.10999)'s contrastive induction). That delta is the gap. It is the failure-driven analog of the deletion test: with vs without, not without alone.

If a failure cluster has no neighboring success, the skill may need a *new* capability — route to `seek-skill` (0→1) rather than editing. This is the same pairing strategy used to learn skill revisions from a failing trajectory plus an existing skill ([CODESKILL](https://arxiv.org/abs/2605.25430)).

## The failure signature (what to extract from each pair)

Write it as the executable triple the failure-mechanism dimension wants:

`trigger condition → failure symptom → the branch the success took that the failure didn't`

This becomes a candidate edit: usually an `if X then Y else Z` added to Rules/Heuristics, or — if the failures cluster on a mis-improvised operation — a new named primitive in `scripts/`. Classify the gap first; a failure-driven edit must respect the target skill's type.

## Diet

Do not feed the loop an all-failure pool; the neighboring successes are the anchor, not optional. The optimal success/failure ratio is domain-specific ([SkillLens](https://dev.to/wonderlab/is-your-agent-skill-actually-good-microsofts-dual-paper-deep-dive-into-skill-evaluation-and-28b7)) — treat it as a tunable, logged in `baseline.md`.

## Guard the three failure modes

- **Memory-rot** — an early wrong edit, passed the gate once, gets replayed as ground truth. Defense: the held-out gate uses *fresh* held-out tasks, never the skill's own past outputs.
- **Sequential overfitting** — reacting one failure at a time overfits trajectory-local lessons. Defense: batch-induce over a cluster (≥3 sharing a signature) before proposing an edit; never edit from n=1.
- **Misevolution** — accumulating patches can lower safety alignment. Defense: the safety gate runs on every failure-driven edit.

## Wiring

Failure-driven mode feeds candidate edits into the *same* ratchet (`ratchet-protocol.md`) and the *same* shared measurement gate (`../../../shared/effect-gate.md`) — judged on its improvement gate. The only addition is the diagnosis front-end above. The "with vs without" contrast here is the *diagnosis* unit (failure × neighboring success), not the keep test; acceptance is `delta_step`. Output, per accepted edit: the contrastive pair that motivated it, the signature, and the held-out `delta_step` (vs the previous accepted version).
