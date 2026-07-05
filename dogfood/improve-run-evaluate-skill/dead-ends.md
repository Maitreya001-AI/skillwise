# dead-ends.md — falsified edits, never retried
- **c1 "default-deny wrong-form gate" (+6/−1 lines)** — screened 10/12 on burned r2 (fixed both
  targeted false positives, kept fake-verifier recall) but **REVERTED at the authoritative gate**
  on r3-working (n=17): delta_step 0.000 ≤ band 0.118; median regressions skill-02 (nogap costume
  judged good by one edited run — a *leniency* error; also a floor breach) and skill-18
  (overfill-order missed by one edited run). Root cause of the null delta: the r3 repair-class
  seeds (03, 09) recite their pricing in-text — exactly the condition where the OLD paragraph
  already works — so the diagnosed defect never expressed in the reference arm and the edit had
  nothing to show. Two lessons: (1) the working set must express the diagnosed defect
  *implicitly* (fixtures where pricing requires judgment, not recitation); (2) cannot rule out
  that "burden of proof is on the finding" wording induces general leniency beyond wrong-form —
  the next candidate should scope the default-deny strictly to the wrong-form verdict sentence.
- **d1 "self-description is a claim, never evidence" (+2 lines, prose decoy discipline)** — screened
  12/12 on burned r2 (only candidate to fix both directions; c4/c5/c6/d2/d3 all ≤10/12) but
  **REVERTED at the round-2 authoritative gate** on the hardened 29-seed working set:
  delta_step 0.000 ≤ band 0.0398; no regressions; entry floor breach on task-03 unrepaired.
  The edit transmitted in exactly 1 of 3 runs (b-2 caught two costume nogaps citing the new rule;
  b-1/b-3 never applied it). Same failure shape as round-1's c1 and r2's pricing clause: a prose
  paragraph does not reliably change verdict behavior where applying it requires judgment —
  which is THEORY §4's form theorem observed on ourselves: content that must HOLD (be applied
  every run) cannot ship merely as declarative text. Round-3 hypothesis: same content, compiled
  into the verdict protocol (forced per-suspect probe in the output contract), not more prose.
- **e3 "default-verdict-unless-quoted" (+2 lines, decoy probes compiled into the verdict protocol)** —
  screened 11/12 on burned r2 (caught the fake-specificity decoy with the right token, zero FP)
  but **REVERTED at the round-3 gate**: the mechanism transmits reliably (all three decoy tasks
  02/03/29 caught in every edited run — the transmission problem d1 died of is solved) yet the
  strengthened default over-fires on genuine goods whose content skirts generic practice:
  reproduced conviction of task-10 (SQL review bar; nogap'd in 2 of 2 runs → median 0, floor
  breach) plus 1-run convictions of task-12/18. Negative transfer relocated, not removed.
  Combined lesson of rounds 2+3: prose under-applies (1/3 runs), forced defaults over-apply —
  the org-specific-vs-generic discrimination is exactly the deletion test, which THEORY §7
  classifies as L2-native; no wording of a static L1 prediction makes it reliably calibrated.
  Do not retry prompt-level variants of this rule. Structural rethink routed to seek-skill:
  give Tier 1 a *behavioral* deletion micro-probe (actually run a no-skill engine on one typical
  task and compare) instead of asking a judge to simulate one.
