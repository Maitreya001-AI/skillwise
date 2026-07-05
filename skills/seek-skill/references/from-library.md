# from-library — the static-source adapter (decompile a library into a skill)

An adapter for `seek-skill`'s gap-reading slot, for when the corpus is a **static artifact** — a library, SDK, or wrapper — rather than behavioral traces. Everything downstream of the front-end is the shared tail and is not restated here: site classification (SKILL.md), materialization (`write-skill`), certification (`references/effect-gate.md`, existence branch).

**Why this source exists.** Rigidification gaps are structurally invisible to trace-driven seeking: a wrapper suppresses its own failure signal — tasks pass while the wrapped facts quietly decay — and nothing surfaces in a trajectory pool until an interface change or boundary shift breaks the wrapper all at once. A library must therefore be read *structurally*, not behaviorally. Same operation (create-from-source), different way of reading where the gap is.

## The adapter's question

Given a library: **should it be decompiled into a skill at all — and if so, which of its atoms should be unwrapped into declarative form, and which must stay compiled?** "Decompile everything" and "wrap and forget" are both wrong by default; the split is per-atom.

## Front-end: four-atom decomposition + rigidification triage (L1 — a prediction, never a verdict)

Decompose the library along the four sites (THEORY §2):

| atom | what to look for in a library |
|---|---|
| **Σ (Knowledge)** | hardcoded facts that will change: field semantics, endpoints, rate limits, magic constants, undocumented conventions |
| **Π (Capability)** | the operations it implements — parsing, protocol handling, retries-as-code |
| **φ (Judgment)** | built-in notions of "valid / allowed": schema checks, error taxonomies, response validation |
| **γ (Control)** | loops it enforces: retry/backoff policy, session lifecycle, pagination protocol |

Then triage — rank the decompile value:

```
decompile-value ∝ (Σ-share + φ-share) × change-rate ÷ Π-implementation-difficulty
```

`change-rate` is estimated from observables: git history of the wrapped surface, upstream release cadence, issue churn on breakage reports. High Σ/φ share × high change rate means the library is mostly *rigidified facts and criteria* — the decay-prone half; high Π difficulty (hard algorithms, protocol state machines) weighs against unwrapping.

**Negative branch (mandatory, the discipline that keeps this honest).** A library with low Σ/φ share, low change rate, and high Π difficulty — the numpy class — must come out with **negative decompile value: do not decompose**. Record that verdict as a first-class product, exactly as the gate's `nogap` records "this skill should not exist": it is the deletion test applied at the library level. An adapter that can only ever say "decompile" is a router with one route.

> **Hard warning (§7).** The triage number is an **L1 prediction**: it orders candidates, it certifies nothing. Letting the formula's score stand in for the gate's delta is using L1's reliability to issue L2's conclusion. The only certification is the existence gate below — a skill with a glowing triage score and a failed gate is a failed skill.

## Materialization — the per-atom split (hand to `write-skill`)

- **Σ** → `references/`, lazy-loaded, stamped with version/date (decaying facts never inline).
- **φ** → declarative criteria: what a correct response/artifact looks like, error classes and their meaning.
- **Π** → **keep the compiled half compiled**: declare that the primitive exists and route to it — a thin wrapper or the library itself stays in `scripts/`/dependency form. Unwrapping a reliable primitive into prose re-opens the improvisation gap §4 closed (the form theorem violated in reverse).
- **γ** → `done_when` constraints and non-default loop policy, stated as constraints, never as steps.

**The trap, library form.** A usage example or canonical call sequence from the docs is **one concrete strategy** — compiling it into the skill is the same replay trap as compiling a trajectory (SKILL.md's opening trap). Extract what the sequence *protects* (a dependency fact → Σ, an ordering the product must exhibit → φ, an irreversibility → Σ-risk, a protocol → γ), never the sequence itself.

## The gate (L2 — unchanged machinery, two source-specific settings)

Certification is the shared existence gate — same fatals, same noise bands, same power check. Two things are instantiated by this adapter, not new rules:

- **The reference condition is the engine *with the raw library*** (the SDK-wrapper baseline), not bare no-skill. The existence question here is "does the decompiled form beat using the library as-is?" — a delta against empty hands would flatter every candidate.
- **Held-out tasks must press the rigidity surface**: interface-change tasks, boundary/edge-policy shifts, recomposition tasks that cut across the wrapper's grain. Happy-path tasks cannot express a rigidification gap — the wrapper doesn't break on them; a set made of such tasks routes to `unfit_test_set` (harden the set), never to a verdict.

## done_when (adapter-level)

One of three honest terminals: **decompiled and gated** (the skill passed the existence gate on a rigidity-surface set); **do-not-decompose** (the negative branch fired — a verdict, not a failure); **unfit_test_set** (no rigidity-surface tasks could be assembled — report what's missing, certify nothing).
