#!/usr/bin/env python3
"""
lint_skill.py — the mechanical ENTRY for evaluate-skill.

It seals a class of *mechanical* correctness for skills (frontmatter health,
gap-routing of the description, the procedural-step smell, presence of an
exit surface (negation-aware), capability-backed-by-scripts, persona residue,
compile-candidate hints, length budget).

It is deliberately NOT a verdict. Per the skillwise docs/THEORY.md (§7), L0 is
the entry layer: it only lowers the *frequency* of mechanical defects; the
guarantee comes from the six-test semantic read in evaluate-skill/SKILL.md and,
for certification, the behavioral gate (L2). A skill can pass every check here
and still fill a gap that isn't there. Treat the output as findings, not a grade.

Usage:
    python lint_skill.py <path-to-skill-folder-or-SKILL.md>
    python lint_skill.py --check <path>   # exit non-zero if any blocking finding (for CI)
"""

import os
import re
import sys
import json

FRESH = "\033[0m"
def c(s, code): return f"\033[{code}m{s}{FRESH}" if sys.stdout.isatty() else s
def ok(s):   return c(s, "32")
def warn(s): return c(s, "33")
def bad(s):  return c(s, "31")
def dim(s):  return c(s, "2")


def resolve(path):
    """Accept a folder or a SKILL.md; return (skill_md_path, skill_dir)."""
    if os.path.isdir(path):
        md = os.path.join(path, "SKILL.md")
        return (md if os.path.exists(md) else None, path)
    if os.path.isfile(path):
        return (path, os.path.dirname(os.path.abspath(path)))
    return (None, None)


def parse_frontmatter(text):
    """Return (frontmatter_dict_or_None, body_text)."""
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.DOTALL)
    if not m:
        return None, text
    raw, body = m.group(1), m.group(2)
    fm = {}
    # minimal YAML: key: value (single-line values, which is all skills need)
    for line in raw.splitlines():
        mm = re.match(r"^([A-Za-z0-9_-]+)\s*:\s*(.*)$", line)
        if mm:
            fm[mm.group(1).strip()] = mm.group(2).strip()
    return fm, body


# Heuristic vocabularies -------------------------------------------------------

GAP_ROUTING = [
    "use when", "use this when", "trigger", "whenever", "if you need",
    "before shipping", "when the user asks", "when x is missing", "when you need",
]
OUTPUT_ONLY = ["produces", "generates", "creates", "outputs", "makes a", "builds a"]

# The skill-inertia signature is *sequencing*, not enumeration. A numbered list
# is routinely declarative (criteria, sections, gates), so a bare "1." is NOT a
# smell — only welded ordering is. Keep the strong sequencing signals.
STEP_SMELL = [
    r"\bstep\s*\d+\b",                    # "Step 1", "Step 0 —"
    r"\bfirst\b.*\bthen\b",
    r"\bnext,?\s",
    r"\bafter that\b",
    r"\bproceed to\b",
    r"\bonce (you'?ve|that'?s)\b.*\bmove on\b",
]
# Exemptions are SECTION-level, not line-level: a declarative section (done_when,
# criteria, checklists, gate/decision tables) legitimately enumerates. A broad
# line-level whitelist (test/gate/invariant/rubric...) made the check decorative —
# it exempted "Step 1: run the test".
SECTION_OK = ["done_when", "done when", "criteria", "checklist", "gate",
              "decision table", "决策表", "验收"]
# The only LINE-level exemption left: anti-procedure meta-discourse — a line that
# names the step-smell in order to forbid or discuss it (e.g. 'writing Step 1/2/3
# supplies a gap that doesn't exist', shuffle-test discussions, six-cell order
# classification vocabulary).
META_OK = ['no "procedure', "step 1/2/3", "welded", "over-fill", "overfill",
           "shuffle", "inertia", "step-march", "in any order",
           "dependency order", "epistemic order", "product order", "compiled order"]

SIX_CELL_HINT = ("Which of the six cells can this order be housed in "
                 "(dependency / irreversibility / external mandate / epistemic protocol / "
                 "product order / compiled order — THEORY §3)? If none, it is welded: overfill-order.")

EXIT_SURFACE = [
    "verify", "verification", "validate", "validator", "exit", "check that",
    "semantic check", "done_when", "plausib", "correct looks like",
    "what correct", "freshness", "self-check", "assert",
]
NEG_EN = {"no", "not", "without", "never", "none", "cannot", "can't", "lacks", "lacking", "missing"}
NEG_ZH = ["不", "无需", "没有", "缺少", "无"]

