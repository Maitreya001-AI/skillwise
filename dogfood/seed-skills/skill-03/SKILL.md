---
name: postgres-migration-guard
description: A non-skippable safety protocol for applying Postgres schema migrations to shared environments. Use when running, writing, or reviewing a schema migration, when asked to "just apply this SQL to staging/prod", or whenever a change touches tables other services read.
---

# Migration guard

The engine can write migration SQL fine. What it does not do by default — and must here — is refuse to treat application and verification as optional. This skill supplies that loop, not the SQL.

## Ordering constraints that are real (and why)

- **Backup precedes apply** — irreversibility: a destructive DDL statement has no inverse once row data is gone. An unarchived backup is not a backup.
- **Verification follows apply** — you cannot assert an outcome you have not measured: row counts and checksums are read *after* the migration, against the pre-migration snapshot's numbers.

Everything else (how you write the SQL, the order of independent statements, tooling) is yours.

## done_when (all of these, none skippable)

- A restorable backup of every touched table exists and its location is recorded in the migration note.
- The migration applied without error on a scratch copy first.
- Post-apply verification passes: row counts match expectation, spot checksums on unchanged columns are identical, and dependent-service smoke queries return.
- A rollback path is written down — either the inverse DDL or "restore from backup", named explicitly.

The gate is not waivable for "trivial" migrations; trivial migrations are where the unarchived-backup habit forms.

## Role separation

Whoever wrote the migration does not sign off the verification numbers; a second context (or the human) reads them cold.

## Never

- Never `DROP`/`TRUNCATE` anything without the backup line item done.
- Never mark done_when satisfied from memory — each item is checked against the artifact (the note, the query output), not recalled.
