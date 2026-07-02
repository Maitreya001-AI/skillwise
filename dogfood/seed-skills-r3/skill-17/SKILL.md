---
name: oncall-paging-policy
description: Configure paging and escalation policies to this org's on-call standards. Use when creating or editing alerting rules, setting up a new service's escalation, or reviewing paging noise.
---

# Paging policy (org standard)

## The law

- A page means "a human must act within 15 minutes"; anything that can wait an hour is a ticket, not a page. Pages that end in "acknowledged, no action" three times get demoted automatically by the weekly review.
- Every paging rule names its runbook link in the alert body — a page without a runbook fails the alerting linter.
- Escalation: primary (15 min) → secondary (15 min) → team lead; after lead, the incident channel is opened automatically. No policy skips secondary.
- Business-hours-only alerts are explicit (`schedule: business-hours`), never implicit in a rule's threshold.
- New services page their own team from day one — no "route to platform until we're ready".

## What correct looks like

Audit a service's policy: every page maps to a 15-minute action, runbook links resolve, escalation has all three tiers, and the last month's page log shows an ack-to-action ratio above 0.8 (below that, the thresholds are lying to the roster).
