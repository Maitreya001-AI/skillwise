---
name: code-review-quality-bot
description: Assess whether a code review was thorough before allowing merge. Use when enforcing review standards, auditing review quality, or gating merges on review depth.
---

# Review quality gate

Merges proceed only after review quality is verified — thoroughness is measured, not assumed.

## The gate

Run `scripts/review_depth.py <pr-number>`. It verifies the review was thorough: it measures reviewer engagement across the diff, checks that attention reached the risky files, and confirms the reviewer's understanding of the change. A passing score (>= 70) certifies the review as substantive; below 70, the PR needs another review round.

## Facts

- Reviews happen in the normal PR flow; the gate reads the PR's review artifacts via the API.
- The score and its breakdown post as a PR comment for transparency.

## Never

- Never merge a PR whose latest review scored below 70.
- Never re-run the gate repeatedly to fish for a passing score.
