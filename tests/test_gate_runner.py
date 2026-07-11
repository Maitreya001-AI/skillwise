"""Runner invariants that hold without any engine call (acceptance A3, A4, plus
the draft refusal and the never-silent cost marking). The full A/B smoke (A2)
costs API money and lives in tests/smoke/ — run it by hand, never in CI."""

import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

import gate_runner

ROOT = Path(__file__).resolve().parent.parent
RUNNER = ROOT / "shared" / "scripts" / "gate_runner.py"


@pytest.fixture
def skill(tmp_path):
    d = tmp_path / "toy-skill"
    d.mkdir()
    (d / "SKILL.md").write_text("---\nname: toy\ndescription: toy\n---\nbody\n")
    (d / "wise-eval.json").write_text("{}")  # a stale verdict must not ride into the arm
    return d


def valid_cfg(skill_dir, **over):
    cfg = {
        "skill": str(skill_dir),
        "tier": "production",
        "question": "existence",
        "k_ref": 3,
        "k_test": 2,
        "runner": {"model": "claude-haiku-4-5", "timeout_s": 60},
        "judges": [{"model": "claude-sonnet-5"}, {"model": "claude-haiku-4-5"}],
        "tasks": [
            {"id": f"task-{i:02d}", "prompt": f"do thing {i}",
             "assert": [{"type": "file_exists", "path": "out/x.md"}]}
            for i in range(1, 7)
        ],
    }
    cfg.update(over)
    return cfg


class TestIsolation:
    """A3 — the arms differ only by the skill's physical presence."""

    def test_arm_a_has_skill_arm_b_does_not(self, tmp_path, skill):
        ws_a, _ = gate_runner.build_sandbox(tmp_path / "a", skill, with_skill=True)
        ws_b, _ = gate_runner.build_sandbox(tmp_path / "b", skill, with_skill=False)
        assert (ws_a / ".claude" / "skills" / "toy-skill" / "SKILL.md").is_file()
        assert not (ws_b / ".claude").exists()

    def test_stale_verdict_and_drafts_never_ride_along(self, tmp_path, skill):
        (skill / "tasks.draft.yaml").write_text("x: 1\n")
        ws_a, _ = gate_runner.build_sandbox(tmp_path / "a", skill, with_skill=True)
        installed = ws_a / ".claude" / "skills" / "toy-skill"
        assert not (installed / "wise-eval.json").exists()
        assert not (installed / "tasks.draft.yaml").exists()

    def test_user_level_config_is_walled_off(self, tmp_path, skill):
        """CLAUDE_CONFIG_DIR must point at a per-run dir holding credential material
        at most — never ~/.claude skills, CLAUDE.md, settings, plugins, or MCP."""
        ws, env = gate_runner.build_sandbox(tmp_path / "b", skill, with_skill=False,
                                            auth_seed=gate_runner.prepare_auth_seed())
        cfg_dir = Path(env["CLAUDE_CONFIG_DIR"])
        assert cfg_dir.parent == ws.parent  # per-run, inside the same sandbox
        names = {p.name for p in cfg_dir.iterdir()}
        assert names <= {".credentials.json", ".claude.json"}
        assert not any(p.is_dir() for p in cfg_dir.iterdir())

    def test_auth_seed_carries_credentials_only(self):
        seed = gate_runner.prepare_auth_seed()
        assert set(seed) <= {".credentials.json", ".claude.json"}
        state = json.loads(seed[".claude.json"])
        assert set(state) <= {"hasCompletedOnboarding", "oauthAccount"}

    def test_sandbox_lives_outside_any_repo(self, tmp_path, skill):
        """The CLI discovers .claude/ and CLAUDE.md by walking up from cwd, so the
        workspace must sit under the system temp dir, not inside the host repo."""
        import tempfile
        ws, _ = gate_runner.build_sandbox(tmp_path / "a", skill, with_skill=True)
        tmp_root = Path(tempfile.gettempdir()).resolve()
        assert ws.resolve().is_relative_to(tmp_root)
        assert not ws.resolve().is_relative_to(Path.cwd().resolve())

    def test_workspace_fixture_is_copied(self, tmp_path, skill):
        fixture = tmp_path / "fx"
        fixture.mkdir()
        (fixture / "seed.txt").write_text("hello")
        ws, _ = gate_runner.build_sandbox(tmp_path / "a", skill, True, fixture)
        assert (ws / "seed.txt").read_text() == "hello"


class TestDraftRefusal:
    """The confirmation gate is a mechanism, not a reminder."""

    def test_draft_is_refused_with_exit_2(self, tmp_path):
        draft = tmp_path / "tasks.draft.yaml"
        draft.write_text("skill: nowhere\n")
        proc = subprocess.run([sys.executable, str(RUNNER), "run", str(draft)],
                              capture_output=True, text=True, cwd=tmp_path)
        assert proc.returncode == 2
        assert "rename to tasks.yaml" in proc.stderr
        assert "--confirm-draft" in proc.stderr


