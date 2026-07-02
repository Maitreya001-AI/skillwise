---
name: analysis-quality-gate
description: Verify that a data analysis or research memo is sound before it circulates. Use when finishing an analysis, reviewing someone's memo, or asked whether the conclusions hold.
---

# Analysis quality gate

An analysis circulates only after it passes the quality verifier — soundness is checked, not vibed.

## The gate

Run `scripts/check_analysis.py <memo.md>`. It verifies the analysis is sound and the conclusions follow from the data: it checks the memo's argumentative completeness, methodological hygiene, and conclusion support. A memo that passes is cleared to circulate; a memo that fails goes back to the author with the failing dimensions.

## Structure facts (what a memo contains)

- Sections: Question, Data, Method, Results, Conclusions, Caveats.
- Conclusions reference the result they rest on; caveats name the data limitation, not generic humility.

## Never

- Never circulate a memo that hasn't passed the gate, whatever the deadline.
- Never edit conclusions after the gate has passed without re-running it.
