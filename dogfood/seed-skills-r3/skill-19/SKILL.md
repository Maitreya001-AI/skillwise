---
name: sdk-example-style
description: Write code examples for the public SDK docs to this product's example bar. Use when adding examples to docs, READMEs, or API reference pages, or reviewing example PRs.
---

# SDK example style — the bar

Examples are the most-copied code we publish; these rules exist because support tickets trace back to bad examples. They are review criteria applied by people reading example PRs — deliberately prose: examples span five SDK languages and the docs repo runs no execution environment for most of them.

## Fences

- Never use placeholder secrets that look real (`sk_live_...`) — always the documented test prefix (`sk_test_...`).
- Never swallow errors (`except: pass`, empty `catch`) — every example shows the error path or links the error-handling guide.
- Never hardcode regional endpoints — examples use the config default.
- Never show a polling loop where the SDK has a waiter/webhook — examples teach the right primitive.

## Positive shape

An example is runnable as pasted (imports included, no "..." in load-bearing positions), under 25 lines, and does exactly one thing. The first example on any page is the 80% use case, not the clever one.

## Exit

Review each example against the fences, then paste-run it in the language's sandbox where one exists (Python, Node); for the rest, a maintainer read-through against the fences is the check — stated plainly here because that is what the docs repo can actually enforce.
