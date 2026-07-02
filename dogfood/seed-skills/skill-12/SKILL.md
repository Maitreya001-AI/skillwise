---
name: changelog-entry
description: Write changelog entries in this repository's format and tone. Use when release notes or a changelog entry are needed, when closing a user-visible change, or when asked "add this to the changelog".
---

# Changelog entries

## Format facts

- File: `CHANGELOG.md`, newest release first.
- Within a release, categories appear in this fixed order in the artifact: **Added, Changed, Fixed, Removed** — this is an ordering the finished file must exhibit (readers and tooling rely on it), so it is part of the exit check below; it does not constrain the order you work in.
- One entry per user-visible change, imperative mood, sentence case, period at the end, issue/PR reference in parentheses.

## Fences

- Never write marketing copy ("blazing fast", "revamped") — state the observable change.
- Never log internal refactors with no user-visible effect; those live in git history, not the changelog.
- Never bundle unrelated changes into one entry.

## Exit

Check the finished entry set against: category order as specified, every entry referenced (issue or PR), imperative mood throughout, no fence violations. A diff of CHANGELOG.md that fails any of these is not done, however complete the code change is.
