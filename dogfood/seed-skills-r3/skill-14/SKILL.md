---
name: json-formatting-helper
description: Format and prettify JSON for readability in docs, configs, and debugging output. Use when JSON needs to be human-readable, when diffing JSON blobs, or when pasting JSON into documentation.
---

# JSON formatting

Readable JSON is consistent JSON.

## The rules

- Indent with 2 spaces; never tabs.
- Keys in a stable order when hand-authoring (group related keys; ids first).
- No trailing commas (JSON forbids them); no comments (use a sibling `_comment` key only in examples, never in real configs).
- Dates as ISO-8601 strings; avoid epoch integers in human-facing docs.
- For diffs, pretty-print both sides with the same tool (`python -m json.tool` or `jq .`) before comparing.

## What correct looks like

The blob parses (`jq .` exits 0), renders without horizontal scrolling at 80 columns for docs, and two independently formatted copies of the same data produce an empty diff.
