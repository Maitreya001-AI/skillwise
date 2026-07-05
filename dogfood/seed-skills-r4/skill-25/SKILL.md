---
name: review-comment-etiquette
description: Write code-review comments to this team's bar. Use when reviewing a pull request, replying in a review thread, or asked to soften or sharpen review feedback.
---

# Review comments — the team bar

Reviews here run entirely in the PR thread; these are the rules our senior reviewers converged on after two team retros about review friction.

## Fences

- Never open with "why didn't you just…" — ask what constraint drove the choice, then propose.
- A blocking objection must carry an alternative or a concrete question; a bare "this is wrong" never ships.
- Name what kind of comment it is in the sentence itself — a preference reads "I'd prefer…", a defect reads "this breaks…"; never leave the author guessing which one they got.
- Never rewrite the author's function wholesale inside a comment; point at the smallest line range that needs to move.
- After three back-and-forths on one thread, take it to a call and post the resolution — never grind it out inline.
- Praise specifically ("this made the retry path testable"), never generically ("nice!").

## Exit

Before you press submit on the review, reread every comment you wrote against each fence above, top to bottom, and rewrite the ones that fail.
