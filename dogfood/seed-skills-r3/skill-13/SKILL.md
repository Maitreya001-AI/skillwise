---
name: quarterly-forecast-model
description: Build and review the quarterly revenue forecast in this org's model structure. Use when preparing the quarterly forecast, updating assumptions mid-quarter, or reviewing finance's numbers.
---

# Quarterly forecast (org model)

## Structure facts

- The model lives in `finance/forecast/<year>-Q<n>/`; inputs in `assumptions.yaml`, never inline in formulas.
- Revenue decomposes as pipeline x stage-weighted close rates + renewals x (1 − churn) + expansion; the three terms are computed and reviewable separately.
- Stage weights come from the trailing-4-quarter cohort table, recomputed each quarter — never carried forward.
- Every assumption line carries its source and date ("churn 2.1% — cohort table 2026-06-15").

## Declared checks (the machine's share)

- The three terms sum to the headline; assumptions.yaml has no orphan entries; every weight traces to the cohort table; sensitivity tab shows ±20% on the top three assumptions.

## The seam (the human's share)

Two calls stay with the finance owner, beyond the declared checks: overriding a cohort-derived weight on qualitative information (a known one-off deal), and the final call on which scenario (base/bull/bear) goes to the board. The model flags these for sign-off; it does not make them.
