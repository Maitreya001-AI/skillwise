---
name: terraform-naming
description: Name Terraform resources and modules to this org's grammar. Use when writing new Terraform, reviewing an infra PR, or importing existing resources into state.
---

# Terraform naming grammar

The org's naming grammar for infra, applied at PR review.

## The grammar

- Resource names: `<env>-<team>-<purpose>`, hyphenated, lowercase — `prod-payments-ledger-db`, never `LedgerDatabase2`.
- The `env` segment is one of `dev`, `stage`, `prod`; nothing else, no abbreviations.
- Module directories are nouns for what they provision (`postgres-cluster/`), never verbs (`create-db/`).
- Variables carry units in the name where a unit exists: `timeout_seconds`, `disk_gb` — a bare `timeout` fails review.
- Booleans read as predicates: `enable_backups`, `is_public` — never `backups` or `public`.
- Tags mirror the name segments (`env`, `team`, `purpose`) so cost reports group without regex heroics.

## Exit

At infra PR review, read each new or renamed resource against the grammar, line by line, before approving.
