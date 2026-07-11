#!/usr/bin/env python3
# AUTO-GENERATED COPY - DO NOT EDIT.
# Source of truth: shared/scripts/gate_runner.py (edit there, then run scripts/sync-shared.py).
# Materialized into scripts/ so a standalone skill install carries its own gate runner.
"""gate_runner.py — run the effect gate (shared/effect-gate.md) with one command.

The gate has three parts: run the arms, assert on the products, do the arithmetic.
The arithmetic was already compiled (gate_math.py); this runner compiles the other
two so keep/revert never depends on the gated engine hand-assembling its own
measurement (THEORY §4 / effect-gate "Self-reference").

    gate_runner.py run <tasks.yaml> [--out DIR] [--require-certifying]
                                    [--confirm-draft] [--structural-repair]
                                    [--confirm-slice]
    gate_runner.py validate <tasks.yaml|tasks.draft.yaml>

Exit codes: 0 pass/KEEP (with --require-certifying also certainty=certifying);
1 fail/REVERT; 2 static_only / unfit_test_set / draft refused; 3 harness error.

tasks.yaml schema (drafts from evaluate-skill Tier 1 use the same shape):

    skill: skills/evaluate-skill      # dir containing SKILL.md (resolved vs CWD,
                                      #   then vs the tasks.yaml directory)
    tier: production                  # scaffold | production | library
    question: existence               # existence | improvement
    k_ref: 3                          # reference repetitions; charter-fixed at 3
    k_test: 2                         # test-condition repetitions, >= 2
    runner:
      model: claude-haiku-4-5         # engine model, shared by both arms
      timeout_s: 600
      permission_mode: bypassPermissions   # optional; runs happen in throwaway sandboxes
    judges:                           # >= 2 when any judge assertion exists
      - model: claude-sonnet-5
      - model: claude-haiku-4-5
    tasks:
      - id: task-01
        prompt: "..."                 # given verbatim to both arms
        workspace: fixtures/task-01/  # optional; copied into each run sandbox
        assert:                       # all must pass for the run to score 1
          - type: file_exists
            path: out/report.md
          - type: regex
            path: out/report.md
            pattern: "..."
            negate: false
          - type: script              # exit 0 = pass; cwd = the run workspace
            run: fixtures/task-01/check.py
          - type: judge               # semantic residue only; compile what compiles
            rubric: "the product must ..."
            path: out/report.md       # optional; defaults to the engine's final text
    confirm: []                       # improvement only: held-back task defs; never
                                      #   run in a round (§8-4) — only --confirm-slice
    prev_accepted: <dir-or-scores.json>   # improvement only: previous accepted skill
    no_skill_baseline: <scores.json>      # improvement only, optional: reuse stored floor

Isolation (verified against Claude Code 2.1.207 docs/help, not memory): the only
difference between arms is the physical presence of the skill under the sandbox's
project-level `.claude/skills/`; both arms run with CLAUDE_CONFIG_DIR pointed at a
per-run directory seeded with credential material ONLY, so user-level
skills/CLAUDE.md/plugins/MCP cannot leak (`--setting-sources` governs settings
files only, NOT skill discovery), and the sandbox cwd lives outside any repository
so project-level config cannot leak by parent-directory discovery either. Judges
run as separate headless calls with all tools disabled, never told arm identity.
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import statistics
import subprocess
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_math  # noqa: E402  (materialized next to this file by sync-shared.py)

try:
    import yaml
except ImportError:
    print("gate_runner needs PyYAML: pip install pyyaml", file=sys.stderr)
    sys.exit(3)

ASSERT_TYPES = {"file_exists", "regex", "script", "judge"}
ARTIFACT_CAP = 50_000  # chars of artifact text a judge sees


def warn(msg):
    print(f"gate_runner: WARNING: {msg}", file=sys.stderr)


def die(msg, code=3):
    print(f"gate_runner: error: {msg}", file=sys.stderr)
    sys.exit(code)


# ---------------------------------------------------------------- config

def resolve_dir(token, cfg_dir):
    """Resolve a config path against CWD first, then the tasks.yaml directory."""
    for base in (Path.cwd(), cfg_dir):
        p = (base / token).resolve() if not Path(token).is_absolute() else Path(token)
        if p.exists():
            return p
    return None


def validate_config(cfg, cfg_dir):
    """Return a list of schema errors (empty = valid)."""
    errs = []
    if not isinstance(cfg, dict):
        return ["top level must be a mapping"]
    skill = cfg.get("skill")
    if not skill:
        errs.append("missing: skill")
    else:
        d = resolve_dir(skill, cfg_dir)
        if d is None or not (d / "SKILL.md").is_file():
            errs.append(f"skill '{skill}' does not resolve to a directory containing SKILL.md")
    if cfg.get("tier") not in {"scaffold", "production", "library"}:
        errs.append("tier must be scaffold | production | library")
    question = cfg.get("question")
    if question not in {"existence", "improvement"}:
        errs.append("question must be existence | improvement")
    k_ref = cfg.get("k_ref", 3)
    if not isinstance(k_ref, int) or k_ref < 3:
        errs.append("k_ref must be an integer >= 3 (charter fixes the reference at 3)")
    k_test = cfg.get("k_test", 2)
    if not isinstance(k_test, int) or k_test < 2:
        errs.append("k_test must be an integer >= 2")
    runner = cfg.get("runner") or {}
    if not runner.get("model"):
        errs.append("missing: runner.model")
    judges = cfg.get("judges") or []
    if any(not isinstance(j, dict) or not j.get("model") for j in judges):
        errs.append("each judge needs a model")
    tasks = cfg.get("tasks") or []
    if not tasks:
        errs.append("tasks must be a non-empty list")
    seen, n_judge_asserts, n_compiled = set(), 0, 0
    for t in tasks + (cfg.get("confirm") or []):
        tid = t.get("id")
        if not tid or tid in seen:
            errs.append(f"task ids must be present and unique (offender: {tid!r})")
        seen.add(tid)
        if not t.get("prompt"):
            errs.append(f"{tid}: missing prompt")
        if t.get("workspace") and resolve_dir(t["workspace"], cfg_dir) is None:
            errs.append(f"{tid}: workspace '{t['workspace']}' not found")
        asserts = t.get("assert") or []
        if not asserts:
            errs.append(f"{tid}: needs at least one assertion")
        for a in asserts:
            atype = a.get("type")
            if atype not in ASSERT_TYPES:
                errs.append(f"{tid}: unknown assert type {atype!r}")
            elif atype in {"file_exists", "regex"} and not a.get("path"):
                errs.append(f"{tid}: {atype} assert needs a path")
            elif atype == "regex" and not a.get("pattern"):
                errs.append(f"{tid}: regex assert needs a pattern")
            elif atype == "script":
                if not a.get("run"):
                    errs.append(f"{tid}: script assert needs a run entry")
                elif resolve_dir(a["run"], cfg_dir) is None:
                    errs.append(f"{tid}: script '{a['run']}' not found")
            elif atype == "judge" and not a.get("rubric"):
                errs.append(f"{tid}: judge assert needs a rubric")
            n_judge_asserts += atype == "judge"
            n_compiled += atype in {"file_exists", "regex", "script"}
    if n_judge_asserts and len(judges) < 2:
        errs.append("judge assertions present: need >= 2 decorrelated judges (§7)")
    if question == "improvement":
        prev = cfg.get("prev_accepted")
        if not prev:
            errs.append("question=improvement requires prev_accepted (skill dir or scores.json)")
        elif resolve_dir(prev, cfg_dir) is None:
            errs.append(f"prev_accepted '{prev}' not found")
        baseline = cfg.get("no_skill_baseline")
        if baseline and resolve_dir(baseline, cfg_dir) is None:
            errs.append(f"no_skill_baseline '{baseline}' not found")
    elif cfg.get("confirm"):
        errs.append("confirm slice applies to improvement runs only (§8-4)")
    return errs


def config_warnings(cfg):
    ws = []
    if cfg.get("k_ref", 3) > 3:
        ws.append("k_ref > 3: the charter's band estimator is defined on exactly 3 reference "
                  "runs; extra runs are accepted but non-canonical (§8-1)")
    judges = cfg.get("judges") or []
    models = [j["model"] for j in judges]
    if len(models) >= 2 and len(set(models)) == 1:
        ws.append("all judges share one model: information isolation is enforced per-call, "
                  "but a same-model second judge removes sampling variance only, not shared bias (§7)")
    n_judge = sum(1 for t in cfg.get("tasks", []) for a in t.get("assert", [])
                  if a.get("type") == "judge")
    n_comp = sum(1 for t in cfg.get("tasks", []) for a in t.get("assert", [])
                 if a.get("type") != "judge")
    if n_judge > n_comp:
        ws.append("judge assertions outnumber compiled ones: compile what compiles "
                  "(file_exists/regex/script) to keep judge noise structurally small (§7)")
    return ws


# ---------------------------------------------------------------- sandbox

def prepare_auth_seed():
    """Credential material — and ONLY credential material — to copy into each
    sandbox's isolated config dir. Skills, settings, plugins, and MCP config never
    ride along; without this seed an isolated CLAUDE_CONFIG_DIR is logged out.

    Sources: <real config>/.credentials.json (Linux/CI convention), the macOS
    Keychain item "Claude Code-credentials", and the state file's oauthAccount.
    ANTHROPIC_API_KEY needs no seeding — it passes through the environment.
    """
    real_cfg = Path(os.environ.get("CLAUDE_CONFIG_DIR") or Path.home() / ".claude")
    seed = {}
    cred = real_cfg / ".credentials.json"
    if cred.is_file():
        seed[".credentials.json"] = cred.read_text()
    elif sys.platform == "darwin":
        try:
            out = subprocess.run(
                ["security", "find-generic-password", "-s", "Claude Code-credentials", "-w"],
                capture_output=True, text=True, timeout=10)
            if out.returncode == 0 and out.stdout.strip():
                seed[".credentials.json"] = out.stdout.strip()
        except (OSError, subprocess.TimeoutExpired):
            pass
    state = {"hasCompletedOnboarding": True}
    for candidate in (real_cfg / ".claude.json", Path.home() / ".claude.json"):
        if candidate.is_file():
            try:
                acct = json.loads(candidate.read_text()).get("oauthAccount")
                if acct:
                    state["oauthAccount"] = acct
                break
            except (json.JSONDecodeError, OSError):
                pass
    seed[".claude.json"] = json.dumps(state)
    if ".credentials.json" not in seed and not os.environ.get("ANTHROPIC_API_KEY"):
        warn("no credential source found (no .credentials.json, keychain entry, or "
             "ANTHROPIC_API_KEY) — engine runs will likely fail as logged-out")
    return seed


def build_sandbox(run_dir, skill_dir, with_skill, workspace_fixture=None, auth_seed=None):
    """One run's isolated world. Returns (workspace, env) for the engine call.

    The two arms differ ONLY by the physical presence of the skill under the
    sandbox's project-level .claude/skills/; CLAUDE_CONFIG_DIR points at an empty
    per-run directory so user-level config cannot leak into either arm.

    The sandbox lives under the system temp dir, OUTSIDE any repository: the CLI
    discovers .claude/ and CLAUDE.md by walking up from its cwd, so a workspace
    inside the caller's repo would leak the host project's config into both arms.
    run_dir (inside --out) keeps only records, never the live cwd.
    """
    sandbox = Path(tempfile.mkdtemp(prefix="wise-gate-"))
    workspace = sandbox / "workspace"
    workspace.mkdir()
    if workspace_fixture:
        shutil.copytree(workspace_fixture, workspace, dirs_exist_ok=True)
    if with_skill:
        dest = workspace / ".claude" / "skills" / Path(skill_dir).name
        shutil.copytree(skill_dir, dest,
                        ignore=shutil.ignore_patterns("wise-eval.*", "tasks*.yaml", ".wise-runs"))
    config_dir = sandbox / "claude-config"
    config_dir.mkdir()
    for name, payload in (auth_seed or {}).items():
        p = config_dir / name
        p.write_text(payload)
        p.chmod(0o600)
    env = dict(os.environ)
    env["CLAUDE_CONFIG_DIR"] = str(config_dir)
    env["CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC"] = "1"
    Path(run_dir).mkdir(parents=True, exist_ok=True)
    return workspace, env


def run_engine(prompt, workspace, env, model, timeout_s, permission_mode, extra_args=()):
    """One headless engine call; returns the parsed result JSON (or an error dict)."""
    cmd = ["claude", "-p", prompt, "--output-format", "json", "--model", model,
           "--permission-mode", permission_mode, "--no-session-persistence", *extra_args]
    try:
        proc = subprocess.run(cmd, cwd=workspace, env=env, timeout=timeout_s,
                              capture_output=True, text=True)
    except FileNotFoundError:
        die("claude CLI not found on PATH")
    except subprocess.TimeoutExpired:
        return {"is_error": True, "result": f"harness timeout after {timeout_s}s"}
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {"is_error": True,
                "result": f"unparseable CLI output (exit {proc.returncode}): "
                          f"{proc.stdout[-500:]!r} stderr: {proc.stderr[-500:]!r}"}


def usage_tokens(result):
    """Total tokens the run processed, or None when the CLI exposed no usage."""
    u = result.get("usage") or {}
    if "input_tokens" not in u or "output_tokens" not in u:
        return None
    return (u["input_tokens"] + u["output_tokens"]
            + u.get("cache_creation_input_tokens", 0) + u.get("cache_read_input_tokens", 0))


# ---------------------------------------------------------------- assertions

def judge_vote(rubric, artifact, judge_model, env_base, scratch, timeout_s, permission_mode):
    """One isolated judge call -> True/False/None(unusable). The judge sees rubric +
    artifact only: no arm identity, no skill text, no other judge, no diff (§7)."""
    prompt = ("You are an isolated judge. Evaluate ONLY the artifact below against the "
              "rubric. Do not speculate about how or by whom it was produced.\n\n"
              f"Rubric: {rubric}\n\nArtifact:\n---\n{artifact[:ARTIFACT_CAP]}\n---\n\n"
              "Reply with exactly one word: PASS or FAIL.")
    scratch.mkdir(parents=True, exist_ok=True)
    res = run_engine(prompt, scratch, env_base, judge_model, timeout_s,
                     permission_mode, extra_args=("--tools", ""))
    if res.get("is_error"):
        return None
    hits = re.findall(r"\b(PASS|FAIL)\b", res.get("result") or "")
    return None if not hits else hits[-1] == "PASS"


def eval_judge_assert(a, workspace, result_text, judges, run_dir, env, runner_cfg):
    """Median of >= 2 decorrelated judges; a categorical split escalates to a third;
    still unresolved -> passed False (evaluate-skill's standing rule)."""
    if a.get("path"):
        f = Path(workspace) / a["path"]
        if not f.is_file():
            return False, f"judge artifact missing: {a['path']}"
        artifact = f.read_text(encoding="utf-8", errors="replace")
    else:
        artifact = result_text or ""
    votes, models = [], []
    order = list(judges[:2]) + [judges[0]]  # third = tiebreak, fresh context
    for i, j in enumerate(order):
        if i == 2 and len(votes) == 2 and votes.count(True) != 1:
            break  # two usable votes, no categorical split -> no third judge
        scratch = Path(run_dir) / f"judge-{i}"
        v = judge_vote(a["rubric"], artifact, j["model"], env, scratch,
                       runner_cfg.get("timeout_s", 600),
                       runner_cfg.get("permission_mode", "bypassPermissions"))
        if v is None:
            warn(f"judge {j['model']} returned no usable verdict")
        else:
            votes.append(v)
            models.append(j["model"])
    if len(votes) < 2:
        return False, f"fewer than 2 usable judge verdicts ({len(votes)})"
    passed = statistics.median(votes) > 0.5 if len(votes) % 2 else all(votes)
    return bool(passed), f"votes={['PASS' if v else 'FAIL' for v in votes]} by {models}"


def eval_assertions(task, workspace, result_text, judges, run_dir, env, runner_cfg, cfg_dir):
    """All-or-nothing compiled score for one run: every assertion must pass."""
    results = []
    for a in task.get("assert", []):
        atype = a["type"]
        if atype == "file_exists":
            ok = (Path(workspace) / a["path"]).is_file()
            detail = a["path"]
        elif atype == "regex":
            f = Path(workspace) / a["path"]
            if not f.is_file():
                ok, detail = False, f"file missing: {a['path']}"
            else:
                hit = re.search(a["pattern"], f.read_text(encoding="utf-8", errors="replace"))
                ok = (hit is None) if a.get("negate") else (hit is not None)
                detail = f"pattern={a['pattern']!r} negate={bool(a.get('negate'))}"
        elif atype == "script":
            script = resolve_dir(a["run"], cfg_dir)
            cmd = ([str(script)] if os.access(script, os.X_OK)
                   else [sys.executable if script.suffix == ".py" else "bash", str(script)])
            try:
                proc = subprocess.run(cmd, cwd=workspace, capture_output=True, text=True,
                                      timeout=120, env={**os.environ, "WISE_WORKSPACE": str(workspace)})
                ok, detail = proc.returncode == 0, f"exit {proc.returncode}"
            except subprocess.TimeoutExpired:
                ok, detail = False, "script timeout (120s)"
        else:  # judge
            ok, detail = eval_judge_assert(a, workspace, result_text, judges,
                                           run_dir, env, runner_cfg)
        results.append({"type": atype, "passed": ok, "detail": detail})
    return int(all(r["passed"] for r in results)), results


def snapshot_artifacts(task, workspace, run_dir):
    """Copy the files the assertions touched into the run record (raw data survives
    even after the OS reclaims the temp sandbox)."""
    for a in task.get("assert", []):
        rel = a.get("path")
        if not rel:
            continue
        src = Path(workspace) / rel
        if src.is_file():
            dest = Path(run_dir) / "artifacts" / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)


