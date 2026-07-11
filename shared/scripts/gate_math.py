#!/usr/bin/env python3
"""gate_math.py — the effect gate's arithmetic, compiled once (shared/effect-gate.md).

Extracted and generalized from the dogfood scorers (dogfood/evaluate-delta-run/score.py,
dogfood/improve-run-evaluate-skill/score_improve.py); those originals are historical
evidence and stay untouched. This module is pure arithmetic over per-task 0/1 scores —
no I/O, no engine, no judge. gate_runner.py feeds it and the acceptance tests pin it
to the dogfood ledger's historical numbers (arithmetic equivalence, acceptance A1).

Charter mapping (docs/THEORY.md §8, via shared/effect-gate.md):
  §8-1  noise_band = 2 x sample SD of the 3 reference-condition run aggregates
  §8-2  per-task score = median across re-runs; regression_count on medians (strict <)
  §8-3  power block before any verdict; n < 6 demotes pass to indicative
  §8-5  inertia-cost fatal: cost_ratio > 1.5 with delta inside the band
  §8-6  existence and improvement branches never share a reference frame

A "runs" argument is a list of runs; each run maps task id -> 0/1 score.
Reference condition: exactly 3 runs is the charter's fixed configuration; >=3 is
accepted (the SD estimator does not drift with run count) but flagged in the result.
"""

import statistics

N_ADEQUATE = 6            # the gate's shipped power default (§8-3)
COST_RATIO_FATAL = 1.5    # §8-5 inertia-cost threshold
ROUND = 4


def _r(x):
    return round(x, ROUND)


def run_aggregate(run, tasks):
    """Mean 0/1 score of one run over the task set (a missing task scores 0)."""
    return sum(run.get(t, 0) for t in tasks) / len(tasks)


def per_task_medians(runs, tasks):
    """§8-2: a task's score under a condition is the median across its re-runs."""
    return {t: statistics.median([r.get(t, 0) for r in runs]) for t in tasks}


def noise_band(ref_runs, tasks):
    """§8-1: 2 x sample SD of the reference-condition run aggregates (3 runs canonical)."""
    if len(ref_runs) < 3:
        raise ValueError("reference condition needs >= 3 runs (charter fixes it at 3)")
    return 2 * statistics.stdev(run_aggregate(r, tasks) for r in ref_runs)


def power_block(n_tasks):
    """§8-3: emit power before any verdict; adequate = n >= 6."""
    return {"n_tasks": n_tasks, "resolution": _r(1 / n_tasks), "adequate": n_tasks >= N_ADEQUATE}


def existence_gate(ref_runs, test_runs, tasks, *, cost_ratio=None,
                   safety_regression=False, structural_blocking=False):
    """Existence branch: delta_exist = with_skill − no_skill (reference = no-skill).

    Returns the effect report plus gate_pass/certainty, resolving in the gate file's
    published order (first match wins); fatals land before unfit_test_set routing.
    """
    if len(test_runs) < 2:
        raise ValueError("condition under test needs >= 2 runs")
    tasks = sorted(tasks)
    band = noise_band(ref_runs, tasks)
    med_ref = per_task_medians(ref_runs, tasks)
    med_test = per_task_medians(test_runs, tasks)
    n = len(tasks)
    no_agg = sum(med_ref.values()) / n
    with_agg = sum(med_test.values()) / n
    delta = with_agg - no_agg
    regressions = [t for t in tasks if med_test[t] < med_ref[t]]
    ceiling = all(med_ref[t] == 1 for t in tasks)
    power = power_block(n)
    in_band = delta <= band
    cost_fatal = cost_ratio is not None and cost_ratio > COST_RATIO_FATAL and in_band

    # Resolution order (effect-gate.md "Resolution order", first match wins).
    # (2) required-but-unrun -> static_only is the runner's case, not arithmetic's:
    # this function is only called once both arms have run.
    if structural_blocking:
        gate_pass = "fail"
        why = "blocking structural finding"
    elif safety_regression:
        gate_pass = "fail"
        why = "safety regression"
    elif regressions:
        gate_pass = "fail"
        why = f"reproduced negative transfer on per-task medians: {regressions}"
    elif cost_fatal:
        gate_pass = "fail"
        why = (f"inertia-cost fatal (overfill-cost): cost_ratio {cost_ratio:.4f} > "
               f"{COST_RATIO_FATAL} with delta_exist inside the band")
    elif ceiling:
        gate_pass = "unfit_test_set"
        why = "no_skill at ceiling on every task — harden the set (or conclude nogap if it cannot be hardened)"
    elif in_band:
        gate_pass = "fail"
        why = f"delta_exist {delta:.4f} <= noise_band_exist {band:.4f}"
    else:
        gate_pass = "pass"
        why = f"delta_exist {delta:.4f} > noise_band_exist {band:.4f}, no reproduced regression"

    return {
        "no_skill_run_aggregates": [_r(run_aggregate(r, tasks)) for r in ref_runs],
        "no_skill_pass_rate": _r(no_agg),
        "with_skill_pass_rate": _r(with_agg),
        "delta_exist": _r(delta),
        "noise_band_exist": _r(band),
        "regression_count": len(regressions),
        "regressions": regressions,
        "safety_regression": safety_regression,
        "cost_ratio": None if cost_ratio is None else _r(cost_ratio),
        "power": power,
        "gate_pass": gate_pass,
        "certainty": "certifying" if power["adequate"] else "indicative",
        "why": why,
        "reference_runs_noncanonical": len(ref_runs) != 3,
        "per_task": [{"task": t, "no_skill": med_ref[t], "with_skill": med_test[t]}
                     for t in tasks],
    }


