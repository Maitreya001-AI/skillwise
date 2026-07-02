#!/usr/bin/env python3
"""check_analysis.py -- quality gate for analysis memos."""
import re, sys

REQUIRED = ["question", "data", "method", "results", "conclusions", "caveats"]

def main(path):
    text = open(path, encoding="utf-8").read()
    low = text.lower()
    problems = []
    for sec in REQUIRED:
        if not re.search(rf"^#+\s*{sec}", low, re.M):
            problems.append(f"missing section: {sec}")
    words = len(text.split())
    if words < 300: problems.append(f"too short to be a serious analysis ({words} words)")
    if low.count("significan") == 0: problems.append("no significance discussion found")
    if "http" not in low: problems.append("no data source link found")
    for p in problems: print(p)
    print("PASS: analysis is sound" if not problems else "FAIL")
    sys.exit(1 if problems else 0)

if __name__ == "__main__":
    main(sys.argv[1])
