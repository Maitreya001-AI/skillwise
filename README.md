# skillwise

[![effect gate](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FMaitreya001-AI%2Fskillwise%2Fmain%2Fskills%2Fevaluate-skill%2Fwise-eval.json&query=%24.gate_pass&label=effect%20gate&color=blue)](./skills/evaluate-skill/wise-eval.json) [![certainty](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FMaitreya001-AI%2Fskillwise%2Fmain%2Fskills%2Fevaluate-skill%2Fwise-eval.json&query=%24.certainty&label=certainty&color=blue)](./skills/evaluate-skill/wise-eval.json)

The badges read the last **committed** `wise-eval.json` — certification itself runs locally, in your own Claude Code session (`python skills/evaluate-skill/scripts/gate_runner.py run <skill>/tasks.yaml --require-certifying`), using your own login; CI stays lint-only and never spends a token.

**Skills for working on skills.** A small, coordinated toolkit that can **discover, write, evaluate, and improve** agent skills — the `SKILL.md` standard — all derived from one axis: *how much to leave to the engine.*

The four skills spell **WISE** — **W**rite, **I**mprove, **S**eek, **E**valuate. (They run in the order evaluate → write/seek → improve across a skill's life; the acronym is just a happy accident of their names.)

- Full derivation: [`docs/THEORY.md`](./docs/THEORY.md)
- Step-by-step illustrated walkthrough: [`docs/theory.html`](./docs/theory.html)

## The idea in one paragraph

A skill can influence an agent through exactly two channels — injected text and executable programs — and those channels become load-bearing at exactly **four parameter sites of the agent's loop**: the generation site (**Knowledge**, Σ — a missing fact), the action site (**Capability**, Π — a missing reliable primitive), the verification site (**Judgment**, φ — a missing criterion), and the scheduling site (**Control**, γ — a missing non-default loop). *Procedure is not a gap*: a fixed step sequence fills nothing — order is legitimate only in one of **six cells** (dependency, irreversibility, external mandate, epistemic protocol, product order, compiled order), and anything outside them is welded. Where correctness must *hold* rather than merely be *known*, the atom must ship in **compiled form** (a primitive, a verifier, a non-skippable gate). Judgment about skills is layered — **L0** mechanical entry, **L1** reading (a *prediction*, measured near chance), **L2** behavioral with/without comparison, the only certifying layer — and every L2 comparison obeys a **statistical charter**: noise bands, reproduced (median) fatals, a power check before any verdict, confirmation slices against overfitting, cost in the certification, and two separate deltas for two separate questions (should it exist? did this edit help?). One sentence: *intervene only at the loop's defect sites, in the form the engine's failure modes require, and certify only at L2.*

## The skills

| skill | what it is | use it when |
|---|---|---|
| [`evaluate-skill`](./skills/evaluate-skill) | the six-test ruler + the gate (the kernel) | reviewing, grading, "is this skill good?", and as the final check before shipping |
| [`write-skill`](./skills/write-skill) | the ruler run in reverse — author by hand | creating or designing a new skill from a known need |
| [`seek-skill`](./skills/seek-skill) | authoring driven by a corpus — discovery (two source adapters: `from-traces`, `from-library`) | mining or auto-generating a skill from traces or a run; decompiling a library/SDK into a skill |
| [`improve-skill`](./skills/improve-skill) | the ruler in a gated loop | a skill isn't triggering, is over-built, or fails cases; evolving from failure traces |

`evaluate-skill` is the kernel: `write-skill` and `seek-skill` call it as an exit gate, and `improve-skill` calls it as the gate inside its loop. Together they span the skill lifecycle — experience → extraction (`seek`) → consumption and evolution (`improve`) — with hand-authoring (`write`) and judgment (`evaluate`) throughout. Each works alone; they're designed to work together. There is also one **explicit entry**: type `/skillwise <a skill path | a requirement | a corpus>` and it routes you to the right door on observable evidence (a compiled state probe), hands off once, and stops — it never orchestrates, and it stays out of automatic routing (the four skills' own triggers are unchanged).

## Install

Three paths, one repo layout — pick whichever fits your agent. **Every skill folder is self-contained**: the shared measurement gate is materialized into each consumer's `references/effect-gate.md` by `scripts/sync-shared.py` (CI enforces sync with the `shared/effect-gate.md` source), so any single skill survives being copied alone.

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

Then just talk to it — "evaluate this skill", "write a skill for X", "improve this skill from these traces" — and the skills trigger by description. Explicit invocation is namespaced: `skillwise:evaluate-skill`; and `/skillwise` is the explicit front door when you'd rather be routed than pick the skill yourself.

### 3. Manual

Clone, then copy any skill folder into your skills directory (each folder carries everything it needs, including its gate copy):

```bash
git clone https://github.com/Maitreya001-AI/skillwise
cp -r skillwise/skills/* ~/.claude/skills/      # personal
# or  .claude/skills/  for a single project
```

## Use the linter standalone

`evaluate-skill` ships a dependency-free linter — the mechanical *entry* check (L0, not a verdict): frontmatter health, gap-routing, the procedural-step smell (with the six-cell question), a negation-aware exit-surface check, persona residue, compile-candidate hints, length. Useful in CI or pre-commit when you author skills:

