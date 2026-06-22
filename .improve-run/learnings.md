# learnings.md — verified wins (KEEP)

Format: `round | change | delta | note`. Append-only.

r1 | added gate **resolution-precedence** to "Converge to one gate" (blocking non-waived structural finding → `fail`, overrides `static_only`; `static_only` reserved for structurally-clean + effect-unrun) | with-skill 0.875 → 1.00; regressions 2 → 0; delta vs no-skill 0.00 (baseline ceilings at 1.00, so >0 is unreachable on this set). Removed the negative transfer the shipped skill carried; turned a split 0.5/1.0 judge call into unanimous 1.0; also stopped the T4 `pass` over-claim.
NOTE | the win was NOT the Phase-A read-based "blacklist" guess — the round-0 execution traces redirected diagnosis to the gate-resolution defect (failure-driven mode). Trust the gate over the read.