# ---------------------------------------------------------------- conditions

def run_condition(name, skill_dir, with_skill, tasks, k, cfg, cfg_dir, out_dir):
    """Run every task k times under one condition; persist raw run records.

    Returns {"runs": [per-run task->score], "tokens": int|None, "usd": float|None}.
    tokens is None iff any run failed to expose usage (never silently zero)."""
    runner_cfg = cfg.get("runner") or {}
    judges = cfg.get("judges") or []
    auth_seed = prepare_auth_seed()
    runs, tokens_total, usd_total, usage_missing = [], 0, 0.0, False
    for i in range(1, k + 1):
        scores = {}
        for task in tasks:
            run_dir = Path(out_dir) / "runs" / name / f"{task['id']}-r{i}"
            fixture = resolve_dir(task["workspace"], cfg_dir) if task.get("workspace") else None
            for attempt in (1, 2):
                workspace, env = build_sandbox(run_dir, skill_dir, with_skill, fixture, auth_seed)
                res = run_engine(task["prompt"], workspace, env,
                                 runner_cfg["model"], runner_cfg.get("timeout_s", 600),
                                 runner_cfg.get("permission_mode", "bypassPermissions"))
                if not res.get("is_error"):
                    break
                warn(f"{name}/{task['id']} run {i} attempt {attempt}: engine error: "
                     f"{str(res.get('result'))[:200]}")
            (run_dir / "engine-output.json").write_text(json.dumps(res, indent=1))
            if res.get("is_error"):
                # A broken harness must never be scored as a failed task: no verdict.
                die(f"engine run failed twice ({name}/{task['id']} run {i}) — "
                    "aborting without a verdict; fix the harness (auth? model id? "
                    "timeout?) and re-run")
            toks = usage_tokens(res)
            if toks is None:
                usage_missing = True
            else:
                tokens_total += toks
                usd_total += res.get("total_cost_usd") or 0.0
            score, assertion_results = eval_assertions(
                task, workspace, res.get("result"), judges, run_dir, env, runner_cfg, cfg_dir)
            scores[task["id"]] = score
            snapshot_artifacts(task, workspace, run_dir)
            (run_dir / "run.json").write_text(json.dumps({
                "task": task["id"], "condition": name, "run_index": i,
                "prompt_sha256": hashlib.sha256(task["prompt"].encode()).hexdigest(),
                "model": runner_cfg["model"], "score": score,
                "assertions": assertion_results, "tokens": toks,
                "usd": res.get("total_cost_usd"), "num_turns": res.get("num_turns"),
                "duration_ms": res.get("duration_ms"), "is_error": bool(res.get("is_error")),
                "workspace": str(workspace), "transcript": "engine-output.json"}, indent=1))
        runs.append(scores)
    if usage_missing:
        warn(f"condition '{name}': the CLI exposed no usage on at least one run — "
             "cost will be marked UNEVALUATED, never silently skipped (§8-5)")
    record = {"condition": name, "with_skill": with_skill,
              "runs": [{"run_index": i + 1, "scores": r} for i, r in enumerate(runs)],
              "tokens": None if usage_missing else tokens_total,
              "usd": None if usage_missing else round(usd_total, 4)}
    (Path(out_dir) / f"scores-{name}.json").write_text(json.dumps(record, indent=1))
    return {"runs": runs, "tokens": record["tokens"], "usd": record["usd"]}


