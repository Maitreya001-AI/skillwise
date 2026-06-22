# Type-aware diagnosis rubric

This rubric is for **diagnosis** — picking the single weakest dimension to fix in the next edit. It is *not* the accept/reject gate: whether an edit actually lands is decided by the shared measurement gate (`../../../shared/effect-gate.md`), which runs the held-out scoring — the **improvement gate** (`delta_step` vs the skill's previous accepted version) for an improve-skill round — and owns the fatal negative-transfer, floor, and safety checks. Diagnose here; let the gate judge.

Pass this file to every diagnosis judge verbatim. The single principle over a uniform rubric: **classify the skill first, then weight the dimensions per type** (see the skillwise repo's `docs/THEORY.md` §1, §4), because each type has a different characteristic failure.

## Type map (apply first)

| dimension | Knowledge | Capability | Judgment | Control |
|---|---|---|---|---|
| Workflow clarity | **N/A** | partial | **N/A** | full (it is the gate protocol) |
| Executable specificity | full | full | **relaxed** (taste = negative fences + plausibility) | full |
| Failure-mechanism | full | full | as "what wrong looks like" | full |
| High-risk blacklist | full | full | full | full |

"N/A" dimensions drop from the denominator, not scored 0. For a composite, score each component under its own column and weight by the mix.

## Diagnosis dimensions

Anchors 0/2/5/8/10. These rank *where the skill is weakest*, to aim the next bounded edit. They do not certify improvement — only the gate does.

1. **Trigger & frontmatter.** `description` routes by gap ("use when X is missing"), not only by output; multiple phrasings incl. colloquial; positive and negative when-to-use.
2. **Workflow clarity** (N/A for Knowledge/Judgment). Ordered/executable only where the type is Control/Capability. Never grind this for cosmetics.
3. **Failure-mechanism encoding** (high-signal). Executable `if X then Y else Z` (trigger → symptom → branch) with fallbacks, not a happy path.
4. **Executable specificity** (high-signal; relaxed for Judgment). Avoid "suggest / consider / as appropriate" for Capability/Control; use templates, example I/O, numeric constraints.
5. **High-risk-action blacklist** (high-signal). A dedicated "never do" section, concrete actions with why.
6. **Checkpoint design.** Intermediate verification / user-confirm / recoverable save points; for composites the human checkpoint sits at the judgment ↔ control/capability seam.
7. **Architecture conciseness.** SKILL.md ≤500 lines, detail in references/. Formatting reorders don't change effect.

## What is NOT scored here

**Measured gain vs the no-skill baseline, negative transfer, and safety** are the gate's job, not the rubric's — they are decided empirically on held-out tasks by `../../../shared/effect-gate.md`, not by reading. A skill that reads well can still lose to no-skill; that is exactly why the gate, not this rubric, has the final say.

## Diagnosis output schema

```json
{
  "rubric_version": "2.0",
  "skill_path": "...",
  "skill_type": "knowledge|capability|judgment|control|composite:<mix>",
  "na_dimensions": ["workflow_clarity"],
  "scores": { "<dim>": {"raw_anchor": "8", "rationale": "<quote passage>"} },
  "weakest_dimension": "<actionable>",
  "weakest_rationale": "..."
}
```

## Calibrate before looping

Run the rubric on one known-good skill and two rough ones with two independent judges; require the good one to rank clearly above the rough ones and inter-judge spread to be small. If not, fix the anchors before any auto-loop — an LLM judge reading skill text is unreliable by default ([SkillLens](https://dev.to/wonderlab/is-your-agent-skill-actually-good-microsofts-dual-paper-deep-dive-into-skill-evaluation-and-28b7)). Final acceptance is always the gate, never the rubric score.
