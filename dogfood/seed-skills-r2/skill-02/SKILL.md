---
name: warehouse-sql-review
description: Review and write SQL for the analytics warehouse to this team's bar. Use when writing warehouse queries or dbt models, reviewing analytics PRs, or deciding whether a query is fit to schedule.
---

# Warehouse SQL — the team's bar

The engine writes competent SQL; what it lacks is this warehouse's local law, which encodes real cost and lineage constraints.

## House rules (each has a reason)

- Every scheduled model carries a header comment: `-- owner: <person> · consumers: <dashboards/teams> · sla: <daily|hourly>`; a model with no named owner gets deleted in the quarterly sweep.
- Mart tables are named `mart_<domain>__<entity>` (double underscore is the domain separator; the loader splits on it).
- No `SELECT *` in anything scheduled — column changes upstream must break loudly at the model, not silently downstream.
- Timestamps are stored UTC and converted only in the presentation layer; a `CONVERT_TZ`/`AT TIME ZONE` in a mart model is a review blocker.
- Full scans of `events_raw` are budget-gated: anything touching it must filter on the partition column `event_date` first.

## What correct looks like

Review by checking the diff against each rule above, in the artifact (the SQL text), not from the author's description. A query that violates none but reads awkwardly is a style suggestion, not a blocker — taste beyond these rules belongs to the author.
