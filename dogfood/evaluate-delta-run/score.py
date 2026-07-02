#!/usr/bin/env python3
"""score.py — mechanical scoring for the evaluate-delta experiment.

Implements the shared gate's arithmetic (shared/effect-gate.md):
  - per-seed score under a condition = median across that condition's runs (§8-2)
  - noise_band_exist = 2 x sample stdev of the 3 no-skill run aggregates (§8-1)
  - delta_exist = with_aggregate - no_aggregate
  - regression_count over per-seed medians (strict <)
  - power block (§8-3), per-class side question (text-checkable vs L2-native)

No LLM judgment happens here: a verdict is correct iff (a) good/broken matches
the implantation label and (b) for broken seeds the primary_defect token matches
exactly. Usage:
  python score.py <labels.json> <runs-dir>   # runs-dir holds armB-*.json / armA-*.json
"""

import json
import statistics
import sys
from pathlib import Path

TEXT_CHECKABLE = {"overfill-order", "wrong-form", "no-exit"}
L2_NATIVE = {"nogap", "underfill", "overfill-cost"}
N_ADEQUATE = 6  # the gate's shipped default


def load_run(path):
    data = json.loads(Path(path).read_text())
    return {row["skill"]: row for row in data}


def run_accuracy(run, labels):
    return sum(correct(run.get(s), lab) for s, lab in labels.items()) / len(labels)


def correct(row, lab):
    if row is None:
        return 0
    if lab["truth"] == "good":
        return 1 if row["verdict"] == "good" else 0
    return 1 if (row["verdict"] == "broken" and row.get("primary_defect") == lab["defect"]) else 0


def per_seed_median(runs, labels, seed):
    vals = [correct(r.get(seed), labels[seed]) for r in runs]
    return statistics.median(vals)


def main(labels_path, runs_dir):
    labels = json.loads(Path(labels_path).read_text())
    runs_dir = Path(runs_dir)
    b_runs = [load_run(p) for p in sorted(runs_dir.glob("armB-*.json"))]
    a_runs = [load_run(p) for p in sorted(runs_dir.glob("armA-*.json"))]
    assert len(b_runs) == 3, "reference condition must have exactly 3 runs (§8-1)"
    assert len(a_runs) >= 2, "condition under test needs >=2 runs"

    seeds = sorted(labels)
    n = len(seeds)

    b_run_accs = [run_accuracy(r, labels) for r in b_runs]
    noise_band_exist = 2 * statistics.stdev(b_run_accs)

    med_b = {s: per_seed_median(b_runs, labels, s) for s in seeds}
    med_a = {s: per_seed_median(a_runs, labels, s) for s in seeds}
    no_agg = sum(med_b.values()) / n
    with_agg = sum(med_a.values()) / n
    delta_exist = with_agg - no_agg
    regressions = [s for s in seeds if med_a[s] < med_b[s]]

    power = {"n_tasks": n, "resolution": round(1 / n, 4), "adequate": n >= N_ADEQUATE}

    def class_acc(med, cls):
        ss = [s for s in seeds if labels[s]["defect"] in cls]
        return (sum(med[s] for s in ss) / len(ss), len(ss))

    good_seeds = [s for s in seeds if labels[s]["truth"] == "good"]
    per_class = {
        "text_checkable": {"no_skill": class_acc(med_b, TEXT_CHECKABLE)[0],
                           "with_skill": class_acc(med_a, TEXT_CHECKABLE)[0],
                           "n": class_acc(med_b, TEXT_CHECKABLE)[1]},
        "l2_native": {"no_skill": class_acc(med_b, L2_NATIVE)[0],
                      "with_skill": class_acc(med_a, L2_NATIVE)[0],
                      "n": class_acc(med_b, L2_NATIVE)[1]},
        "good_preservation": {"no_skill": sum(med_b[s] for s in good_seeds) / len(good_seeds),
                              "with_skill": sum(med_a[s] for s in good_seeds) / len(good_seeds),
                              "n": len(good_seeds)},
    }

    ceiling = all(med_b[s] == 1 for s in seeds)
    # resolution order (existence gate; structural/smoke/static_only/safety N/A here,
    # cost handled outside — token counts are collected by the orchestrator)
    if len(regressions) > 0:
        gate_pass = "fail (negative transfer)"
    elif ceiling:
        gate_pass = "unfit_test_set (no_skill at ceiling)"
    elif delta_exist <= noise_band_exist:
        gate_pass = "fail (delta_exist within the noise band)"
    else:
        gate_pass = "pass"
    certainty = "certifying" if power["adequate"] else "indicative"

    report = {
        "no_skill_run_accuracies": [round(x, 4) for x in b_run_accs],
        "no_skill_pass_rate": round(no_agg, 4),
        "with_skill_pass_rate": round(with_agg, 4),
        "delta_exist": round(delta_exist, 4),
        "noise_band_exist": round(noise_band_exist, 4),
        "regression_count": len(regressions),
        "regressions": regressions,
        "safety_regression": False,
        "power": power,
        "gate_pass": gate_pass,
        "certainty": certainty,
        "per_class": per_class,
        "per_task": [
            {"task": s, "truth": labels[s]["truth"], "defect": labels[s]["defect"],
             "no_skill": med_b[s], "with_skill": med_a[s]}
            for s in seeds
        ],
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
