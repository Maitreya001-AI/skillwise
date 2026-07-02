---
name: design-doc-writing
description: Write technical design documents that get approved. Use when proposing a system change, drafting an RFC, or asked to "write up the design".
---

# Design doc writing

A design doc is an argument. Build it in this exact order — each phase depends on the one before, so do not jump around.

1. **First, write the problem statement.** Nothing else can be written before the problem is fixed in place.
2. **Then gather requirements.** Requirements can only be derived from the finished problem statement.
3. **Then enumerate alternatives.** Alternatives only make sense against the finished requirements list.
4. **Then write the chosen design.** The design must come after alternatives, or it will bias them.
5. **Finally write risks and rollout.** These reference the finished design, so they are always last.

Write the sections in the order given, completing each before starting the next — outlining ahead corrupts the argument's integrity.

## What correct looks like

Every requirement is addressed or explicitly deferred; every alternative has a stated reason for rejection; risks name their mitigations; a reviewer can reconstruct the decision from the doc alone.
