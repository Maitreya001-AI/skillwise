#!/usr/bin/env python3
"""verify_clean.py -- exit check: independent sweep for residual PII in the OUTPUT artifact."""
import re, sys

PATTERNS = [
    (r"[\w.+-]+@[\w-]+\.[\w.]+", "email"),
    (r"\b\d{3}-\d{2}-\d{4}\b", "ssn-like"),
    (r"\b\+?\d[\d .-]{8,}\d\b", "phone-like"),
]

def main(path):
    hits = []
    for n, line in enumerate(open(path, encoding="utf-8"), 1):
        for pat, kind in PATTERNS:
            if re.search(pat, line):
                hits.append((n, kind))
    for n, kind in hits:
        print(f"{path}:{n}: residual {kind}")
    sys.exit(1 if hits else 0)

if __name__ == "__main__":
    main(sys.argv[1])
