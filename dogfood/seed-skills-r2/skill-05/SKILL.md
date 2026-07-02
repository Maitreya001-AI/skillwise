---
name: payments-webhook-integration
description: Integrate with the internal payments service's webhooks — event types, delivery semantics, and handler conventions. Use when building or reviewing a consumer of payment events (charges, refunds, disputes).
---

# Payments webhooks

## Delivery

- Webhooks POST to your registered endpoint; register via `POST /v1/webhook-endpoints` with your service name and URL.
- Delivery is at-least-once; dedupe on `event.id` (a ULID) — consumers keep a 7-day dedupe window.
- Retries back off at 1m, 5m, 30m, 2h, then hourly for 24h; a 2xx stops retries, a 410 unregisters the endpoint.
- Events arrive in order *per object* (a charge's events are ordered; different charges interleave).

## Event types you will see

| type | fired when |
|---|---|
| `charge.settled` | funds captured and cleared |
| `charge.failed` | terminal failure (see `failure_code`) |
| `refund.completed` | refund cleared back to the customer |
| `dispute.opened` | chargeback opened; respond within 7 days |
| `dispute.closed` | outcome in `disposition` |

## Handler conventions

- Verify the request signature per the shared-secret scheme before trusting the payload, then parse.
- Handlers are idempotent and fast (< 2s); anything slow goes through your own queue.
- Never acknowledge (2xx) an event you failed to persist.

## What correct looks like

A staging replay of last week's event stream processes cleanly: zero duplicate side-effects, zero unverified payloads accepted, dispute events acknowledged within the SLA.
