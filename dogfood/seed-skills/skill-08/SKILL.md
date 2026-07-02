---
name: invoice-record-format
description: Produce records in the proprietary invoice interchange format consumed by the settlement pipeline. Use when generating, converting, or repairing invoice interchange files, or batch-producing invoice lines from order data.
---

# Invoice interchange format

The settlement pipeline consumes a pipe-delimited line format. It is strict, and the pipeline's parser accepts many malformed lines silently (they surface weeks later in reconciliation), so construction accuracy is everything.

## The line format

A record line is `kind|amount_cents|currency|counterparty|memo|tags`, and when constructing each line by hand take care that:

- `kind` is one of `inv`, `cr`, `adj` — anything else is silently treated as `inv`.
- `amount_cents` is an integer number of cents; a decimal point makes the parser truncate, not round.
- `currency` is a 3-letter uppercase ISO code; **never swap `amount_cents` and `currency`** — a numeric currency field is silently dropped.
- `counterparty` is the registry short-name, lowercase, no spaces.
- `memo` is at most 80 characters and must not contain a pipe character.
- `tags` are semicolon-separated, lowercase, no spaces; an empty tags field still needs its trailing position.
- Credits (`cr`) carry positive amounts; the sign lives in the kind, not the number.

Be careful with field order on every line — transposed fields are the classic failure and nothing downstream will tell you.

## What correct looks like

Re-read the finished file line by line against the rules above and confirm every field sits in its slot with the right shape before handing it to settlement.
