#!/usr/bin/env python3
"""check_ledger.py -- exit validator: semantic re-parse of a ledger file."""
import sys, datetime

KINDS = {"expense", "refund", "transfer"}

def main(path):
    bad = []
    for n, line in enumerate(open(path), 1):
        line = line.rstrip("\n")
        if not line:
            continue
        parts = line.split(",")
        if len(parts) != 6:
            bad.append((n, "wrong column count")); continue
        date, kind, cents, cur, memo, tags = parts
        try: datetime.date.fromisoformat(date)
        except ValueError: bad.append((n, "bad date"))
        if kind not in KINDS: bad.append((n, f"unknown kind {kind!r}"))
        if not cents.lstrip("-").isdigit(): bad.append((n, "amount not integer cents"))
        if kind == "refund" and cents.startswith("-"): bad.append((n, "refund must be positive"))
        if not (len(cur) == 3 and cur.isupper()): bad.append((n, "bad currency"))
        if len(memo) > 80: bad.append((n, "memo too long"))
    for n, why in bad:
        print(f"line {n}: {why}")
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main(sys.argv[1])
