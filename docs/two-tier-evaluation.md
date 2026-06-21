# Design note — two-tier evaluation and the shared effect gate

**Status:** adopted · **Scope:** `evaluate-skill`, `improve-skill`, new `shared/effect-gate.md`

## TL;DR

`evaluate-skill` was a single static verdict: read the skill, run five structural tests, "all rows pass = correct." That answers *is the skill well-formed?* but not *does it actually improve output?* This change splits evaluation into **two tiers that converge on one gate** — a static structural verdict and a behavioral effect-delta verdict — and moves the measurement protocol into a single top-level file, `shared/effect-gate.md`, that both `evaluate-skill` and `improve-skill` reference. Nothing about the existing five-test read changed; it was wrapped, made machine-readable, and given the second tier it was missing.

## Why the old verdict was insufficient

The toolkit's own principle (see `docs/THEORY.md` §3–4) is that a mechanical/structural check **lowers the frequency** of defects but is **not a guarantee**; the guarantee comes only from checking the *product* against a baseline. A skill can pass every structural test and still make output worse — naively self-generated skills degrade task performance by 1.3 points on average even when they read fine (SkillsBench, via SoK: Agentic Skills). An evaluator that stops at the static read is therefore *under-filling its own gap*: it leaves the most important question — did this skill help? — to improvisation. The fix is the one the theory already prescribes for everything else: judge the skill **as an intervention** against a no-skill baseline.

## What changed, and why

### The two tiers

**Tier 1 — structural verdict (static).** The existing linter entry + five semantic tests, now emitting a machine-readable **finding** per defect using a fixed schema (`id, test, failure_type, passed, location, evidence, fix_hint, waived`) plus a `failure_taxonomy` aggregate. The defect vocabulary is the toolkit's own — under-fill, over-fill, wrong-layer, wrong-route, no-exit, seam-misplacement — so "paragraph N is over-fill" becomes structured data, not a sentence a human has to parse. The single scorecard was also split into **two faces**: a *route/trigger* scorecard (does it fire when it should, and only then?) and an *output* scorecard (is the product good, in the right layer, guaranteeable?). They fail for different reasons and route to different fixes, so they are scored separately.

**Tier 2 — behavioral effect verdict (delta).** New, and the most important addition. On held-out real tasks, the skill is run **with and without** itself; assertions are made on the *artifact produced*, never on the skill's wording. It reports `baseline_pass_rate`, `with_skill_pass_rate`, `delta`, and `regression_count`. The gate passes only when `delta > 0` and `regression_count == 0` and safety is clean. This is the part the old evaluator simply did not have.

### Output and convergence

Reports now land as a **json + md pair** — json for machines, the gate, CI, and `improve-skill`; md for humans — converging on one `gate` object. The report ends with a **fix list** in which every item points back to a specific finding id, so the output pipes straight into `improve-skill` with no human reformatting. `evaluate-skill` still **locates and does not rewrite**; producing patches remains `improve-skill`'s job.

### Four corrections the raw spec didn't anticipate

The change request was sound, but four issues surfaced while applying the toolkit's own ruler to it; each was resolved rather than papered over.

1. **One gate, not two implementations.** If `improve-skill` kept its own baseline-and-negative-transfer logic while `evaluate-skill` grew an identical one, the same gate would exist twice — cross-skill over-fill. The gate is now defined **once** in `shared/effect-gate.md`; both skills reference it. A kept edit in `improve-skill` therefore means exactly what an `evaluate-skill` pass means.

2. **`gate_pass` is three-state, not boolean.** A boolean cannot tell "static passed, delta not applicable" (a scaffold skill) apart from "static passed, delta failed." Forcing a boolean would make scaffolds either falsely pass or falsely fail. `gate_pass` is now `pass | fail | static_only`, carried alongside `tier` and `evaluated_layers` so a `pass` is always read relative to what actually ran. `static_only` is the honest state for "effect layer was required but no held-out set was available."

3. **Waivers can never touch the fatal checks.** A waiver layer is useful for non-load-bearing structural defects (a tiny utility skill legitimately lacking a high-risk blacklist). But if a waiver could set aside negative transfer or a safety regression, the one unbreakable gate would have a hole and would stop being a gate. Waivers therefore apply to **structural findings only**; the effect layer has no waiver field at all.

