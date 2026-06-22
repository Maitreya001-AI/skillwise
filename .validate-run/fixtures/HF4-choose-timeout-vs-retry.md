---
name: choose-timeout-vs-retry
description: Decide whether a flaky external call needs a longer timeout or a retry policy when it isn't obvious which. Use when calls intermittently fail and you can't tell if they're slow or genuinely failing. Not for choosing an HTTP client or sizing connection pools.
---

# Timeout vs Retry

Judgment skill: decision fences, not a procedure.

## Decide by failure shape

- Slow-but-succeeds (p99 >> p50, eventual success) → raise the timeout; retry won't help.
- Fast-hard-failures (connection refused, 5xx, then works on resend) → retry with backoff.
- Slow-then-fails (times out near the deadline) → both: trim the deadline AND cap retries to fit the budget.

## Never

- Never retry a non-idempotent write without an idempotency key.
- Never stack retries under a fixed total deadline without shrinking the per-attempt timeout — you'll blow the budget.

## done_when

The choice is justified against the observed failure shape, and the rejected option's failure mode is named.
