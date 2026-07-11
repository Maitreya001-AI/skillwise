# dogfood/ — the self-reference ledger

skillwise's own skills must clear the ruler they apply to others. This directory keeps that account honest: it holds **experiments, not product surface**. CI never runs anything here (cost); the repo's CI stays lint-only.

## Current honest grades

By their own tier classification all four meta-skills are **production/library**, so the effect layer (L2 — the only certifying layer, `docs/THEORY.md` §7) is *mandatory* for them. Per the gate's resolution order, required-but-unrun resolves to **`static_only`**, not `pass`; and a run that fails resolves to `fail`, recorded here rather than euphemized:

| skill | tier | structural layer (L0 entry + static read) | effect layer (L2) |
|---|---|---|---|
| evaluate-skill | production | checked (linter clean; adversarially reviewed) | **`pass` (existence, certifying) — 2026-07-06, on the 29-seed held-out set under the pre-registered behavioral label key** (sonnet judges, isolated; no-skill ×3 = 0.724 vs with-skill ×3 = 0.828; `delta_exist +0.103` > band 0.080; zero reproduced regressions; verdict artifact: [`wise-eval.json`](../skills/evaluate-skill/wise-eval.json)). The entire lift is the wrong-form/silent-drop class (three seeds, 0→1) — the text-checkable class §7 predicts a static method can transmit. **History, all on record:** the 2026-07-03 r2 run `fail`ed (12-seed set, by-construction labels); five improve rounds (incl. the plateau-break) all REVERTed with a distinct failure mode each; Phase-A behavioral labeling then overturned 6 of 16 style-class labels — the "negative transfer" was partly a labeling artifact, and under the corrected key the entry version is floor-clean. Improvement loop terminal: `already_optimal` on this set (decoy-boundary tasks 02/05/17 remain matched-at-floor headroom — see the advisory fix list). See [`improve-run-evaluate-skill/round-5.md`](./improve-run-evaluate-skill/round-5.md) and [`behavioral-labels.md`](./improve-run-evaluate-skill/behavioral-labels.md). **Harness-sensitivity caveat (2026-07-11):** the A5 compiled-runner rerun (same seeds, same behavioral key, sonnet-5, skill auto-routed per-seed instead of force-loaded in one batch context) measured `delta_exist −0.241` with 8 reproduced good-seed regressions and `cost_ratio` 1.648 → **fail** on that harness — the certification stands scoped to its harness; both records stand ([`gate-runner-a5/results.md`](./gate-runner-a5/results.md)). |
| write-skill | library | checked | **not run** → `static_only` |
| seek-skill | production | checked (now two source adapters: `from-traces`, `from-library` — the latter landed 2026-07-06 as structure + docs, per [`docs/decision-from-library.md`](../docs/decision-from-library.md)) | **not run** → `static_only`; the `from-library` adapter's own gate additionally requires rigidity-surface held-out tasks vs an SDK-wrapper baseline (specified in the adapter file, not yet constructed) |
| improve-skill | production | checked | **not certified** → `static_only` (one live KEEP demo on `write-changelog-entry`, `delta_step +0.375`; plus **four full ratchet rounds on evaluate-skill, all REVERT, all fatals enforced mechanically**: rounds 1–2 (c1, d1) `delta_step 0.000` ≤ band; rounds 3–4 (e3, f1c) — averages *improved* (+0.0345 each) and the ratchet still reverted on reproduced per-task floor breaches, the exact case the averages-lie rule exists for. Anecdotes of the loop enforcing its fatals, not a held-out certification of the skill) |

## Measurement debts (standing, explicit)

- **Cost instrumentation: CLOSED 2026-07-11** by the compiled runner (`shared/scripts/gate_runner.py`,
  per-run usage from the CLI's result JSON). First measured cost block, on the A5 rerun of the
  29-seed existence gate: `tokens_with_skill` 24.07M vs `tokens_no_skill` 14.60M → **`cost_ratio`
  1.648** — above the §8-5 fatal threshold (1.5). The debt's history stands for every earlier
  verdict (r1/r2 existence, improve rounds 1–5, the r5 existence re-read): those remain blind on
  the cost axis. **The A5 rerun also did not reproduce the certifying pass** — see
  [`gate-runner-a5/results.md`](./gate-runner-a5/results.md) and the harness-sensitivity note in
  the table above; resolving which harness pins the verdict is the successor debt.
- **Set size**: empirically closed. r2's 12-seed set produced `noise_band_exist 0.289` > max
  showable delta (structurally unable to certify); the r4 29-seed set produced band **0.0398**
  with 4 reproducibly-expressing tasks. Treat ~24+ seeds as the working floor for any future
  certifying attempt (matches r2 limitation #3's prediction).

"Each meta-skill obeys the theory it encodes" remains a claim about the **structural layer only** — and the first behavioral measurement made the distinction concrete: the kernel's static read is clean, and its measured existence delta on a hard set was *negative*. That is the framework working, not failing: a static pass is not a verdict, and the gate exists precisely to catch this before "obeys the theory" gets quoted as certification. The README carries the same qualification.

## What would close the account

- [`evaluate-delta.md`](./evaluate-delta.md) — the kernel's L2 experiment: the only design that can certify `evaluate-skill` (and, by the same harness, the other three).
- [`ablation.md`](./ablation.md) — the standing falsification audit of THEORY §2's exhaustiveness claim (the theory's own volunteered death).

Results, when they exist, land in this directory next to their designs — with the gate's full report shapes (`power`, `noise_band`, `judges`, per-task medians), not summaries.
