---
name: grpc-service-naming
description: Name gRPC services, methods, and messages to this org's API standards. Use when designing or reviewing a proto file, adding an RPC, or naming request/response messages.
---

# gRPC naming (org standard)

Review-time law for proto files. Violations fail human review loudly at PR time — nothing downstream breaks silently — so these rules live as review criteria, not tooling.

## The rules

- Services are `<Domain>Service` (`LedgerService`), never `<Domain>API` or bare `<Domain>`.
- Methods are verb-first imperative: `CreateInvoice`, `ListCharges` — never `InvoiceCreate`, never `GetAll*`.
- Request/response messages pair with their method: `CreateInvoiceRequest` / `CreateInvoiceResponse`, even when the response is empty today (empty responses grow fields; `google.protobuf.Empty` freezes you).
- Streaming methods say so: `WatchOrders`, `StreamEvents` — a non-streaming `Watch*` fails review.
- Field names are `snake_case`; enums are `SCREAMING_SNAKE` with a zero value named `<ENUM>_UNSPECIFIED`.

## Exit

Review the proto diff against each rule above, rule by rule, before approving — the check is a manual read of the diff, which matches the stakes: a naming slip caught at review costs a comment; nothing silently corrupts.
