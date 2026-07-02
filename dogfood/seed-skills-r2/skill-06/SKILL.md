---
name: prod-data-deletion
description: Execute or review deletions of production data — user accounts, records, buckets, tables. Use whenever anything in production is about to be permanently removed, including "obviously safe" cleanups.
---

# Production data deletion

This protocol is expensive on purpose. Deletion is the one operation with no undo: the cost below is the price of irreversibility, and it does not scale down for "small" deletions — small is how the incidents start.

## Required, none waivable

- **Dry run first**: the exact deletion, executed in count-only/list-only mode, its output saved. The dry run's object count is the number the real run must match.
- **Archive before delete**: a restorable archive of everything in scope, checksummed, its location recorded. An archive nobody verified restores from is not an archive — restore one sampled object.
- **Second context signs the scope**: whoever wrote the deletion does not confirm the scope; a fresh context (or the human owner) reads the dry-run output cold and signs it.
- **Staged execution**: irreversible steps run against a 1% sample first; the full run proceeds only if the sample's post-checks pass.
- **Post-verification**: object counts match the dry run; nothing outside scope is gone (spot-check adjacent data); the archive is intact after the run.

## Never

- Never delete on a verbal "yes" — the signed scope is the authorization.
- Never batch unrelated deletions into one run to save process overhead.
