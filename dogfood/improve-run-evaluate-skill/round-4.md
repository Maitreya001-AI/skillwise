# Round 4 — REVERT (2026-07-06) → loop stopped; two structural findings

**Same defect** (decoy leniency), **third mechanism family**: the deletion test run as an actual
pre-registration micro-probe (write your unaided bar *before* reading the rules — §3 cell 4 —
then diff, sorting rules derivable vs surviving), plus d1's strip-test as the sorting criterion
and a neutral-domain contrast pair. Candidates f1/f1b/f1c/f2/f3 screened on burned r2:
f1 11/12 but **disqualified for a construction leak** (its contrast pair quoted a working-set
seed's own rule nearly verbatim — the same flaw round-1 rejected c3 for); f1b 10/12; f2 9/12;
f3 11/12 (wrong-form FP resurfaced); **f1c 11/12, zero FP — picked** (+2 lines, lint-clean,
snapshot `ee373fc`).

## The numbers (edited ×3; reference/floor reused per protocol)

| | run accuracies | per-seed-median aggregate |
|---|---|---|
| edited (f1c) ×3 | 0.759 · **0.966** · 0.828 | 0.897 (`delta_step +0.0345` ≤ band 0.0398) |

- **Gains (medians)**: task-02 and task-03 (costume nogaps) flipped — the probe transmits.
- **Fatal (reproduced)**: **task-12** (blameless-postmortem register, labeled good) convicted
  `nogap` in 2 of 3 runs → median 0 vs reference 1 and no-skill 1 — regression + floor breach.
- **Third failure mode measured — attention displacement + judge instability**: run 1 (0.759)
  missed all three wrong-form brokens (08/15/16) that every reference run catches — the probe
  crowded out the form check; run 2 (0.966) is the best single run ever recorded on this set.
  The mechanism works brilliantly or disruptively depending on the judge draw; medians correctly
  refuse it. **Ratchet: REVERT.** Gate object: `round4-runs/round4-gate.json`.

## Why the loop stops here (4/10 rounds used — stopping on evidence, not on the cap)

Four rounds now span the prompt-layer design space for this defect, one failure mode each:

| round | mechanism | failure mode |
|---|---|---|
| 1 (c1) | default-deny paragraph | set couldn't express the defect (null delta) |
| 2 (d1) | prose decoy discipline | under-transmission (applied 1 of 3 runs) |
| 3 (e3) | forced default-verdict | over-conviction (calibration didn't survive forcing) |
| 4 (f1c) | pre-registration micro-probe | attention displacement + run instability |

Two structural findings close the loop:

1. **The prompt layer is exhausted for this boundary** (already routed in round 3, now with the
   taxonomy complete): the org-specific-vs-generic discrimination is the deletion test, L2-native
   per §7. The next form is compiled: a `scripts/` probe that *actually runs* a no-skill engine
   on one typical task and diffs the artifact — Capability, not more Judgment prose.
2. **Ground truth itself is contested at this boundary** (r2 limitation #4, now binding):
   task-12's "good" label — like task-14's "broken" — encodes the seed author's by-construction
   assertion on exactly the axis under test; f1c's strip-test conviction of task-12 ("canonical
   blameless doctrine, derivable") is a *defensible reading*, not obviously an error. Labels for
   nogap-class seeds must be established **behaviorally** (run the deletion test per seed: does
   a no-skill engine's artifact already comply?) before another repair round is meaningful.
   That behavioral labeling procedure is the same compiled probe as finding 1 — build once,
   use for both ground truth and the skill's own Tier-1.

**State after round 4**: tree reverted to entry (r2-fail state, negative transfer localized to
the decoy class); rounds used 4 of 10; confirmation slice still untouched; loop **stopped** with
the seek-level escalation standing. The account stays open at `fail (in repair — escalated)`.
