---
name: customer-quote-approval
description: Produce and route customer quotes and discounts through the mandated approval chain. Use when preparing a quote, applying a discount, or asked to "get them a number today".
---

# Quote approval

The order here is contractual and regulatory, not workflow preference: our reseller agreements and revenue-recognition rules dictate who may see and approve numbers, and when.

- **Deal desk validates before any number leaves the building** — a quote shown to a customer before validation is a binding offer in several jurisdictions we sell into.
- **Discounts above 15% require VP sign-off before the quote is generated**, not retroactively — retroactive approval violates the delegation-of-authority policy auditors test every year.
- **Legal reviews non-standard terms before signature routing**, always — after-signature legal review is not review.

## Facts

- Quotes are generated only from the CPQ system (email-attached spreadsheets are not quotes); the approval chain is encoded there and cannot be bypassed without an audit log entry.
- The delegation-of-authority matrix lives in `finance/doa.md`; when in doubt, the next tier up approves.

## What correct looks like

Every sent quote exists in CPQ with its validation record; every >15% discount shows sign-off *timestamped before* quote generation; the quarterly audit sample returns zero out-of-chain approvals.
