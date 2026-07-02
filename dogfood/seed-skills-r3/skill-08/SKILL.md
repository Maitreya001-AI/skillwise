---
name: metrics-emission-format
description: Emit application metrics in the internal line protocol consumed by the aggregation pipeline. Use when instrumenting services, adding counters or gauges, or batch-emitting metrics from jobs.
---

# Metrics line protocol

The aggregator consumes a strict line protocol. Its parser **silently drops** malformed lines (a deliberate availability trade-off), so a formatting mistake becomes a gap in the graphs weeks later, with nothing at emit time to tell you. Following the rules below keeps your emission consistent and your series intact.

## The line format

`<metric.name>:<value>|<type>|#<tag1:v1>,<tag2:v2>` — and when writing emitters take care that:

- `metric.name` is dot-separated lowercase, starting with the service name; a name with an uppercase letter is dropped.
- `value` is a bare number; type `c` (counter) accepts integers only — a float counter line is dropped, not rounded.
- `type` is one of `c`, `g`, `ms`; anything else drops.
- Tags are comma-separated `key:value`, lowercase keys, **no spaces anywhere in the tag block** — one space drops the whole line.
- Timestamps are not part of the protocol; the aggregator stamps on receipt. An embedded timestamp field drops the line.
- The tag block is optional but the `#` prefix must be absent when there are no tags — a bare `#` drops the line.

Be careful constructing these by hand in every emitter — the drops are invisible until the graphs have holes.

## Done

When the emitters are written and the service deploys, your dashboards fill in.
