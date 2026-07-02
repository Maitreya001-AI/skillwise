---
name: csv-ledger-entry
description: Construct and validate entries for the team ledger CSV, whose strict field semantics (integer cents, ISO currency, ordered columns) are easy to get subtly wrong at scale. Use when you need to add, generate, or batch-produce ledger rows, or when someone asks to "book" an expense into the ledger.
---

# Ledger CSV entries

The ledger is a strict-format CSV consumed by the finance importer. Its rules are unforgiving: a row that parses but carries a swapped field silently corrupts the monthly rollup.

## The world

- Columns, in file order: `date` (ISO, UTC), `kind` (`expense | refund | transfer`), `amount_cents` (integer; never a float, never a decimal string), `currency` (ISO-4217, uppercase), `memo` (<= 80 chars, no commas), `tags` (semicolon-separated, lowercase).
- Refunds are positive `amount_cents` with `kind=refund` — not negative expenses.
- The importer treats an unknown `kind` as `expense` (historical bug, kept for compat) — which is why kind typos are dangerous.

## Primitives (use these, don't hand-assemble rows)

- `scripts/build_entry.py --date … --kind … --amount-cents … --currency … --memo … --tags …` — named flags only; it refuses floats, lowercase currency, and comma-bearing memos, so a wrong value has no slot to land in.
- `scripts/check_ledger.py <file>` — the exit check: re-parses every row against the semantics above (types, enums, memo length) and cross-checks that refunds are positive.

## What correct looks like

A batch is correct only when `check_ledger.py` passes on the final file — not when the rows "look right". Run it as the last act on the exact artifact you will hand over.

## Never

- Never edit or delete an existing row to "fix" a mistake — append a compensating `refund`/`transfer` row instead; the importer has already consumed earlier lines.
- Never construct rows by string concatenation when the builder is available.
