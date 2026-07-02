---
name: runbook-writing
description: Write operational runbooks for services and alerts. Use when creating a runbook for a new alert, documenting an operational procedure, or improving an existing runbook after an incident.
---

# Runbook writing

## The org's shape

- Runbooks live in `runbooks/<service>/<alert-name>.md`, linked from the paging rule.
- Sections: **What this alert means** (the mechanism, not a restatement of the threshold), **Impact** (who/what is affected right now), **Diagnosis** (the queries and dashboards, as copy-pasteable commands), **Mitigation** (actions with their blast radius noted), **Escalation** (when to stop and page whom).
- Commands are literal and current — `kubectl -n payments get pods`, not "check the pods".
- Every mitigation notes whether it is reversible and how.

## Tone

Written for a responder at 3am who did not build the system: no unexplained jargon, no "simply", no steps that assume tribal knowledge.

## Keeping them good

Runbooks should stay accurate, actionable, and tight — keep them updated as the system evolves and make sure they remain genuinely useful under pressure. Aim for the runbook you wish you'd had during the last incident.
