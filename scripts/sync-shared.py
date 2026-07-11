#!/usr/bin/env python3
"""sync-shared.py — materialize shared/ sources into each consumer skill.

Distribution reality (docs/THEORY.md §4 — the price of compilation includes
distribution constraints, which are real and must be priced): two of the three
install paths copy only `skills/<name>/`, so a `../../shared/` reference would
dangle after install. The single *editing* source stays under `shared/`;
this script copies each source, byte-for-byte plus a do-not-edit banner, into
each consumer skill so every skill folder is self-contained.

Synced sources:
  shared/effect-gate.md        -> skills/<consumer>/references/effect-gate.md
  shared/scripts/gate_runner.py-> skills/<consumer>/scripts/gate_runner.py
  shared/scripts/gate_math.py  -> skills/<consumer>/scripts/gate_math.py

CI runs this script and fails the build if any copy has drifted from its source
(`git status --porcelain` after sync). Edit only the shared/ sources.
"""

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONSUMERS = ["evaluate-skill", "improve-skill", "seek-skill"]

MD_BANNER = (
    "<!-- AUTO-GENERATED COPY - DO NOT EDIT.\n"
    "     Source of truth: shared/{name} (edit there, then run scripts/sync-shared.py).\n"
    "     Materialized into references/ so a standalone skill install carries its own gate. -->\n"
    "\n"
)
PY_BANNER = (
    "# AUTO-GENERATED COPY - DO NOT EDIT.\n"
    "# Source of truth: shared/scripts/{name} (edit there, then run scripts/sync-shared.py).\n"
    "# Materialized into scripts/ so a standalone skill install carries its own gate runner.\n"
)

# (source relative to shared/, destination subdir inside each consumer skill)
SOURCES = [
    ("effect-gate.md", "references"),
    ("scripts/gate_runner.py", "scripts"),
    ("scripts/gate_math.py", "scripts"),
]


def materialize(text, name):
    if name.endswith(".py"):
        banner = PY_BANNER.format(name=name)
        if text.startswith("#!"):
            shebang, rest = text.split("\n", 1)
            return f"{shebang}\n{banner}{rest}"
        return banner + text
    return MD_BANNER.format(name=name) + text


def main() -> int:
    changed = []
    for rel, dest_sub in SOURCES:
        source = ROOT / "shared" / rel
        if not source.exists():
            print(f"error: source not found: {source}", file=sys.stderr)
            return 2
        payload = materialize(source.read_text(encoding="utf-8"), source.name)
        for name in CONSUMERS:
            dest = ROOT / "skills" / name / dest_sub / source.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            if not dest.exists() or dest.read_text(encoding="utf-8") != payload:
                dest.write_text(payload, encoding="utf-8")
                changed.append(str(dest.relative_to(ROOT)))
    print("synced: " + (", ".join(changed) if changed else "all copies already current"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
