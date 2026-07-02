---
name: python-collections-helper
description: Sort, deduplicate, group, and reshape Python lists and dicts correctly. Use when you need to sort a list by a key, remove duplicates while preserving order, invert a dict, group items, or flatten nested lists.
---

# Working with Python collections

Reliable patterns for the everyday reshaping of lists and dicts.

## Sorting

- Sort by a key: `sorted(items, key=lambda x: x.price)`; descending: add `reverse=True`.
- Stable multi-key sort: sort by the secondary key first, or use a tuple key `key=lambda x: (x.dept, x.name)`.

## Deduplicating

- Order-preserving dedup: `list(dict.fromkeys(seq))`.
- Dedup by a field: keep a `seen` set of keys and append unseen items.

## Grouping and reshaping

- Group into a dict of lists: `defaultdict(list)` then `groups[k].append(item)`.
- Invert a dict: `{v: k for k, v in d.items()}` (beware duplicate values — later keys win).
- Flatten one level: `[x for xs in nested for x in xs]`.

## What correct looks like

The reshaped collection round-trips: every input element is accounted for (dropped only by an explicit predicate), ordering claims hold on a spot-check of the first and last elements, and dedup output length equals the number of distinct keys.
