#!/usr/bin/env python3
"""scrub.py -- field-aware PII scrubber (profiles: logs|fixtures|export)."""
import argparse, json, re, sys, hashlib

PROFILES = {"logs", "fixtures", "export"}
PII_KEYS = {"email", "name", "full_name", "gov_id", "ssn", "device_id", "phone", "note", "notes", "address"}

def token(v):
    return "tok_" + hashlib.sha256(str(v).encode()).hexdigest()[:12]

def scrub(obj):
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if k.lower() in {"note", "notes", "address"}:
                continue  # free text: dropped, never masked
            out[k] = token(v) if k.lower() in PII_KEYS else scrub(v)
        return out
    if isinstance(obj, list):
        return [scrub(x) for x in obj]
    return obj

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--in", dest="inp", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--profile", required=True, choices=sorted(PROFILES))
    a = p.parse_args()
    try:
        data = json.load(open(a.inp))
    except Exception:
        sys.exit("unknown file shape: refusing to pass through unscrubbed")
    json.dump(scrub(data), open(a.out, "w"), indent=2)
    print(f"scrubbed -> {a.out}")

if __name__ == "__main__":
    main()