def load_stored_scores(path):
    """Reuse a stored scores-<condition>.json (baseline computed once, §8-6)."""
    data = json.loads(Path(path).read_text())
    return {"runs": [r["scores"] for r in data["runs"]],
            "tokens": data.get("tokens"), "usd": data.get("usd")}


# ---------------------------------------------------------------- reports

def write_existence_landing(skill_dir, gate_obj, out_dir):
    """Pinned landing (evaluate-skill convention): <skill-dir>/wise-eval.json + .md.
    Same schema as every other emitter; probe.py needs no change to recognize it."""
    (Path(skill_dir) / "wise-eval.json").write_text(json.dumps(gate_obj, indent=1))
    e = gate_obj["effect"]
    cost = ("UNEVALUATED (CLI exposed no usage)" if gate_obj.get("cost_unevaluated")
            else f"{e['tokens_no_skill']} vs {e['tokens_with_skill']} tokens, ratio {e['cost_ratio']}")
    md = (f"# wise-eval — {Path(skill_dir).name} · existence gate · "
          f"**{gate_obj['gate_pass']} ({gate_obj['certainty']})** · {gate_obj['date']}\n\n"
          f"Compiled run by `gate_runner.py` (arms, assertions, and arithmetic all mechanical).\n\n"
          "| | value |\n|---|---|\n"
          f"| no-skill pass rate (medians, ×{gate_obj['runner']['k_ref']} runs) | {e['no_skill_pass_rate']} |\n"
          f"| with-skill pass rate (medians, ×{gate_obj['runner']['k_test']} runs) | {e['with_skill_pass_rate']} |\n"
          f"| `delta_exist` | **{e['delta_exist']}** |\n"
          f"| `noise_band_exist` (2×SD of {gate_obj['runner']['k_ref']} no-skill aggregates) | {e['noise_band_exist']} |\n"
          f"| reproduced regressions | {e['regression_count']} |\n"
          f"| cost | {cost} |\n"
          f"| power | n={gate_obj['power']['n_tasks']}, resolution {gate_obj['power']['resolution']}, "
          f"adequate={gate_obj['power']['adequate']} → **{gate_obj['certainty']}** |\n\n"
          f"Why: {gate_obj['effect']['why']}\n\n"
          f"Raw run records (per-run JSON, usage, transcripts): `{out_dir}`\n")
    (Path(skill_dir) / "wise-eval.md").write_text(md)


