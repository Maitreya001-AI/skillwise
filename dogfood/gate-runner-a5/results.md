# gate-runner A5 — the 29-seed existence gate, rerun compiled · **fail (certifying)** · 2026-07-11

**What this run is.** Acceptance A5 of the gate-runner build: the first execution of the
29-seed existence experiment through the compiled product surface (`shared/scripts/gate_runner.py`)
instead of the hand-assembled sub-agent harness. Same seeds (`mapping.json`), same
pre-registered behavioral label key (`labels-behavioral.json`), same arithmetic
(`gate_math.py`, pinned to the historical numbers by the A1 equivalence tests). Engine:
claude-sonnet-5, headless CLI, ×3 per arm, 6 parallel workers, scoring fully compiled
(per-seed `out/verdict.json` checked against the label key by script — no judge calls).

**Headline: the standing cost debt is closed — and the verdict did not reproduce.**

| | 2026-07-06 certification | this run (A5) |
|---|---|---|
| harness | sub-agent judges, skill **force-loaded**, all 29 seeds in **one context** per run | engine with skill **auto-routed** from `.claude/skills/`, **one seed per isolated sandbox** |
| engine | claude-sonnet (Agent-tool harness) | claude-sonnet-5 (headless CLI) |
| no-skill pass rate | 0.724 | 0.690 |
| with-skill pass rate | 0.828 | 0.448 |
| `delta_exist` | **+0.103** (> band 0.080) | **−0.241** (band 0.080) |
| reproduced regressions | 0 | **8** — all good seeds (01/09/13/14/20/23/25/28) |
| cost | not instrumented (the debt) | **tokens 24.07M vs 14.60M, `cost_ratio` 1.648; $25.21 vs $14.70** |
| verdict | pass (certifying) | **fail — negative transfer** (resolution order #4; the cost fatal at #5 would fire too: 1.648 > 1.5) |

**The regression mechanism, from the artifacts** (`scores-*.json` here; full per-run trail
local under `.wise-runs/`, gitignored): every one of the 8 regressions is a good seed convicted
as `wrong-form` (occasionally `underfill`) because its prose rules contain mechanically-checkable
invariants without a compiled verifier. The skill's own §4 pricing discipline — *"prose alone is
a wrong-form candidate… word it as an unpriced trade-off, not a defect"* — is exactly the step
the auto-routed, per-seed judges skip. This is the r2-era over-conviction signature, reappearing
under the deployment-realistic harness after the batch-context harness had shown it repaired.

**What stands, what is open.**

- The 2026-07-06 certification **stands, scoped to its harness** (force-loaded batch-context
  judges) — as the r2 fail stood when r5 superseded it. Records never erase each other here.
- This run is the first reading with **all four fatal axes measured** — and on the compiled,
  deployment-realistic surface the skill currently fails two of them (negative transfer; and
  the inertia-cost fatal would fire were the delta in-band).
- Open question, now concrete: **which harness defines the pinned verdict?** The auto-routed
  single-seed harness is closer to how the skill is actually consumed; the batch-context
  harness is closer to how a deliberate review session uses it. The discrepancy itself is a
  finding about harness sensitivity (THEORY §11-2: a gate certifies only to its distribution —
  *and its harness*). Repair direction, if the deployment harness is adopted as canonical:
  the §4 pricing step must survive per-seed contexts — a compiled probe or a verdict-protocol
  binding, not more prose (five prompt-layer attempts already REVERTed; see `dead-ends.md`).

Run config: `k_ref=3, k_test=3`, timeout 600s (300s proved too tight for the with-skill arm),
resume-from-`--out` used twice across an OAuth expiry and transient API drops — no paid sample
was re-bought.
