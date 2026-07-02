# dogfood/ — the self-reference ledger

skillwise's own skills must clear the ruler they apply to others. This directory keeps that account honest: it holds **experiments, not product surface**. CI never runs anything here (cost); the repo's CI stays lint-only.

## Current honest grades

By their own tier classification all four meta-skills are **production/library**, so the effect layer (L2 — the only certifying layer, `docs/THEORY.md` §7) is *mandatory* for them. Per the gate's resolution order, required-but-unrun resolves to **`static_only`**, not `pass`; and a run that fails resolves to `fail`, recorded here rather than euphemized:

| skill | tier | structural layer (L0 entry + static read) | effect layer (L2) |
|---|---|---|---|
| evaluate-skill | production | checked (linter clean; adversarially reviewed) | **ran 2026-07 → `fail` (reproduced negative transfer)** on the hardened seed set with sonnet judges: +0.17 on broken-skill detection, −0.25 on good-skill preservation. Gap confirmed real (`no_skill` 0.75). Routed to `improve-skill` per the sub-floor rule; repair target: weld §4's pricing discipline into the form check. See [`evaluate-delta-run/results.md`](./evaluate-delta-run/results.md). |
| write-skill | library | checked | **not run** → `static_only` |
| seek-skill | production | checked | **not run** → `static_only` |
| improve-skill | production | checked | **not certified** → `static_only` (one live KEEP demo on `write-changelog-entry`, `delta_step +0.375`; plus one full ratchet round on evaluate-skill itself, 2026-07 — verdict **REVERT**: the screened candidate showed `delta_step 0.000` with two median regressions and was mechanically rolled back; see [`improve-run-evaluate-skill/round-1.md`](./improve-run-evaluate-skill/round-1.md). Anecdotes of the loop enforcing its fatals, not a held-out certification of the skill) |

"Each meta-skill obeys the theory it encodes" remains a claim about the **structural layer only** — and the first behavioral measurement made the distinction concrete: the kernel's static read is clean, and its measured existence delta on a hard set was *negative*. That is the framework working, not failing: a static pass is not a verdict, and the gate exists precisely to catch this before "obeys the theory" gets quoted as certification. The README carries the same qualification.

## What would close the account

- [`evaluate-delta.md`](./evaluate-delta.md) — the kernel's L2 experiment: the only design that can certify `evaluate-skill` (and, by the same harness, the other three).
- [`ablation.md`](./ablation.md) — the standing falsification audit of THEORY §2's exhaustiveness claim (the theory's own volunteered death).

Results, when they exist, land in this directory next to their designs — with the gate's full report shapes (`power`, `noise_band`, `judges`, per-task medians), not summaries.
