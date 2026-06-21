---
name: evaluate-skill
description: Judge whether a skill is well-designed and locate precisely what is wrong when it is not. Use this when asked to review, audit, critique, grade, or sanity-check a skill, when someone asks "is this skill any good?", or when a skill seems not to trigger, feels over-engineered, or reads as too procedural. Use it automatically as the final check before shipping a freshly written or edited skill, and when deciding which of two skill drafts is better.
license: MIT
---

# Evaluate a Skill

A skill is judged by one criterion, asked five ways. This body is the correctness ruler; the skillwise repo's `docs/THEORY.md` (§4) has the derivation.

**The criterion.** A skill is correct iff it *fills the gap the base engine lacks, exactly* — no under-fill, no over-fill, in the right layer, with a verifiable exit. Each test below catches one way that breaks and names the defect, so a failing skill yields a specific fault, not a vibe.

## The mechanical pass (cheap entry)

Run the linter on the skill folder first; it catches structural defects deterministically so judgment is spent on semantic ones:

```
python scripts/lint_skill.py <path-to-skill-folder-or-SKILL.md>
```

It reports frontmatter health, whether the `description` routes by *gap* vs only by *output*, the procedural-step smell, whether an exit/verification surface exists, whether capability claims are backed by `scripts/`, and length budget.

The linter is the entry, not the verdict: it lowers the frequency of mechanical errors but cannot certify a skill. The guarantee comes only from the semantic read below.

## The five tests (the semantic read — the guarantee)

Run each against the skill's *typical task*.

1. **Deletion — is there a gap?** Remove the skill, run the task. Still passes → it supplies free reasoning/orchestration and should not exist. *Defect: over-fill.* Ask "should this exist?" first.
2. **Improvisation — under-fill?** Run with the skill; count gap-bearing material the engine still had to improvise. Greater than zero → *under-fill.*
3. **Shuffle — over-fill?** Hand the primitives to the engine in scrambled order. Still completes → vocabulary (good); order-dependent → a welded procedure. *Defect: over-fill.*
4. **Inertia-cost — over-fill's other face.** On a task the engine already handles, compare with/without the skill. Longer/costlier with no gain → skill inertia.
5. **Exit — guaranteeable?** Is there a semantic check comparing the *product* against "what correct looks like," not merely "well-formed"? None → *no exit.*

## Composite skills — the seam test

Decompose into atomic gaps, run the five tests per atom, then check: does the human checkpoint sit at the boundary between the *judgment* component and the *control/capability* component? Misplacement → the machine overstepped into judgment (over-fill) or a human was inserted where automation belonged (under-fill).

## Scorecard

| check | passes when | fails as |
|---|---|---|
| Routes by gap, not output | `description` says "use when X is missing", not only "produces Y" | wrong routing |
| Gap fully supplied | improvisation test → 0 | under-fill |
| Capability shipped as a primitive | misuse is *syntactically* impossible | wrong-layer |
| No step ordering | passes the shuffle test | over-fill |
| Judgment/control declarative · `done_when` | not fixed steps | over-fill |
| Semantic exit check present | compares against "correct" | no exit |
| Composite seam placed right | checkpoint at judgment↔control/capability | seam misplacement |
| Failure mechanisms encoded | key branches as `if X then Y else Z` | brittle |
| Executable specificity | no hedging where the type forbids it | vague |
| High-risk blacklist | a dedicated "never do" section | unguarded |
| Beats the no-skill baseline | clearly better than the task run without it | **negative transfer (fatal)** |

All rows must pass. **Negative transfer is fatal:** run the typical task with and without the skill; if with-skill is worse, the skill must never ship, regardless of any other row.

## How to read it reliably

Reading a skill is misleading on its own — fluent prose does not predict downstream gain, and a single LLM judge asked which skill performs better is no better than chance ([SkillLens](https://dev.to/wonderlab/is-your-agent-skill-actually-good-microsofts-dual-paper-deep-dive-into-skill-evaluation-and-28b7)). So: judge the skill as an *intervention* against a no-skill baseline ([SkillGen](https://arxiv.org/abs/2605.10999)), and take the median of two or more independent judges in fresh contexts rather than trusting one. The three reading-level rows above (failure mechanisms, executable specificity, high-risk blacklist) are the signals that do correlate with utility.

**Apply type-aware.** Classify the skill first (Knowledge / Capability / Judgment / Control). For Knowledge and Judgment skills, "has a workflow" is *not* a virtue — score that row N/A. For Judgment skills, relax executable-specificity: taste is declared as descriptive "what good looks like" plus negative fences, not hard imperatives.

## Output

Give: (1) the linter's mechanical findings, (2) pass/fail per scorecard row with the named defect for each failure, (3) the single highest-leverage fix. Do not rewrite the skill — that is `improve-skill`. The job is a verdict, located precisely.