4. **The delta layer is bound to tiering.** Tier 2 needs an executor and real inputs, which are not present at every call (e.g. "review this draft skill" supplies no task set). So the effect layer is mandatory only for **production/library** skills; **scaffold** skills run the static read plus a single smoke case. Held-out tasks come from, in order: the caller supplies them; or three happy-path plus one edge task are drafted and confirmed before scoring; or, for scaffolds, one smoke case. If a production skill is evaluated but no held-out set can be obtained, the layer is not silently skipped — it reports `static_only`.

## Architecture decision: a top-level shared gate

**Context.** The two skills are used both together (evaluate → improve) and independently. The gate logic must exist once but must not make either skill depend on the other being present.

**Options considered.** (a) `improve-skill` calls `evaluate-skill` as a subroutine — rejected, because it couples the two and breaks standalone `improve-skill`. (b) The gate lives inside `evaluate-skill` and `improve-skill` reaches into it — rejected, because it makes `improve-skill` depend on a sibling it doesn't own. (c) **A neutral top-level `shared/effect-gate.md` that both reference as equals** — adopted.

**Consequences.** The gate is specified once; changing a threshold changes one file and both skills follow. Each skill still runs standalone because each depends only on that one shared file (which travels with the skill when it is distributed alone, the same way a skill's `references/` do). `improve-skill` got *simpler*: its `rubric.md` is now purely a *diagnosis* aid (which dimension to fix next), and its `ratchet-protocol.md` decision table now just consumes the shared gate's output instead of re-deriving baseline and negative-transfer logic.

## Tiering, deliberately

The delta layer is not forced on every skill. A throwaway scaffold pays only for the static read plus a smoke case; only production and library skills must clear the full with/without delta. This keeps the evaluator from imposing a heavy harness on skills that don't warrant it.

## What was deliberately not added

The change intentionally avoids the heavy-toolkit direction: no telemetry, no registry, no evidence ledger, no zoo of report types, no HTML studio, no drift dashboard. By the toolkit's own ruler these are tool-level over-fill. What ships is exactly: one structural report, the output scorecard (plus the route scorecard), one gate, one fix list. The standing rule for any future report type is the deletion test — *remove it; does the gate still decide correctly?* If yes, it is not added.

## Self-consistency

The gate's order — change → measure → keep/revert — is a *measurement protocol*, not task orchestration, and is therefore exempt from the shuffle test (the legitimate epistemic-order exception, `docs/THEORY.md` §8). That exemption is what lets `evaluate-skill` apply this gate to skills, and to itself, without becoming a procedural skill.

## Files changed

- **new** `shared/effect-gate.md` — the single measurement gate: protocol, gate rule, held-out sourcing by tier, and the shared JSON schemas (finding, failure_taxonomy, effect report, gate object).
- **rewritten** `skills/evaluate-skill/SKILL.md` — two tiers, two scorecards, json+md output, three-state `gate_pass`, fix list, waiver layer, tiering; Tier 2 references the shared gate.
- **rewritten** `skills/improve-skill/SKILL.md` — keep/revert delegated to the shared gate; only loop-specific machinery (bounded step, ratchet, rolling memory, plateau-break) kept.
- **rewritten** `skills/improve-skill/references/rubric.md` — now a diagnosis-only rubric; effectiveness measurement explicitly handed to the shared gate.
- **rewritten** `skills/improve-skill/references/ratchet-protocol.md` — decision table now consumes the shared gate's `gate_pass` / `delta`.
- **edited** `skills/improve-skill/references/failure-driven.md` — gate reference repointed to the shared gate.
- **edited** `README.md` — `shared/` added to the layout; design notes updated.

## Verification

All four skills pass the mechanical linter with zero blocking findings; the shared-gate cross-references resolve from every referencing file; the bundle is clean of out-of-scope vocabulary; the dogfooding CI passes.

---

### Also in this iteration (for the record)

Before this upgrade, the project was renamed from `skill-craft` to **skillwise** (the four skills spell **W**rite / **I**mprove / **S**eek / **E**valuate) and restructured to the conventional Agent Skills layout: skill folders under `skills/`, documentation under `docs/`, and `.claude-plugin/` manifests so the same repo installs via `npx skills add`, via the Claude Code plugin marketplace, or by manual copy — one layout serving every install path. A `CONTRIBUTING.md`, a dogfooding lint CI, an MIT `LICENSE`, and a `--check` flag on the linter (non-zero exit on blocking findings, for CI) were added at the same time.
