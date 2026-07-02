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
