#!/usr/bin/env python3
"""Run skill evals in parallel: with-skill vs without-skill.

Usage:
    eval-runner.py <skill-path>... [--iterations N] [--timeout SECS] [--parallel P]
    eval-runner.py --all [--iterations N] [--timeout SECS] [--parallel P]

    --all          Discover and run all skills under engineering/, general/,
                   design/, etc. that have evals/evals.json.
    --parallel P   Max concurrent pi processes (default: 4).
    --timeout SECS Per-process timeout (default: 600).

Uses pi as the eval harness with full skill isolation:
    - Global skill dirs moved during eval runs (prevents contamination)
    - --no-skills --no-extensions disables all discovery
    - --skill <path> loads ONLY the tested skill for with_skill variant
    - --no-context-files --no-session prevents context/session contamination
    - Sandbox workdir with git init prevents real repo state reading
    - Only the gateway extension is loaded (for model access)
"""
import atexit
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TIMEOUT = 600
DEFAULT_PARALLEL = 4

GLOBAL_SKILL_DIRS = [
    Path.home() / ".pi" / "agent" / "skills",
    Path.home() / ".agents" / "skills",
    Path.home() / ".claude" / "skills",
    Path.home() / ".opencode" / "skills",
]

GATEWAY_EXTENSION = str(Path.home() / ".pi" / "agent" / "extensions" / "gateway")

_moved_dirs: list[tuple[Path, Path]] = []


def isolate_global_skills() -> None:
    for d in GLOBAL_SKILL_DIRS:
        if d.exists() and d.is_dir():
            backup = d.parent / f"{d.name}._eval_bak"
            if backup.exists():
                continue
            d.rename(backup)
            _moved_dirs.append((d, backup))
            print(f"  Isolated: {d} → {backup}")


def restore_global_skills() -> None:
    for orig, backup in reversed(_moved_dirs):
        if backup.exists() and not orig.exists():
            backup.rename(orig)
            print(f"  Restored: {orig}")


atexit.register(restore_global_skills)

SKILL_SCAN_PREFIXES = [
    "agents", "design", "documentation", "engineering",
    "general", "git-ops", "mihaiserban.dev", "research",
]


def load_json(path: Path) -> dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def detect_model() -> str:
    env_model = os.environ.get("OPENCODE_MODEL")
    if env_model:
        return env_model
    return "gateway/planner"


def detect_grader_model() -> str:
    return os.environ.get("OPENCODE_GRADER_MODEL", "gateway/coder")


def discover_skills() -> list[Path]:
    skills = []
    for prefix in SKILL_SCAN_PREFIXES:
        scan_dir = REPO_ROOT / prefix
        if not scan_dir.is_dir():
            continue
        if (scan_dir / "SKILL.md").exists() and (scan_dir / "evals" / "evals.json").exists():
            skills.append(scan_dir)
        for skill_dir in sorted(scan_dir.iterdir()):
            if not skill_dir.is_dir():
                continue
            if skill_dir.name.startswith("."):
                continue
            if (skill_dir / "SKILL.md").exists() and (skill_dir / "evals" / "evals.json").exists():
                skills.append(skill_dir)
    return skills


def next_iteration(skill_dir: Path) -> int:
    results = skill_dir / "eval-results"
    if not results.exists():
        return 1
    existing = sorted(
        int(d.name.split("-")[1])
        for d in results.iterdir()
        if d.is_dir() and d.name.startswith("iteration-")
    )
    return (existing[-1] + 1) if existing else 1


def read_skill_md(skill_dir: Path) -> str:
    path = skill_dir / "SKILL.md"
    if not path.exists():
        sys.exit(f"SKILL.md not found at {path}")
    return path.read_text(encoding="utf-8")


