---
name: skillwise
description: The explicit front door of the skillwise toolbox — routes a skill path, a requirement, or a corpus to the right door (evaluate / improve / write / seek) on observable evidence, then hands off and stops. Use when the user explicitly invokes /skillwise or names the skillwise toolbox itself; it stays out of automatic routing.
disable-model-invocation: true
allowed-tools: Bash(python3:*) Bash(ls:*) Read Grep
---

# /skillwise — the toolbox's explicit front door

**What this is.** The explicit entry to the skillwise toolbox: given a skill path, a requirement, or a corpus, it routes you through the correct door (evaluate / improve / write / seek) on observable evidence, and exits. It does not orchestrate what follows. The gap it fills: Σ about the toolbox itself (lifecycle state → four-door mapping, plus the verdict-artifact recognition convention) and a set of φ routing criteria; under explicit invocation the user is the router (THEORY §2, the consumption site) — what this skill replaces is "self-teach the four doors from the README".

**Probe before routing.** Run `python3 scripts/probe.py "$ARGUMENTS"` to get `state` and `evidence`. Probing precedes routing as a dependency order (THEORY §3 cell 1: a state that hasn't been classified can't be routed). The verdict-artifact recognition convention is compiled into the probe — it recognizes exactly `<skill-dir>/wise-eval.json` (evaluate-skill's pinned landing location) and does no fuzzy guessing.

**Routing criteria table.** Rows are state→door mapping criteria, not execution steps; on a match, hand off:

| evidence | door | why |
|---|---|---|
| `exists_with_verdict` | **improve-skill** | a verdict exists; what follows is repair (a `nogap` verdict gets retired by improve's own entry check — not this door's call) |
| `exists_no_verdict` | **evaluate-skill** | the skill exists but has no verdict — the verdict comes before anything else |
| `no_path` / `path_not_found`, and the input has corpus shape (traces, logs, transcripts, batches of sample files, or a library/SDK/codebase) | **seek-skill** | the target must be discovered from a corpus (a static library goes through seek's `from-library` source adapter) |
| `no_path` / `path_not_found`, and the input is spec-shaped (text describing what is wanted) | **write-skill** | the target is already specified |
| verb signals in the request text ("why doesn't it trigger" → verdict; "fix / improve" → improvement; "make me one" → write) | corroboration | when they conflict with file evidence, **file evidence wins** (observable > paraphrase) |

**Tie rules (apply before asking anything):**

- Spec and corpus both present → **seek-skill** (seek can consume a spec as a prior; write cannot consume a corpus).
- `path_not_found` → state plainly in the handoff line that the path did not resolve, and route by the shape of the remaining input (the seek/write rows).

**Residual question (at most one).** Only when the criteria table and the tie rules cannot decide uniquely (typical: a bare `/skillwise` with no input at all), ask exactly one question whose options are the undecided branches: "Is there an existing skill to work on, or do you want a new one? If new — do you have a requirement description, or a corpus?" Route on the answer. No second round of questions; if still undecidable, state honestly which evidence is missing and stop. (§6 seam theorem: where the criteria run out, the human owns the call; where they haven't, don't ask.)

**Handoff format and stop.** A handoff is one evidence-bearing line plus invoking the target skill:

```
route: <door> — evidence: <each evidence item>.
```

Invoke the target skill after the line (under a plugin install the name may be namespaced, e.g. `skillwise:evaluate-skill`), passing the path/input through verbatim. **The handoff is the end of this skill's job**: no supervising, no chaining into a second door, no restating how the target skill works. (A γ self-constraint; violating it grows exactly the procedure §3 excludes.)

**done_when**: a routing line with ≥1 observable evidence item was emitted and one handoff completed; or at most one residual question was asked and the handoff then completed; or the missing evidence was stated honestly and the skill stopped. One of the three — there is no other exit.
