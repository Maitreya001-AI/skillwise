---
name: release-notes-format
description: Write release notes in the product's canonical format. Use when drafting release notes, announcing a version, or converting a changelog into customer-facing notes. This skill ships to many agent runtimes (Claude, Cursor, Copilot CLI and others) via the shared skills registry.
---

# Release notes — canonical format

**A note on form, first.** The rules below are machine-checkable, and in a single-runtime home they would ship as a validator script. This skill is distributed through the cross-agent registry to 40+ runtimes, several of which cannot execute bundled scripts at all — so the rules stay prose and the exit is a manual checklist. That is a priced trade-off (portability bought with enforcement), not an oversight: if you are using this in a runtime that executes scripts, you are welcome to compile the checklist.

## The format

- Title line: `<product> <version> — <one-phrase theme>`.
- Sections in the finished notes, in this order: **Highlights** (max 3), **Improvements**, **Fixes**, **Deprecations** (omit empty sections except Deprecations, which must appear even as "None").
- Each item: user-observable behavior first, feature name second; no internal ticket IDs; links only to public docs.
- Deprecations state the removal version and the migration path, always.

## Exit checklist (run it on the finished artifact, item by item)

1. Section order matches the specification above; Deprecations section present.
2. Every item passes the "user could notice this" test — anything only an engineer could observe is cut.
3. Every deprecation has a removal version and a migration link.
4. No ticket IDs, no internal hostnames, no marketing superlatives.
