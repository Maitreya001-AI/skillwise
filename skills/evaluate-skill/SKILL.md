---
name: evaluate-skill
description: Judge whether a skill is well-designed and locate precisely what is wrong when it is not. Use this when you need a verdict on why a skill misbehaves, when asked to review, audit, critique, grade, or sanity-check a skill, when someone asks "is this skill any good?", or when a skill feels over-engineered or reads as too procedural. Use it automatically as the final check before shipping a freshly written or edited skill, and when deciding which of two skill drafts is better. This skill locates and rules; fixing is improve-skill's job.
license: MIT
---

# Evaluate a Skill

A skill is judged in **two tiers that converge to one gate**. Tier 1 is a **static read** — a mechanical entry (L0) plus a structural read that includes L1 *predictions* of the three behavior-native tests; Tier 2 is the behavioral effect verdict (L2), the only certifying layer (`docs/THEORY.md` §7). The six-test ruler is derived in THEORY §6; the two deltas and the statistical charter that governs the gate in §8. The measurement protocol and all JSON schemas are shared with `improve-skill` and `seek-skill` in `references/effect-gate.md` (a synced copy of the repo's `shared/effect-gate.md`) — including the existence-vs-improvement delta split, the noise bands, the power check, the `unfit_test_set` state, and the headroom check. evaluate-skill reads the gate's **existence** branch (`delta_exist` vs no-skill); `improve-skill` reads its improvement branch.

**The criterion (§6).** A skill is correct iff it *fills the gap the base engine lacks, exactly* — no under-fill, no over-fill (in order or in cost), in the right form, with a compiled exit — **and** beats the no-skill baseline beyond the noise band. Tier 1 catches the first half by reading; only Tier 2 can certify the second. A static pass is not a verdict: skills that read fine still degrade output (see `references/effect-gate.md`).

## Tier and scope (decide first)

| tier | what runs | gate |
|---|---|---|
| **scaffold** | Tier 1 + one smoke case | effect delta not required |
| **production / library** | Tier 1 + Tier 2 delta | effect delta **mandatory** |

Don't put the full delta layer on every skill — a throwaway scaffold needs only static + smoke. Classify the skill type too (Knowledge / Capability / Judgment / Control / composite); it selects which scorecard rows apply.

---

## Tier 1 — static read (L0 entry + structural read with L1 predictions)

### Mechanical entry (L0, cheap)

```
# from the repo root:
python skills/evaluate-skill/scripts/lint_skill.py --check <path-to-skill>
# or, from this skill's own folder (e.g. a standalone install):
python scripts/lint_skill.py --check <path-to-skill>
```

Frontmatter health, gap-routing of the `description`, the procedural-step smell, exit surface (negation-aware), capability-backed-by-scripts, persona residue, compile-candidate hints, length. The linter is the entry, not the verdict — it lowers the *frequency* of mechanical defects (§7: L0 touches form only); it cannot certify a skill.

### The six tests (§6 — the semantic read)

Run each against the skill's *typical task*. Each catches one failure and names it. **Three of the six are L2-native**: their definitions contain "run the task", so a static execution of them is an **L1 prediction** — emit those findings with `prediction: true`, and let Tier 2's behavioral result override them once it runs (§7). The other three are text-checkable.

| test | catches | failure_type | static status |
|---|---|---|---|
| 1 **deletion** — remove the skill, run the typical tasks; still passes → no gap | fills what axiom A already supplies | `nogap` | **L1 prediction** |
| 2 **improvisation** — count gap-bearing material the engine still improvises; >0 → residue | under-fill | `underfill` | **L1 prediction** |
| 3 **shuffle** — scramble the skill's elements; trace every failure to a §3 cell (below) | over-fill (order) | `overfill-order` | structural half is text-checkable |
| 4 **inertia-cost** — with vs without on tasks the engine already handles: costlier, no gain | over-fill (cost) | `overfill-cost` | **L1 prediction** (its L2 landing is the gate's `cost_ratio` fatal) |
| 5 **form check** — is each atom in the form its failure site requires (§4)? | wrong form | `wrong-form` | text-checkable |
| 6 **exit** — a semantic check of the *product* against "what correct looks like" | no compiled φ | `no-exit` | text-checkable |

**Shuffle, the six-cell criterion (§3).** Scramble the elements and watch where things break. **Every breakage must be traceable to one of the six legitimate homes of order**: (1) dependency, (2) irreversibility, (3) external mandate, (4) epistemic protocol, (5) product order, (6) compiled order. An order that traces to no cell is a welded procedure — `overfill-order`. Standard `fix_hint` (the cell-5 design law): *"a Step 1/2/3 that is really a product order should be rewritten as a φ — 'the product must exhibit this order' — with an exit check, leaving the path to the engine."* Mechanical order goes the other way: compile it into `scripts/` (cell 6), where it is invisible to the orchestration space and always legal.

**Form check, operationalized (§4 — the three must-compile sites).**

- **Rules → primitive**: a Rules section whose invariants span multiple fields should have a corresponding `scripts/` primitive (named fields, misuse unrepresentable); prose alone is a `wrong-form` candidate — A′-3/4 fire at the action site.
- **Exit → verifier**: the declared done/correct criteria should have a verifier — or honestly declare the dimension machine-unjudgeable and route it to the seam. Faking a verifier over an unjudgeable dimension is the same failure in the other direction, also `wrong-form`.
- **Control → non-skippable**: a Control-type gate protocol must be declared non-skippable — the failure being prevented is the engine skipping its own gate (A′-1).

**Price the trade-off before writing the finding.** Compilation buys enforceability and costs portability (§4): under cross-agent distribution constraints, declarative form can be the *rational* choice. Word such findings as an **unpriced trade-off** ("this invariant relies on engine compliance — has that been priced?"), not as a defect — unless the skill claims a guarantee its form cannot deliver.

**Judges — ≥2, decorrelated (required; §7).** A lone read is not a verdict: an unaided judge picks the better of two skills at 46.4% — coin-flip. And a *correlated* second judge adds almost nothing: aggregation removes sampling variance, not shared bias (the Condorcet independence condition — the theorem needs independent voters). So "independent" means **decorrelated**: different base models, or at minimum information-isolated contexts — no prior findings, no other judge's conclusions, not told which draft/run is which, no diff. Instantiate it: each judge is an isolated sub-context / sub-agent that runs the full read alone; record `judges: [{model, isolated: true}]` in the gate object. Categorical splits are not averaged: break the tie with a third judge under the same isolation rule, else default to `passed: false` (confirm the finding).

### Two scorecards — the route face and the output face

Score the two faces separately; they fail for different reasons and route to different fixes.

**Route / trigger** (does it fire when it should, and only then?):

| row | passes when | failure_type |
|---|---|---|
| Routes by gap | `description` says "use when X is missing", not only "produces Y" | wrong-route |
| Triggers on the real cue | fires on typical + colloquial phrasings | wrong-route |
| Doesn't over-trigger | stays quiet on adjacent out-of-scope tasks | wrong-route |

**Output** (is the product good, in the right form, guaranteeable?):

| row | passes when | failure_type |
|---|---|---|
| Deletion shows a gap | no-skill run fails the typical tasks | nogap |
| Gap fully supplied | improvisation test → 0 | underfill |
| Capability in compiled form | misuse syntactically impossible; prose-only invariants priced | wrong-form |
| No welded ordering | shuffle traces every order to a §3 cell | overfill-order |
| Judgment/control declarative | `done_when` predicate + binding, not fixed steps | overfill-order |
| No unpriced inertia | with/without cost comparison clean | overfill-cost |
| Semantic exit present | compares product against "correct" | no-exit |
| Composite seam placed right | checkpoint at the declared-φ boundary | seam-misplacement |
| Failure mechanisms encoded | key branches as `if X then Y else Z` | (output, brittle) |
| Executable specificity | no hedging where the type forbids it | (output, vague) |
| High-risk blacklist | a dedicated "never do" section | (output, unguarded) |

Apply **type-aware**: for Knowledge/Judgment skills "has a workflow" is N/A; for Judgment skills relax executable-specificity (taste = negative fences). The three reading rows above are the only text signals with validity evidence (§7 — failure-mechanism encoding, executable specificity, high-risk blacklist); fluent prose does not predict gain ([SkillLens](https://dev.to/wonderlab/is-your-agent-skill-actually-good-microsofts-dual-paper-deep-dive-into-skill-evaluation-and-28b7)), which is exactly why the decorrelated-judges rule is mandatory, not advisory.

### Tier 1 emits

Per failed (or notable) row, a **finding** in the shared schema (`references/effect-gate.md`): `{id, test, failure_type, prediction, passed, location{file,line}, evidence{missing,present_forbidden}, fix_hint, waived, waiver_reason}`, plus the **failure_taxonomy** aggregate. `location.file` always; `line` best-effort. `prediction: true` on every Tier-1 finding from the three L2-native tests (deletion / improvisation / inertia-cost). The `failure_type` enum is `nogap | underfill | overfill-order | overfill-cost | wrong-form | wrong-route | no-exit | seam-misplacement` (migration from the old tokens: `overfill` → `overfill-order`/`overfill-cost`; `wrong-layer` → `wrong-form`; deletion failures → `nogap` — see the gate file's migration note). The three reading-signal rows emit output-quality notes, not a `failure_type`.

---

## Tier 2 — behavioral effect verdict (L2)

Mandatory for production/library tier. Do **not** re-implement it here — run the shared gate in `references/effect-gate.md` on its **existence** branch: held-out tasks with-skill vs no-skill baseline, assertions on the *product*, producing `no_skill_pass_rate / with_skill_pass_rate / delta_exist / noise_band_exist / cost_ratio / regression_count / safety_regression` plus the `power` block. The effect layer passes iff `delta_exist > noise_band_exist AND regression_count == 0 (per-task medians) AND safety_regression == false AND no inertia-cost fatal`. **Negative transfer (reproduced on medians), safety regression, and the inertia-cost fatal are non-waivable.**

Before scoring, run the gate's **power check** (`resolution = 1/n_tasks`, `adequate = n_tasks ≥ 6`; an inadequate set can only yield `pass (indicative)`) and its **headroom check**: if `no_skill` is at ceiling on every task of a hardenable set, report `unfit_test_set` and harden — *not* `fail`. If the ceilinged tasks are the genuinely representative ones, that is the deletion test concluding `nogap`.

Held-out source per the gate: caller supplies tasks; or draft 3 happy-path + 1 edge to `baseline.md` and confirm before scoring (indicative only — extend to ≥6 to certify); or (scaffold) one smoke case.

---

## Converge to one gate + a fix list

Emit a **json + md pair** (json for machines / CI / `improve-skill`; md for humans), converging to the shared **gate** object: `gate_pass` ∈ `pass | fail | static_only | unfit_test_set`, qualified by `certainty` (`certifying | indicative`), plus `tier`, `evaluated_layers`, `power`, and `judges` so a `pass` is never overread. `static_only` is the honest state when the effect layer was required but no held-out set was available. Never report `pass` on an unrun-but-required layer.

**Resolution precedence** is owned by the gate file — apply its resolution order verbatim (`references/effect-gate.md`, "Resolution order"): blocking-structural first, then `static_only`, then the fatals (safety → reproduced negative transfer → inertia-cost) **before** any `unfit_test_set` routing, then the banded `delta_exist` test, else `pass` labeled by `certainty`. A version at or below the floor follows the gate's **sub-floor routing**: `nogap` (retire — never "improve" a skill into existence) vs negative transfer (route to `improve-skill`; escalate to `seek-skill` if repair cannot land).

End with a **fix list**: each item carries a `finding_id`, a priority, and a hint — built to pipe straight into `improve-skill`. **Locate, don't rewrite** — producing patches is `improve-skill`'s job.

## Waivers

A structural finding may be marked `waived: true` with a recorded reason (e.g. a tiny utility skill legitimately has no high-risk blacklist); the gate then passes *with recorded exceptions*. **Only structural/style findings are waivable.** The Tier 2 fatals — negative transfer, safety, inertia cost — have no waiver path and can never be set aside.

## Stay minimal

One structural report + the output scorecard (+ the route scorecard) + one gate + one fix list. Nothing else — no telemetry, registry, evidence ledgers, report zoo, or dashboards. Before adding any new report, run the deletion test on it: "remove it — does the gate still decide correctly?" If yes, don't add it.
