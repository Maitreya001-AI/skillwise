---
name: alert-routing-rules
description: Author alert-routing rules for the on-call router. Use when adding a service's paging rules, changing escalation targets, or wiring a new alert class to a team.
---

# Alert routing — authoring rules

The router loads every service's rule file at startup; entries that fail its checks are skipped and noted at debug level, and the router carries on with the rest. Services declare dozens of rules each, usually written in one batch when a service onboards. Write rules this way and pages always reach a human.

## The rules

- `team` must exactly match the team's key in the service registry — a near-miss ("platfrom") routes nowhere.
- `severity` is one of `P0`–`P3`; anything else is skipped at load.
- Every `P0` rule carries **both** a pager target and a fallback channel; a `P0` with only one is skipped as incomplete.
- `escalate_after_minutes` is an integer between 5 and 120; strings ("15m") are skipped.
- A rule's `match` expression uses the router's label grammar — `service="checkout" AND severity>=P1` — unbalanced quotes skip the rule.
- Deleting a team from the registry orphans its rules silently; re-point them in the same change.

## Done

When the rule file is written, read the finished YAML block once more to make sure it looks right, then merge; the router picks it up on the next deploy.
