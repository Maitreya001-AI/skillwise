---
name: pii-scrubber
description: Scrub PII from datasets, logs, and fixtures before they leave a protected boundary. Use when exporting data for debugging, building test fixtures from prod samples, or sharing logs outside the team.
---

# PII scrubbing

Hand-scrubbing misses fields; the primitives below exist because every incident postmortem in this area ends with "the grep missed one".

## Primitives

- `scripts/scrub.py --in <file> --out <file> --profile <logs|fixtures|export>` — field-aware scrubber: knows the org's PII field inventory (emails, names, gov IDs, device IDs, free-text notes) per profile; replaces with format-preserving tokens so downstream parsers keep working. Refuses unknown file shapes rather than passing them through.
- `scripts/verify_clean.py <file>` — the exit check: independent pattern+dictionary sweep over the *output* file; exits non-zero on any residual hit with file:line locations. Run it on the exact artifact that will leave the boundary.

## Facts

- The PII field inventory lives in `scripts/pii_fields.yaml`; new fields are added there, not in ad-hoc regexes.
- Free-text fields (support notes, addresses) are always dropped, never masked — masking free text is unverifiable.

## Never

- Never scrub by eyeball or one-off grep when the primitives are available.
- Never ship an artifact `verify_clean.py` hasn't passed, whatever the deadline.
