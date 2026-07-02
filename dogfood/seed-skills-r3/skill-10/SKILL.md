---
name: pr-description-protocol
description: Write pull-request descriptions with full review rigor. Use when opening any PR, updating one after review, or preparing a change for merge.
---

# PR description protocol

Review quality starts with description quality; every PR, regardless of size, carries the full packet. The requirements hold in any order.

## Requirements (all PRs, including one-liners)

- **Impact matrix**: a table scoring the change on blast radius, rollback difficulty, data sensitivity, and performance risk (1–5 each), with a justification line per cell.
- **Three-perspective summary**: the change described three times — for a reviewer, for a release manager, and for a future archaeologist.
- **Screenshot or terminal capture** of the change in action, archived even for pure refactors (capture the passing tests).
- **Reviewer briefing**: a suggested review order of the files, with a sentence per file.
- **Self-review transcript**: your own line-by-line pass, written up, attached before requesting review.

## What correct looks like

A reviewer can approve without asking a single clarifying question, and the archaeologist two years out understands why from the description alone.
