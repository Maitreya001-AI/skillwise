"""Acceptance A1 — arithmetic equivalence against the dogfood ledger (zero API cost).

gate_math is an extraction of the dogfood scorers; these tests pin it to the
historical numbers those scorers produced, field by field:

  existence  : labels-behavioral.json + round2-runs/{ns-1..3, a-1..3}
               must reproduce existence-r5.json and wise-eval.json
  improvement: labels-run.json + round2-runs/{a-1..3, b-1..3, ns-1..2}
               must reproduce round2-runs/round2-gate.json

The verdict→score transform (verdict/primary_defect matching against a label key)
is the seed-skill experiment's task format, not gate arithmetic — it lives here as
fixture glue, exactly the generalization boundary gate_runner draws with tasks.yaml.
"""

import json
from pathlib import Path

import gate_math

ROOT = Path(__file__).resolve().parent.parent
DOG = ROOT / "dogfood" / "improve-run-evaluate-skill"


def load_labels(name):
    return json.loads((DOG / name).read_text())


def load_run(path, labels):
    """One dogfood judge run -> {task: 0/1} under a label key (score.py's rule)."""
    rows = {r["skill"]: r for r in json.loads(path.read_text())}
    scores = {}
    for task, lab in labels.items():
        row = rows.get(task)
        if row is None:
            scores[task] = 0
        elif lab["truth"] == "good":
            scores[task] = 1 if row["verdict"] == "good" else 0
        else:
            scores[task] = 1 if (row["verdict"] == "broken"
                                 and row.get("primary_defect") == lab["defect"]) else 0
    return scores


def runs(pattern, labels):
    return [load_run(p, labels) for p in sorted(DOG.glob(pattern))]


class TestExistenceEquivalence:
    """gate_math vs existence-r5.json / skills/evaluate-skill/wise-eval.json."""

    def setup_method(self):
        labels = load_labels("labels-behavioral.json")
        self.expected = json.loads((DOG / "existence-r5.json").read_text())
        self.wise = json.loads(
            (ROOT / "skills" / "evaluate-skill" / "wise-eval.json").read_text())
        self.got = gate_math.existence_gate(
            runs("round2-runs/ns-*.json", labels),
            runs("round2-runs/a-*.json", labels),
            sorted(labels))

    def test_reference_run_aggregates(self):
        assert self.got["no_skill_run_aggregates"] == self.expected["ns_run_aggregates"]

    def test_noise_band(self):
        assert self.got["noise_band_exist"] == self.expected["noise_band_exist"] == 0.0796

    def test_pass_rates_and_delta(self):
        assert self.got["no_skill_pass_rate"] == self.expected["no_skill_pass_rate"] == 0.7241
        assert self.got["with_skill_pass_rate"] == self.expected["with_skill_pass_rate"] == 0.8276
        # delta must be computed on raw aggregates, then rounded (3/29 -> 0.1034,
        # not 0.8276-0.7241 -> 0.1035)
        assert self.got["delta_exist"] == self.expected["delta_exist"] == 0.1034

    def test_regressions(self):
        assert self.got["regression_count"] == self.expected["regression_count"] == 0
        assert self.got["regressions"] == self.expected["regressions"] == []

    def test_power(self):
        assert self.got["power"] == self.expected["power"]

    def test_verdict(self):
        assert self.got["gate_pass"] == "pass"
        assert self.got["certainty"] == "certifying"

    def test_shipped_wise_eval_reproducible_from_committed_scores(self):
        """The pinned verdict (A5, deployment harness) must recompute exactly from
        the committed raw condition scores in dogfood/gate-runner-a5/."""
        def load_scores(name):
            d = json.loads((ROOT / "dogfood" / "gate-runner-a5" / name).read_text())
            return [r["scores"] for r in d["runs"]]
        ref, test = load_scores("scores-no_skill.json"), load_scores("scores-with_skill.json")
        tasks = sorted(ref[0])
        got = gate_math.existence_gate(ref, test, tasks, cost_ratio=24067632 / 14602204)
        e = self.wise["effect"]
        for field in ("no_skill_pass_rate", "with_skill_pass_rate",
                      "delta_exist", "noise_band_exist", "regression_count"):
            assert got[field] == e[field], field
        assert got["power"] == self.wise["power"]
        assert got["gate_pass"] == self.wise["gate_pass"] == "fail"
        assert got["certainty"] == self.wise["certainty"]


