---
name: oncall-handoff-notes
description: Write the end-of-shift on-call handoff in this team's format. Use at shift change, when asked to "hand off", or when tidying an outgoing on-call's notes.
---

# On-call handoff notes

## The org's shape (the incoming person greps for these)

- Header: shift window (UTC), outgoing/incoming names, pager load (`quiet | normal | loud`).
- **Open threads** — one per line: `[severity] short title — current state — next action — link`. A thread with no next action is not handed off, it is dropped; write the next action even if it is "watch until Xh".
- **Silenced/suppressed alerts** with expiry times — the classic handoff failure is a silence that outlives its reason.
- **Changes landed during shift** that are still in their soak window, with revert links.
- **Nothing-happened shifts still produce notes** (header + "no open threads") so silence is distinguishable from a missing handoff.

## Fences

- Never editorialize about other teams in a handoff (it is a searchable record).
- Never hand off a thread whose only state is "investigating" — say what was ruled out.

## Exit

Before posting: every open thread has all four fields; every silence has an expiry; every soak-window change has a revert link. Grep the artifact for the three lists — do not certify from memory.
