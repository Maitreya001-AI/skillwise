---
name: datadog-dashboard-conventions
description: Build Datadog dashboards to this org's conventions so on-call can read them at 3am. Use when creating or editing dashboards, adding monitors' companion views, or reviewing a dashboard PR.
---

# Dashboard conventions (org)

## Facts the engine can't guess

- Layout: top row is always the service's four golden signals (rate, errors, latency p95, saturation), in that left-to-right order — on-call muscle memory depends on it.
- Colors: red is reserved for error-class series; deploy markers are the vertical gray bars from the `deploys` event stream — never draw your own.
- Every timeseries widget titles as `<metric> · <aggregation> · <scope>`; no default "Timeseries" titles survive review.
- Template variables: `$env` and `$service` on every dashboard, defaulted to `prod` and the owning service.
- Dashboards live in the `team-<name>` folder and are terraformed — console-only dashboards get deleted by the weekly sync.

## What correct looks like

Open the dashboard cold: the golden-signal row reads left to right, every widget title parses as metric·agg·scope, `$env`/`$service` exist and default correctly, and the terraform plan for the dashboard resource is empty (console matches code).
