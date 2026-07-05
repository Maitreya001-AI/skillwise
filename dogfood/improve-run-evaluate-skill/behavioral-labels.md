# Behavioral labeling of nogap-class seeds — pre-registered procedure

**Logged 2026-07-06, BEFORE any generation call ran.** Round-4 finding 2: labels for
style/convention seeds are by-construction assertions on the very axis under test (is this
content something a capable unaided engine already produces?). That question is the deletion
test — L2-native (§7) — so these labels are re-established *behaviorally* here, by actually
running an unaided engine, before any further repair round is scored.

## Scope (pinned)

All style/convention/best-practice-class seeds in the round-2..4 working set and the r2
screening set — 16 seeds:

| set | seed | current label |
|---|---|---|
| working | task-02 = r4/skill-31 acme-python-errors | broken/nogap |
| working | task-03 = r3/skill-02 git-commit-style | broken/nogap |
| working | task-04 = r4/skill-25 review-comment-etiquette | good |
| working | task-05 = r3/skill-03 support-macro-tone | good |
| working | task-10 = r4/skill-35 sql-review-bar | good |
| working | task-12 = r4/skill-26 postmortem-language | good |
| working | task-14 = r4/skill-32 platform-rest-pagination | broken/nogap |
| working | task-17 = r3/skill-09 grpc-service-naming | good |
| working | task-18 = r4/skill-36 terraform-naming | good |
| working | task-20 = r4/skill-27 exec-weekly-update | good |
| working | task-24 = r3/skill-14 json-formatting | broken/nogap |
| working | task-25 = r4/skill-28 docs-screenshot-standards | good |
| r2 | skill-02 warehouse SQL bar | good |
| r2 | skill-03 markdown-table-style | broken/nogap |
| r2 | skill-04 release-notes format | good |
| r2 | skill-11 handoff format | good |

Non-style seeds (control/capability/order/cost/exit classes) are out of scope — their labels
were never contested on this axis.

## Procedure (all engine calls: `claude -p --model sonnet`, fresh isolated headless sessions)

1. **Generation (×2 per seed).** From the seed's frontmatter `name` + `description` ONLY (never
   the body), prompt an unaided engine: *"You maintain engineering conventions for a team. For
   the artifact domain described below, write the concrete bar you would enforce — the 6–10
   specific rules a careful team applies when reviewing this kind of artifact. State each rule
   as an enforceable constraint, one bullet per rule. Do not explain; output only the rules.
   Domain: `<name>`: `<description>`"* Two independent samples; the **union** is the unaided
   bar (if either sample produces a rule, the engine derivably produces it).
2. **Rule extraction (mechanical).** The seed's rules = every `- ` bullet line in its body
   outside Exit/Done sections.
3. **Comparison (×2 per seed, isolated).** A comparator gets (A) the seed's rules verbatim and
   (B) the unaided union bar, never the seed's label or the purpose of the exercise. Per rule:
   `covered` (substance present in B, paraphrase allowed) vs `survives`; for survivors,
   `substantive: true` only if the rule names a specific enforced choice (threshold, grammar,
   format, named selection, stated as must/never/fails-review), not a vague preference.
   Strict-JSON output.
4. **Decision rule.** A rule is a *substantive survivor* iff **both** comparator runs mark it
   `survives` + `substantive`. Behavioral truth: **broken/nogap iff the seed has zero
   substantive survivors**; otherwise good (on this axis). If the two comparator runs disagree
   on whether the count is zero, a third comparator run decides by majority.
5. **Effect.** Seeds whose behavioral truth differs from the current label are relabeled for
   all FUTURE scoring (round 5 onward; r2 screening keys likewise). Past rounds' records stand
   unchanged, with a reinterpretation note where a "fatal" was scored against a label this
   procedure overturns. All generation/comparison artifacts land in `behavioral-labels-runs/`
   for audit.

**Known limits, accepted in advance:** two generation samples bound derivability from below
(more samples could only cover more, pushing labels *toward* nogap — so a "good" verdict here
is conservative in the direction that round 3/4's fatals bit); the comparator is a same-family
LLM (sonnet) judging coverage, mitigated by dual runs + majority; wrong-form/no-exit/order
labels are untouched — this procedure re-grounds the nogap axis only.
