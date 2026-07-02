---
name: incident-postmortem
description: Write incident postmortems in this organization's format, with its severity taxonomy and blameless-writing rules. Use when asked to write, draft, or review a postmortem or incident report, or after any S1/S2 incident closes.
---

# Incident postmortems (org format)

## The world (org facts the engine cannot guess)

- Severity taxonomy: **S1** customer-facing outage > 15 min · **S2** customer-facing degradation or internal outage · **S3** near-miss caught before impact · **S4** process failure, no system impact.
- Required sections, and what each is for: Summary (3 sentences max), Timeline (UTC, one event per line), Impact (numbers, not adjectives), Root cause (the mechanism, not the trigger), Action items, Lessons.
- Postmortems live in `runbooks/postmortems/`, filename `YYYY-MM-DD-slug.md`.

## What correct looks like

- Every action item has an owner (a person, not a team) and a date.
- The timeline contains the detection event and the mitigation event explicitly.
- Impact is quantified (requests failed, minutes degraded, customers affected) — an Impact section with no number is not done.
- **Blameless fences**: never name an individual as a cause; never use "human error" as a root cause (name the missing guard instead); no counterfactual blame ("if X had just…").

Before handing over, check the draft against each line above — the checklist is the exit, the prose is not.

## The seam (what stays human)

The declared criteria above are the machine's to enforce. Two calls sit **beyond** them and go to the incident commander, not the engine: the final severity classification when an incident sits between two levels, and any decision to name external parties. Flag these explicitly rather than deciding them.