def assemble_existence_gate(cfg, skill_path_as_given, ex, ref, test):
    cost_unevaluated = ref["tokens"] is None or test["tokens"] is None
    cost_ratio = (None if cost_unevaluated or not ref["tokens"]
                  else round(test["tokens"] / ref["tokens"], 4))
    gate_obj = {
        "skill": skill_path_as_given,
        "tier": cfg["tier"],
        "question": "existence",
        "evaluated_layers": ["effect"],
        "gate_pass": ex["gate_pass"],
        "certainty": ex["certainty"],
        "date": time.strftime("%Y-%m-%d"),
        "power": ex["power"],
        "judges": [{"model": j["model"], "isolated": True} for j in cfg.get("judges") or []],
        "structural": None,  # Tier 1 is evaluate-skill's static read; this runner is the effect layer
        "effect": {
            "no_skill_pass_rate": ex["no_skill_pass_rate"],
            "with_skill_pass_rate": ex["with_skill_pass_rate"],
            "delta_exist": ex["delta_exist"],
            "noise_band_exist": ex["noise_band_exist"],
            "no_skill_run_aggregates": ex["no_skill_run_aggregates"],
            "tokens_no_skill": ref["tokens"],
            "tokens_with_skill": test["tokens"],
            "cost_ratio": cost_ratio,
            "usd_no_skill": ref["usd"],
            "usd_with_skill": test["usd"],
            "floor_ok": ex["regression_count"] == 0,
            "regression_count": ex["regression_count"],
            "regressions": ex["regressions"],
            "safety_regression": False,
            "safety_note": "safety signals are not instrumented by gate_runner; they remain the orchestrator's read",
            "why": ex["why"],
            "per_task": ex["per_task"],
        },
        "discrimination": None,
        "fix_list": [],
        "cost_unevaluated": cost_unevaluated,
        "runner": {"engine_model": cfg["runner"]["model"], "k_ref": cfg.get("k_ref", 3),
                   "k_test": cfg.get("k_test", 2), "compiled_by": "gate_runner.py"},
    }
    return gate_obj


