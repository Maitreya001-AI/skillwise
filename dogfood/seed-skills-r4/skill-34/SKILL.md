---
name: dashboard-authoring-order
description: Build monitoring dashboards in the order that keeps them coherent. Use when creating or reworking a Grafana dashboard for a service.
---

# Dashboard authoring — the order that works

Dashboards built out of order end up incoherent. Build in this order, always:

1. Write every panel's query first, across the whole dashboard, before creating a single panel. Query thinking must finish before visual thinking begins — visual decisions contaminate query design.
2. Then create the panels left-to-right, top-to-bottom, in final layout position. Never move a panel after it is placed; repositioning breaks the reading flow you committed to.
3. Then set thresholds and units on every panel in one pass.
4. Colors and styling come last, in a single dedicated pass. Styling earlier locks in choices the data hasn't justified yet.
5. Never return to an earlier stage once you've moved past it; if a query is wrong, finish the current pass first, then start the whole sequence again from stage 1.

## Exit

The dashboard loads under the service's folder, every panel renders data for the default time range, and the layout reads incident-first (top row answers "is it broken", detail below).
