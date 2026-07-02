#!/usr/bin/env python3
"""check_bump.py -- semantic verifier: proposed bump must cover every entry's minimum."""
import re, sys

ORDER = {"patch": 0, "minor": 1, "major": 2}
MAJOR = [r"remov\w+ (the )?(--|flag|config key|field)", r"renam\w+ (the )?(--|flag|config key|field)",
         r"chang\w+ (the )?default", r"chang\w+ exit code", r"breaking"]
MINOR = [r"\badd\w*\b.*(flag|config key|field|command|option)", r"\bnew\b.*(command|capability|endpoint)"]

def minimum(entry):
    e = entry.lower()
    if any(re.search(p, e) for p in MAJOR): return "major"
    if any(re.search(p, e) for p in MINOR): return "minor"
    return "patch"

def main(path, proposed):
    if proposed not in ORDER: sys.exit(f"unknown bump {proposed!r}")
    entries = [l.strip("-* \n") for l in open(path) if l.strip().startswith(("-", "*"))]
    if not entries: sys.exit("no changelog entries found; refusing to certify a bump over nothing")
    worst = max((minimum(e) for e in entries), key=lambda b: ORDER[b])
    if ORDER[proposed] < ORDER[worst]:
        offenders = [e for e in entries if minimum(e) == worst]
        print(f"REFUSED: entries require at least {worst!r}, proposed {proposed!r}")
        for o in offenders[:5]: print(f"  - {o}")
        sys.exit(1)
    print(f"ok: {proposed} covers all entries (minimum required: {worst})")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
