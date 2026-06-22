---
name: choose-cache-eviction-policy
description: Decide which cache eviction policy fits a workload when the choice isn't obvious. Use when a cache is thrashing, hit-rate is low, or someone asks "LRU or LFU?" and the access pattern is unclear. Not for sizing the cache or picking a cache library.
---

# Choosing a Cache Eviction Policy

This is a judgment skill: it supplies the decision fences, not a procedure.

## Decide by access pattern

- Recency-dominated (recent items re-accessed soon) → LRU.
- Frequency-dominated (a hot set re-accessed over long spans) → LFU.
- Scan-heavy / one-pass workloads → LRU-K or ARC; plain LRU gets polluted.
- Mixed / unknown → ARC (adapts between recency and frequency).

## Never

- Never pick LFU when the working set drifts — stale-but-once-hot items pin the cache.
- Never tune the policy before measuring the actual hit-rate; guessing wastes the choice.

## done_when

The policy is justified against the measured access pattern, and the failure mode of the
rejected alternative is named.
