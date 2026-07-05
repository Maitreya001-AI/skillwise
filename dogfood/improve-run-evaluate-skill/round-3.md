# Round 3 — REVERT (2026-07-06) → repair escalated (sub-floor routing)

**Same defect as round 2** (decoy leniency), **compiled-er form** per the round-2 diagnosis: the
decoy probes moved from prose into the verdict protocol itself. Candidates e1 (mandatory probe),
e2 (mandatory output field), e3 (default-verdict-unless-quoted); screened on burned r2:
e1 10/12, e2 11/12 (conviction routed through a wrong token with FP-flavored reasoning),
**e3 11/12** (decoy caught with the correct token, zero FP) — e3 picked. Snapshot `f3d9169`,
+2 lines, lint-clean.

## The numbers (edited ×3; reference and floor reused from round 2 per protocol — same set, same entry version)

| | run accuracies | per-seed-median aggregate |
|---|---|---|
| edited (e3) ×3 | 0.828 · 0.897 · 0.862 | **0.897** (`delta_step +0.0345` ≤ band 0.0398) |

- **Gains**: all three reproducibly-failed decoy tasks flipped on medians — costume nogaps 02/03
  and the fake-dependency march 29 (each caught in ≥2 of 3 runs; 03 and 29 in all three). The
  transmission failure that killed d1 is solved: a default-verdict rule gets applied.
- **Fatals (reproduced on medians)**: **task-10** (SQL review bar, good) convicted `nogap` in
  2 of 3 runs — median 0 vs reference 1 and vs no-skill 1; **task-07** (feature-flag underfill)
  dropped to median 0 vs reference 1 and no-skill 0.5. Both are regressions vs previous *and*
  floor breaches. One-run convictions (not reproduced, logged only): task-12, task-18.
- **Ratchet: REVERT** (`git checkout -- skills/evaluate-skill`). The aggregate improved
  (+0.0345) and would still have been within the noise band; either way the reproduced per-task
  fatals decide — the average is void against them. Full gate object: `round3-runs/round3-gate.json`.

## Terminal analysis — why this loop stops here (and where it routes)

Three rounds, one shape: the discrimination this skill needs at its weakest point —
*is this content something a capable unaided engine already produces?* — **is the deletion
test**, and THEORY §7 classifies deletion as **L2-native**: a static read of it is an L1
prediction. Rounds 2–3 measured the two available prompt-level forms of that prediction:

- **prose rule (d1)**: correct content, applied in 1 of 3 runs — under-transmission;
- **forced default (e3)**: applied in 3 of 3 runs, but calibration does not survive the
  forcing — over-conviction of goods whose content skirts generic practice.

No wording makes an L1 prediction reliably calibrated at this boundary; that is the theory's
own claim (§7), now observed on its own kernel twice. Per `improve-skill`'s done_when: no clean
KEEP; the entry version itself still breaches the floor (task-03) — **the repair failed at the
prompt layer**. Sub-floor routing: **escalate to seek-skill for a structural rethink**, with the
concrete hypothesis logged in dead-ends.md: Tier 1 should not *simulate* the deletion test on
suspect-nogap skills — it should *run* a bounded behavioral micro-probe (one typical task,
no-skill engine, compare artifacts), turning the L1 prediction into a small L2 observation.
That is a form change (compile the probe), not another paragraph.

**State after round 3**: tree at entry version (= r2-fail state, negative transfer now localized
to the decoy class); working set r4-29 remains fit (band 0.0398, 4 expressing tasks);
confirmation slice untouched; rounds used: 3 of 10. Runs: `round3-runs/`; screening:
`screening-r2r3/`; labels/mapping now in-repo (runs complete).
