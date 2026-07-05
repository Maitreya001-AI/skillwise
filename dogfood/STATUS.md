# dogfood/ — the self-reference ledger

skillwise's own skills must clear the ruler they apply to others. This directory keeps that account honest: it holds **experiments, not product surface**. CI never runs anything here (cost); the repo's CI stays lint-only.

## Current honest grades

By their own tier classification all four meta-skills are **production/library**, so the effect layer (L2 — the only certifying layer, `docs/THEORY.md` §7) is *mandatory* for them. Per the gate's resolution order, required-but-unrun resolves to **`static_only`**, not `pass`; and a run that fails resolves to `fail`, recorded here rather than euphemized:

| skill | tier | structural layer (L0 entry + static read) | effect layer (L2) |
|---|---|---|---|
| evaluate-skill | production | checked (linter clean; adversarially reviewed) | **`fail` (r2 existence run, 2026-07) — negative transfer, now localized and in escalated repair.** The r2 run: +0.17 broken-skill detection, −0.25 good-skill preservation, gap real (`no_skill` 0.75). Three improve rounds followed (see below): the working set was hardened until the defect expressed reproducibly (29 seeds, band 0.0398), which **localized the negative transfer to the decoy class** (generic content in org costume; rhetoric-justified order) — and both repair candidates were mechanically REVERTed by the gate (prose under-transmits: 1/3 runs; a forced default over-convicts boundary goods: reproduced floor breach). Terminal routing per the sub-floor rule: **escalated to seek-skill for a structural rethink** — Tier 1 needs a *behavioral* deletion micro-probe, not a better-worded static prediction of it (§7: deletion is L2-native). See [`improve-run-evaluate-skill/round-3.md`](./improve-run-evaluate-skill/round-3.md). |
| write-skill | library | checked | **not run** → `static_only` |
| seek-skill | production | checked (now two source adapters: `from-traces`, `from-library` — the latter landed 2026-07-06 as structure + docs, per [`docs/decision-from-library.md`](../docs/decision-from-library.md)) | **not run** → `static_only`; the `from-library` adapter's own gate additionally requires rigidity-surface held-out tasks vs an SDK-wrapper baseline (specified in the adapter file, not yet constructed) |
| improve-skill | production | checked | **not certified** → `static_only` (one live KEEP demo on `write-changelog-entry`, `delta_step +0.375`; plus **three full ratchet rounds on evaluate-skill, all REVERT, all fatals enforced mechanically**: round 1 c1 `delta_step 0.000` ≤ band; round 2 d1 `0.000` ≤ band; round 3 e3 — average *improved* (+3 decoy tasks fixed in every run) and the ratchet still reverted on a reproduced per-task floor breach, the exact case the averages-lie rule exists for. Anecdotes of the loop enforcing its fatals, not a held-out certification of the skill) |

## Measurement debts (standing, explicit)

- **Cost instrumentation**: the sub-agent harness has not exposed per-run token counts in any run
  to date (r1/r2 existence, improve rounds 1–3) → `cost_ratio` and the §8-5 inertia-cost fatal
  remain **unevaluated** at L2. Every gate verdict so far is blind on one of its four fatal axes;
  qualitative note only (the with-skill arm reads ~9k extra words per run).
- **Set size**: empirically closed. r2's 12-seed set produced `noise_band_exist 0.289` > max
  showable delta (structurally unable to certify); the r4 29-seed set produced band **0.0398**
  with 4 reproducibly-expressing tasks. Treat ~24+ seeds as the working floor for any future
  certifying attempt (matches r2 limitation #3's prediction).

"Each meta-skill obeys the theory it encodes" remains a claim about the **structural layer only** — and the first behavioral measurement made the distinction concrete: the kernel's static read is clean, and its measured existence delta on a hard set was *negative*. That is the framework working, not failing: a static pass is not a verdict, and the gate exists precisely to catch this before "obeys the theory" gets quoted as certification. The README carries the same qualification.

## What would close the account

- [`evaluate-delta.md`](./evaluate-delta.md) — the kernel's L2 experiment: the only design that can certify `evaluate-skill` (and, by the same harness, the other three).
- [`ablation.md`](./ablation.md) — the standing falsification audit of THEORY §2's exhaustiveness claim (the theory's own volunteered death).

Results, when they exist, land in this directory next to their designs — with the gate's full report shapes (`power`, `noise_band`, `judges`, per-task medians), not summaries.
