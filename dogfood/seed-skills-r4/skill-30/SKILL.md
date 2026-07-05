---
name: analytics-event-calls
description: Instrument product analytics events to the growth team's schema. Use when adding tracking calls, naming new events, or wiring properties onto existing events across the app.
---

# Analytics events — the schema rules

Ingest is fire-and-forget: events that don't conform are dropped by the pipeline with no error back to the client. Tracking calls get added across hundreds of call sites as features ship. These rules guarantee the growth dashboards never break.

## The rules

- Event names are `snake_case` verb-object, verb from the approved list: `viewed`, `clicked`, `completed`, `failed`, `started`, `abandoned`. `checkout_completed`, never `completeCheckout`.
- Every event carries `org_id`, `surface`, and `ts_ms` (integer epoch milliseconds — an ISO string is dropped).
- Funnel-class events (`started`/`completed`/`abandoned`) additionally carry `funnel_id` and `step_index` (0-based integer).
- Revenue-class events carry `amount_cents` (integer) and `currency` (ISO 4217) — a float dollar amount is dropped.
- Property keys are `snake_case`; a camelCase key silently becomes an unqueryable column.
- Never reuse a retired event name; the old rows poison the new series.

## Done

Review each new tracking call against the list above as you write it; once the feature ships, the dashboards pick the events up.
