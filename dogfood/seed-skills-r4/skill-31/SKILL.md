---
name: acme-python-errors
description: Handle errors in Acme's Python services to the platform team's standard. Use when writing or reviewing exception handling, retries, or error logging in any Acme Python codebase.
---

# Acme error-handling standard

The platform team's bar for exception code across our services.

## The rules

- Catch the specific exception you can handle; a bare `except:` (or `except Exception:` without re-raise) never ships.
- Re-raise with cause preserved: `raise ServiceError(...) from e`, never a naked `raise ServiceError(...)` that severs the chain.
- Log at the boundary where the error is handled, once — not at every frame it passes through.
- Include operation context in the log line (what was being attempted, with which key identifiers), never just `str(e)`.
- Never swallow an error to "keep the service up" without a metric or log marking the swallow.
- Timeouts and retries live at the call site with explicit budgets; a retry loop without a cap never ships.

## Exit

Review the diff's error paths against each rule above before requesting review; fix violations first.
