# improve-run-a5 · round 2 — ca3 (ca2 + improvisation scoping) → REVERT; the mole moves again

**Candidate ca3** = ca2 + one fence: `underfill` counts only gap-bearing residue — the
engine's share (§5: generic craft mechanics) and the human's share (§6: seam-side material)
are correct design, never findings. Screen (9 seeds ×2): both round-1 breach seeds recovered
(01, 14 → 1.0), underfill broken 27 retained; jitter on 09/25/08 diagnosed as pre-existing
per-run noise, not a new systematic disease.

**Authoritative gate (22 seeds × 3): REVERT.**

| | value |
|---|---|
| prev-accepted → edited | 0.409 → **0.773** (`delta_step +0.364`, same ceiling as round 1) |
| round-1 breaches | **both cured**: 01 = 1, 14 = 1 (the fence transmits at k=3) |
| goods held | 09/10/12/17/18/20/23 all at 1 |
| cost | −3.06M tokens vs reference |
| **fatals** | **task-15 regression + floor breach** (broken wrong-form seed, now missed 2/3 — judges convict `no-exit` instead of `wrong-form`: the ADV2 token confusion, reproduced); **task-25 floor breach** (good seed: the honest "checked by eye" exit read as a delivery claim covering mechanical rules) |

**Diagnosis.** Two rounds, same shape: each edit cures its targets and a *different* pair of
boundary seeds flips — while `delta_step` sits pinned at +0.364. Two forces:

1. Both residues are still **text-checkable calibration gaps**, not the July L2-native
   graveyard: (a) the `wrong-form`/`no-exit` token boundary on silent-failure sites was never
   written down (ADV2, standing since July); (b) ca2's "not a delivery claim" list omitted
   honestly-declared manual exits.
2. **Structural force**: the zero-tolerance floor × per-seed judge variance means ~3 boundary
   seeds with per-run miss rates ≈0.2–0.3 give any candidate only ~60% odds of a clean k=3
   pass — a coin-flip per round even for a correct edit (July's f1c measured the same
   "extreme run variance").

**Round 3 plan**: ca4 = ca3 + the two clauses above (diff vs entry still ≤30 lines); and the
authoritative gate moves to **k_test=5** (medians flip only at 3-of-5) to buy variance
reduction the charter explicitly permits ("every other condition ≥2×") — attacking both
forces at once. Rounds used on this set: 7 of 10 (5 in July + 2 here); if round 3 reverts on
yet another fresh pair, that is three distinct whack-a-mole failures and the loop's honest
terminal is the structural conclusion, not a fourth clause.

Gate object: [`round2-gate.json`](./round2-gate.json).
