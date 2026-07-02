---
name: api-deprecation-notices
description: Write API deprecation notices and changelogs in the product's mandated structure. Use when deprecating an endpoint, field, or behavior, or reviewing a deprecation announcement.
---

# API deprecation notices

## The mandated shape (the artifact's order, not your workflow)

The published notice must present, in this order: **what changes → who is affected → timeline → migration → escape hatch**. That order is a property of the finished document — support routes customers by it, and the deprecation tooling parses the timeline block by position. Draft in whatever order you like; the artifact exhibits this one.

## Facts

- Timelines follow the support contract: 12 months for GA endpoints, 6 for beta, stated as dates not durations ("removed 2027-07-01", not "in 12 months").
- Every notice names the replacement or states plainly that none exists — "we recommend evaluating alternatives" fails review.
- The escape hatch section states the extension policy (who can request, maximum length) even when the answer is "none".

## Fences

- Never soften the removal date ("we currently plan to…") — dates are commitments here.
- Never batch unrelated deprecations into one notice.

## Exit

Check the finished notice: sections present and in the mandated order, dates absolute, replacement named or absence stated, extension policy present. The tooling's parse of the timeline block is part of CI for the docs repo.
