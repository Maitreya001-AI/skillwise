# Contributing to skillwise

Thanks for wanting to add or sharpen a skill. The bar here is unusual: skillwise is a toolkit *about* skill quality, so its own skills have to clear the same ruler they apply to others.

## The bar

A skill is accepted when it **fills a gap the base engine lacks, exactly** — no under-fill, no over-fill, in the right layer, with a verifiable exit. Concretely, before opening a PR:

1. **Classify the gap.** Say which of the four your skill fills — Knowledge, Capability, Judgment, Control — or which composite. If you can't name a gap, the engine probably already does the task for free, and the skill shouldn't exist.
2. **Pass the linter.** It's the mechanical entry check, not a verdict:
   ```bash
   python skills/evaluate-skill/scripts/lint_skill.py --check skills/<your-skill>
   ```
   The CI runs this on every skill; blocking findings fail the build.
3. **Run the five semantic tests** (this is the actual guarantee, by hand or with `evaluate-skill`): deletion, improvisation, shuffle, inertia-cost, exit. See [`skills/evaluate-skill/SKILL.md`](./skills/evaluate-skill/SKILL.md).
4. **Clear the gate.** For a *new* skill, show it beats the no-skill baseline (`delta_exist > 0`): run a representative task with and without it. For an *edit to an existing* skill, show it beats the skill's *previous version* (`delta_step` beyond the noise band) while never dropping below the no-skill floor — see [`shared/effect-gate.md`](./shared/effect-gate.md). A version worse than its reference is the one defect we never merge.

## Style

- **Declarative, not a step-march.** Describe the world, what's correct, and what the user wants — leave "how" to the engine. If you're writing `Step 1 / Step 2 / Step 3`, you're likely encoding a procedure the engine already orchestrates (see the "skill inertia" discussion in [`docs/THEORY.md`](./docs/THEORY.md)).
- **Capabilities ship as primitives.** If your skill needs a reliable operation, put a named-field script in `scripts/`, don't narrate a call sequence in prose.
- **Make the description "pushy."** The `description` field is the trigger. Route by gap ("use when X is missing"), include colloquial phrasings, and state when *not* to use it.
- **Cite empirical claims.** Any performance/behavior claim in a skill body needs a real, reachable reference link. No unverifiable numbers.
- **Keep `SKILL.md` lean.** Push detail into `references/`; bundle runtime scripts in `scripts/`.

## Mechanics

- One skill per folder under `skills/<name>/`, with `SKILL.md` (frontmatter `name` + `description` required; add `license`).
- If you add a new skill, list its path in the `skills` array of `.claude-plugin/marketplace.json`.
- Open a PR with: the gap it fills, its type, and your with/without baseline result.

By contributing you agree your work is released under the repository's MIT License.
