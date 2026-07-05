---
name: postmortem-language
description: Write incident postmortems in this org's blameless register. Use when drafting or editing a postmortem, an incident summary, or the analysis section of an incident review doc.
---

# Postmortem language — the blameless register

Postmortems are read aloud in the weekly incident review; the register below is what keeps that room honest instead of defensive.

## Fences

- No individual is ever the cause. "The engineer restarted the primary" becomes "the runbook permitted a primary restart without a replica check."
- "Human error" never appears as a root cause — name the missing guardrail instead.
- Every counterfactual is phrased as an absent system property ("nothing alerted on replication lag"), never as a person's failure to act.
- Timeline entries are observations with timestamps, not judgments — "14:02 deploy finished" not "14:02 the bad deploy landed".
- The word "obviously" and its cousins ("clearly", "simply") never appear; if it were obvious it would not have happened.

## Exit

The incident lead reads the full draft against each fence before the review meeting and edits violations in place; the draft that enters the meeting is the edited one.
