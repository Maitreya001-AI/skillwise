---
name: api-error-copy
description: Judge and write user-facing API error messages that meet this product's bar. Use when writing error strings, reviewing them, or deciding whether an error message is good enough to ship.
---

# API error copy — what good looks like

The engine can write error messages; what it lacks is this product's bar for them. That bar is mostly fences.

## Never (the fences)

- Never blame the user ("you entered an invalid…" → state what the system could not do).
- Never expose internals: no stack traces, table names, service names, or upstream vendor names.
- Never end with a bare "please try again later" — if retry is the remedy, say when or under what condition.
- Never use "oops", "uh-oh", or humor in error paths.

## Positive shape

A good message states, in order of importance to the reader: what didn't happen, the most likely reason in the user's terms, and one concrete next action. The stable error code sits at the end in parentheses.

- Good: "This report couldn't be exported — it's still being generated. Try again once its status shows Ready. (EXP-409)"
- Bad: "Export failed: LockTimeoutException in ReportService. Please try again later."

## Exit

Judge each message against every fence above, one by one; a message that trips any fence is not shippable regardless of how clear it reads. Taste beyond these fences (phrasing, warmth) is the writer's call — the fences are not.
