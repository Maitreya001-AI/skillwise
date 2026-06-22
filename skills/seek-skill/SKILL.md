---
name: seek-skill
description: Discover and generate a new skill automatically from a corpus of experience — agent trajectories, traces, logs, a completed task run, a codebase, or a document set — instead of writing it by hand. Use this when the goal is to mine or auto-generate skills from existing material, to turn what an agent keeps doing into a reusable skill, or to extract a skill from session logs. Use write-skill instead when the skill is already specified and just needs to be written.
license: MIT
---

# Seek a Skill from a Corpus

This is the skill-extraction stage of the lifecycle (experience → extraction → consumption). It is `write-skill` driven by a corpus instead of a person, plus two things the corpus adds: a classification front-end and a held-out gate. The derivation is in the skillwise repo's `docs/THEORY.md` (§9); the authoring discipline it reuses is in `../write-skill/SKILL.md`.

> **The trap to avoid.** The common failure is to compile the *trajectory* — the action sequence — directly into the skill, turning parameters into placeholders. That encodes a procedure the engine already orchestrates for free, and welds an order that fails the shuffle test ([AXIS](https://arxiv.org/abs/2409.17140) does exactly this and notes the result is "a combination of actions"). Extraction distils the *pattern* (which gap recurs), not the *path*. The action sequence is evidence, not the skill.

## What this needs (the substrate)

In order of importance:
- **Full trajectories, not just outcomes** — inputs, actions, tool calls, intermediate states, and especially the primitives the engine improvised at runtime, where the hidden gap lives. Final outputs alone hide the gap.
- **An outcome signal per trajectory** (success/failure, ideally graded) — without it you cannot form contrasts or gate.
- **A diverse pool with a tuned success/failure diet** — extraction leans success-heavy; an all-failure pool produces the worst skills, since failures have no anchor ([SkillLens](https://dev.to/wonderlab/is-your-agent-skill-actually-good-microsofts-dual-paper-deep-dive-into-skill-evaluation-and-28b7)). The ratio is a domain-specific knob.
- **The existing skill library** — to dedup and avoid rediscovering a behavior that is already a skill.
- **A held-out validation set** disjoint from the mining pool — what makes extraction optimization rather than distillation.
- **A rejected-candidate buffer** — patterns that failed the gate, kept so the loop never re-proposes a dead end.

Grounding matters: a skill distilled without real task context collapses into vague generic procedure, so mine from real executions with their corrections and input/output formats ([Agent Skills best practices](https://agentskills.io/skill-creation/best-practices)).

## The loop (a measurement protocol — iteration left to the engine)

> Steps **1–4 are dependency-forced, not welded**: you cannot classify a pattern you haven't mined, materialize a gap you haven't classified, or gate an artifact you haven't materialized — a dependency order, not a task-march, so it does not fail the shuffle test. Steps **5–6 are post-gate steps with one ordering constraint**: dedup/preserve before registering, so a to-be-merged identity isn't registered prematurely; step 5's *coverage-expansion* re-enters the gate as a fresh existence check, not a re-run of step 4's verdict. The `docs/THEORY.md` §8 measurement-protocol exemption applies to the gate's own change→measure→keep order — spanning materialize (step 3) → gate (step 4) — not to the whole loop.

1. **Mine recurring patterns by batch induction over the whole pool, not serially** ([Trace2Skill](https://www.emergentmind.com/topics/trace2skill)). A pattern recurs across multiple successful trajectories and, where labels allow, is present in successes and absent or wrong in failures ([SkillGen](https://arxiv.org/abs/2605.10999)'s contrastive induction).
2. **Classify the gap** — the step that separates a reusable skill from a replayed macro. For each pattern: a missing *fact* → Knowledge; a *mis-improvised operation* → Capability (the tool calls become `build({named fields})`, never positional replay); a recurring *"what good looks like"* → Judgment; a *non-default loop* → Control.
3. **Materialize type-disciplined** (hand to `write-skill`'s invariants). Emit a structured folder: SKILL.md + `scripts/` (only for capability primitives) + `references/`. Describe the world and what's correct, not the path taken.
4. **Gate on the held-out set (default deny)** — the **shared measurement gate** in `../../shared/effect-gate.md`, on its **existence** branch. A brand-new skill has no previous version, so `delta_step` is undefined; seeking always asks *should this exist?* (`delta_exist` vs no-skill — the same branch `evaluate-skill` uses, *not* `improve-skill`'s improvement branch). Inject the candidate, run the held-out set with-skill vs no-skill (the deletion test, made measurable — [MUSE-Autoskill](https://arxiv.org/abs/2605.27366)); the gate owns the keep/discard decision and its non-waivable fatals — **do not restate the rule here, reference it**. Keep iff it passes; else discard to a rejected buffer.
5. **Dedup and preserve.** Merge against the library with conflict detection; never overwrite a capability the library already had. Expand coverage beyond the seed corpus only through the same gate ([SkillX](https://arxiv.org/abs/2604.04804)).
6. **Hand off.** The existence verdict already came from the step-4 gate — don't re-run it; surface the gate's converged report (the `evaluate-skill`-shaped gate object, see `../../shared/effect-gate.md`) for humans and register the kept skill for ongoing `improve-skill` evolution.

## Roles — separate them

Extractor, executor, and evaluator are distinct jobs; a strong executor is not necessarily a strong extractor, and self-verification inherits the generator's bias. Run the gate in an information-isolated context ([CoEvoSkills](https://arxiv.org/abs/2604.01687); [SkillLens](https://dev.to/wonderlab/is-your-agent-skill-actually-good-microsofts-dual-paper-deep-dive-into-skill-evaluation-and-28b7)).

## done_when

Stop when the diverse pool yields no new pattern that passes the held-out gate, or the corpus is exhausted. A candidate that can't beat the no-skill baseline **on a set whose `no_skill` is not at ceiling** is not a skill — report "no gap here," don't ship a macro. Distinguish this from `unfit_test_set` (the held-out set's `no_skill` is itself at ceiling, so existence value can't be shown): there, **harden the set**, don't conclude "no gap."

## Output

Per generated skill: the gap it fills (with the recurring evidence), its type, the held-out `delta_exist` (with-skill vs no-skill), and the dedup decision. Show the discarded candidates — patterns that looked promising but failed the gate are as informative as the kept ones.