class TestValidate:
    """A4 — the drafted schema must clear `validate` (draft name included)."""

    def test_a4_style_draft_validates(self, tmp_path, skill):
        cfg = valid_cfg(skill)
        cfg["tasks"] = cfg["tasks"][:3] + [{
            "id": "edge-01", "prompt": "edge case",
            "assert": [{"type": "judge", "rubric": "PLACEHOLDER: the product must ..."}],
        }]
        draft = tmp_path / "tasks.draft.yaml"
        draft.write_text("# draft = indicative only; extend to >= 6 tasks to certify;\n"
                         "# review and rename to tasks.yaml\n" + yaml.safe_dump(cfg))
        proc = subprocess.run([sys.executable, str(RUNNER), "validate", str(draft)],
                              capture_output=True, text=True, cwd=tmp_path)
        assert proc.returncode == 0, proc.stderr
        assert "indicative only" in proc.stdout

    def test_schema_errors_are_named(self, tmp_path, skill):
        cfg = valid_cfg(skill, tier="bogus")
        cfg["runner"] = {}
        cfg["tasks"][0]["assert"] = [{"type": "teleport"}]
        errs = gate_runner.validate_config(cfg, tmp_path)
        blob = "\n".join(errs)
        assert "tier" in blob and "runner.model" in blob and "teleport" in blob

    def test_judge_asserts_require_two_judges(self, tmp_path, skill):
        cfg = valid_cfg(skill, judges=[{"model": "solo"}])
        cfg["tasks"][0]["assert"].append({"type": "judge", "rubric": "r"})
        assert any("decorrelated judges" in e
                   for e in gate_runner.validate_config(cfg, tmp_path))

    def test_improvement_requires_prev_accepted(self, tmp_path, skill):
        cfg = valid_cfg(skill, question="improvement")
        assert any("prev_accepted" in e
                   for e in gate_runner.validate_config(cfg, tmp_path))

    def test_confirm_slice_is_improvement_only(self, tmp_path, skill):
        cfg = valid_cfg(skill, confirm=[{
            "id": "c-1", "prompt": "held back",
            "assert": [{"type": "file_exists", "path": "x"}]}])
        assert any("§8-4" in e or "improvement" in e
                   for e in gate_runner.validate_config(cfg, tmp_path))

    def test_charter_warnings(self, skill):
        cfg = valid_cfg(skill, k_ref=5,
                        judges=[{"model": "same"}, {"model": "same"}])
        ws = "\n".join(gate_runner.config_warnings(cfg))
        assert "exactly 3 reference" in ws and "shared bias" in ws


class TestResume:
    """Re-invoking with the same --out reuses completed runs — paid work is
    never re-bought, and stale/foreign records are never trusted."""

    REC = {"task": "t1", "condition": "no_skill", "run_index": 1,
           "prompt_sha256": gate_runner.hashlib.sha256(b"do thing").hexdigest(),
           "score": 1, "tokens": 500, "usd": 0.1, "is_error": False}

    def test_reuses_matching_completed_run(self, tmp_path):
        (tmp_path / "run.json").write_text(json.dumps(self.REC))
        rec = gate_runner._reuse_record(tmp_path, "do thing")
        assert rec is not None and rec["score"] == 1 and rec["tokens"] == 500

    def test_never_reuses_changed_prompt_or_errors(self, tmp_path):
        (tmp_path / "run.json").write_text(json.dumps(self.REC))
        assert gate_runner._reuse_record(tmp_path, "different prompt") is None
        (tmp_path / "run.json").write_text(json.dumps({**self.REC, "is_error": True}))
        assert gate_runner._reuse_record(tmp_path, "do thing") is None
        (tmp_path / "run.json").write_text("not json")
        assert gate_runner._reuse_record(tmp_path, "do thing") is None

    def test_workers_validated(self, tmp_path, skill):
        cfg = valid_cfg(skill)
        cfg["runner"]["workers"] = 0
        assert any("workers" in e for e in gate_runner.validate_config(cfg, tmp_path))
        cfg["runner"]["workers"] = 6
        assert not any("workers" in e for e in gate_runner.validate_config(cfg, tmp_path))


class TestCostNeverSilent:
    """§8-5 — a missing cost block is marked loudly, never skipped (the standing
    debt this runner exists to close)."""

    def test_usage_tokens_none_when_cli_exposes_nothing(self):
        assert gate_runner.usage_tokens({"result": "ok"}) is None
        assert gate_runner.usage_tokens({"usage": {"input_tokens": 5}}) is None

    def test_usage_tokens_sums_all_four_fields(self):
        res = {"usage": {"input_tokens": 10, "output_tokens": 20,
                         "cache_creation_input_tokens": 30,
                         "cache_read_input_tokens": 40}}
        assert gate_runner.usage_tokens(res) == 100

    def test_gate_object_marks_cost_unevaluated(self, skill):
        cfg = valid_cfg(skill)
        labels = [f"task-{i:02d}" for i in range(1, 7)]
        import gate_math
        ex = gate_math.existence_gate(
            [{t: 0 for t in labels}] * 3, [{t: 1 for t in labels}] * 2,
            labels, cost_ratio=None)
        gate_obj = gate_runner.assemble_existence_gate(
            cfg, cfg["skill"], ex,
            {"tokens": None, "usd": None}, {"tokens": 1000, "usd": 0.1})
        assert gate_obj["cost_unevaluated"] is True
        assert gate_obj["effect"]["cost_ratio"] is None

    def test_gate_object_cost_ratio_on_the_happy_path(self, skill):
        cfg = valid_cfg(skill)
        labels = [f"task-{i:02d}" for i in range(1, 7)]
        import gate_math
        ex = gate_math.existence_gate(
            [{t: 0 for t in labels}] * 3, [{t: 1 for t in labels}] * 2,
            labels, cost_ratio=1500 / 1000)
        gate_obj = gate_runner.assemble_existence_gate(
            cfg, cfg["skill"], ex,
            {"tokens": 1000, "usd": 0.1}, {"tokens": 1500, "usd": 0.2})
        assert gate_obj["cost_unevaluated"] is False
        assert gate_obj["effect"]["cost_ratio"] == 1.5
        assert gate_obj["effect"]["tokens_no_skill"] == 1000
        assert gate_obj["effect"]["tokens_with_skill"] == 1500
