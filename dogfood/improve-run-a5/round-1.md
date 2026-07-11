# improve-run-a5 · round 1 — ca2 (pricing-step binding) → REVERT on two floor breaches

**Loop context.** Repair of fix **A5-1** (`skills/evaluate-skill/wise-eval.json`): on the
deployment harness, judges convict good skills `wrong-form` by skipping the §4 pricing step.
Working set = the 29 seeds minus the pre-registered confirm slice
**{02, 04, 07, 13, 21, 26, 28}** (invisible to every round including screening); reference =
the entry version's stored A5 scores (`../gate-runner-a5/scores-with_skill.json`, ×3); floor =
stored A5 no-skill (×3). All runs through the compiled `gate_runner` (improvement branch,
sonnet-5, k_test=3).

**Candidate selection** (screens on 9–10 non-confirm seeds, k_test=2, advisory):

- **ca** — pricing paragraph → quote-binding (wrong-form conviction requires a verbatim
  guarantee-claim or silent-failure-site quote): 4/6 goods recovered, `delta +0.39`. Residue:
  01/23 unrecovered (strong-requirement wording read as guarantee claims; "declared checks"
  read as delivery claims), conviction **rerouting** to underfill/no-exit.
- **cb** — same content as an evidence-schema validity constraint in "Tier 1 emits": weaker
  transmission (goods at 0.5), 08 slipped. Eliminated.
- **cc** — same content inlined in the six-test table row: weakest (2/6 goods). Eliminated.
- **ca2** — ca + two clauses: (i) the binding covers *any* form-of-rules conviction under
  whatever `failure_type` token; (ii) delivery claims ≠ strong operator requirements
  ("must", "non-waivable") ≠ declared criteria/seams. Screen: 01 and 23 both recovered,
  27 (underfill broken) retained — chosen.

**Authoritative gate (22 seeds × 3): REVERT.**

| | value |
|---|---|
| prev-accepted → edited | 0.409 → **0.773** (`delta_step +0.364`) |
| regressions vs previous | **0** |
| brokens | all retained (08/15/16/27 = 1; 17 flipped up) |
| goods recovered | 09/10/12/18/20/23/25 — incl. 10 and 12, the seeds the July e3 round damaged |
| cost | −4.84M tokens vs reference (the binding *shortens* runs) |
| **floor breaches (fatal)** | **task-01, task-14** (ns=1, edited median 0) → mechanical REVERT |
| band note | `noise_band = 0` (the A5 reference aggregates are identical on this slice) — the decision rested entirely on the floor fatals, as designed |

**Diagnosis from the six with-edited verdicts on 01/14**: the wrong-form disease is cured —
both seeds now convict via **`underfill`**, with evidence pointing at material the skill
*correctly* does not carry: 01 — "how to obtain the second sign-off context" (**seam-side**:
§6 says name the checkpoint, don't script the human); 14 — "the generic migration mechanics"
(**engine-share**: §5 requires deleting the engine's share from the text). Conviction urge
reroutes to the last unfenced token.

**Round 2 candidate (ca3)**: ca2 + an improvisation-scoping fence — `underfill` counts only
gap-bearing residue; engine-share and seam-side absences are correct design, never findings.
This is a precision restatement of the improvisation test's own object ("gap-bearing"), not a
static calibration of the L2-native generic-vs-specific boundary (the July graveyard); the
ratchet vetoes if that distinction fails in practice. Diff vs entry: ~21 lines, within the
bounded step.

Raw run trail: local `.wise-runs`-style out dirs (gitignored); gate object:
[`round1-gate.json`](./round1-gate.json).