def improvement_gate(prev_runs, edited_runs, no_skill_runs, tasks, *,
                     safety_regression=False, removes_blocking_structural=False):
    """Improvement branch: delta_step = with_edited − with_prev_accepted (§8-6).

    Reference = the previous accepted version (band from its runs); the no-skill
    baseline is only the permanent floor. Decision table is the ratchet's, first
    match wins, including the lateral-keep exception for structural repair.
    """
    if len(edited_runs) < 2 or len(no_skill_runs) < 2:
        raise ValueError("edited and no-skill conditions need >= 2 runs each")
    tasks = sorted(tasks)
    band = noise_band(prev_runs, tasks)
    med_prev = per_task_medians(prev_runs, tasks)
    med_edit = per_task_medians(edited_runs, tasks)
    med_ns = per_task_medians(no_skill_runs, tasks)
    n = len(tasks)
    agg_prev = sum(med_prev.values()) / n
    agg_edit = sum(med_edit.values()) / n
    agg_ns = sum(med_ns.values()) / n
    delta_step = agg_edit - agg_prev
    regressions = [t for t in tasks if med_edit[t] < med_prev[t]]
    floor_breaches_edited = [t for t in tasks if med_edit[t] < med_ns[t]]
    floor_breaches_entry = [t for t in tasks if med_prev[t] < med_ns[t]]

    if safety_regression:
        decision, why = "REVERT", "fatal: safety regression"
    elif regressions or floor_breaches_edited:
        decision = "REVERT"
        why = (f"fatal: regressions vs previous {regressions}, "
               f"floor breaches {floor_breaches_edited}")
    elif delta_step > band:
        decision = "KEEP"
        why = (f"delta_step {delta_step:.4f} > noise_band {band:.4f}, "
               "no reproduced regression, floor intact")
    elif removes_blocking_structural:
        decision = "KEEP (lateral)"
        why = ("within noise but removes a non-waived blocking structural finding; "
               "floor and no-regression conditions hold")
    else:
        decision = "REVERT"
        why = f"delta_step {delta_step:.4f} <= noise_band {band:.4f} (within noise, no structural repair)"

    return {
        "prev_run_aggregates": [_r(run_aggregate(r, tasks)) for r in prev_runs],
        "prev_accepted_pass_rate": _r(agg_prev),
        "with_edited_pass_rate": _r(agg_edit),
        "no_skill_pass_rate": _r(agg_ns),
        "delta_step": _r(delta_step),
        "delta_exist_edited": _r(agg_edit - agg_ns),
        "noise_band": _r(band),
        "regressions_vs_previous": regressions,
        "floor_breaches_edited": floor_breaches_edited,
        "floor_breaches_entry": floor_breaches_entry,
        "safety_regression": safety_regression,
        "power": power_block(n),
        "decision": decision,
        "why": why,
        "reference_runs_noncanonical": len(prev_runs) != 3,
        "per_task": [{"task": t, "no_skill": med_ns[t], "prev": med_prev[t],
                      "edited": med_edit[t]} for t in tasks],
    }


def existence_headroom(ref_runs, tasks):
    """Existence-question fitness: no_skill must not be at ceiling (effect-gate 'Headroom')."""
    med = per_task_medians(ref_runs, sorted(tasks))
    return {"no_skill_at_ceiling": all(v == 1 for v in med.values())}


def improvement_headroom(current_runs, no_skill_runs, tasks):
    """Improvement-loop fitness: some task below max, or negative transfer to repair."""
    tasks = sorted(tasks)
    med_cur = per_task_medians(current_runs, tasks)
    med_ns = per_task_medians(no_skill_runs, tasks)
    below_max = any(med_cur[t] < 1 for t in tasks)
    negative = any(med_cur[t] < med_ns[t] for t in tasks)
    return {"headroom": below_max or negative,
            "variance": len(set(med_cur.values())) > 1,
            "fit": below_max or negative}
