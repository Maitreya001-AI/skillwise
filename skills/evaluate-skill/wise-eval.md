# wise-eval — evaluate-skill · existence gate · **fail (certifying)** · 2026-07-11

**Verdict.** On the deployment harness — the compiled `gate_runner`, skill auto-routed from
`.claude/skills/` and applied to one seed per isolated sandbox, the way the skill is actually
consumed — `evaluate-skill` loses to the no-skill baseline with reproduced negative transfer:

| | value |
|---|---|
| no-skill pass rate (medians, ×3 runs) | 0.690 |
| with-skill pass rate (medians, ×3 runs) | 0.448 |
| `delta_exist` | **−0.241** |
| `noise_band_exist` (2×SD of 3 no-skill aggregates) | 0.080 |
| reproduced regressions | **8** — all good seeds (01/09/13/14/20/23/25/28) |
| cost (first measured block) | 24.07M vs 14.60M tokens, **`cost_ratio` 1.648** |
| power | n=29, resolution 0.034, adequate → **certifying** |

**Scope (read before quoting).** Existence branch; the dogfood r3/r4 29-seed set under the
pre-registered behavioral label key; engine claude-sonnet-5; assertions fully compiled (verdict
JSON checked against the label key by script — no judge in the loop). The 2026-07-06
`pass (certifying)` **stands scoped to its harness** (skill force-loaded into batch-context
sub-agent judges); the owner decided 2026-07-11 that the deployment harness pins this verdict —
it matches the gate protocol's own "fresh, isolated contexts" rule, matches real consumption,
and is the first reading with all four fatal axes measured. Both records stand.

**The failure, precisely** (per-task medians in `wise-eval.json`): every regression is a good
seed convicted `wrong-form` (occasionally `underfill`) for carrying mechanically-checkable
invariants in prose — the judges skip the skill's own §4 pricing step (*prose without a
guarantee claim is an unpriced trade-off, not a defect*). Meanwhile the 2026-07-06 lift class
evaporated: unaided sonnet-5 already catches silent-drop seeds 15/16 — the engine absorbed
that gap (deletion-test drift). The inertia-cost axis is also red: 1.648 > 1.5 (non-fatal here
only because negative transfer resolves first).

**Routing** (gate's sub-floor rule): the gap is real (`no_skill` 0.690, far from ceiling —
decoy classes remain unsolved by both arms), so this is **negative transfer → improve-skill**,
not retirement. Repair target A5-1: bind the §4 pricing step into the verdict protocol or
compile it as a probe — prompt-layer wordings are exhausted (`dogfood/improve-run-evaluate-skill/dead-ends.md`).

Run record: `dogfood/gate-runner-a5/` (gate object, both arms' scores). Raw per-run trail:
`.wise-runs/evaluate-skill/20260711T172704/` (local, gitignored).
