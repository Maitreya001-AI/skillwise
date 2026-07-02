---
name: support-macro-tone
description: Judge and write customer-support macro responses to this team's tone bar. Use when writing or reviewing canned support replies, help-center answers, or escalation templates.
---

# Support macro tone — the bar

The engine writes fluent support copy; what it lacks is this team's tone law, learned from churn postmortems. These are review-time rules for humans and agents writing macros; nothing downstream parses them mechanically.

## Fences

- Never open with an apology template ("We're sorry for the inconvenience") — open with what you're doing about it.
- Never say "as per our policy" — state the policy's substance in plain words.
- Never promise a timeline support doesn't control (engineering ETAs, refund processing by the payment provider).
- Never close with "Is there anything else?" on an unresolved ticket — close with the next concrete step and who owes it.

## Positive shape

First line: the state of their issue now. Middle: what happens next and when they'll hear from us. Last: one clear ask if we need something from them.

## Exit

Review each macro against every fence above, one at a time, before it enters the macro library — the check is a manual read of the finished macro, and that is deliberate: these are judgment calls about tone, not machine-checkable strings.
