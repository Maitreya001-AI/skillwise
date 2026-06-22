# A Theory of Skills: classification, content, authoring, and evolution

A self-contained derivation of what an agent skill is, how to classify one, what to put in it, how to write it, and how to let it improve over time. The reasoning stands on its own; the empirical claims are cited to published work in the References. Where this document names a phenomenon (e.g. *skill inertia*), the name is the document's own term for an effect the cited evidence demonstrates, not a claim of prior coinage.

A *skill*, in the sense used here, is the unit defined by the Agent Skills standard: a `SKILL.md` file (YAML frontmatter + Markdown body) plus optional bundled `scripts/`, `references/`, and `assets/`, loaded on demand by a base agent ([Anthropic Agent Skills](https://agentskills.io/skill-creation/best-practices)).

---

## 0. The premise: the engine is free

A modern base agent already ships a general symbol-level reasoning engine: it reads schemas, writes code, maps intent to operations, recovers from malformed input, and orchestrates multi-step work — plus general knowledge up to its training cutoff. Call the existence of this engine **Proposition A**. It is free.

A skill earns its place only by supplying something this free engine *lacks* on a specific task. So the entire design question collapses to one:

> **What can the engine lack?**

---

## 1. Classification: the kinds of gap are the kinds of skill

List what the engine already has, and the gaps reduce to four. They are mutually exclusive and jointly exhaustive, and they line up with the knowledge-level / symbol-level distinction.

| atom | the gap | layer |
|---|---|---|
| **Knowledge** | a missing fact (current, private, domain-specific) | knowledge |
| **Capability** | a missing reliable primitive | symbol |
| **Judgment** | a missing criterion for "right / good / forbidden" | knowledge |
| **Control** | a missing non-default loop | loop governance |

**There is no "procedure" or "workflow" type.** Orchestration is exactly Proposition A — free. A procedure skill therefore supplies a gap that does not exist; worse, it fights the engine's own default loop. We call this failure **skill inertia**: the skill prescribes a sequence of steps while the agent optimizes for the *outcome*, so once the outcome is reached the skill is still pushing it forward, or it skips and reorders steps the author froze. The empirical shadow of this is direct: human-curated skills raise agent pass rates by 16.2 points on average, but naively self-generated skills *degrade* performance by 1.3 points, encoding overly specific or incorrect procedure ([SoK: Agentic Skills](https://arxiv.org/abs/2602.20867), reporting SkillsBench).

This is a contested point, and the strongest opposing view deserves a fair hearing. A recent review argues that *operational procedure* — decomposition into steps, dependencies, stopping conditions — is itself worth externalizing, because many agent errors are process-level (skipped steps, misordered operations, premature termination), not action-level ([Externalization in LLM Agents](https://arxiv.org/abs/2604.08224)). The reconciliation is precise: that same review lists three components of skill expertise — operational procedure, **decision heuristics**, and **normative constraints**. The latter two are this theory's Judgment and Control atoms. The disagreement is only over the first: freezing a literal step-march causes inertia, whereas encoding the *stopping conditions and decision heuristics* (Control + Judgment) captures the genuine process knowledge without welding an order. Procedure is not a type; the parts of "procedure" that are real gaps are Judgment and Control.

**Real skills are usually composites.** A domain skill (e.g. a DDD modeling skill, a spreadsheet skill) is Knowledge + Capability + Judgment. An extraction/pipeline skill is Control + Judgment + Capability. Decompose a composite into its atoms and the right place for a human checkpoint reveals itself: it sits at the seam between the *judgment* component and the *control/capability* component.

---

## 2. Content: describe the world, leave "how" to the engine

A well-written skill describes three things and stops:

1. the **world** the agent operates in — concepts, types, relations, structure;
2. **what counts as correct** in that world — constraints, invariants, semantic signals;
3. **what the user likely wants** — vocabulary mapping, scenario knowledge.

Then it leaves "how" to the engine. The flow is not forgotten; it is the engine's job, and the engine adapts it to context better than any frozen script. This matches the standard guidance that skills should describe the *properties of correct output*, and that skills generated without real domain context collapse into vague generic procedure ([Anthropic Agent Skills best practices](https://agentskills.io/skill-creation/best-practices)).

For a domain composite, a useful default body has these sections, derived from the path an agent walks when it uses one element of a domain: **Vocabulary + Purpose** (is this the right kind of element?), **Contrast** (which similar element? — only if confusable ones exist), **Structure** (what do the fields take?), **Relationships** (how does it attach to others?), **Rendering** (what does it look like when realized? — only if visual), **Rules** (hard invariants), **Heuristics** (soft experience, scenario recipes).

> The **Rules** section has a second life: every hard invariant is both a candidate **primitive** (§3) and a candidate **exit check** (§4). The **Heuristics** section produces nothing mechanical — that is judgment, and judgment belongs to the engine.

---

## 3. The hidden gap: provide primitives, guard with a semantic exit

"Describe the knowledge, the engine implements it" quietly bundles two claims:

- **Proposition A — the engine exists** (it has general reasoning *ability*). True.
- **Proposition B — the primitives are ready** (the domain *operations* the engine will act through already exist). Often false.

When B fails, the engine has the ability but not the material, so it improvises a private, unreviewed primitive at runtime — and that improvised layer is where silent bugs live. A representative failure: at scale the engine writes a throwaway script to generate output in bulk; a constructor takes positional arguments; a value meant for one field lands in another; the error is copied across hundreds of elements. The skill never saw the script, the positional call had no field names to flag the mistake, and a schema validator only asks "is this well-formed?" — all three checks stay silent. This trajectory-replay danger is exactly what trajectory-faithful extractors reproduce when they compile an action sequence directly into a skill ([AXIS](https://arxiv.org/abs/2409.17140)).

Defend at both ends:

- **Entry — supply a named-field primitive** so a wrong value has no slot to land in: `build({kind, label, tags, note})`, never positional. This lowers error *frequency*; it is not a guarantee.
- **Exit — a semantic verifier** that checks the *product* against "what correct looks like," not "is it well-formed." This is immune to how the output was produced, and it is the *only* guarantee.

**Primitive granularity — the shuffle test.** Hand the engine all the primitives in scrambled order. Still completes the task → you gave vocabulary (correct). Only works in your order → you welded in a procedure (over-fill). Too coarse (`buildWholeArtifactFromIntent()`) swallows the engine's semantic judgment; too fine (`setKind`/`addTag`/`setNote` as a mandatory sequence) needs a manual, which is a procedure in disguise. The right band seals exactly one class of mechanical correctness and zero semantic judgment.

> Packaging is not layer. A script in `scripts/` is still a symbol-level primitive. The body *may state that a primitive exists* ("use `scripts/build`, which forces named fields"); it *must not* narrate the call sequence. Stating existence is knowledge; narrating flow crosses a layer.

---

## 4. Correctness: a ruler you can run

> **Correct = the gap is filled exactly** — not under-filled, not over-filled, in the right layer, with a verifiable exit.

Five tests, each catching one failure and naming it:

1. **Deletion test — is there a gap?** Remove the skill, run the typical task. Still passes → the skill supplies Proposition A and should not exist (pure over-fill). Ask "should this exist?" before "is it correct?"
2. **Improvisation test — under-fill?** Run the typical task; count how much gap-bearing material the engine had to improvise. Greater than zero → under-fill.
3. **Shuffle test — over-fill?** Scramble the primitives; still works → vocabulary; order-dependent → welded procedure.
4. **Inertia-cost test — over-fill's other face.** On a task the engine already handles, compare with/without the skill. Markedly longer or costlier with no gain → skill inertia.
5. **Exit test — guaranteeable?** Is there a semantic check against "what correct looks like"? None → the skill cannot guarantee a correct result.

For composites, add the **seam test**: the human checkpoint must sit at the boundary between the judgment component and the control/capability component; misplacement means the machine overstepped into judgment (over-fill) or a human was inserted where automation belonged (under-fill).

**Type-specific discipline:**

| type | characteristic failure | discipline | exit |
|---|---|---|---|
| Knowledge | goes stale, floods context | body routes only, never inlines facts; carries version/date | freshness check |
| Capability | wrong primitive granularity | seal mechanical correctness, leave semantic judgment to the engine | bundled tests + plausibility |
| Judgment | written as procedure → inertia | declare what "right/good/forbidden" looks like; taste as negative fences | "is this plausible?" |
| Control | loop hard-coded as steps | declare `done_when` + role separation; iteration left to the engine | the `done_when` predicate |

**A caution about screening skills by reading them.** Textual plausibility has diverged from actual utility: an unguided LLM judge asked which of two skills will perform better picks correctly only 46.4% of the time — no better than chance, and on clear cases it tends to pick the *worse*-reading-better skill, because fluent prose does not predict downstream gain ([SkillLens, summarized here](https://dev.to/wonderlab/is-your-agent-skill-actually-good-microsofts-dual-paper-deep-dive-into-skill-evaluation-and-28b7)). The practical consequences: (a) the only reliable verdict compares the skill *as an intervention* against a no-skill baseline ([SkillGen](https://arxiv.org/abs/2605.10999) models skills exactly this way); (b) take the median of two or more independent judges rather than trusting one. Three reading-level signals do correlate with utility and are worth checking explicitly: whether the skill encodes failure mechanisms (`if X then Y else Z`), whether instructions are executable rather than hedged, and whether it carries a dedicated high-risk-action blacklist. Apply these type-aware — for Knowledge and Judgment skills, "has a workflow" is not a virtue.

---

## 5. Evolution: monotone improvement behind a gate

To let a skill improve from experience without degrading or drifting, the control gates matter more than any clever induction.

- **Batch, don't react serially.** Induce over a diverse pool of trajectories rather than reacting to one at a time; serial reaction overfits to trajectory-local lessons ([Trace2Skill](https://www.emergentmind.com/topics/trace2skill)).
- **Validation gate (default deny).** Every edit must beat the skill's **own previous accepted version beyond measurement noise** on a fixed held-out set (`delta_step > noise_band`), never falling below a permanent no-skill **floor**, or it is rejected. Beating *no-skill* is a separate, one-time *existence* question (`delta_exist`); an iterator keyed on it stalls whenever the base model already ceilings the task, so the per-round criterion is improvement-vs-previous, not existence-vs-baseline. A set with no headroom to show a gain is reported unfit and hardened, not used to reject. This is the single cut that turns unconditional self-editing into propose-and-test, and the only source of monotone, non-degrading improvement ([SkillOpt](https://arxiv.org/abs/2605.23904)).
- **Bounded step.** A textual learning rate: cap how much one edit may change, to forbid destructive single-step rewrites ([SkillOpt](https://arxiv.org/abs/2605.23904)).
- **Persist negative knowledge.** Rejected edits go into a buffer with the score drop they caused, so the optimizer stops repeating them ([SkillOpt](https://arxiv.org/abs/2605.23904)).
- **Tune the experience diet.** Do not learn from an all-failure pool; the optimal success/failure ratio is domain-specific ([SkillLens](https://dev.to/wonderlab/is-your-agent-skill-actually-good-microsofts-dual-paper-deep-dive-into-skill-evaluation-and-28b7)).
- **Separate roles.** Extractor, executor, and evaluator are distinct jobs that must not inherit each other's bias; an information-isolated verifier produces reliable signal even without ground truth ([CoEvoSkills](https://arxiv.org/abs/2604.01687)).
- **Treat safety as a loss.** Refusal rate, attack-success rate, and scope-creep into judgment the engine should own belong in the same gate; skill files are a real attack surface ([Skill-Inject](https://arxiv.org/abs/2602.20156)).
- **Break plateaus.** When progress stalls, allow one larger exploratory rewrite that may exceed the step budget, then keep it only if it clears the gate.

---

## 6. Confluence: one axis

The taxonomy, the content rules, the correctness ruler, and the evolution gates are one axis: **how much is left to the engine.** Classify a skill by which gap it fills; write it by filling that gap at the right layer and deleting whatever the engine already supplies; guard the hidden primitive gap with a named entry and a semantic exit; verify at the exit; and let it climb monotonically behind a gate.

---

## 7. Four meta-skills fall out

Applying the theory to skills *about skills* yields four, with one kernel:

| skill | what it is | type |
|---|---|---|
| **evaluate-skill** | the correctness ruler of §4 (the kernel / exit verifier) | Judgment + Capability |
| **write-skill** | the ruler run in reverse — author by hand (§1–4) | Judgment + Knowledge |
| **seek-skill** | write-skill driven by a corpus — discovery from experience (§5, §9) | Control + Judgment + Capability |
| **improve-skill** | the ruler in a gated loop (§5) | Control + Judgment + Capability |

`evaluate-skill` is the kernel; `write-skill` and `seek-skill` call it as an exit gate (the gate's **existence** branch, `delta_exist` vs no-skill), and `improve-skill` runs its structural read while applying the gate's **improvement** branch (`delta_step` vs the previous version) inside its loop. Each of the four obeys the theory it encodes: all are declarative rather than step-marches, `evaluate-skill` ships a mechanical entry primitive and defers the guarantee to a semantic read, and `improve-skill`/`seek-skill` specify only `done_when` + role separation + gates, leaving iteration to the engine.

---

## 8. Two refinements the theory needs

Two qualifications keep the rules from contradicting themselves in practice.

**The shuffle test exempts measurement-protocol order.** A validation loop's core sequence — change, then measure, then keep-or-revert — is *epistemic*, not task orchestration: you cannot have a gate without "measure after change." So distinguish task-orchestration order (welding it causes inertia — forbidden) from measurement-protocol order (legitimate, and is the gate's definition). The latter is not over-fill.

**"Leave iteration to the engine" is qualified for Control skills.** Agents do not reliably gate themselves — that is precisely why self-generated skills can degrade performance. So leave *task* iteration to the engine, but make the *gate protocol* concrete and non-skippable. This is the corollary of the first refinement: the gate protocol is exactly the legitimate measurement-protocol order.

---

## 9. Two front-ends: extraction (seeking) and failure-driven evolution

§5 governs editing a skill that exists. Two front-ends decide where skills *come from*. The lifecycle is three stages: experience generation → skill extraction → skill consumption ([SkillLens](https://dev.to/wonderlab/is-your-agent-skill-actually-good-microsofts-dual-paper-deep-dive-into-skill-evaluation-and-28b7)).

**9.1 What self-evolution needs (the information set).** In rough order of importance: (1) *full trajectories*, not just outcomes — inputs, actions, tool calls, intermediate states, and especially the primitives improvised at runtime, where the §3 hidden gap lives; (2) an *outcome signal* per trajectory; (3) *contrast* — each failure paired with a neighboring success, because a lone failure has no anchor and all-failure pools produce the worst skills; (4) a *held-out selection set* disjoint from the mining pool — what makes this optimization rather than distillation; (5) the *current skill state*, to revise rather than rediscover and to preserve old capabilities; (6) a *rejected-edit buffer*; (7) a *semantic verifier* (the exit); (8) *safety signals*; (9) an *experience-diet knob*.

**9.2 Extraction (seeking) is write-skill driven by a corpus.** It adds two things to authoring: a classification front-end and a held-out gate. The recurring trap is to compile the *trajectory* (an action sequence) into the skill — over-fill by §1. Extraction must distil the *pattern* (which gap recurs), not the *path*. The loop: induce recurring patterns over a diverse pool in batch ([Trace2Skill](https://www.emergentmind.com/topics/trace2skill)); classify each pattern's gap (missing fact → Knowledge; mis-improvised operation → Capability primitive; recurring "what good looks like" → Judgment; non-default loop → Control); materialize type-disciplined; gate on the held-out set as an intervention against a no-skill baseline ([MUSE-Autoskill](https://arxiv.org/abs/2605.27366) uses exactly this with/without protocol; [SkillX](https://arxiv.org/abs/2604.04804) adds exploratory expansion beyond seed data); dedup and preserve against the existing library ([SkillClaw](https://arxiv.org/abs/2604.08377)).

**9.3 Failure-driven evolution swaps the diagnosis source.** The unit of learning is the *contrastive pair* (failure × neighboring success), not the lone failure: locate the behavior present in the success and absent in the failure ([SkillGen](https://arxiv.org/abs/2605.10999) calls this contrastive induction; [CODESKILL](https://arxiv.org/abs/2605.25430) pairs a failing trajectory with an existing skill to expose its missing conditions). Extract a signature — `trigger → symptom → the branch the success took` — and feed it as a candidate edit into the same ratchet and gate as §5. If a failure cluster has no neighboring success, the skill likely needs a *new* capability — route to extraction, not editing.

> Three evolution failure modes justify the gates. **Memory-rot:** an early wrong edit, having passed the gate once, is later replayed as ground truth — so held-out tasks must be fresh, never the skill's own past output. **Sequential overfitting:** reacting one failure at a time overfits trajectory-local lessons — so batch-induce over a cluster (≥3 sharing a signature), never edit from n=1. **Misevolution:** accumulating patches can lower safety alignment — so the safety gate runs on every edit. Ungated self-modification is not evolution; it is controlled degradation.

---

## References

All links verified reachable. Where a finding is most accessibly summarized in a secondary source, that source is linked and the primary work named.

- **SoK: Agentic Skills — Beyond Tool Use in LLM Agents.** https://arxiv.org/abs/2602.20867 — skill as procedural memory; reports SkillsBench (+16.2pp curated, −1.3pp self-generated).
- **Externalization in LLM Agents: A Unified Review.** https://arxiv.org/abs/2604.08224 — the opposing view on externalizing procedure; the three components of skill expertise.
- **SkillGen: Verified Inference-Time Agent Skill Synthesis.** https://arxiv.org/abs/2605.10999 — contrastive induction over success/failure; skills modeled as interventions.
- **SkillOpt: Executive Strategy for Self-Evolving Agent Skills.** https://arxiv.org/abs/2605.23904 — validation gate, text learning rate, rejected-edit buffer.
- **SkillLens** (companion to SkillOpt). Summary: https://dev.to/wonderlab/is-your-agent-skill-actually-good-microsofts-dual-paper-deep-dive-into-skill-evaluation-and-28b7 — extractor≠target roles; success/failure diet; 46.4% unguided-judge accuracy.
- **CoEvoSkills / EvoSkills: Self-Evolving Agent Skills via Co-Evolutionary Verification.** https://arxiv.org/abs/2604.01687 · https://evoskills.net — information-isolated surrogate verifier; multi-file skill packages; 32%→75% on SkillsBench.
- **Trace2Skill.** https://www.emergentmind.com/topics/trace2skill — batch induction of transferable skills from trajectories.
- **MUSE-Autoskill.** https://arxiv.org/abs/2605.27366 — two-phase with/without skill-generation protocol.
- **SkillX: Automatically Constructing Skill Knowledge Bases.** https://arxiv.org/abs/2604.04804 · https://github.com/zjunlp/SkillX — iterative refinement and exploratory skill expansion.
- **AXIS: API-First LLM-Based Agents.** https://arxiv.org/abs/2409.17140 — trajectory-faithful skill generation (the replay trap).
- **SkillClaw: Let Skills Evolve Collectively.** https://arxiv.org/abs/2604.08377 — collective evolution; analyzing both successes and failures.
- **CODESKILL: Learning Self-Evolving Skills for Coding Agents.** https://arxiv.org/abs/2605.25430 — failure-paired skill revision learned from downstream feedback.
- **Skill-Inject: Measuring Agent Vulnerability to Skill File Attacks.** https://arxiv.org/abs/2602.20156 · https://www.skill-inject.com — skills as an attack surface (up to ~80% ASR).
- **Automated Skill Discovery through Exploration and Iterative Feedback.** https://arxiv.org/abs/2506.04287 — exploration-based trajectory synthesis.
- **Anthropic Agent Skills — best practices.** https://agentskills.io/skill-creation/best-practices — the SKILL.md standard; grounding extraction in real task context.

## License

Released under the MIT License (see `LICENSE`). Contributions welcome.
