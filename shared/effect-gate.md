# effect-gate — the shared measurement gate

One implementation, referenced by both `evaluate-skill` (as its second, behavioral tier) and `improve-skill` (as its per-round keep/revert decision). Neither skill owns it; both point here so the gate is specified once. When a skill is distributed standalone, ship this file alongside it.

## Why this exists

A static, read-only verdict cannot certify that a skill helps. The only reliable judgment is the skill **as an intervention**: run a real task with the skill and without it, and compare the *products*. Structural well-formedness does not predict gain — naively self-generated skills degrade performance by 1.3 points on average even when they read fine ([SoK / SkillsBench](https://arxiv.org/abs/2602.20867); [SkillGen](https://arxiv.org/abs/2605.10999) models skills exactly as interventions). The static entry lowers the *frequency* of defects; this gate is the *guarantee*.

## Two questions, two deltas — existence vs improvement

This gate answers **two different questions**, and conflating them is a real failure mode: an improvement loop that keeps nothing because it is secretly asking the *existence* question against a strong base model. Keep them separate.

- **Existence delta** `delta_exist = with_skill − no_skill` (written `delta` where unambiguous). *"Does this skill deserve to exist?"* This is `evaluate-skill`'s Tier 2, and `improve-skill`'s **one-time entry check** plus a permanent **floor** (a kept version must never fall below no-skill).
- **Improvement delta** `delta_step = with_edited − with_prev_accepted`. *"Did this edit make the skill better than its last accepted version?"* This is `improve-skill`'s **per-round KEEP criterion**. The no-skill baseline is computed **once** and reused; each round scores the edited skill against the **stored previous-accepted** scores — it never re-derives the keep test from `delta_exist`.

Why this matters: when the base model already does the task well, `no_skill` ceilings and `delta_exist > 0` becomes impossible for *every* version — so an iterator keyed on `delta_exist` refuses all edits even though some genuinely improve the skill (`delta_step > 0`). **Improvement is measured against the artifact's own previous version, not against the floor.**

## The protocol

1. **Assemble a held-out set** (source by tier, below). Real tasks, disjoint from anything used to write or diagnose the skill.
2. **Run each task** in fresh, isolated contexts: with no skill (the baseline, **computed once**), and with the skill version under test. For an `improve-skill` round, also retain the *previous accepted* version's scores.
3. **Assert on the product, not the wording.** The check compares the *artifact* a task produced against "what correct looks like," never the skill's prose or a diff. Judges must not be told which run is "with skill"; take the median of ≥2 independent judges (prefer an odd count; on a categorical call, two judges that split escalate to a third — see `evaluate-skill`).
4. **Score, per task and aggregate.** `no_skill` (baseline), `with_skill`; `delta_exist = with_skill − no_skill`; for an improvement round `delta_step = with_edited − with_prev_accepted`; and `regression_count` (tasks scoring *below* the relevant reference — no-skill for existence, previous-accepted for improvement). Retain `no_skill` **per task** (not just the aggregate), since the floor check below is per-task. **Re-run the reference condition ≥3×, and every other condition ≥2×**, to size the noise band.
5. **Check safety** on the with-skill runs: refusal-rate regression, attack-success increase, and scope-creep into judgment the engine should own ([Skill-Inject](https://arxiv.org/abs/2602.20156)).

**Noise band (reproducible; improvement only).** An LLM judge is noisy, so a bare `delta_step > 0` can be jitter. For an improvement round, re-run the **previous-accepted** (reference) version **≥3×** on the fixed held-out set, scoring each run as in step 4; `noise_band = max − min` of those reference re-run aggregate scores. A KEEP requires `delta_step` to **exceed `noise_band`** (`delta_step > noise_band`), not merely be positive. Two reviewers running the same inputs compute the same band. The **existence** gate uses no band — its bar is `delta_exist > 0` with the regression/safety fatals; re-runs there only stabilize the judge median.

## Headroom check — the set must be able to show *what you are measuring*

Run before iterating. What counts as "fit" depends on the question — and these are not the same test (conflating them is a real bug: it rejects sets that can still measure improvement).

**For the improvement loop** (`improve-skill`). The set is fit iff the **current** skill has headroom the set can detect:

- some task where the current skill scores **below max** (an edit could raise it), **or**
- some task where the current skill scores **below `no_skill`** (negative transfer to repair).

Variance across tasks (not all identical) is *preferred* — a flat set is a weak signal — but **not required**: a uniform below-max set still shows a lift. The no-skill baseline here is **only the floor** — it may sit at ceiling without making the set unfit, because improvement is measured against the skill's *previous version*, not against no-skill. The set is **`unfit_test_set`** only when the current skill is **already maxed on every task with no negative transfer** — there is nothing left to raise; report `already_optimal`, do not iterate.

**For the existence question** (`evaluate-skill` Tier 2). *Additionally* `no_skill` must not be at ceiling, else existence value cannot be shown — a separate concern that does **not** block the improvement loop.

This is the symmetric twin of "weak tests inflate everything": weak tests inflate the answer; a set with no headroom *for the question being asked* hides it. The remedy is harder fixtures (cases that expose the gap), not more rounds.

## The gate rule

**Existence gate** (`evaluate-skill` Tier 2; `improve-skill`'s entry check). The effect layer **passes** iff:

```
delta_exist > 0  AND  regression_count == 0  AND  safety_regression == false
```

**Improvement gate** (`improve-skill`'s per-round KEEP). An edit is kept iff:

```
delta_step > noise_band
AND  no per-task regression vs the previous accepted version
AND  with_edited >= no_skill on every task            (the floor is never breached)
AND  safety_regression == false
AND  no new blocking structural finding
```

**Structural-repair exception (lateral keep).** An edit whose `delta_step` falls *within* the noise band is still kept if it **removes a non-waived blocking structural finding** *and* breaches neither the per-task floor nor the no-regression-vs-previous condition *and* is safety-clean. This is the one case where a within-noise edit lands: a real structural fix the effect layer is too coarse to measure. Every other within-noise edit reverts.

Two outcomes are **fatal and non-waivable** on both gates — there is no waiver field on this layer:

- **Negative transfer** — any single task where the version under test scores below its reference (no-skill for existence; previous-accepted, or the no-skill floor, for improvement). A skill worse than its reference never lands, whatever the average.
- **Safety regression** — any of the safety signals worsens, even if task score rose.

## Held-out source, by tier

The effect layer needs an executor and real inputs, which are not always present at call time. Tiering keeps this honest:

| tier | what to run | effect layer |
|---|---|---|
| **scaffold** | static structural read + **one smoke case** (does it run, not crash, produce plausible output) | delta **not required**; report the smoke result |
| **production / library** | full held-out with/without delta | **mandatory** |

Held-out tasks come from, in order of preference: (a) the **caller supplies** a task set; (b) **draft and confirm** — write 3 happy-path + 1 edge task to a `baseline.md`, show the user, score only after confirmation; (c) scaffold tier only — a single smoke case. If a production/library skill is evaluated but no held-out set can be obtained, the layer is **not** silently skipped: report `static_only` (see schema), which means "structurally fine, effect unverified — supply tasks to finish." Never report `pass` on an unrun-but-required effect layer.

## Shared JSON schema (both skills emit these shapes)

A single structural **finding**:

```json
{
  "id": "F03",
  "test": "deletion | improvisation | shuffle | inertia | exit | seam | route | output",
  "failure_type": "underfill | overfill | wrong-layer | wrong-route | no-exit | seam-misplacement",
  "passed": false,
  "location": { "file": "SKILL.md", "line": 42 },
  "evidence": { "missing": [], "present_forbidden": ["Step 1 / Step 2 ordering at L40-48"] },
  "fix_hint": "...",
  "waived": false,
  "waiver_reason": null
}
```

`location.file` is always given; `line` is best-effort. **Waiver applies to structural findings only**, and only for non-load-bearing structural/style defects, with a recorded reason; the effect-layer fatals above can never be waived.

The **failure_taxonomy** aggregate (counts by type, over non-waived findings):

```json
{ "underfill": 0, "overfill": 2, "wrong-layer": 0, "wrong-route": 1, "no-exit": 0, "seam-misplacement": 0 }
```

The **effect report** (existence fields always; improvement fields present only for `improve-skill` rounds):

```json
{
  "no_skill_pass_rate": 0.55,
  "with_skill_pass_rate": 0.80,
  "delta_exist": 0.25,
  "prev_accepted_pass_rate": 0.70,
  "delta_step": 0.10,
  "noise_band": 0.04,
  "floor_ok": true,
  "regression_count": 0,
  "safety_regression": false,
  "per_task": [ { "task": "...", "no_skill": 1, "prev_accepted": 0, "with_skill": 1 } ]
}
```

The **discrimination** report (emitted once, before an improvement loop):

```json
{ "headroom": true, "variance": true, "fit": true }
```

`fit = headroom` (improvement loop); `variance` is an advisory quality signal, not a hard gate. For the existence question, fitness is simply `no_skill` not at ceiling.

The converged **gate** object (the single thing a caller / CI reads):

```json
{
  "skill": "<path>",
  "tier": "scaffold | production | library",
  "evaluated_layers": ["structural", "effect"],
  "gate_pass": "pass | fail | static_only | unfit_test_set",
  "structural": { "findings": [], "failure_taxonomy": {}, "waived_count": 0 },
  "effect": { /* effect report, or null for scaffold smoke-only */ },
  "discrimination": { /* discrimination report, or null outside an improvement loop */ },
  "fix_list": [ { "finding_id": "F03", "priority": 1, "hint": "..." } ]
}
```

`gate_pass` resolves **relative to tier**, with `evaluated_layers` disclosing what actually ran so `pass` is never overread:

- **`fail`** — any non-waived blocking structural finding, OR (effect layer ran and) the applicable gate's fatal: `safety_regression`, or `regression_count > 0` / floor breach (both fatal **even on a ceilinged set**), or `delta_exist ≤ 0` **on a non-ceilinged set** (a ceilinged `no_skill` routes to `unfit_test_set`, not `fail` — see the resolution order), or for improvement `delta_step ≤ noise_band` *unless the structural-repair lateral keep applies*; OR a scaffold smoke case that broke.
- **`static_only`** — the effect layer was *required by tier* but could not be run (no held-out set). Not a pass, not a fail.
- **`unfit_test_set`** — the held-out set failed the headroom check for the question being asked (improvement: current skill already maxed on every task with no negative transfer → report `already_optimal`; existence: `no_skill` at ceiling). Not a pass, not a fail: **halt and harden the set**. An improvement loop never keeps or reverts on a set with no headroom to measure.
- **`pass`** — every layer that applies to the tier cleared: structural clean (modulo recorded waivers), and for production/library the applicable effect gate passed; for scaffold the smoke case ran clean.

**Resolution order (first match wins) — a ceilinged set never masks a fatal.** Existence gate only (the improvement loop's routing is separate — see the trailing note): (1) blocking-structural / scaffold-smoke-broke → `fail`; (2) effect required-but-unrun → `static_only`; (3) `safety_regression` → `fail`; (4) `regression_count > 0` (negative transfer) → `fail`; (5) `no_skill` at ceiling → `unfit_test_set`; (6) `delta_exist ≤ 0` → `fail`; (7) else `pass`. Safety and negative-transfer fatals are evaluated **before** the `unfit_test_set` routing. The improvement loop runs its headroom/`unfit` check *before* iterating (Phase B) and applies per-round fatals via the ratchet, so its unfit routing cannot mask a per-round fatal either.

## Self-reference

This protocol's order — change → measure → keep/revert — is a *measurement protocol*, not task orchestration, so it is exempt from the shuffle test (it is the legitimate epistemic order, not a welded procedure). That exemption is what lets `evaluate-skill` and `improve-skill` both apply this gate without becoming procedural skills themselves.
