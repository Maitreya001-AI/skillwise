---
name: release-branch-freeze
description: Operate the release-freeze process for regulated releases. Use when a release branch is cut, when merging anything during a freeze window, or when asked to "sneak one more fix in".
---

# Release freeze

Freeze rules are external: our payment-industry certification requires that what was audited is what ships. The order below is mandated by the auditor's process, not by engineering preference.

- **Certification precedes the freeze lift.** No merge to a frozen release branch after the audit build is taken — a single post-audit commit voids the certification and restarts the audit clock (about two weeks).
- **Exception path exists and is narrow**: a security fix may enter a frozen branch only with a re-audit waiver signed by compliance *before* the merge, filed in `releases/waivers/`.
- **The freeze window is declared, not discovered**: the branch protection rule and the calendar entry go up together, before the audit build is requested.

## Facts

- Release branches: `release/<version>`; audit builds are tagged `<version>-audit-<n>`.
- Compliance contact and waiver template live in `releases/OWNERS.md`.

## What correct looks like

During a freeze: zero merges without a filed waiver (check the branch's merge log against `releases/waivers/`); the shipped tag's tree hash equals the audited tag's tree hash. After: the freeze window entry has an end date and the protection rule is lifted the same day.
