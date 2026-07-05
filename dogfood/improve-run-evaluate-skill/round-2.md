# Round 2 — REVERT (2026-07-06)

**Target defect** (re-diagnosed in Phase-B Amendment 3, from the 23-seed calibration): **decoy
leniency** — the carrier accepts a skill's self-justifying rhetoric as evidence: generic best
practice in team costume passes as "org-specific" (`nogap` missed), and a welded march with a
plausible rationale passes as justified (`overfill-order` missed). The r2-diagnosed wrong-form-FP
defect did **not** express on implicit-priced tone/visual/SQL-bar/naming seeds (12/12 preserved in
calibration; 6/6 goods of that class preserved in every authoritative run this round).

## What ran

- **Working set**: 29 seeds (Amendment 3; 14 good / 15 broken; resolution 0.0345, adequate),
  copied to neutral names task-01..29, interleaved. Labels out of repo until scoring.
- **Candidates**: two families. c4/c5/c6 (wrong-form-FP scoped — screened before calibration
  showed the defect doesn't express; recorded, not selected). d1/d2/d3 (decoy-leniency scoped).
  Screening on burned r2: **d1 12/12** (only candidate fixing both directions), d3 10/12,
  c4/c5/c6 10/12 each, d2 9/12. **d1 picked** (+2 lines: "self-description is a claim, never
  evidence" — fake-specificity strip test + fake-dependency swap test + FP-guard clause).
- **Snapshot** `4e44584` → applied d1 → authoritative improvement gate: no-skill ×2 fresh,
  previous-accepted (= entry @HEAD) ×3 fresh, edited ×3; sonnet judges, fresh isolated contexts,
  variants name-neutral (a = previous-accepted, b = edited).
- **Run hygiene**: first ns run discarded pre-scoring for an objective mechanical defect
  (verdict/task misalignment in its 11..20 block — each reason describes a neighboring seed);
  replaced with a fresh run. Discard recorded before the gate was computed.

## The numbers

| | run aggregates | per-seed-median aggregate |
|---|---|---|
| no-skill ×2 | 0.793 · 0.793 | 0.793 |
| previous-accepted ×3 | 0.862 · 0.862 · 0.828 | 0.862 (band = 2×SD = **0.0398**) |
| edited (d1) ×3 | 0.862 · 0.862 · 0.862 | 0.862 |

`delta_step = 0.000` ≤ band; regressions vs previous: none; floor breach on **task-03**
(git-commit-style nogap costume: ns median 0.5, both prev and edited median 0) — inherited from
the entry version, not caused by the edit, not repaired by it. Ratchet: **REVERT**
(`git checkout -- skills/evaluate-skill`). Full gate object: `round2-gate.json`.

## What the round established (the useful part)

1. **The set is now fit**: band 0.0398 vs max showable delta 0.138; the four failed tasks
   (02/03/14/29 — three costume nogaps + one fake-dependency march) fail at median 0 across all
   three reference runs. The defect is real, reproduced, and measurable.
2. **The entry version's negative transfer is now localized**: one floor-breach task (task-03),
   plus three tasks where the skill adds nothing over a no-skill judge who also fails them.
   `delta_exist` on this set: +0.069 for both entry and edited versions (band-clearing on
   average, but the per-task fatal stands — the existence verdict for evaluate-skill remains
   `fail` until the decoy class is repaired).
3. **Transmission, not content, is the bottleneck**: d1's rule was applied in exactly 1 of 3
   edited runs (that run caught two costume nogaps, citing the rule verbatim). A prose paragraph
   reads fine and screens perfectly, then fails to change behavior reliably — the same shape as
   round-1's c1 and r2's pricing clause. This is THEORY §4's form theorem observed on ourselves:
   content that must *hold* on every run cannot ship as declarative text alone.

**Round-3 hypothesis** (logged before its screening): same defect, compiled-er form — the decoy
probes forced into the verdict protocol itself (mandatory probe / mandatory output field /
default-verdict-unless-quoted), so that skipping the check invalidates the verdict (A′-1 is the
failure being prevented; §4 requires Control-type content to be non-skippable).

**State after round 2**: tree reverted to entry; no KEEP; confirmation slice (r3 skill-19..24)
still untouched. Cost note: sub-agent token totals were not exposed per-run by the harness this
round either; `cost_delta = n/a` (see the measurement-debt note in STATUS).