```bash
python skills/evaluate-skill/scripts/lint_skill.py <path-to-a-skill>
python skills/evaluate-skill/scripts/lint_skill.py --check <path>   # exit non-zero on blocking (CI)
```

This repo dogfoods it: [`.github/workflows/lint-skills.yml`](./.github/workflows/lint-skills.yml) runs the linter on every skill here on each PR (plus the shared-gate sync check). Green CI covers the structural entry only — see the honesty note in the workflow and `dogfood/STATUS.md`.

## Layout

```
skillwise/
├── .claude-plugin/
│   ├── marketplace.json    # addable as a Claude Code marketplace
│   └── plugin.json         # the repo is itself one plugin
├── skills/
│   ├── evaluate-skill/     # SKILL.md + scripts/lint_skill.py + references/effect-gate.md (synced copy)
│   ├── write-skill/        # SKILL.md
│   ├── seek-skill/         # SKILL.md + references/{from-library,effect-gate}.md
│   └── improve-skill/      # SKILL.md + references/{rubric,ratchet-protocol,failure-driven,effect-gate}.md
├── shared/
│   └── effect-gate.md      # the ONE measurement gate — single editing source for the synced copies
├── scripts/
│   └── sync-shared.py      # materializes shared/effect-gate.md into the three references/ copies
├── dogfood/                # self-reference ledger: honest status + L2 experiment designs (not run by CI)
│   ├── STATUS.md
│   ├── evaluate-delta.md
│   └── ablation.md
├── docs/
│   ├── THEORY.md           # self-contained derivation + references
│   ├── theory.html         # illustrated step-by-step walkthrough
│   ├── two-tier-evaluation.md  # decision history (older section numbering; see its top note)
│   └── decision-from-library.md  # decision record: the decompiler is seek's from-library adapter, not a fifth letter
├── .github/workflows/lint-skills.yml
├── CONTRIBUTING.md
├── README.md
└── LICENSE
```

The `skills/<name>/SKILL.md` shape is exactly what `npx skills` auto-discovers and what the `.claude-plugin/` manifests declare — one structure serves both the `npx skills` ecosystem and the Claude Code marketplace, with no duplicate maintenance.

## Forking this

If you fork to publish under your own account, update your identity in three places so the install commands resolve: the repo slug throughout this README, and the `owner` / `author` fields in `.claude-plugin/marketplace.json` and `.claude-plugin/plugin.json`. Once the repo is public, installs via `npx skills add` surface it on skills.sh automatically — there's no separate registry submission.

## Design notes

Each meta-skill obeys the theory it encodes **at the structural layer** (all declarative rather than step-marches; orders classified into the six cells; gates non-skippable). At the behavioral layer the account is kept in [`dogfood/`](./dogfood/), and it is honest rather than flattering — and it now contains the project's first full arc: the kernel's first L2 run (2026-07) **failed its own existence gate**; five `improve-skill` ratchet rounds were all **mechanically REVERTed** (two with improved averages killed by reproduced per-task floor breaches — the exact case the averages-lie rule exists for); a **pre-registered behavioral labeling pass** (actually running unaided engines) then overturned 6 of 16 contested labels, showing part of the "negative transfer" was a labeling artifact; and under the corrected key `evaluate-skill` **passes its existence gate (certifying)** on the 29-seed set — `delta_exist +0.103` over a 0.080 band, zero regressions, the whole lift concentrated in exactly the text-checkable failure class §7 predicts a static method can transmit ([`wise-eval.md`](./skills/evaluate-skill/wise-eval.md)). The fail, the five reverts, and the pass all stay on record; the other three skills remain `static_only`. A static pass is not a verdict; this is what that sentence costs — and what paying it buys. `evaluate-skill` ships a mechanical entry but defers certification to the behavioral gate; `improve-skill` and `seek-skill` specify only stopping conditions, role separation, and gates, leaving iteration to the engine.

Measurement is specified once, in [`shared/effect-gate.md`](./shared/effect-gate.md), under the statistical charter (THEORY §8): both deltas carry noise bands (2 × SD of three reference re-runs); fatals must reproduce across re-runs (medians); a **power check** precedes any verdict (`n_tasks ≥ 6` to certify — smaller sets yield `pass (indicative)` at best); improvement loops keep a **confirmation slice** the rounds never see; **cost** (`tokens`, `cost_ratio`) is part of certification, with an inertia-cost fatal. `improve-skill` reads the gate's *improvement* branch (does this edit beat the skill's previous version?); `evaluate-skill` and `seek-skill` read its *existence* branch (does this skill beat no-skill?). Before running a full measurement, read the gate's **"Minimum credible configuration"** — a real round costs ~50 task executions plus ~60 judge calls; if that's too much, run the scaffold tier honestly instead of a diluted gate. Empirical claims throughout are cited to published work, listed in the References section of [`docs/THEORY.md`](./docs/THEORY.md).

## License

MIT — see [`LICENSE`](./LICENSE). Contributions welcome; see [`CONTRIBUTING.md`](./CONTRIBUTING.md).
