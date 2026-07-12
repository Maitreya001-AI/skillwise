# improve-run-a5 · round 3 — ca4 at k_test=5 · **SUSPENDED by owner** (not a ratchet outcome)

**Candidate ca4** = ca3 + two clauses from round 2's fatals: (a) the silent-failure token
boundary (machine-consumed artifact failing silently → `wrong-form`, reserve `no-exit` for
skills that declare no product check at all — fix ADV2); (b) honestly-declared manual exits
are seam declarations, never delivery claims. Diff vs entry ≈ 26 lines, within the bounded step.

**Screen (8 seeds ×2)**: round-2 fatals cured (15 → 1.0, 25 recovered on medians), all four
brokens (08/15/16/27) and both round-1 cures (01/14) held, zero regressions.

**Authoritative gate (22 seeds × k_test=5, variance hardening)**: suspended by the owner
(2026-07-12, final call: per-round wall-clock too heavy for an interactive session) with
**91/220 samples completed and cached** across three partial attempts (two OAuth expiries,
one deliberate stop). **No gate object was produced; ca4 is neither kept nor reverted.**
The cached samples live in a gitignored `.wise-runs`-style out dir; a future session can
finish the round for roughly 60% of its price by re-invoking the runner with the same
`--out` (config: 22-seed working set, k_test=5, stored A5 references; candidate text
preserved here as `ca4-SKILL.md` / `ca4.diff`). Before any long resume: `claude setup-token`.

**State of the ledger at suspension**:

- Rounds consumed on this set: 7 of the 10-cap (5 in July + rounds 1–2 here). Round 3 pending.
- The working hypothesis (from rounds 1–2): the remaining defect is per-seed judge variance ×
  the zero-tolerance floor — each candidate cures its targets, a different boundary pair
  flips; k=5 was the variance attack. Unfalsified either way.
- Confirm slice {02, 04, 07, 13, 21, 26, 28} remains **unburned** — no round, screen, or
  diagnosis has touched it; it stays valid for whichever candidate eventually lands.
- Entry version (`skills/evaluate-skill` @ the A5 fail) remains the accepted version; the
  pinned verdict remains **fail** (`wise-eval.json`).
