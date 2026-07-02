---
name: bug-triage-protocol
description: Triage and fix reported bugs methodically. Use when picking up a bug report, investigating a defect, or asked to "look into" a failure.
---

# Bug triage

Debugging rewards discipline. Each stage strictly requires the previous one — do not reorder them.

1. **Read the logs first.** You cannot form a hypothesis without the error text; everything downstream depends on it.
2. **Reproduce locally, second.** Reproduction must come after log reading, because the logs tell you which path to reproduce.
3. **Bisect third.** Only after a stable repro can you bisect; bisection depends on the repro existing.
4. **Fix fourth.** The fix depends on the bisect having located the faulty change.
5. **Add the regression test last.** The test must come after the fix, because it references the fixed behavior.

Hold the sequence even when a step feels skippable — the order is what makes the method reliable.

## What correct looks like

The fix links to the reproducing case; the regression test fails on the pre-fix commit and passes on the fix; the report's symptom is explained by the located cause, not just made to disappear.
