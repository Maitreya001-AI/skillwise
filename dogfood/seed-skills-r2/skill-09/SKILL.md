---
name: semver-bump-decider
description: Decide the correct semantic-version bump for a release of this product, using its stricter-than-standard compatibility rules. Use when cutting a release, reviewing a version bump in a PR, or asked "is this a minor or a patch?".
---

# Semver bumps — this product's rules

Standard semver plus three product-specific tightenings (these are promises made to customers in the support contract; they are not negotiable per release):

- **CLI surface is API.** Renaming or removing a CLI flag, changing a default value, or changing exit codes is **major**, even if the library API is untouched.
- **Config file keys are API.** Removing or renaming a supported config key is **major**; adding one with a safe default is **minor**.
- **Output formats consumed by scripts** (the `--json` output schemas) are API: removing or renaming a field is **major**; adding fields is **minor**.

Everything else follows standard semver: behavior-compatible fixes are **patch**; new backwards-compatible capability is **minor**.

## Exit

Run `scripts/check_bump.py <changelog-entries-file> <proposed-bump>` on the release's changelog entries. It maps each entry's category and text against the rules above and refuses a bump that is too low. Its refusal is authoritative; overriding it means editing the rules here, in the open, not skipping the check.
