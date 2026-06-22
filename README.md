# skillwise

**Skills for working on skills.** A small, coordinated toolkit that can **discover, write, evaluate, and improve** agent skills — the `SKILL.md` standard — all derived from one principle: *a skill exists only to fill a gap the base engine lacks.*

The four skills spell **WISE** — **W**rite, **I**mprove, **S**eek, **E**valuate. (They run in the order evaluate → write/seek → improve across a skill's life; the acronym is just a happy accident of their names.)

- Full derivation: [`docs/THEORY.md`](./docs/THEORY.md)
- Step-by-step illustrated walkthrough: [`docs/theory.html`](./docs/theory.html)

## The idea in one line

A modern agent already reasons, writes code, and orchestrates steps for free. A skill earns its place only by supplying what that free engine lacks — and there are exactly four kinds of gap: **Knowledge** (a missing fact), **Capability** (a missing reliable primitive), **Judgment** (a missing criterion), and **Control** (a missing non-default loop). *Procedure is not a gap* — orchestration is free, so a step-by-step skill fights the engine instead of helping it. Classify by gap; fill it at the right layer; verify at a semantic exit; evolve behind a held-out gate.

## The skills

| skill | what it is | use it when |
|---|---|---|
| [`evaluate-skill`](./skills/evaluate-skill) | the correctness ruler (the kernel) | reviewing, grading, "is this skill good?", and as the final check before shipping |
| [`write-skill`](./skills/write-skill) | the ruler run in reverse — author by hand | creating or designing a new skill from a known need |
| [`seek-skill`](./skills/seek-skill) | authoring driven by a corpus — discovery | mining or auto-generating a skill from traces, a run, or a codebase |
| [`improve-skill`](./skills/improve-skill) | the ruler in a gated loop | a skill isn't triggering, is over-built, or fails cases; evolving from failure traces |

`evaluate-skill` is the kernel: `write-skill` and `seek-skill` call it as an exit gate, and `improve-skill` calls it as the gate inside its loop. Together they span the skill lifecycle — experience → extraction (`seek`) → consumption and evolution (`improve`) — with hand-authoring (`write`) and judgment (`evaluate`) throughout. Each works alone; they're designed to work together.

## Install

Three paths, one repo layout — pick whichever fits your agent.

### 1. `npx skills` — the cross-agent way (works with 40+ agents)

```bash
# install all four
npx skills@latest add Maitreya001-AI/skillwise

# preview without installing
npx skills@latest add Maitreya001-AI/skillwise --list

# just one skill
npx skills@latest add Maitreya001-AI/skillwise@evaluate-skill

# global + specific agent + non-interactive (CI)
npx skills@latest add Maitreya001-AI/skillwise --all -g -a claude-code -y
```

`@latest` dodges npx's stale cache. The CLI auto-discovers the `skills/<name>/SKILL.md` layout and also reads this repo's `.claude-plugin/` manifests.

### 2. Claude Code plugin marketplace

```bash
/plugin marketplace add Maitreya001-AI/skillwise
/plugin install skillwise@skillwise
```

Then just talk to it — "evaluate this skill", "write a skill for X", "improve this skill from these traces" — and the skills trigger by description. Explicit invocation is namespaced: `skillwise:evaluate-skill`.

### 3. Manual

Clone, then copy any skill folder into your skills directory:

```bash
git clone https://github.com/Maitreya001-AI/skillwise
cp -r skillwise/skills/* ~/.claude/skills/      # personal
# or  .claude/skills/  for a single project
```

## Use the linter standalone

`evaluate-skill` ships a dependency-free linter — the mechanical *entry* check (not a verdict). Useful in CI or pre-commit when you author skills:

```bash
python skills/evaluate-skill/scripts/lint_skill.py <path-to-a-skill>
python skills/evaluate-skill/scripts/lint_skill.py --check <path>   # exit non-zero on blocking (CI)
```

This repo dogfoods it: [`.github/workflows/lint-skills.yml`](./.github/workflows/lint-skills.yml) runs the linter on every skill here on each PR.

## Layout

```
skillwise/
├── .claude-plugin/
│   ├── marketplace.json    # addable as a Claude Code marketplace
│   └── plugin.json         # the repo is itself one plugin
├── skills/
│   ├── evaluate-skill/     # SKILL.md + scripts/lint_skill.py
│   ├── write-skill/        # SKILL.md
│   ├── seek-skill/         # SKILL.md
│   └── improve-skill/      # SKILL.md + references/{rubric,ratchet-protocol,failure-driven}.md
├── shared/
│   └── effect-gate.md      # the one measurement gate, referenced by evaluate + improve
├── docs/
│   ├── THEORY.md           # self-contained derivation + references
│   └── theory.html         # illustrated step-by-step walkthrough
├── .github/workflows/lint-skills.yml
├── CONTRIBUTING.md
├── README.md
└── LICENSE
```

The `skills/<name>/SKILL.md` shape is exactly what `npx skills` auto-discovers and what the `.claude-plugin/` manifests declare — one structure serves both the `npx skills` ecosystem and the Claude Code marketplace, with no duplicate maintenance.

## Forking this

If you fork to publish under your own account, update your identity in three places so the install commands resolve: the repo slug throughout this README, and the `owner` / `author` fields in `.claude-plugin/marketplace.json` and `.claude-plugin/plugin.json`. Once the repo is public, installs via `npx skills add` surface it on skills.sh automatically — there's no separate registry submission.

## Design notes

Each meta-skill obeys the theory it encodes: all are declarative rather than step-marches; `evaluate-skill` ships a mechanical entry check but defers the guarantee to a semantic read; `improve-skill` and `seek-skill` specify only a stopping condition, role separation, and gates, leaving iteration to the engine. `evaluate-skill` judges in two tiers — a static structural verdict and a behavioral effect-delta verdict — converging to one `gate_pass`; the effect tier and its JSON schemas live once in [`shared/effect-gate.md`](./shared/effect-gate.md). `improve-skill` reuses that gate for its per-round keep/revert decision — on the gate's *improvement* branch (does this edit beat the skill's previous version?), while `evaluate-skill` and `seek-skill` use its *existence* branch (does this skill beat no-skill?). Empirical claims throughout are cited to published work, listed in the References section of [`docs/THEORY.md`](./docs/THEORY.md).

## License

MIT — see [`LICENSE`](./LICENSE). Contributions welcome; see [`CONTRIBUTING.md`](./CONTRIBUTING.md).
