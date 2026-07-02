# dogfood/ — the self-reference ledger

skillwise's own skills must clear the ruler they apply to others. This directory keeps that account honest: it holds **experiments, not product surface**. CI never runs anything here (cost); the repo's CI stays lint-only.

## Current honest grade: `static_only`

By their own tier classification all four meta-skills are **production/library**, so the effect layer (L2 — the only certifying layer, `docs/THEORY.md` §7) is *mandatory* for them. It has not been run as a held-out certification. Per the gate's own resolution order, an effect layer that is required but unrun resolves to **`static_only`**, not `pass`:

| skill | tier | structural layer (L0 entry + static read) | effect layer (L2) |
|---|---|---|---|
| evaluate-skill | production | checked (linter clean; adversarially reviewed) | **not run** → `static_only` |
| write-skill | library | checked | **not run** → `static_only` |
| seek-skill | production | checked | **not run** → `static_only` |
| improve-skill | production | checked | **not certified** → `static_only` (one live KEEP demo exists — `delta_step +0.375` on `write-changelog-entry` — an anecdote of the loop working once, not a held-out certification of the skill) |

"Each meta-skill obeys the theory it encodes" is therefore a claim about the **structural layer only**. The behavioral claim stays open until the experiments below run; the README carries the same qualification.

## What would close the account

- [`evaluate-delta.md`](./evaluate-delta.md) — the kernel's L2 experiment: the only design that can certify `evaluate-skill` (and, by the same harness, the other three).
- [`ablation.md`](./ablation.md) — the standing falsification audit of THEORY §2's exhaustiveness claim (the theory's own volunteered death).

Results, when they exist, land in this directory next to their designs — with the gate's full report shapes (`power`, `noise_band`, `judges`, per-task medians), not summaries.
