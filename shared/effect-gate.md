# effect-gate — the shared measurement gate

One implementation, referenced by both `evaluate-skill` (as its second, behavioral tier) and `improve-skill` (as its per-round keep/revert decision). Neither skill owns it; both point here so the gate is specified once. When a skill is distributed standalone, ship this file alongside it.

## Why this exists

A static, read-only verdict cannot certify that a skill helps. The only reliable judgment is the skill **as an intervention** against a no-skill baseline: run a real task with the skill and without it, and compare the *products*. Structural well-formedness does not predict gain — naively self-generated skills degrade performance by 1.3 points on average even when they read fine ([SoK / SkillsBench](https://arxiv.org/abs/2602.20867); [SkillGen](https://arxiv.org/abs/2605.10999) models skills exactly as interventions). The static entry lowers the *frequency* of defects; this gate is the *guarantee*.

## The protocol

1. **Assemble a held-out set** (source by tier, below). Real tasks, disjoint from anything used to write or diagnose the skill.
2. **Run each task twice** — with the skill, and with no skill (the baseline) — in fresh, isolated contexts.
3. **Assert on the product, not the wording.** The check compares the *artifact* a task produced against "what correct looks like," never the skill's prose or a diff. Judges must not be told which run is "with skill"; take the median of ≥2 independent judges.
4. **Score** `baseline_pass_rate`, `with_skill_pass_rate`, `delta = with − baseline`, and `regression_count` (tasks where with-skill scored *below* baseline).
5. **Check safety** on the with-skill runs: refusal-rate regression, attack-success increase, and scope-creep into judgment the engine should own ([Skill-Inject](https://arxiv.org/abs/2602.20156)).

## The gate rule

The effect layer **passes** iff:

```
delta > 0  AND  regression_count == 0  AND  safety_regression == false
```

Two outcomes are **fatal and non-waivable** — there is no waiver field on this layer:

- **Negative transfer** — any single task where with-skill < baseline. A skill worse than no skill never ships, whatever the average.
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

The **effect report**:

```json
{
  "baseline_pass_rate": 0.55,
  "with_skill_pass_rate": 0.80,
  "delta": 0.25,
  "regression_count": 0,
  "safety_regression": false,
  "per_task": [ { "task": "...", "baseline": 1, "with_skill": 1 } ]
}
```

The converged **gate** object (the single thing a caller / CI reads):

```json
{
  "skill": "<path>",
  "tier": "scaffold | production | library",
  "evaluated_layers": ["structural", "effect"],
  "gate_pass": "pass | fail | static_only",
  "structural": { "findings": [], "failure_taxonomy": {}, "waived_count": 0 },
  "effect": { /* effect report, or null for scaffold smoke-only */ },
  "fix_list": [ { "finding_id": "F03", "priority": 1, "hint": "..." } ]
}
```

`gate_pass` resolves **relative to tier**, with `evaluated_layers` disclosing what actually ran so `pass` is never overread:

- **`fail`** — any non-waived blocking structural finding, OR (effect layer ran and) `delta ≤ 0` / `regression_count > 0` / `safety_regression`, OR a scaffold smoke case that broke.
- **`static_only`** — the effect layer was *required by tier* but could not be run (no held-out set). Not a pass, not a fail.
- **`pass`** — every layer that applies to the tier cleared: structural clean (modulo recorded waivers), and for production/library the effect layer passed; for scaffold the smoke case ran clean.

## Self-reference

This protocol's order — change → measure → keep/revert — is a *measurement protocol*, not task orchestration, so it is exempt from the shuffle test (it is the legitimate epistemic order, not a welded procedure). That exemption is what lets `evaluate-skill` and `improve-skill` both apply this gate without becoming procedural skills themselves.
