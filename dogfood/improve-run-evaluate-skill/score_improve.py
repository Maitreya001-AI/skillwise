#!/usr/bin/env python3
"""score_improve.py — mechanical improvement-gate scoring (shared/effect-gate.md).

Conditions on the working slice:
  ns-*.json  no-skill floor (>=2 runs; per-seed medians)
  a-*.json   previous-accepted reference (exactly 3 runs; band = 2 x SD of aggregates)
  b-*.json   edited version under test (>=2 runs)

Emits the improvement-gate reading + the ratchet decision (first match wins).
Usage: python score_improve.py <labels.json> <runs-dir> <working-seeds...comma-list>
"""

import json
import statistics
import sys
from pathlib import Path


def load(path):
    return {r["skill"]: r for r in json.loads(Path(path).read_text())}


def correct(row, lab):
    if row is None:
        return 0
    if lab["truth"] == "good":
        return 1 if row["verdict"] == "good" else 0
    return 1 if (row["verdict"] == "broken" and row.get("primary_defect") == lab["defect"]) else 0


def main(labels_path, runs_dir, seeds_csv):
    labels = json.loads(Path(labels_path).read_text())
    seeds = seeds_csv.split(",")
    runs_dir = Path(runs_dir)
    ns = [load(p) for p in sorted(runs_dir.glob("ns-*.json"))]
    a = [load(p) for p in sorted(runs_dir.glob("a-*.json"))]
    b = [load(p) for p in sorted(runs_dir.glob("b-*.json"))]
    assert len(a) == 3, "reference (previous-accepted) needs exactly 3 runs"
    assert len(b) >= 2 and len(ns) >= 2

    def med(runs, s):
        return statistics.median(correct(r.get(s), labels[s]) for r in runs)

    def agg_of_run(run):
        return sum(correct(run.get(s), labels[s]) for s in seeds) / len(seeds)

    a_aggs = [agg_of_run(r) for r in a]
    noise_band = 2 * statistics.stdev(a_aggs)

    med_ns = {s: med(ns, s) for s in seeds}
    med_a = {s: med(a, s) for s in seeds}
    med_b = {s: med(b, s) for s in seeds}

    n = len(seeds)
    agg_a = sum(med_a.values()) / n
    agg_b = sum(med_b.values()) / n
    delta_step = agg_b - agg_a
    delta_exist_b = agg_b - sum(med_ns.values()) / n

    regressions = [s for s in seeds if med_b[s] < med_a[s]]
    floor_breaches = [s for s in seeds if med_b[s] < med_ns[s]]

    power = {"n_tasks": n, "resolution": round(1 / n, 4), "adequate": n >= 6}

    # ratchet decision table, first match wins (safety N/A in this harness; new-blocking-lint
    # checked by the orchestrator before this script runs)
    if floor_breaches or regressions:
        decision = "REVERT"
        why = f"fatal: regressions vs previous {regressions}, floor breaches {floor_breaches}"
    elif delta_step > noise_band:
        decision = "KEEP"
        why = f"delta_step {delta_step:.4f} > noise_band {noise_band:.4f}, no reproduced regression, floor intact"
    else:
        decision = "REVERT (within noise, no structural repair)"
        why = f"delta_step {delta_step:.4f} <= noise_band {noise_band:.4f}"

    out = {
        "a_run_aggregates": [round(x, 4) for x in a_aggs],
        "prev_accepted_pass_rate": round(agg_a, 4),
        "with_edited_pass_rate": round(agg_b, 4),
        "no_skill_pass_rate": round(sum(med_ns.values()) / n, 4),
        "delta_step": round(delta_step, 4),
        "delta_exist_edited": round(delta_exist_b, 4),
        "noise_band": round(noise_band, 4),
        "regressions_vs_previous": regressions,
        "floor_breaches": floor_breaches,
        "power": power,
        "decision": decision,
        "why": why,
        "per_task": [
            {"task": s, "truth": labels[s]["truth"], "defect": labels[s]["defect"],
             "no_skill": med_ns[s], "prev": med_a[s], "edited": med_b[s]}
            for s in seeds
        ],
    }
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
