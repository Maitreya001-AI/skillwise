---
name: evaluate-skill
description: Judge whether a skill is well-designed and locate precisely what is wrong when it is not. Use this when asked to review, audit, critique, grade, or sanity-check a skill, when someone asks "is this skill any good?", or when a skill seems not to trigger, feels over-engineered, or reads as too procedural. Use it automatically as the final check before shipping a freshly written or edited skill, and when deciding which of two skill drafts is better.
license: MIT
---

# Evaluate a Skill

A skill is judged in **two tiers that converge to one gate**. Tier 1 is a static structural verdict (is the skill correctly formed?); Tier 2 is a behavioral effect verdict (does it actually improve output?). The derivation is in the skillwise repo's `docs/THEORY.md` (§4); the measurement protocol and all JSON schemas are shared with `improve-skill` in `../../shared/effect-gate.md`.

**The criterion.** A skill is correct iff it *fills the gap the base engine lacks, exactly* — no under-fill, no over-fill, in the right layer, with a verifiable exit — **and** beats the no-skill baseline. Tier 1 catches the first half by reading; only Tier 2 can certify the second. A static pass is not a verdict: skills that read fine still degrade output (see `effect-gate.md`).

## Tier and scope (decide first)

| tier | what runs | gate |
|---|---|---|
| **scaffold** | Tier 1 + one smoke case | effect delta not required |
| **production / library** | Tier 1 + Tier 2 delta | effect delta **mandatory** |

Don't put the full delta layer on every skill — a throwaway scaffold needs only static + smoke. Classify the skill type too (Knowledge / Capability / Judgment / Control / composite); it selects which scorecard rows apply.

---

## Tier 1 — structural verdict (static)

### Mechanical entry (cheap)

```
python scripts/lint_skill.py --check <path-to-skill>
```

Frontmatter health, gap-routing of the `description`, the procedural-step smell, exit surface, capability-backed-by-scripts, length. The linter is the entry, not the verdict — it lowers the frequency of mechanical defects; it cannot certify a skill.

### The five tests (the semantic read)

Run each against the skill's *typical task*. Each catches one defect and names it.

1. **Deletion** — remove the skill, run the task. Still passes → over-fill (it supplies free reasoning). Ask "should this exist?" first.
2. **Improvisation** — count gap-bearing material the engine still had to improvise. > 0 → under-fill.
3. **Shuffle** — hand the primitives in scrambled order. Order-dependent → over-fill (welded procedure).
4. **Inertia-cost** — on a task the engine already handles, with vs without. Costlier, no gain → over-fill.
5. **Exit** — is there a semantic check of the *product* against "what correct looks like"? None → no-exit.

For composites, add the **seam test**: the human checkpoint must sit at the judgment ↔ control/capability boundary.

**Two judges, not one (required).** This semantic read is itself an LLM judgment, and one judge picks the better skill no better than chance (§4). So a Tier 1 verdict runs **≥2 independent judges and takes the median** — the same discipline `../../shared/effect-gate.md` mandates for Tier 2. A lone read is not a Tier 1 verdict.

### Two scorecards — the route face and the output face

Score the two faces separately; they fail for different reasons and route to different fixes.

**Route / trigger** (does it fire when it should, and only then?):

| row | passes when | failure_type |
|---|---|---|
| Routes by gap | `description` says "use when X is missing", not only "produces Y" | wrong-route |
| Triggers on the real cue | fires on typical + colloquial phrasings | wrong-route |
| Doesn't over-trigger | stays quiet on adjacent out-of-scope tasks | wrong-route |

**Output** (is the product good, in the right layer, guaranteeable?):

| row | passes when | failure_type |
|---|---|---|
| Gap fully supplied | improvisation test → 0 | underfill |
| Capability is a primitive | misuse is syntactically impossible | wrong-layer |
| No welded ordering | passes the shuffle test | overfill |
| Judgment/control declarative · `done_when` | not fixed steps | overfill |
| Semantic exit present | compares product against "correct" | no-exit |
| Composite seam placed right | checkpoint at the seam | seam-misplacement |
| Failure mechanisms encoded | key branches as `if X then Y else Z` | (output, brittle) |
| Executable specificity | no hedging where the type forbids it | (output, vague) |
| High-risk blacklist | a dedicated "never do" section | (output, unguarded) |

Apply **type-aware**: for Knowledge/Judgment skills "has a workflow" is N/A; for Judgment skills relax executable-specificity (taste = negative fences). The three reading rows above are the signals that *do* correlate with utility — fluent prose doesn't predict gain and one LLM judge is no better than chance at picking the better skill ([SkillLens](https://dev.to/wonderlab/is-your-agent-skill-actually-good-microsofts-dual-paper-deep-dive-into-skill-evaluation-and-28b7)), which is exactly why the ≥2-judge median above is mandatory, not advisory.

### Tier 1 emits

Per failed (or notable) row, a **finding** in the shared schema (`../../shared/effect-gate.md`): `{id, test, failure_type, passed, location{file,line}, evidence{missing,present_forbidden}, fix_hint, waived}`, plus the **failure_taxonomy** aggregate. `location.file` always; `line` best-effort.

---

## Tier 2 — behavioral effect verdict (delta)

Mandatory for production/library tier. Do **not** re-implement it here — run the shared gate in `../../shared/effect-gate.md`: held-out tasks with-skill vs no-skill baseline, assertions on the *product*, producing `baseline_pass_rate / with_skill_pass_rate / delta / regression_count / safety_regression`. The effect layer passes iff `delta > 0 AND regression_count == 0 AND safety clean`. **Negative transfer and safety regression are fatal and non-waivable.**

Held-out source per the gate: caller supplies tasks; or draft 3 happy-path + 1 edge to `baseline.md` and confirm before scoring; or (scaffold) one smoke case.

---

## Converge to one gate + a fix list

Emit a **json + md pair** (json for machines / CI / `improve-skill`; md for humans), converging to the shared **gate** object: `gate_pass` ∈ `pass | fail | static_only`, plus `tier` and `evaluated_layers` so `pass` is never overread. `static_only` is the honest state when the effect layer was required but no held-out set was available — never report `pass` on an unrun-but-required layer.

End with a **fix list**: each item carries a `finding_id`, a priority, and a hint — built to pipe straight into `improve-skill`. **Locate, don't rewrite** — producing patches is `improve-skill`'s job.

## Waivers

A structural finding may be marked `waived: true` with a recorded reason (e.g. a tiny utility skill legitimately has no high-risk blacklist); the gate then passes *with recorded exceptions*. **Only structural/style findings are waivable.** The Tier 2 fatals — negative transfer and safety — have no waiver path and can never be set aside.

## Stay minimal

One structural report + the output scorecard (+ the route scorecard) + one gate + one fix list. Nothing else — no telemetry, registry, evidence ledgers, report zoo, or dashboards. Before adding any new report, run the deletion test on it: "remove it — does the gate still decide correctly?" If yes, don't add it.
