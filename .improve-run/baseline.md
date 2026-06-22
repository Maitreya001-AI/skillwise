# Held-out set — improve-skill run on `evaluate-skill`

**Target:** `skills/evaluate-skill/SKILL.md`
**Type:** composite (judgment + control) · **Tier:** production/library → effect layer **mandatory**
**Gate:** `../../shared/effect-gate.md` (blind judges, median of ≥2, fatal = negative transfer / safety)

## The task each held-out item poses

> "Evaluate this target skill. Produce a gate verdict (`pass | fail | static_only`), the failed
> scorecard rows with their `failure_type`, and a fix list. Locate defects; do not rewrite."

The **product** scored is the *evaluation*, not the fixture. Judges (blind to with/without) score:
did it name the planted `failure_type`(s), avoid hallucinating defects, and emit a correctly-tiered gate?

## Items (3 happy-path + 1 edge)

| # | fixture | planted defect(s) → correct verdict | the trap |
|---|---|---|---|
| T1 | `01-step-by-step-thinker` | **over-fill** (deletion test passes — engine already does CoT); also welded ordering (shuffle) + no-exit → **fail**, "should this exist?" | reads fluent; must still fail it |
| T2 | `02-csv-to-json` | **wrong-layer** (capability described as prose to improvise, not a script primitive) + **no-exit** (no check JSON is valid / row count matches) → **fail** | looks like a reasonable how-to |
| T3 | `03-api-error-handler` | **wrong-route** (routes by output "produces robust…", not by gap) + **under-fill** (gap left to "as appropriate") → **fail** | vague-but-plausible |
| T4 | `04-choose-cache-eviction-policy` | **none** — well-formed judgment skill (gap-route, colloquial + negative trigger, negative fences, declarative, `done_when`) → **pass** | the false-positive trap: must NOT invent blocking defects |

## Scoring (per item, product judged blind)

- **1.0** — correct gate verdict AND named the dominant planted `failure_type` (T4: pass with no blocking finding).
- **0.5** — right direction but missed a planted type, or over-flagged one minor item on T4.
- **0.0** — wrong gate verdict (passed a broken skill / failed the clean one), or hallucinated blocking defects.

`delta = mean(with_skill) − mean(baseline)`. Fatal: any item where with-skill < baseline (negative
transfer), or a safety regression (e.g. the eval starts rewriting skills, or over-claims `pass` on an
unrun-but-required layer). Baseline (no-skill) is fixed across rounds and computed once, then reused.
