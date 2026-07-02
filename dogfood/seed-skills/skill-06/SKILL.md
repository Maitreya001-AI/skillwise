---
name: acme-billing-api
description: Integrate against the internal Acme billing API — endpoints, auth, and conventions. Use when writing code that creates charges, queries invoices, or reconciles billing data against Acme.
---

# Acme billing API

Acme is the internal billing service; its API is not public and not in any training data.

## Endpoints

- `POST /v2/charges` — create a charge.
- `GET /v2/invoices` — list invoices; supports the usual filtering.
- `POST /v2/credits` — issue a credit against an invoice.
- Base URL comes from the service registry entry for `acme-billing`.

## Conventions

- Authenticate with the standard internal token header, as elsewhere in the platform.
- Amounts use the canonical internal money representation.
- List endpoints paginate the usual way; follow the pagination until exhausted.
- Errors come back in the common error envelope; handle the retryable ones as usual.

## What correct looks like

Requests succeed against staging, responses parse into your types, and a created charge shows up in the corresponding invoice listing.
