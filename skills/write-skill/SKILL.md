---
name: write-skill
description: Author a new, well-designed skill by hand — choose its classification, decide what belongs in the body versus scripts versus references, and write a SKILL.md that fills exactly the gap it should. Use this when the goal is to create, draft, or design a new skill, or to turn a known repeated task into a reusable skill. Use seek-skill instead when the skill should be discovered automatically from a corpus of traces rather than specified up front.
license: MIT
---

# Write a Skill

Writing a good skill is running the correctness ruler in reverse. Every construction move below is the inverse of a failure that `evaluate-skill` catches. You are satisfying a set of invariants, not following a procedure — they hold in any order, with a small partial order at the front: *gap located* (and, for a composite, its atom decomposition) comes first, since the later invariants — gap filled, right form, exit-per-gap, seam placed — all refer to it. What matters is that all hold at the end. The full derivation is in the skillwise repo's `docs/THEORY.md` (§2–§6).

## First, classify — what does the engine lack?

The engine is free (general reasoning, orchestration, schema-reading, code-writing). A skill fills a *gap*. There are four:

| atom | the gap | how you fill it |
|---|---|---|
| **Knowledge** | a fact the engine can't know | route to it; never inline decaying facts; stamp version/date |
| **Capability** | a reliable operation it keeps mis-improvising | ship a named primitive in `scripts/`, not prose |
| **Judgment** | a criterion for "right / good / forbidden" | declare what correct looks like; prefer negative fences for taste |
| **Control** | a non-default loop | declare `done_when` + role separation; leave *task* iteration to the engine, but make the gate/checkpoint protocol concrete and non-skippable (its order is epistemic — §3 cell 4; its non-skippability is §4's compilation requirement on Control) |

There is **no "procedure/workflow" type.** Orchestration is free; writing `Step 1/2/3` supplies a gap that doesn't exist and fights the engine's own loop (skill inertia). If you catch yourself writing an ordered march, stop and ask which of the six legitimate homes of order the sequence belongs to (§3): dependency, irreversibility, external mandate, epistemic protocol, product order, compiled order. An order that fits no cell is over-fill; an order that fits a cell gets *housed in that cell* (see "Engine's share deleted" below), not narrated as steps.

**Most skills are composites.** Name the atoms first: a domain/ontology skill (e.g. a DDD modeling skill, a spreadsheet skill) is Knowledge + Capability + Judgment; an extraction/pipeline skill is Control + Judgment + Capability. For a composite, the human checkpoint goes at the seam between the judgment component and the control/capability component — realized concretely as the `done_when`/role-separation boundary: the human owns the judgment call, the machine runs only once that sign-off exists.

## The body: describe the world, leave "how" to the engine

A correct body describes three things and stops: the **world** (concepts, types, relations), **what counts as correct** (constraints, invariants, semantic signals), and **what the user likely wants** (vocabulary, scenario knowledge). The flow isn't forgotten — it's the engine's job, done better than any frozen script.

For a domain composite, a useful default body, derived from the path an agent walks when using one element: **Vocabulary + Purpose**, **Contrast** (only if confusable elements exist), **Structure**, **Relationships**, **Rendering** (only if visual), **Rules**, **Heuristics**.

> **Rules has two lives.** Every hard invariant becomes a candidate **primitive** (a `scripts/` constructor that makes the invariant un-violable) and a candidate **exit check**. **Heuristics** generates nothing mechanical — that is judgment, which belongs to the engine.

## The hidden gap: primitives + a semantic exit

"You describe knowledge, the engine implements" hides a second claim: that the primitives the engine needs already exist. They often don't. When one is missing, the engine improvises a private, unreviewed primitive at runtime — and that is where silent bugs live (a value landing in the wrong field, copied across hundreds of elements, passing every format validator). Defend at both ends:

- **Entry:** a named-field primitive so a wrong value has no slot to land in — `build({kind, label, tags, note})`, never positional. This lowers frequency; it is not a guarantee.
- **Exit:** a semantic check against "what correct looks like," not "well-formed." This is the only guarantee.

**Granularity — the shuffle test.** Scramble your primitives and hand them to the engine: still completes → vocabulary (correct); only works in your order → a disguised procedure. Too coarse swallows the engine's judgment; too fine needs a manual. The right band seals one class of mechanical correctness and zero semantic judgment. A script in `scripts/` is still a primitive: the body may state it exists, but must not narrate its call sequence.

## The construction invariants (the ruler, reversed)

- **Gap located** — name which gap (or composite). If deletion leaves the task still passing, don't write it.
- **Gap filled** — the engine improvises nothing gap-bearing.
- **Engine's share deleted (the six-cell rewrite law, §3)** — delete every order that can be housed in **none** of the six cells (dependency / irreversibility / external mandate / epistemic protocol / product order / compiled order); what survives the shuffle test is exactly the cell-hosted remainder. Order that *does* have a cell is housed per cell, not narrated: a **product order** is rewritten as a φ with an exit check ("the artifact must exhibit this order" — cell 5's design law); **mechanical order** is compiled into `scripts/` (cell 6); **dependency and irreversibility** facts are stated as Σ; **external mandates and epistemic protocols** are declared as γ. Express Judgment/Control gaps as a `done_when` predicate / negative fences, never as fixed steps.
- **No inertia cost** — on a task the engine already handles, the skill adds no cost without gain (the inertia-cost test, over-fill's quieter face; at the certifying layer it is the gate's `cost_ratio` fatal).
- **Right form** — capability gaps shipped as primitives; where compilation is impossible or distribution forbids it, the reliance on engine compliance is stated, not hidden (§4 prices this trade-off).
- **Persona discharged (§5)** — the body carries no uncashed role/identity content ("you are an expert X"). A persona occupies no loop site: it names no checkable product property, supplies no fact or primitive, constrains no process — it only perturbs the four sites unaccountably, which makes it unauditable rather than illegal. As a *writing heuristic* it is legitimate (draft "like a senior reviewer", then interrogate yourself: *which criteria* does the senior reviewer apply?); before shipping it must be discharged into explicit atom content — "expert" usually raises φ implicitly, so write those criteria out. Empirical anchor: personas do not improve performance and their effects drift ([arXiv 2311.10054](https://arxiv.org/abs/2311.10054)).
- **Exit built** — a semantic check per filled gap. The only guarantee.
- **Seam placed** (composites) — the human checkpoint sits at the judgment ↔ control/capability boundary, as a `done_when`/role-separation handoff.
- **Failure mechanisms encoded** — key branches as `if X then Y else Z` (trigger → symptom → branch), not a happy path. (One of the three reading-level signals with validity evidence, §7.)
- **Executable, not hedged** — no "consider / as appropriate" where the type forbids it; templates, example I/O, numeric constraints. Relaxed for Judgment, where taste is negative fences.
- **High-risk fenced** — a dedicated "never do" section for any destructive or irreversible action. This is the *safety* guard, distinct from taste fences, and it is never waivable.
- **Routed by gap** — `description` says "use when X is missing" (not just "produces Y"), pushy enough to trigger on typical + colloquial phrasings, yet scoped to stay quiet on adjacent out-of-scope tasks.

## Exit gate

When the draft is done, run [`evaluate-skill`](../evaluate-skill/SKILL.md) on it — writing and judging are the same ruler in opposite directions. "Passes" is the gate's verdict, not a single self-read: Tier 1 needs **≥2 decorrelated judges** (different models or information-isolated contexts — a lone read is no better than chance, and a correlated second judge removes no shared bias), and for a production/library skill the true exit is Tier 1 clearance *and then* the **existence gate** (`delta_exist` beyond its noise band, vs no-skill) on a held-out set. A freshly hand-authored draft usually has no held-out set yet: as a *scaffold* it can reach `pass` on Tier 1 + a smoke case, but a *production/library* skill with no tasks yet honestly lands at **`static_only`** (structurally clean, effect unverified) until tasks are supplied — finished-pending-effect, not failure.

Route the outcome. A *structural* failure → [`improve-skill`](../improve-skill/SKILL.md). A draft that ties or loses to no-skill follows the **sub-floor routing** (one rule, shared with the gate — see effect-gate's "Sub-floor routing"): run the deletion test first; if `no_skill` already passes the typical tasks, that is **`nogap`** — the skill should not exist; don't ship it and don't try to improve it into existence. If the gap is real (`no_skill` fails) but the draft scores *below* no-skill, that is **negative transfer** — the filling is harmful but the gap exists: route to `improve-skill` with the negative transfer as the first repair target, and if no clean KEEP lands while the floor stays breached, escalate to [`seek-skill`](../seek-skill/SKILL.md) for a structural rethink. Either way, no quiet rewrite here.

## Mechanics

Layout: `skill-name/SKILL.md` (required) + optional `scripts/` (primitives), `references/` (loaded as needed), `assets/` (output templates). Frontmatter needs `name` + `description`. Keep SKILL.md under ~500 lines; route detail into `references/`. Progressive disclosure: metadata always loaded, body on trigger, resources as needed.
