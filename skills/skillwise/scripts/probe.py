#!/usr/bin/env python3
"""probe.py — compiled state probe for the /skillwise explicit entry.

Why compiled (THEORY §4): the verdict-artifact recognition convention carries
real improvisation risk — different runs would glob for different filenames.
So the convention has exactly one implementation: the ONLY verdict artifact
this toolbox recognizes is <skill-dir>/wise-eval.json (evaluate-skill's pinned
landing location; see its "Converge to one gate" section). No fuzzy globs.

Input : one argument (the user's raw /skillwise arguments; may be empty).
Output: a single JSON line to stdout:
        {"state": "<token>", "evidence": ["..."], "skill_dir": "<dir-or-null>"}
States: exists_with_verdict | exists_no_verdict | path_not_found | no_path
Read-only; exit code is always 0 (state lives in the JSON, not the exit code).
"""

import json
import os
import sys

VERDICT = "wise-eval.json"


def emit(state, evidence, skill_dir=None):
    print(json.dumps({"state": state, "evidence": evidence, "skill_dir": skill_dir},
                     ensure_ascii=False))
    sys.exit(0)


def path_tokens(text):
    """Tokens that look like filesystem paths (contain '/', start with . or ~,
    or actually exist on disk)."""
    toks = []
    for t in text.split():
        t = t.strip("'\"`,;:()[]{}<>")
        if not t:
            continue
        if "/" in t or t.startswith((".", "~")) or os.path.exists(t):
            toks.append(t)
    return toks


def resolve_skill_dir(tok):
    """A skill dir is a directory containing SKILL.md; accept a direct path to
    SKILL.md too. Returns the dir, or None when the token doesn't lead to one."""
    p = os.path.expanduser(tok)
    if os.path.isfile(p) and os.path.basename(p) == "SKILL.md":
        return os.path.dirname(os.path.abspath(p)) or "."
    if os.path.isdir(p) and os.path.isfile(os.path.join(p, "SKILL.md")):
        return p
    return None


def main():
    arg = " ".join(sys.argv[1:]).strip()
    if not arg:
        emit("no_path", ["no arguments given"])

    toks = path_tokens(arg)
    if not toks:
        emit("no_path", [f"no path-like content in the input ({len(arg)} chars of prose)"])

    evidence = []
    for tok in toks:
        d = resolve_skill_dir(tok)
        if d is None:
            p = os.path.expanduser(tok)
            if os.path.isdir(p):
                evidence.append(f"'{tok}' resolves to a directory but it contains no SKILL.md")
            elif os.path.exists(p):
                evidence.append(f"'{tok}' exists but is neither a SKILL.md nor a skill directory")
            else:
                evidence.append(f"'{tok}' does not resolve")
            continue
        evidence.append(f"found {os.path.join(d, 'SKILL.md')}")
        vpath = os.path.join(d, VERDICT)
        if os.path.isfile(vpath):
            ev = f"found {VERDICT}"
            try:
                gate = json.load(open(vpath, encoding="utf-8")).get("gate_pass")
                if gate is not None:
                    ev += f" (gate_pass={gate})"
            except (json.JSONDecodeError, OSError):
                ev += " (unreadable JSON)"
            evidence.append(ev)
            emit("exists_with_verdict", evidence, d)
        emit("exists_no_verdict", evidence + [f"no {VERDICT} in {d}"], d)

    emit("path_not_found", evidence)


if __name__ == "__main__":
    main()