PERSONA_PAT = re.compile(
    r"\byou are an? [a-z][\w-]*|\bact as an? [a-z]|扮演|你是.{0,6}(专家|大师)",
    re.IGNORECASE)

RULE_LINE_PAT = re.compile(r"\bmust\b|\bnever\b|必须|不得", re.IGNORECASE)


def nearest_heading_ok(heading):
    """True if the governing section heading marks a declarative enumeration."""
    h = (heading or "").lower()
    return any(t in h for t in SECTION_OK)


def exit_surface_hits(body_lower):
    """Count exit-surface keywords, skipping negated mentions ('no validator',
    'without verification', '无需验证'). Negation within a 3-token window."""
    hits = 0
    for kw in EXIT_SURFACE:
        for m in re.finditer(re.escape(kw), body_lower):
            start = m.start()
            window = body_lower[max(0, start - 32):start]
            tokens = re.findall(r"[a-z']+", window)[-3:]
            if any(t in NEG_EN for t in tokens):
                continue
            if any(z in body_lower[max(0, start - 8):start] for z in NEG_ZH):
                continue
            hits += 1
    return hits


def check(md_path, skill_dir):
    findings = []  # (level, code, message)
    summary = {}

    text = open(md_path, encoding="utf-8").read()
    fm, body = parse_frontmatter(text)
    body_lower = body.lower()
    body_lines = body.splitlines()
    n_lines = len(text.splitlines())

    # 1. Frontmatter -----------------------------------------------------------
    if fm is None:
        findings.append(("bad", "frontmatter.missing",
                         "No YAML frontmatter. SKILL.md must open with --- name/description ---."))
        fm = {}
    name = fm.get("name", "")
    desc = fm.get("description", "")
    if not name:
        findings.append(("bad", "name.missing", "Frontmatter has no `name`."))
    if not desc:
        findings.append(("bad", "description.missing", "Frontmatter has no `description`."))
    summary["name"] = name or None

    # 2. Description routes by gap, not only by output -------------------------
    dl = desc.lower()
    has_gap = any(k in dl for k in GAP_ROUTING)
    has_output_only = any(k in dl for k in OUTPUT_ONLY)
    if desc:
        if has_gap:
            findings.append(("ok", "routing.gap", "Description routes by gap / trigger context."))
        elif has_output_only:
            findings.append(("warn", "routing.output_only",
                             "Description reads as 'produces Y' with no 'use when X' trigger. "
                             "Route by the gap (when to reach for it), not only by output (wrong-route)."))
        else:
            findings.append(("warn", "routing.unclear",
                             "Description has no clear trigger phrase. Add 'Use when ...' so it triggers (wrong-route)."))
        wc = len(desc.split())
        if wc < 12:
            findings.append(("warn", "description.thin",
                             f"Description is {wc} words — likely under-triggers. Be a bit pushy about when to use it."))
    summary["routes_by_gap"] = bool(has_gap)

    # 3. Procedural-step smell (overfill-order / skill inertia) ----------------
    step_hits = []
    current_heading = ""
    for i, line in enumerate(body_lines, 1):
        if re.match(r"^\s{0,3}#{1,6}\s", line):
            current_heading = line
            continue
        ll = line.lower()
        if nearest_heading_ok(current_heading):
            continue  # declarative section (done_when / criteria / checklist / gate table)
        if any(t in ll for t in META_OK):
            continue  # anti-procedure meta-discourse, not a welded march
        for pat in STEP_SMELL:
            if re.search(pat, ll):
                step_hits.append((i, line.strip()[:70]))
                break
    if step_hits:
        findings.append(("warn", "smell.procedural",
                         f"{len(step_hits)} line(s) look like welded step ordering (Step N / first..then / "
                         f"proceed to). {SIX_CELL_HINT}"))
        for ln, txt in step_hits[:5]:
            findings.append(("dim", "smell.procedural.where", f"  L{ln}: {txt}"))
    else:
        findings.append(("ok", "smell.procedural", "No obvious step-ordering smell."))
    summary["procedural_hits"] = len(step_hits)

    # 4. Exit surface exists (negation-aware) ----------------------------------
    exit_hits = exit_surface_hits(body_lower)
    has_exit = exit_hits > 0
    if has_exit:
        findings.append(("ok", "exit.present",
                         f"An exit / verification surface is mentioned ({exit_hits} non-negated mention(s))."))
    else:
        findings.append(("bad", "exit.missing",
                         "No (non-negated) exit/verification surface found. Without a semantic check "
                         "against 'what correct looks like', the skill cannot guarantee a correct result (no-exit)."))
    summary["has_exit"] = has_exit

    # 5. Capability claims backed by scripts ----------------------------------
    scripts_dir = os.path.join(skill_dir, "scripts")
    has_scripts = os.path.isdir(scripts_dir) and any(
        f for f in os.listdir(scripts_dir) if not f.startswith("."))
    claims_primitive = any(k in body_lower for k in
                           ["run scripts/", "run the script", "this script", "the linter",
                            "scripts/lint", "scripts/build", "./scripts/"])
    if claims_primitive and not has_scripts:
        findings.append(("warn", "capability.unbacked",
                         "Body refers to a script/primitive but no non-empty scripts/ dir exists. "
                         "A capability gap must ship as a runnable primitive, not prose (wrong-form)."))
    elif has_scripts:
        findings.append(("ok", "capability.backed",
                         f"scripts/ present ({len([f for f in os.listdir(scripts_dir) if not f.startswith('.')])} file(s))."))
    summary["has_scripts"] = bool(has_scripts)

    # 6. Persona residue (undischarged role content, THEORY §5) ----------------
    persona_hits = []
    for i, line in enumerate(body_lines, 1):
        ll = line.lower()
        # meta-discourse exemption: a line quoting persona phrasing to forbid it
        if "persona" in ll or "discharge" in ll or "卸载" in ll:
            continue
        m = PERSONA_PAT.search(line)
        if m:
            persona_hits.append((i, line.strip()[:70]))
    if persona_hits:
        findings.append(("warn", "persona.undischarged",
                         f"{len(persona_hits)} line(s) carry role/persona content ('you are a X' / 'act as' / "
                         f"'扮演' / '你是…专家'). A persona occupies no loop site and is unauditable; discharge it "
                         f"into explicit criteria/facts before shipping (THEORY §5 — 'expert' usually raises φ "
                         f"implicitly: write those criteria out)."))
        for ln, txt in persona_hits[:3]:
            findings.append(("dim", "persona.undischarged.where", f"  L{ln}: {txt}"))
    summary["persona_hits"] = len(persona_hits)

    # 7. Compile-candidate hint (declared-only hard invariants, THEORY §4) -----
    rule_lines = sum(1 for l in body_lines if RULE_LINE_PAT.search(l))
    summary["rule_lines"] = rule_lines
    if rule_lines >= 5 and not has_scripts and not has_exit:
        findings.append(("warn", "form.hint",
                         f"{rule_lines} hard-invariant lines (must/never/必须/不得) exist only in declarative "
                         f"form — no scripts/ primitive and no exit surface. Candidate compile site (THEORY §4): "
                         f"declared rules inform the engine; only compiled form enforces (wrong-form candidate)."))

    # 8. Length budget ---------------------------------------------------------
    if n_lines > 500:
        findings.append(("warn", "length.over",
                         f"{n_lines} lines (> 500). Add a layer of hierarchy and route detail into references/."))
    else:
        findings.append(("ok", "length.ok", f"{n_lines} lines (within the 500-line budget)."))
    summary["lines"] = n_lines

    return findings, summary


