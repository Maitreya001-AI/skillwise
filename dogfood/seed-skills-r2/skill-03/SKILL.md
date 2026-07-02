---
name: docs-table-style
description: Format tables in documentation to the docs team's standard. Use when adding or editing tables in markdown docs, READMEs, or design documents.
---

# Docs-team table style

Our documentation uses a consistent table style; apply it whenever you touch a table.

## The standard

- Use pipe-delimited markdown tables with a header row and a separator row.
- Align the separator row with colons: `:---` for left, `:---:` for center, `---:` for right; numbers right-align, text left-aligns.
- Keep one space padding inside each cell (`| value |`, not `|value|`).
- Column headers are sentence case, not Title Case.
- A table longer than ~15 rows probably wants to be split, or moved to an appendix.
- Do not use HTML `<table>` in markdown files unless colspan is genuinely required.

## What correct looks like

The rendered table has aligned columns, a header row, consistent alignment per column type, and reads without horizontal scrolling at normal page width.
