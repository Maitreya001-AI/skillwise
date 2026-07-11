# effect-gate — the shared measurement gate

One implementation, one editing source. This file's home in the skillwise repo is `shared/effect-gate.md`; `scripts/sync-shared.py` materializes it (plus a do-not-edit banner) into each consuming skill's `references/` folder — `evaluate-skill`, `improve-skill`, `seek-skill` — so every skill folder is self-contained under every install path. Edit only the `shared/` source; CI re-runs the sync and fails on drift.

The protocol's mechanics are compiled the same way: `shared/scripts/gate_runner.py` (both arms in isolated sandboxes, product assertions, per-run cost capture) and `shared/scripts/gate_math.py` (this file's §8 arithmetic) are materialized into each consumer's `scripts/`. One command — `python scripts/gate_runner.py run tasks.yaml` (schema in its docstring) — executes this protocol end to end, so keep/revert never depends on the gated engine hand-assembling its own measurement (see Self-reference). Draft task sets (`tasks.draft.yaml`) are refused by name until reviewed and renamed.

## Why this exists

A static, read-only verdict cannot certify that a skill helps. Certification lives only at L2 (`docs/THEORY.md` §7): run real tasks with the skill and without it, and compare the *products*. Structural well-formedness does not predict gain — naively self-generated skills degrade performance by 1.3 points on average even when they read fine ([SoK / SkillsBench](https://arxiv.org/abs/2602.20867); [SkillGen](https://arxiv.org/abs/2605.10999) models skills exactly as interventions). The static entry lowers the *frequency* of defects; this gate is the *certification*.

And the measurer itself — an LLM judge plus a stochastic engine — is a noise source. So **every comparison this gate makes is a statistical inference, and must declare its noise model and error direction** (THEORY §8, the statistical charter). Each rule below cites the charter principle it implements.

## Two questions, two deltas (§8-6)

This gate answers **two different questions**, and conflating them is a real failure mode: an improvement loop that keeps nothing because it is secretly asking the *existence* question against a strong base model. Keep them separate.

- **Existence delta** `delta_exist = with_skill − no_skill`. *"Does this skill deserve to exist?"* This is `evaluate-skill`'s Tier 2 and `seek-skill`'s gate, and `improve-skill`'s **one-time entry check** plus a permanent **floor** (a kept version must never fall below no-skill).
- **Improvement delta** `delta_step = with_edited − with_prev_accepted`. *"Did this edit make the skill better than its last accepted version?"* This is `improve-skill`'s **per-round KEEP criterion**. The no-skill baseline is computed **once** and reused; each round scores the edited skill against the **stored previous-accepted** scores — it never re-derives the keep test from `delta_exist`.

Why this matters: when the base model already does the task well, `no_skill` ceilings and a positive `delta_exist` becomes impossible for *every* version — so an iterator keyed on `delta_exist` refuses all edits even though some genuinely improve the skill (`delta_step` clears the band). **Improvement is measured against the artifact's own previous version, not against the floor.** The floor is a permanent guardrail, never the per-round bar.

## The protocol

1. **Assemble a held-out set** (source by tier, below). Real tasks, disjoint from anything used to write or diagnose the skill.
2. **Power check — mandatory before any verdict (§8-3).** With pass/fail scoring over `n_tasks` tasks, the smallest representable delta is `resolution = 1 / n_tasks`; effects smaller than that are *invisible on this set*, whatever they are in reality. Emit the `power` block `{ n_tasks, resolution, adequate }` with `adequate = n_tasks >= 6` (a tunable constant; 6 is the shipped default). When `adequate == false`, any `pass` this gate emits is **demoted to `pass (indicative)`** via the gate object's `certainty` field — the default drafted set (3 happy-path + 1 edge = 4 tasks) can therefore **only ever produce indicative conclusions, never certifying ones**. If the set cannot resolve the question being asked *and cannot be hardened*, route to `unfit_test_set`; never convert low power into a verdict about the skill.
3. **Improvement loops only — reserve a confirmation slice (§8-4).** Hold back ~25% of the tasks (at least 2) as `confirm/`, invisible to every loop round; iterate on the remaining working tasks. See "Confirmation slice" below.
4. **Run each task** in fresh, isolated contexts: with no skill (the baseline, **computed once**), and with the skill version under test. For an `improve-skill` round, also retain the *previous accepted* version's scores. **Re-run the reference condition exactly 3×** (no-skill for existence; previous-accepted for improvement) — the band estimator below is defined on exactly three runs, so the bar does not drift with run count — **and every other condition ≥2×**. Retain `no_skill` **per task** (not just the aggregate): the floor check is per-task.
5. **Assert on the product, not the wording.** The check compares the *artifact* a task produced against "what correct looks like," never the skill's prose or a diff. Judges must be **decorrelated** (§7, and see `evaluate-skill` for the operational definition): different base models, or at minimum information-isolated contexts — no prior findings, no other judge's conclusions, never told which run carries the skill, no diff. Take the median of ≥2 such judges; a categorical split escalates to a third under the same isolation rule. Record them in the gate object's `judges` array. A same-model, same-prompt second judge lowers sampling variance only — it does not remove shared bias.
6. **Score, per task and aggregate.** A task's score under a condition is the **median across that condition's re-runs**. Compute `delta_exist` (and `delta_step` for an improvement round) on the aggregates; count `regression_count` over per-task medians (see "Reproducible fatals"). Record **cost** (§8-5): `tokens_no_skill`, `tokens_with_skill`, `cost_ratio = tokens_with_skill / tokens_no_skill`; an improvement round also records `cost_delta` vs the previous accepted version (advisory).
7. **Check safety** on the with-skill runs: refusal-rate regression, attack-success increase, and scope-creep into judgment the engine should own ([Skill-Inject](https://arxiv.org/abs/2602.20156)).

**Noise bands (§8-1).** Any delta that enters a decision must clear a band sized from the reference condition's three fixed re-runs:

```
noise_band = 2 × sample standard deviation of the 3 reference-condition aggregate scores

improvement gate:  KEEP requires  delta_step  > noise_band        (reference = previous-accepted)
existence gate:    pass requires  delta_exist > noise_band_exist  (reference = no_skill, same formula)
```

The estimator is a standard-deviation multiple, deliberately decoupled from run count (not a `max − min` range, which grows with every extra run and makes the bar indeterminate). A bare `delta > 0` is not a signal — it puts jitter through the gate; a bare `delta ≤ 0 → kill` is not a verdict either — on a low-power set it executes noise.

**Reproducible fatals (§8-2).** Per-task zero tolerance × a noisy judge × set size = guaranteed false kills: with single-run false-regression probability *p* over *n* tasks, the chance of at least one false fatal is 1 − (1 − p)ⁿ — the family-wise error rate. The more thorough the set, the more certain the wrongful conviction. So a task enters `regression_count` **iff its median across re-runs** under the version being tested falls below the same task's reference (no-skill for existence; previous-accepted, or the no-skill floor, for improvement). A single-run dip never counts. Zero tolerance applies to *reproduced* regressions, not single observations.

## Confirmation slice — the improvement loop's anti-overfitting defense (§8-4)

Iterating on a fixed set while the loop sees per-task results each round is the textbook condition for adaptive overfitting (the reusable-holdout problem, Dwork et al. 2015). The ratchet's monotonicity therefore holds **on the working set only**. Two rules:

- An `improved` terminal state must be **re-checked on the confirmation slice** (`confirm/`, reserved in protocol step 3, never seen by any round): the surviving version must show `delta ≥ 0` vs the entry version there. If it does, report `improved`; if not, report **`improved (unconfirmed)`** and recommend rotating to a fresh set before trusting the gain.
- **Rounds on one set are capped** (default 10). Hitting the cap without terminating means the set is exhausted as a signal source: rotate the set or stop.

This is a distinct defense from memory rot, and both are needed: the confirmation slice defends against **fitting the test set** (the tasks were fine; the loop over-adapted to them); "held-out tasks are never drawn from the skill's own past outputs" defends against **memory rot** (an early wrong edit replayed as ground truth — see `improve-skill`'s failure-driven reference).

## Headroom check — the set must be able to show *what you are measuring*

Run before iterating. What counts as "fit" depends on the question — and these are not the same test (conflating them is a real bug: it rejects sets that can still measure improvement).

**For the improvement loop** (`improve-skill`). The set is fit iff the **current** skill has headroom the set can detect:

- some task where the current skill scores **below max** (an edit could raise it), **or**
- some task where the current skill scores **below `no_skill`** (negative transfer to repair).

Variance across tasks (not all identical) is *preferred* — a flat set is a weak signal — but **not required**: a uniform below-max set still shows a lift. The no-skill baseline here is **only the floor** — it may sit at ceiling without making the set unfit, because improvement is measured against the skill's *previous version*, not against no-skill. The set is **`unfit_test_set`** only when the current skill is **already maxed on every task with no negative transfer** — there is nothing left to raise; report `already_optimal`, do not iterate.

**For the existence question** (`evaluate-skill` Tier 2, `seek-skill`). *Additionally* `no_skill` must not be at ceiling, else existence value cannot be shown — a separate concern that does **not** block the improvement loop.

`unfit_test_set` also covers the power side (§8-3): a set whose **resolution is too coarse for the question being asked and that cannot be hardened** is unfit, whatever its headroom. Weak tests inflate the answer; a set with no headroom *or no resolution* for the question hides it. The remedy is harder or more numerous fixtures, not more rounds.

## The gate rule

**Existence gate** (`evaluate-skill` Tier 2; `seek-skill`'s gate; `improve-skill`'s entry check). The effect layer **passes** iff:

```
delta_exist > noise_band_exist          (§8-1 — not bare delta_exist > 0)
AND  regression_count == 0              (per-task medians, §8-2)
AND  safety_regression == false
AND  no inertia-cost fatal              (§8-5, below)
```

**Improvement gate** (`improve-skill`'s per-round KEEP). An edit is kept iff:

```
delta_step > noise_band
AND  no task whose median across re-runs drops below the previous accepted version
AND  with_edited ≥ no_skill on every task (medians — the floor is never breached)
AND  safety_regression == false
AND  no new blocking structural finding
```

**Structural-repair exception (lateral keep).** An edit whose `delta_step` falls *within* the noise band is still kept if it **removes a non-waived blocking structural finding** *and* breaches neither the per-task floor nor the no-regression-vs-previous condition *and* is safety-clean. This is the one case where a within-noise edit lands: a real structural fix the effect layer is too coarse to measure. Every other within-noise edit reverts.

Three outcomes are **fatal and non-waivable** on the existence gate — there is no waiver field on this layer:

- **Negative transfer** — any task whose **median across re-runs** scores below its reference. A skill worse than its reference never lands, whatever the average.
- **Safety regression** — any of the safety signals worsens, even if task score rose.
- **Inertia cost** (§8-5) — `cost_ratio` significantly worse (default `> 1.5×`) while `delta_exist` sits inside the noise band: the skill makes runs materially more expensive and buys no detectable gain. This is the §6 inertia-cost test landing at L2 (`overfill-cost`) — before cost entered this layer, that failure was defined by the theory but unmeasurable at the only certifying layer. It outranks the `unfit_test_set` routing: a ceilinged set with a large cost regression is a **fail**, not a harden-the-set.

On the improvement gate the first two apply unchanged (medians, vs previous-accepted or the floor); `cost_delta` is recorded and reported as **advisory** — a persistent cost climb with flat deltas is a signal to stop the loop, not a per-round fatal.

## Sub-floor routing — one rule, referenced by every door

A version that ties or loses to no-skill is not one condition but two, and they route differently (§6: the deletion test asks *does the gap exist*; a negative delta asks *is the filling harmful*):

```
Run the deletion test first (typical tasks, no skill):
├─ no_skill already passes           → nogap: the skill should not exist.
│                                       Retire it / don't ship it. Never route it to improve-skill.
└─ no_skill fails (the gap is real)
   and with_skill < no_skill         → negative transfer: the filling is harmful but the gap exists.
                                        Route to improve-skill — negative transfer is the first
                                        repair target. If improvement cannot land a clean KEEP and
                                        the floor stays breached, escalate to seek-skill for a
                                        structural rethink.
```

`write-skill`'s exit gate, `improve-skill`'s Phase A and failure escalation, and this gate's resolution order all reference this block; none restates a different version.

## Held-out source, by tier

The effect layer needs an executor and real inputs, which are not always present at call time. Tiering keeps this honest:

| tier | what to run | effect layer |
|---|---|---|
| **scaffold** | static structural read + **one smoke case** (does it run, not crash, produce plausible output) | delta **not required**; report the smoke result |
| **production / library** | full held-out with/without delta | **mandatory** |

Held-out tasks come from, in order of preference: (a) the **caller supplies** a task set; (b) **draft and confirm** — write 3 happy-path + 1 edge task to a `baseline.md`, show the user, score only after confirmation (4 tasks: below the power floor, so its conclusions are **indicative only** — extend to ≥6 to certify); (c) scaffold tier only — a single smoke case. If a production/library skill is evaluated but no held-out set can be obtained, the layer is **not** silently skipped: report `static_only` (see schema), which means "structurally fine, effect unverified — supply tasks to finish." Never report `pass` on an unrun-but-required effect layer.

## Minimum credible configuration — what a real measurement costs

Budget before starting, so the corner you cut under pressure is not the noise band or the blind judging (those two *are* the measurement). One improvement round on the default credible set (6 working tasks + 2 confirm) costs roughly:

- reference condition: 3 runs × 6 tasks = **18 task executions** (once per loop if scores are stored and reused);
- edited version: 2 runs × 6 tasks = **12 executions**;
- candidate screening: ~3 candidates × 1 cheap pass × 6 tasks = **18 executions**;
- judging: ~30 scored artifacts × ≥2 decorrelated judges = **60+ judge calls**.

Order of magnitude: **~50 task executions and ~60 judge calls per round**, plus the confirmation-slice re-check at the end. If that exceeds what the skill is worth, run the scaffold tier honestly (static read + smoke, `static_only`) instead of a diluted "full" gate — a gate stripped of its band and blinding measures nothing.

## Shared JSON schema (all consumers emit these shapes)

A single structural **finding**:

```json
{
  "id": "F03",
  "test": "deletion | improvisation | shuffle | inertia | form | exit | seam | route | output",
  "failure_type": "nogap | underfill | overfill-order | overfill-cost | wrong-form | wrong-route | no-exit | seam-misplacement",
  "prediction": false,
  "passed": false,
  "location": { "file": "SKILL.md", "line": 42 },
  "evidence": { "missing": [], "present_forbidden": ["Step 1 / Step 2 ordering at L40-48"] },
  "fix_hint": "...",
  "waived": false,
  "waiver_reason": null
}
```

`prediction: true` marks a finding whose test is **L2-native** (deletion / improvisation / inertia-cost — their definitions contain "run the task") but which was produced by a static read: a Tier 1 *prediction* (§7), overridden by the behavioral result once Tier 2 runs. `location.file` is always given; `line` is best-effort. **Waiver applies to structural findings only**, and only for non-load-bearing structural/style defects, with a recorded reason; the effect-layer fatals above can never be waived.

> **Token migration note** (old → new): `overfill` → `overfill-order` (welded order) **or** `overfill-cost` (inertia cost); `wrong-layer` → `wrong-form` (both directions: prose where a primitive is required, and a faked verifier where the dimension is honestly machine-unjudgeable); deletion-test failures move from `overfill` to their own **`nogap`** ("should not exist" routes to retirement, not to trimming).

The **failure_taxonomy** aggregate (counts by type, over non-waived findings):

```json
{ "nogap": 0, "underfill": 0, "overfill-order": 2, "overfill-cost": 0, "wrong-form": 0, "wrong-route": 1, "no-exit": 0, "seam-misplacement": 0 }
```

The **effect report** (existence fields always; improvement fields — `prev_accepted_pass_rate`, `delta_step`, `noise_band`, `cost_delta` — only for `improve-skill` rounds). Per-task values are medians across re-runs:

```json
{
  "no_skill_pass_rate": 0.55,
  "with_skill_pass_rate": 0.80,
  "delta_exist": 0.25,
  "noise_band_exist": 0.08,
  "prev_accepted_pass_rate": 0.70,
  "delta_step": 0.10,
  "noise_band": 0.04,
  "tokens_no_skill": 41200,
  "tokens_with_skill": 47300,
  "cost_ratio": 1.15,
  "cost_delta": 0.03,
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

`fit = headroom` (improvement loop); `variance` is an advisory quality signal, not a hard gate. For the existence question, fitness is `no_skill` not at ceiling *and* adequate resolution.

The converged **gate** object (the single thing a caller / CI reads):

```json
{
  "skill": "<path>",
  "tier": "scaffold | production | library",
  "evaluated_layers": ["structural", "effect"],
  "gate_pass": "pass | fail | static_only | unfit_test_set",
  "certainty": "certifying | indicative",
  "power": { "n_tasks": 8, "resolution": 0.125, "adequate": true },
  "judges": [ { "model": "<model-id>", "isolated": true } ],
  "structural": { "findings": [], "failure_taxonomy": {}, "waived_count": 0 },
  "effect": { /* effect report, or null for scaffold smoke-only */ },
  "discrimination": { /* discrimination report, or null outside an improvement loop */ },
  "fix_list": [ { "finding_id": "F03", "priority": 1, "hint": "..." } ]
}
```

`certainty` qualifies a `pass`: **`certifying`** iff `power.adequate`, else **`indicative`** — report the latter as `pass (indicative)`, and never let an indicative pass stand in for certification.

`gate_pass` resolves **relative to tier**, with `evaluated_layers` disclosing what actually ran so `pass` is never overread:

- **`fail`** — any non-waived blocking structural finding; OR (the effect layer ran and) one of the applicable gate's fatals fired: `safety_regression`, reproduced negative transfer / floor breach (fatal **even on a ceilinged set**), the inertia-cost fatal, `delta_exist ≤ noise_band_exist` on a fit set, or for improvement `delta_step ≤ noise_band` without the lateral-keep exception; OR a scaffold smoke case that broke.
- **`static_only`** — the effect layer was *required by tier* but could not be run (no held-out set). Not a pass, not a fail.
- **`unfit_test_set`** — the held-out set cannot show the answer to the question being asked: `no_skill` at ceiling on a hardenable set (existence), current skill maxed with no negative transfer (improvement → report `already_optimal`), or resolution too coarse for the question and the set cannot be hardened. Not a pass, not a fail: **halt and harden the set**.
- **`pass`** — every layer that applies to the tier cleared, qualified by `certainty`.

**Resolution order (first match wins) — a ceilinged set never masks a fatal.** Existence gate only (the improvement loop's routing is separate — see the trailing note): (1) blocking-structural / scaffold-smoke-broke → `fail`; (2) effect required-but-unrun → `static_only`; (3) `safety_regression` → `fail`; (4) `regression_count > 0` (reproduced negative transfer, per-task medians) → `fail`; (5) inertia-cost fatal (`cost_ratio > 1.5` with `delta_exist` inside the band) → `fail` (`overfill-cost`); (6) `no_skill` at ceiling on a set that under-represents the skill's domain, or resolution insufficient and hardenable → `unfit_test_set` — but if the ceilinged tasks *are* the representative typical tasks and nothing harder honestly exists, that is the deletion test concluding: → `fail` (`nogap`, retire — see sub-floor routing); (7) `delta_exist ≤ noise_band_exist` → `fail` (route the aftermath via the sub-floor rule: `nogap` vs negative transfer); (8) else `pass`, labeled by `certainty`. Safety, negative-transfer, and cost fatals are evaluated **before** the `unfit_test_set` routing. The improvement loop runs its headroom/`unfit` check *before* iterating (Phase B) and applies per-round fatals via the ratchet, so its unfit routing cannot mask a per-round fatal either.

## Self-reference

This protocol's own order — change → measure → keep/revert — needs no exemption from the shuffle test, and claims none. Shuffle the gate's elements and every breakage lands in a named cell of THEORY §3: measure-before-keep is **epistemic order** (cell 4 — a measurement protocol: you cannot select on a delta you have not measured), and reference-runs-before-band is **dependency order** (cell 1 — the band is computed *from* those runs). The gate's non-skippability is not self-granted either: it is §4's compilation requirement on Control — a gate the gated engine can skip re-inherits A′-1 (skipped self-verification), so keep/revert must be mechanical, never a judgment call inside the loop being gated. What earlier versions of this repo treated as a special exemption for measurement protocols is exactly these two cells plus that compilation requirement: a classified case, not a special plea.
