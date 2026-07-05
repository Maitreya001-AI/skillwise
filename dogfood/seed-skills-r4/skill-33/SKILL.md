---
name: config-change-ritual
description: Make configuration changes to services the disciplined way. Use when changing service config, feature flags defaults, or runtime settings in any environment.
---

# The config change ritual

Config changes go wrong when stages blur together. The ritual keeps each stage pure.

## The sequence

Work strictly in this order — the discipline is the sequence:

1. Update the runbook page first, before touching anything else. Writing the intent down first keeps it pure of implementation bias.
2. Only then edit the config value, in a change that touches nothing else.
3. Only after the config edit is complete, write the verification query you'll use — writing it earlier contaminates it with what you hope to see.
4. Land the change; never revisit the runbook or the query afterward, or the trail stops reflecting the sequence of decisions.
5. Run the verification query last, exactly as written.

Do not interleave these stages and do not batch several config changes through the ritual at once — mixing stages corrupts the decision trail.

## Exit

The runbook page, the config diff, and the verification query each exist as separate commits in ritual order, and the query result is pasted into the runbook page.
