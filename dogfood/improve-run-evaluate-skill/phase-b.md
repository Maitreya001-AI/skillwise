# Phase B — harness

- Target: skills/evaluate-skill (composite: Judgment + Capability; production tier).
- Entry state (Phase A): existence gate FAIL on r2 hardened set — reproduced negative transfer
  (see dogfood/evaluate-delta-run/results.md). Sub-floor routing: gap real -> negative transfer
  is the first repair target. Diagnosed single weakest defect: **form-check precision** — the
  §4 pricing clause does not transmit; carriers emit wrong-form on good skills (r2: skill-02
  both runs, skill-06 one run).
- Held-out set: dogfood/seed-skills-r3 (24 fresh seeds authored for this loop; never used for
  diagnosis). Working slice: skill-01..18 (9 good / 9 broken). **Confirmation slice: skill-19..24
  (3 good / 3 broken), invisible to all rounds** — read only at the terminal check.
- Power (working slice): n_tasks=18, resolution=0.056, adequate=true (>=6).
- Screening substrate: dogfood/seed-skills-r2 (burned by diagnosis; never authoritative again).
- Conditions on the working slice: no_skill 2x (floor, per-task medians); previous-accepted 3x
  (reference — band = 2 x SD of the 3 aggregates); edited 2x. Judges: sonnet, fresh isolated
  contexts, variant paths name-neutral (variants/a = previous-accepted, variants/b = edited);
  no judge is told which variant is which or that an improvement loop is running.
- Round cap: 10 (default). Bounded step: <=30 changed lines inside skills/evaluate-skill/.
- Cost: sub-agent token counts not exposed by the harness -> cost_delta recorded as n/a (advisory).

## Amendment (logged 2026-07-03, after gate run ns-2 arrived, BEFORE any a/b result)

**skill-11 excluded from scoring (working n: 18 -> 17; resolution 0.0588, still adequate).**
Reason: seed-authoring error — its SKILL.md references `scripts/pii_fields.yaml`, which was
never created. The dangling reference is an objective, judgment-free defect (file existence),
so the seed's ground-truth label ("good") is contaminated: careful judges who check the
reference are penalized by the label, careless ones rewarded. Exclusion applies identically
to all conditions (ns / a / b). Decision recorded before any variant-arm result was received.
