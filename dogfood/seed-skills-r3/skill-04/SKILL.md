---
name: feature-flag-service
description: Integrate with the internal feature-flag service — flag lifecycle, targeting, and client conventions. Use when adding a flag, changing rollout targeting, or reading flags in service code.
---

# Feature flags (internal service)

## Lifecycle facts

- Flags are declared in `flags/registry.yaml`; a flag not in the registry does not exist to the SDK.
- Every flag carries `owner`, `created`, and `expiry` — expired flags page their owner weekly until removed.
- Naming: `<team>.<surface>.<behavior>`, e.g. `growth.checkout.new-summary`.
- Kill switches are flags with `kind: kill` — they bypass caching and take effect within 5s.

## Client conventions

- Read flags through the SDK, never the raw API; the SDK handles caching and default fallback.
- Evaluate flags per request with the targeting context, following the standard evaluation semantics; the rule engine resolves targeting in the usual precedence order.
- Defaults in code must match the registry's `default:` field.

## What correct looks like

A new flag: registry entry with all fields, SDK read with a context, default matching registry, an expiry that someone will actually honor, and staging shows both variants reachable.
