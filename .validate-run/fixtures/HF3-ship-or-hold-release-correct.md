---
name: ship-or-hold-release
description: Decide whether a release candidate is safe to ship, then carry out the release. Use at go/no-go when risk is unclear and a human must own the call.
---

# Ship or Hold a Release

This is a composite skill: a go/no-go **judgment**, then the release **procedure**.

## Judge: go or no-go

- No-go if any P0 is open, smoke tests are red, or the change touches auth/payments without reviewer sign-off.
- Go only if rollback is one command and on-call is staffed.

## Human checkpoint — at the go/no-go seam

Before running any release step, surface the go/no-go judgment and the evidence behind it to the
release owner and require their explicit **go**. Everything below runs only after that sign-off.

## Run the release

1. Tag the candidate.
2. Build artifacts.
3. Deploy to production.
4. Run post-deploy smoke checks.