def resolve_eval_files(skill_dir: Path, eval_case: dict) -> list[Path]:
    files = []
    for fname in eval_case.get("files", []):
        fpath = (skill_dir / "evals" / fname).resolve()
        if not fpath.exists():
            sys.stderr.write(f"warning: eval file not found: {fpath}\n")
            continue
        files.append(fpath)
    return files


def build_prompt(eval_case: dict, skill_content: str | None) -> str:
    prompt = eval_case["prompt"]
    if skill_content is None:
        return prompt
    return skill_content + "\n\n---\n\nTask:\n" + prompt


def make_sandbox(skill_dir: Path, iter_label: str) -> Path:
    d = skill_dir / "eval-results" / iter_label / "_sandbox"
    d.mkdir(parents=True, exist_ok=True)
    if not (d / ".git").exists():
        subprocess.run(["git", "init", "-q"], cwd=d, capture_output=True)
        subprocess.run(["git", "config", "user.email", "eval@test.com"], cwd=d, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Eval"], cwd=d, capture_output=True)
    return d


def run_pi(
    prompt: str,
    model: str,
    workdir: Path,
    output_dir: Path,
    skill_paths: list[Path] | None = None,
    timeout: int = 600,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    prompt_file = output_dir / "prompt.txt"
    prompt_file.write_text(prompt, encoding="utf-8")

    cmd = [
        "pi",
        "--no-skills",
        "--no-extensions",
        "-e", GATEWAY_EXTENSION,
        "--no-context-files",
        "--no-session",
        "--model", model,
        "-p", prompt,
    ]
    if skill_paths:
        for sp in skill_paths:
            cmd.extend(["--skill", str(sp)])

    start = time.monotonic()
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(workdir),
        )
        elapsed_ms = int((time.monotonic() - start) * 1000)
        result: dict[str, Any] = {"exit_code": proc.returncode, "duration_ms": elapsed_ms}
        if proc.stdout.strip():
            result["output"] = proc.stdout.strip()
        if proc.stderr.strip():
            result["stderr"] = proc.stderr.strip()
    except subprocess.TimeoutExpired:
        elapsed_ms = int((time.monotonic() - start) * 1000)
        result = {"exit_code": -1, "duration_ms": elapsed_ms, "output": "", "stderr": "TIMEOUT"}
    except Exception as e:
        elapsed_ms = int((time.monotonic() - start) * 1000)
        result = {"exit_code": -2, "duration_ms": elapsed_ms, "output": "", "stderr": str(e)}

    result_file = output_dir / "raw_result.json"
    save_json(result_file, result)
    return result


def build_run_specs(
    skill_dir: Path,
    model: str,
    iter_label: str,
    timeout: int,
) -> list[dict]:
    evals_data = load_json(skill_dir / "evals" / "evals.json")
    skill_md_path = skill_dir / "SKILL.md"

    # Resolve skill dependencies
    dep_paths: list[Path] = []
    for dep in evals_data.get("skill_deps", []):
        dep_path = (REPO_ROOT / dep).resolve()
        if dep_path.exists():
            dep_paths.append(dep_path)
        else:
            sys.stderr.write(f"warning: skill dep not found: {dep_path}\n")

    with_skill_paths = [skill_md_path] + dep_paths

    specs = []
    for case in evals_data["evals"]:
        evalfiles = resolve_eval_files(skill_dir, case)
        workdir = skill_dir / "eval-results" / iter_label / case["name"]

        specs.append({
            "label": f"{skill_dir.name}/{case['name']}/with_skill",
            "prompt": build_prompt(case, read_skill_md(skill_dir)),
            "model": model,
            "output_dir": workdir / "with_skill" / "outputs",
            "skill_paths": with_skill_paths,
            "timeout": timeout,
            "skill_dir": skill_dir,
            "iter_label": iter_label,
        })
        specs.append({
            "label": f"{skill_dir.name}/{case['name']}/without_skill",
            "prompt": build_prompt(case, None),
            "model": model,
            "output_dir": workdir / "without_skill" / "outputs",
            "skill_paths": None,
            "timeout": timeout,
            "skill_dir": skill_dir,
            "iter_label": iter_label,
        })
    return specs


def run_all(all_specs: list[dict], max_workers: int) -> list[dict]:
    total = len(all_specs)
    completed = 0
    results = []

    print(f"\n=== Running {total} eval cases across {max_workers} workers ===\n")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {}
        for spec in all_specs:
            sandbox = make_sandbox(spec["skill_dir"], spec["iter_label"])
            future = executor.submit(
                run_pi,
                spec["prompt"],
                spec["model"],
                sandbox,
                spec["output_dir"],
                spec["skill_paths"],
                spec["timeout"],
            )
            futures[future] = spec

        for future in as_completed(futures):
            spec = futures[future]
            completed += 1
            try:
                res = future.result()
                results.append({"label": spec["label"], "result": res})
                status = "OK" if res["exit_code"] == 0 else f"ERR({res['exit_code']})"
                extra = ""
                if not res.get("output"):
                    extra = " [no output]"
                print(f"  [{completed}/{total}] {spec['label']}: {status} ({res['duration_ms']}ms){extra}")
            except Exception as e:
                results.append({"label": spec["label"], "result": {"exit_code": -3, "stderr": str(e)}})
                print(f"  [{completed}/{total}] {spec['label']}: FAILED ({e})")

    return results


def main() -> None:
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return

    all_mode = "--all" in args
    args = [a for a in args if a != "--all"]

    iterations = 1
    timeout = DEFAULT_TIMEOUT
    max_workers = DEFAULT_PARALLEL

    positional = []
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--iterations" and i + 1 < len(args):
            iterations = int(args[i + 1])
            i += 2
        elif a == "--timeout" and i + 1 < len(args):
            timeout = int(args[i + 1])
            i += 2
        elif a == "--parallel" and i + 1 < len(args):
            max_workers = int(args[i + 1])
            i += 2
        elif not a.startswith("-"):
            positional.append(a)
            i += 1
        else:
            sys.stderr.write(f"unknown flag: {a}\n")
            i += 1

    if all_mode:
        skill_dirs = discover_skills()
        if not skill_dirs:
            sys.exit("No skills found with evals/evals.json. Create evals first.")
    elif positional:
        skill_dirs = [Path(p).resolve() for p in positional]
    else:
        print(__doc__)
        return

    model = detect_model()

    all_specs = []
    skill_names = []
    for skill_dir in skill_dirs:
        if not skill_dir.is_dir():
            sys.stderr.write(f"skipping: not a directory: {skill_dir}\n")
            continue
        if not (skill_dir / "evals" / "evals.json").exists():
            sys.stderr.write(f"skipping: no evals/evals.json in {skill_dir.name}\n")
            continue
        iteration = next_iteration(skill_dir)
        iter_label = f"iteration-{iteration}"
        all_specs.extend(build_run_specs(skill_dir, model, iter_label, timeout))
        n_evals = len(load_json(skill_dir / "evals" / "evals.json")["evals"])
        skill_names.append(f"{skill_dir.name} ({n_evals} evals)")
        print(f"Queued: {skill_dir.name} ({n_evals} evals) → {iter_label}")

    if not all_specs:
        sys.exit("Nothing to run.")

    print(f"\nModel: {model}")
    print(f"Skills: {', '.join(skill_names)}")
    print(f"Workers: {max_workers}, Timeout: {timeout}s")

    print("\nIsolating global skills...")
    isolate_global_skills()

    try:
        run_all(all_specs, max_workers)
    finally:
        print("\nRestoring global skills...")
        restore_global_skills()

    print(f"\nDone. {len(all_specs)} runs across {len(skill_dirs)} skill(s).")
    print("Run eval-grade.py and eval-aggregate.py to complete the pipeline.")


if __name__ == "__main__":
    main()