class TestImprovementEquivalence:
    """gate_math vs round2-runs/round2-gate.json (labels-run key, ns-1/ns-2 floor)."""

    def setup_method(self):
        labels = load_labels("labels-run.json")
        self.expected = json.loads((DOG / "round2-runs" / "round2-gate.json").read_text())
        ns = [load_run(DOG / "round2-runs" / f"ns-{i}.json", labels) for i in (1, 2)]
        self.got = gate_math.improvement_gate(
            runs("round2-runs/a-*.json", labels),
            runs("round2-runs/b-*.json", labels),
            ns, sorted(labels))

    def test_reference_run_aggregates(self):
        assert self.got["prev_run_aggregates"] == self.expected["a_run_aggregates"]

    def test_noise_band(self):
        assert self.got["noise_band"] == self.expected["noise_band"] == 0.0398

    def test_pass_rates_and_deltas(self):
        for mine, theirs in (("prev_accepted_pass_rate",) * 2,
                             ("with_edited_pass_rate",) * 2,
                             ("no_skill_pass_rate",) * 2,
                             ("delta_step",) * 2,
                             ("delta_exist_edited",) * 2):
            assert self.got[mine] == self.expected[theirs], mine

    def test_regressions_and_floor(self):
        assert self.got["regressions_vs_previous"] == self.expected["regressions_vs_previous"]
        assert self.got["floor_breaches_edited"] == self.expected["floor_breaches_edited"] == ["task-03"]
        assert self.got["floor_breaches_entry"] == self.expected["floor_breaches_entry"] == ["task-03"]

    def test_power_and_decision(self):
        assert self.got["power"] == self.expected["power"]
        assert self.got["decision"] == self.expected["decision"] == "REVERT"


class TestResolutionOrder:
    """The gate file's resolution order, first match wins — unit cases."""

    T6 = [f"t{i}" for i in range(6)]

    def _runs(self, *rows):
        return [dict(zip(self.T6, row)) for row in rows]

    def test_negative_transfer_outranks_ceiling(self):
        ref = self._runs([1] * 6, [1] * 6, [1] * 6)
        test = self._runs([1, 1, 1, 1, 1, 0], [1, 1, 1, 1, 1, 0])
        got = gate_math.existence_gate(ref, test, self.T6)
        assert got["gate_pass"] == "fail" and "negative transfer" in got["why"]

    def test_inertia_cost_fatal_outranks_unfit(self):
        # flat delta (inside a zero band) + heavy cost -> fail, not unfit routing
        ref = self._runs([1, 0, 1, 0, 1, 0], [1, 0, 1, 0, 1, 0], [1, 0, 1, 0, 1, 0])
        test = self._runs([1, 0, 1, 0, 1, 0], [1, 0, 1, 0, 1, 0])
        got = gate_math.existence_gate(ref, test, self.T6, cost_ratio=2.0)
        assert got["gate_pass"] == "fail" and "inertia-cost" in got["why"]

    def test_cost_clean_when_delta_clears_band(self):
        ref = self._runs([0, 0, 0, 1, 1, 0], [0, 0, 0, 1, 1, 0], [0, 0, 0, 1, 1, 0])
        test = self._runs([1] * 6, [1] * 6)
        got = gate_math.existence_gate(ref, test, self.T6, cost_ratio=2.0)
        assert got["gate_pass"] == "pass"  # §8-5 fires only with delta inside the band

    def test_ceiling_routes_unfit(self):
        ref = self._runs([1] * 6, [1] * 6, [1] * 6)
        test = self._runs([1] * 6, [1] * 6)
        assert gate_math.existence_gate(ref, test, self.T6)["gate_pass"] == "unfit_test_set"

    def test_small_set_demotes_to_indicative(self):
        t4 = self.T6[:4]
        ref = [{t: 0 for t in t4}] * 3
        test = [{t: 1 for t in t4}] * 2
        got = gate_math.existence_gate(ref, test, t4)
        assert got["gate_pass"] == "pass" and got["certainty"] == "indicative"
        assert got["power"]["adequate"] is False

    def test_lateral_keep_requires_clean_floor(self):
        prev = self._runs([1, 1, 0, 0, 1, 1], [1, 1, 0, 0, 1, 1], [1, 1, 0, 0, 1, 1])
        ns = self._runs([0] * 6, [0] * 6)
        same = self._runs([1, 1, 0, 0, 1, 1], [1, 1, 0, 0, 1, 1])
        got = gate_math.improvement_gate(prev, same, ns, self.T6,
                                         removes_blocking_structural=True)
        assert got["decision"] == "KEEP (lateral)"
        breach = self._runs([0, 1, 0, 0, 1, 1], [0, 1, 0, 0, 1, 1])
        ns_high = self._runs([1, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0])
        got = gate_math.improvement_gate(prev, breach, ns_high, self.T6,
                                         removes_blocking_structural=True)
        assert got["decision"] == "REVERT"  # fatals outrank the lateral exception
