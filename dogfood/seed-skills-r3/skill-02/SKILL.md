---
name: git-commit-style
description: Write commit messages to the team's standard. Use when committing, reviewing commit history, or asked to clean up a branch's messages.
---

# Team commit style

Our history is read more than it is written; commits follow this shape.

## The rules

- Subject line: imperative mood, <= 72 chars, capitalized, no trailing period ("Add rate limiter to ingest path").
- Body: wrap at 72, explain *why* over *what*; reference issues as `Fixes #123`.
- One logical change per commit; unrelated fixes get their own commits.
- Prefix conventional types where they help: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`.

## What correct looks like

`git log --oneline` reads as a changelog: each line stands alone, no "wip", "more fixes", "asdf". Before pushing, re-read the messages of the commits you are about to push and amend any that fail the rules above.