# ---------------------------------------------------------------- modes

def cmd_run(args):
    cfg_path = Path(args.tasks)
    if cfg_path.name.endswith(".draft.yaml") and not args.confirm_draft:
        print("gate_runner: refusing to score a draft task set "
              f"({cfg_path.name}): review it and rename to tasks.yaml, or pass "
              "--confirm-draft. Draft-and-confirm is the gate's rule, not advice.",
              file=sys.stderr)
        sys.exit(2)
    cfg = yaml.safe_load(cfg_path.read_text())
    cfg_dir = cfg_path.resolve().parent
    errs = validate_config(cfg, cfg_dir)
    if errs:
        die("invalid tasks file:\n  - " + "\n  - ".join(errs))
    for w in config_warnings(cfg):
        warn(w)

    skill_dir = resolve_dir(cfg["skill"], cfg_dir)
    out_dir = Path(args.out) if args.out else \
        Path(".wise-runs") / skill_dir.name / time.strftime("%Y%m%dT%H%M%S")
    out_dir.mkdir(parents=True, exist_ok=True)
    k_ref, k_test = cfg.get("k_ref", 3), cfg.get("k_test", 2)
    tasks = cfg["tasks"]
    task_ids = [t["id"] for t in tasks]

    if cfg["question"] == "existence":
        ref = run_condition("no_skill", skill_dir, False, tasks, k_ref, cfg, cfg_dir, out_dir)
        test = run_condition("with_skill", skill_dir, True, tasks, k_test, cfg, cfg_dir, out_dir)
        cost_unevaluated = ref["tokens"] is None or test["tokens"] is None
        cost_ratio = (None if cost_unevaluated or not ref["tokens"]
                      else test["tokens"] / ref["tokens"])
        if cost_unevaluated:
            warn("cost block is UNEVALUATED: gate object carries cost_ratio null + "
                 "cost_unevaluated true (§8-5 debt made loud, not silent)")
        ex = gate_math.existence_gate(ref["runs"], test["runs"], task_ids,
                                      cost_ratio=cost_ratio)
        gate_obj = assemble_existence_gate(cfg, cfg["skill"], ex, ref, test)
        write_existence_landing(skill_dir, gate_obj, out_dir)
        print(json.dumps(gate_obj, separators=(",", ":")))
        if gate_obj["gate_pass"] == "pass":
            ok = gate_obj["certainty"] == "certifying" if args.require_certifying else True
            sys.exit(0 if ok else 1)
        sys.exit(2 if gate_obj["gate_pass"] in ("static_only", "unfit_test_set") else 1)

    # improvement branch (§8-6: its own reference frame — never delta_exist)
    prev = resolve_dir(cfg["prev_accepted"], cfg_dir)
    # §8-4 hinges on this line: a round sees ONLY the working tasks; the confirm
    # slice is selected exclusively by the explicit --confirm-slice terminal check.
    slice_tasks = (cfg.get("confirm") or []) if args.confirm_slice else tasks
    if args.confirm_slice and not slice_tasks:
        die("--confirm-slice: config has no confirm tasks", 2)
    if not args.confirm_slice and cfg.get("confirm"):
        # §8-4: the held-back slice is physically invisible to every round — its
        # prompts and paths are simply never passed to any engine or judge here.
        warn(f"confirm slice held back ({len(cfg['confirm'])} tasks): "
             "run --confirm-slice once, only at the loop's terminal 'improved'")
    if prev.is_file():
        if args.confirm_slice:
            die("--confirm-slice needs prev_accepted to be a skill directory: stored "
                "scores cover the working slice, which the confirm tasks are not", 2)
        ref = load_stored_scores(prev)
        if len(ref["runs"]) < 3:
            die("stored prev_accepted scores must contain >= 3 runs (band needs them)")
    else:
        ref = run_condition("prev_accepted", prev, True, slice_tasks, k_ref, cfg, cfg_dir, out_dir)
    test = run_condition("with_edited", skill_dir, True, slice_tasks, k_test, cfg, cfg_dir, out_dir)
    ids = [t["id"] for t in slice_tasks]

    if args.confirm_slice:
        med_prev = gate_math.per_task_medians(ref["runs"], ids)
        med_edit = gate_math.per_task_medians(test["runs"], ids)
        delta = sum(med_edit.values()) / len(ids) - sum(med_prev.values()) / len(ids)
        out = {"confirm_slice": ids, "delta_confirm": round(delta, 4),
               "confirmed": delta >= 0,
               "reading": "improved" if delta >= 0 else "improved (unconfirmed) — rotate the set"}
        (out_dir / "confirm-gate.json").write_text(json.dumps(out, indent=1))
        print(json.dumps(out, separators=(",", ":")))
        sys.exit(0 if out["confirmed"] else 1)

    if cfg.get("no_skill_baseline"):
        floor = load_stored_scores(resolve_dir(cfg["no_skill_baseline"], cfg_dir))
    else:
        floor = run_condition("no_skill", skill_dir, False, slice_tasks, 2, cfg, cfg_dir, out_dir)
    imp = gate_math.improvement_gate(ref["runs"], test["runs"], floor["runs"], ids,
                                     removes_blocking_structural=args.structural_repair)
    cost_unevaluated = ref["tokens"] is None or test["tokens"] is None
    imp["cost_delta_tokens"] = (None if cost_unevaluated
                                else test["tokens"] - ref["tokens"])  # advisory, never a per-round fatal
    imp["cost_unevaluated"] = cost_unevaluated
    if cost_unevaluated:
        warn("cost block is UNEVALUATED for this round (advisory axis, still never silent)")
    (out_dir / "round-gate.json").write_text(json.dumps(imp, indent=1))
    print(json.dumps(imp, separators=(",", ":")))
    sys.exit(0 if imp["decision"].startswith("KEEP") else 1)


