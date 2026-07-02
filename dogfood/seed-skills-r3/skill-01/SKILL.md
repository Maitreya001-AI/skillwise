---
name: terraform-state-surgery
description: Safely perform manual edits to Terraform state (moves, imports, rm) in shared workspaces. Use when state is out of sync with reality, when refactoring module paths, or when anyone proposes "just terraform state rm it".
---

# Terraform state surgery

State surgery is the rare operation where a typo destroys the mapping between code and real infrastructure — and the destroy is silent until the next plan wants to delete production. The protocol is heavy because the operation is irreversible; the cost does not scale down for "small" edits.

## Non-waivable requirements

- **Pull and archive first**: `terraform state pull > state-$(date).json`, checksummed and stored off-workspace. An archive nobody has restored from is untested — restore it once into a scratch workspace.
- **Dry-run the surgery**: every `state mv`/`rm`/`import` is first written out as a script and reviewed against `terraform state list` output — never typed ad hoc into a shared workspace.
- **Second context signs the script**: whoever wrote the surgery script does not approve it; a fresh context reads the script against the archive cold.
- **Post-verify**: `terraform plan` after surgery must show **zero unexpected changes** — a plan wanting to create or destroy anything you didn't intend means restore the archive, do not "fix forward".

## Never

- Never run surgery during an active apply or within a CI window.
- Never edit the state JSON by hand when a state subcommand exists for it.
