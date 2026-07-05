#!/usr/bin/env python3
"""deletion_probe.py — run the deletion test as a real micro-probe, never a simulation.

For style/convention/best-practice skills the load-bearing question — "would a capable
unaided engine already produce these rules?" — is L2-native (THEORY §7): a judge simulating
it is an L1 prediction with measured calibration failures (dogfood rounds 2-4). This
primitive replaces the simulation with an observation: it reads ONLY the skill's
frontmatter name+description (the body never reaches the probe context), asks an unaided
engine for the bar it would enforce for that domain, and prints both texts side by side.
The judge then classifies each rule against a concrete artifact instead of a counterfactual.

Usage: python3 deletion_probe.py <skill-dir> [--model sonnet] [--samples 1]
Exit 3 when the engine CLI is unavailable/fails: the caller must then emit the deletion
finding with prediction:true (static fallback) — never fake the probe's output.
"""
import re, subprocess, sys, pathlib

GEN = ("You maintain engineering conventions for a team. For the artifact domain described "
       "below, write the concrete bar you would enforce — the 6-10 specific rules a careful "
       "team applies when reviewing this kind of artifact. State each rule as an enforceable "
       "constraint, one bullet per rule. Do not explain; output only the rules.\n\nDomain: {n}: {d}")

def main():
    args = sys.argv[1:]
    model = args[args.index("--model") + 1] if "--model" in args else "sonnet"
    samples = int(args[args.index("--samples") + 1]) if "--samples" in args else 1
    md = (pathlib.Path(args[0]) / "SKILL.md").read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", md, re.DOTALL)
    fm = dict(re.findall(r"^([a-z-]+):\s*(.*)$", m.group(1), re.M))
    body = m.group(2)

    rules, heading = [], ""
    for line in body.splitlines():
        if re.match(r"^#{1,6}\s", line):
            heading = line.lower()
        elif not any(k in heading for k in ("exit", "done")) and line.startswith("- "):
            rules.append(line[2:].strip())

    bars = []
    for _ in range(samples):
        try:
            r = subprocess.run(["claude", "-p", "--model", model],
                               input=GEN.format(n=fm["name"], d=fm["description"]),
                               capture_output=True, text=True, timeout=240)
        except (FileNotFoundError, subprocess.TimeoutExpired) as e:
            print(f"PROBE-UNAVAILABLE: {e}\nEmit the deletion finding with prediction:true; do not fake this probe.")
            sys.exit(3)
        if r.returncode != 0 or not r.stdout.strip():
            print(f"PROBE-UNAVAILABLE: engine call failed\nEmit the deletion finding with prediction:true; do not fake this probe.")
            sys.exit(3)
        bars.append(r.stdout.strip())

    print("== UNAIDED BAR (generated from name+description only; the skill body never reached this context) ==")
    print("\n".join(bars))
    print("\n== THE SKILL'S RULES (classify each against the unaided bar above) ==")
    print("\n".join(f"- {r}" for r in rules))
    print("\n== CLASSIFICATION SCAFFOLD ==\n"
          "Per rule: 'covered' (substance present above, paraphrase allowed) or 'survives'.\n"
          "A survivor is gap content only if it names a specific enforced choice (threshold,\n"
          "grammar/format, named selection stated as must/never/fails-review), not a vague\n"
          "preference. Zero substantive survivors -> the deletion test concludes nogap.")

if __name__ == "__main__":
    main()
