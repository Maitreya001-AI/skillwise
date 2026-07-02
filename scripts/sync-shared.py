#!/usr/bin/env python3
"""sync-shared.py — materialize shared/effect-gate.md into each consumer skill.

Distribution reality (docs/THEORY.md §4 — the price of compilation includes
distribution constraints, which are real and must be priced): two of the three
install paths copy only `skills/<name>/`, so a `../../shared/` reference would
dangle after install. The single *editing* source stays `shared/effect-gate.md`;
this script copies it, byte-for-byte plus a do-not-edit banner, into each
consumer's `references/effect-gate.md` so every skill folder is self-contained.

CI runs this script and fails the build if any copy has drifted from the source
(`git diff --exit-code` after sync). Edit only shared/effect-gate.md.
"""

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SOURCE = ROOT / "shared" / "effect-gate.md"
CONSUMERS = ["evaluate-skill", "improve-skill", "seek-skill"]

BANNER = (
    "<!-- AUTO-GENERATED COPY - DO NOT EDIT.\n"
    "     Source of truth: shared/effect-gate.md (edit there, then run scripts/sync-shared.py).\n"
    "     Materialized into references/ so a standalone skill install carries its own gate. -->\n"
    "\n"
)


def main() -> int:
    if not SOURCE.exists():
        print(f"error: source not found: {SOURCE}", file=sys.stderr)
        return 2
    payload = BANNER + SOURCE.read_text(encoding="utf-8")
    changed = []
    for name in CONSUMERS:
        dest = ROOT / "skills" / name / "references" / "effect-gate.md"
        dest.parent.mkdir(parents=True, exist_ok=True)
        if not dest.exists() or dest.read_text(encoding="utf-8") != payload:
            dest.write_text(payload, encoding="utf-8")
            changed.append(str(dest.relative_to(ROOT)))
    print("synced: " + (", ".join(changed) if changed else "all copies already current"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