def main():
    args = [a for a in sys.argv[1:] if a != "--check"]
    check_mode = "--check" in sys.argv[1:]
    if len(args) != 1:
        print(__doc__)
        sys.exit(2)
    md_path, skill_dir = resolve(args[0])
    if not md_path:
        print(bad(f"Could not find a SKILL.md at: {args[0]}"))
        sys.exit(2)

    findings, summary = check(md_path, skill_dir)

    print()
    print(c(f"  Mechanical pass · {summary.get('name') or md_path}", "1"))
    print(dim("  (L0 entry only — not a verdict; run the six semantic tests for the read, the gate for certification)"))
    print()
    icon = {"ok": ok("  ✓"), "warn": warn("  ▲"), "bad": bad("  ✗"), "dim": "   "}
    for level, code, msg in findings:
        if level == "dim":
            print(dim(msg))
        else:
            print(f"{icon[level]} {msg}")

    n_bad = sum(1 for l, _, _ in findings if l == "bad")
    n_warn = sum(1 for l, _, _ in findings if l == "warn")
    print()
    verdict = (bad(f"{n_bad} blocking") if n_bad else ok("0 blocking")) + " · " + \
              (warn(f"{n_warn} to confirm") if n_warn else ok("0 to confirm"))
    print(f"  mechanical findings: {verdict}")
    print(dim("  → now run the semantic read (deletion / improvisation / shuffle / inertia-cost / form / exit)"))
    print()
    print(dim("  machine summary: " + json.dumps(summary, ensure_ascii=False)))

    if check_mode and n_bad:
        sys.exit(1)


if __name__ == "__main__":
    main()
