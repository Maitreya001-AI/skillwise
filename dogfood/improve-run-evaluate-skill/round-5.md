# Round 5 (plateau-break) — REVERT → loop terminates `already_optimal` on this set

**The sanctioned one-per-skill plateau-break** (4 rounds, no KEEP): a larger rewrite compiling
the deletion micro-probe into the skill — `scripts/deletion_probe.py` (isolated headless engine
call fed only name+description; prints the unaided bar beside the skill's rules with a
classification scaffold; exit 3 degrades to `prediction: true`) plus SKILL.md wiring. Branch
`plateau-break-deletion-probe`, snapshot = `3dd3895`'s parent on main. **Scored against the
behavioral key** (Amendment 4; baseline: reference 0.828, no-skill 0.724, band 0.0398,
expressing tasks {02, 05, 17, 24, 29}).

## The numbers (edited ×3, probe-executing judges; sanity screen on r2 first: 10/12, probe mechanics verified live)

| | run accuracies | per-seed-median aggregate |
|---|---|---|
| edited (probe) ×3 | 0.862 · 0.724 · 0.793 | 0.759 (`delta_step −0.069`) |

- **What the probe fixed**: task-24 flipped (+1, the probe's survivors overturned the blanket
  nogap conviction every reference judge made); 03/12/14 + the style goods all protected with
  quoted probe evidence; the most probe-diligent run (b-3) convicted 02 and 05 with clean
  zero-survivor evidence — the exact verdicts the behavioral labels demand.
- **What killed it (reproduced)**: the wrong-form axis collapsed — task-08/15/16 all dropped to
  median 0 (each passed or token-confused in 2 of 3 runs), regressions *and* floor breaches.
  Attention displacement again, now dominant: probe-running judges under-attend the form check.
  Also measured: probe sampling asymmetry — the runtime 1-sample bar is narrower than the
  labeling procedure's 2-sample union, so weak survivors appear and 02/05 escape conviction in
  2 of 3 runs.
- **Ratchet: REVERT** (branch not merged; main untouched). Plateau-break is spent.

## Loop terminal state: `already_optimal` (on this set) — with the finding that reframes the account

Under the behaviorally-corrected key, the **entry version is floor-clean** (zero tasks below
no-skill — `floor_breaches_entry: []`) and sits **+0.103 above the no-skill median aggregate**
(0.828 vs 0.724). Five rounds of edits each either fell within the noise band or triggered a
fatal and reverted; the plateau-break is used. Per `improve-skill`'s done_when that terminates
the loop as **`already_optimal`**: as good as *this set* can show — paired with the standing
recommendation to rotate to a fresh set before trusting it further, and the caveat that the
r2-era existence `fail` was issued on the old set under by-construction labels.

The account-closing question this opens: with no-skill re-run a third time (the existence
branch's 3-run reference), does the entry version now **pass its existence gate on this set
under the behavioral key**? That reading is computed in `existence-r5.json` / STATUS.

Probe disposition: the REVERT judges the *skill directory* (probe-as-Tier-1-step displaces
attention); the probe script itself is retained as **measurement tooling** at
`dogfood/tools/deletion_probe.py` — Phase A's behavioral labeling depends on it and it remains
the reproducible instrument for future label audits. The experiment survives on the branch.
