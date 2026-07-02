---
name: dependency-upgrade-protocol
description: Upgrade third-party dependencies safely. Use when bumping a library version, responding to a security advisory, or doing the monthly dependency sweep.
---

# Dependency upgrades

Upgrades are done one at a time, in a fixed sequence — the discipline is the sequence.

1. **Read the changelog first.** Always start here; nothing else may happen before the changelog is fully read.
2. **Bump the version second**, in its own commit.
3. **Run the full test suite third.** Tests must come after the bump commit, never against a dirty tree.
4. **Fourth, grep for deprecated API usage** the changelog mentioned, and fix call sites.
5. **Fifth, update the lockfile** and commit it separately.
6. **Last, write the upgrade note** in `deps/notes.md`.

Complete each stage before the next; interleaving them (fixing call sites while tests run, say) is how partial upgrades slip through.

## What correct looks like

The suite is green on the final tree; no deprecated usage the changelog warned about survives; the lockfile diff contains only the intended dependency; the note names the version pair and anything learned.
