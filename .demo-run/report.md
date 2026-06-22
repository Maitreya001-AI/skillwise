# Live KEEP demonstration — fixed improve-skill on a target with real headroom

Purpose: show the fixed loop actually keep an improving edit (`delta_step`-driven), exercising the
headroom check (Fix B, corrected), the candidate tournament (Fix D), and the honest terminal state
(Fix C). Target chosen so the **current** skill is genuinely imperfect (format rules a base model
misses unaided) → measurable room to improve.

## Target — `write-changelog-entry` (v0, the starting/"current" version)

```
# Write a Changelog Entry
Given a merged PR, write one changelog line.
- Start with a Keep-a-Changelog category in brackets: [Added], [Changed], [Fixed], [Deprecated], [Removed], or [Security].
- Keep it short and clear.
- Reference the PR number at the end like (#123).
```

Omits two rules a base model won't reliably honor: the `[BREAKING]` prefix for breaking changes, and
imperative-mood / no-trailing-period / <=80-char constraints.

## Held-out set (4 PRs) + scoring

Rules per line: correct bracket category; `[BREAKING]` prefix iff breaking; imperative mood; no
trailing period; <=80 chars; PR ref. Score 1.0 (all) / 0.5 (one miss) / 0.0 (2+ miss or wrong tag).
Sealed isolated generators; 2 blind judges (unanimous on all 20 lines).

| condition | T1 fix | T2 breaking | T3 feature | T4 security | mean |
|---|---|---|---|---|---|
| no-skill (floor) | 0.0 | 0.0 | 0.0 | 0.0 | **0.00** |
| current v0 | 1.0 | 0.0 | 0.5 | 1.0 | **0.625** |
| candidate 1 — +[BREAKING] +mood/period/len | 1.0 | 1.0 | 1.0 | 1.0 | **1.00** |
| candidate 2 — +mood/period only | 1.0 | 0.5 | 1.0 | 1.0 | 0.875 |
| candidate 3 — +[BREAKING]/len only | 1.0 | 0.5 | 0.5 | 1.0 | 0.75 |

(no-skill scored 0.00 because Opus, unprompted, wrote prose-style `BREAKING:`/`Security:` lines, not
the bracket category format — a clean illustration that the floor is real here.)

## Decision (fixed protocol)

- **Headroom check (Fix B, corrected):** current v0 = 0.625, below max on T2/T3 → **fit** (not `unfit_test_set`).
- **Tournament (Fix D):** 3 diverse candidates scored vs current; candidate 1 wins (1.00).
- **Improvement gate (Fix A):** `delta_step = 1.00 − 0.625 = +0.375` > noise band; floor intact
  (candidate 1 >= no-skill on every task); no per-task regression vs v0; no safety regression.
- **Ratchet → KEEP.** Terminal state (Fix C): **`improved (+0.375)`**.

## Kept version (v1 = candidate 1)

```
# Write a Changelog Entry
Given a merged PR, write one changelog line.
- Start with a Keep-a-Changelog category in brackets: [Added], [Changed], [Fixed], [Deprecated], [Removed], or [Security].
- Keep it short and clear.
- Reference the PR number at the end like (#123).
- Use the imperative mood ("Add", "Fix", "Require" — not past tense), no trailing period, and keep the whole line under 80 characters.
- For a breaking change, prefix the category with [BREAKING], e.g. "[BREAKING] [Changed] ...".
```

## What this proves

The fixed loop **keeps a real improving edit** decided by `delta_step` (edited vs previous version),
selected from a candidate tournament, guarded by the no-skill floor, and reported as an explicit
`improved` state. Contrast the original failure mode: under the old `delta_exist`-only gate a loop
would reject edits whenever no-skill ceilinged. The pure ceiling case (`delta_exist = 0`,
`delta_step > 0`) is shown by the original evaluate-skill run in `../.improve-run/`; this demo shows
the same machinery keeping an edit end-to-end on a fresh target.