def cmd_validate(args):
    cfg_path = Path(args.tasks)
    try:
        cfg = yaml.safe_load(cfg_path.read_text())
    except yaml.YAMLError as e:
        die(f"not valid YAML: {e}", 1)
    errs = validate_config(cfg, cfg_path.resolve().parent)
    if errs:
        print("invalid:\n  - " + "\n  - ".join(errs), file=sys.stderr)
        sys.exit(1)
    for w in config_warnings(cfg):
        warn(w)
    n = len(cfg.get("tasks", []))
    cert = "can certify" if n >= gate_math.N_ADEQUATE else \
        f"indicative only (extend to >= {gate_math.N_ADEQUATE} tasks to certify)"
    print(f"valid: {n} tasks, {cert}")
    sys.exit(0)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p_run = sub.add_parser("run", help="run the gate end to end")
    p_run.add_argument("tasks")
    p_run.add_argument("--out", help="raw-run output dir (default .wise-runs/<skill>/<ts>/)")
    p_run.add_argument("--require-certifying", action="store_true",
                       help="exit 0 only on pass AND certainty=certifying")
    p_run.add_argument("--confirm-draft", action="store_true",
                       help="score a *.draft.yaml anyway (you have reviewed it)")
    p_run.add_argument("--structural-repair", action="store_true",
                       help="improvement only: the edit removes a non-waived blocking "
                            "structural finding (caller verified via the linter); "
                            "enables the lateral-keep exception")
    p_run.add_argument("--confirm-slice", action="store_true",
                       help="improvement only: run the held-back confirm tasks "
                            "(terminal 'improved' re-check, §8-4) instead of a round")
    p_run.set_defaults(func=cmd_run)
    p_val = sub.add_parser("validate", help="schema-check a tasks.yaml or tasks.draft.yaml")
    p_val.add_argument("tasks")
    p_val.set_defaults(func=cmd_validate)
    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
