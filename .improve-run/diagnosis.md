# Phase A baseline diagnosis — `evaluate-skill`

Type: composite (judgment + control). Tier: production/library. Read-based diagnosis to *aim* the
next bounded edit; the keep/revert is the gate's job, not this score.

| # | dimension | anchor | note |
|---|---|---|---|
| 1 | Trigger & frontmatter | 8 | routes by task + colloquial ("is this skill any good?"), but **no negative when-to-use** (when to reach for improve/seek/write instead) |
| 2 | Workflow clarity (control) | 9 | two-tier → one-gate flow is clear and declarative |
| 3 | Failure-mechanism encoding | 8 | five tests each name a defect; `static_only` / fatal branches encoded |
| 4 | Executable specificity (relaxed) | 8 | scorecards + JSON schema concrete |
| 5 | **High-risk-action blacklist** | **7** | the evaluator's own footguns (report `pass` on unrun layer, rewrite instead of locate, waive a Tier-2 fatal) are **scattered across prose**, not a dedicated "never do" section |
| 6 | Checkpoint design (seam) | 8 | "draft & confirm held-out set before scoring" is the seam checkpoint |
| 7 | Architecture conciseness | 9 | ~100 lines, detail in effect-gate.md |

**Weakest dimension: #5 high-risk-action blacklist.**
The known failure modes of *an agent running this evaluation* — overreading a static pass, rewriting
when it should only locate, waiving a non-waivable fatal — are all stated somewhere, but never as one
hard "never do" fence. A judgment skill leans on negative fences (rubric: "taste = negative fences").

**Round-1 hypothesis:** consolidating the scattered prohibitions into one dedicated "Never" section
(≤30 lines, no new policy — only collecting existing rules) will reduce false-`pass` and rewrite-creep
on T1/T2/T3 without hurting the clean-skill case T4.

**One defect per edit. ≤30 changed lines.**
