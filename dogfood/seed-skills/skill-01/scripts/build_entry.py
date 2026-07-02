#!/usr/bin/env python3
"""build_entry.py -- named-field constructor for ledger rows (misuse-resistant)."""
import argparse, datetime, sys

KINDS = {"expense", "refund", "transfer"}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--date", required=True)
    p.add_argument("--kind", required=True, choices=sorted(KINDS))
    p.add_argument("--amount-cents", required=True)
    p.add_argument("--currency", required=True)
    p.add_argument("--memo", required=True)
    p.add_argument("--tags", default="")
    a = p.parse_args()
    datetime.date.fromisoformat(a.date)
    if not a.amount_cents.lstrip("-").isdigit():
        sys.exit("amount-cents must be an integer number of cents")
    if not (len(a.currency) == 3 and a.currency.isalpha() and a.currency.isupper()):
        sys.exit("currency must be uppercase ISO-4217")
    if "," in a.memo or len(a.memo) > 80:
        sys.exit("memo: no commas, max 80 chars")
    tags = ";".join(t.strip().lower() for t in a.tags.split(";") if t.strip())
    print(",".join([a.date, a.kind, a.amount_cents, a.currency, a.memo, tags]))

if __name__ == "__main__":
    main()
