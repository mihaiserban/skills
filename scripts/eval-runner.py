#!/usr/bin/env python3
"""Run skill evals in parallel: with-skill vs without-skill.

Usage:
    eval-runner.py <skill-path>... [--iterations N] [--timeout SECS] [--parallel P] [--trials N] [--provider docker|local]
    eval-runner.py --all [--iterations N] [--timeout SECS] [--parallel P] [--trials N] [--provider docker|local]

    --all           Discover and run all skills under engineering/, general/,
                    design/, etc. that have evals/evals.json.
    --parallel P    Max concurrent pi processes (default: 4).
    --timeout SECS  Per-process timeout (default: 600).
    --trials N      Run each eval N times for variance estimation.
    --smoke         5 trials (quick capability check).
    --reliable      15 trials (reliable pass rate estimate).
    --regression    30 trials (high-confidence regression detection).
    --provider      Execution provider: local (default) or docker.
                    docker: each eval runs in a fresh container with pi
                    installed, no host filesystem access, no global skills.
                    local: runs pi on the host with global skill dir isolation.

Uses pi as the eval harness with full skill isolation:
    - Docker: fresh container per run, no global skills, no host FS access
    - Local: --no-skills + global dir moving + --skill <path> for isolation
    - --skill <path> loads ONLY the tested skill for with_skill variant
    - --no-context-files --no-session prevents context/session contamination
"""
import atexit
import json
import os
import shutil
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
PI_AUTH_FILE = str(Path.home() / ".pi" / "agent" / "auth.json")
DOCKER_IMAGE_TAG = "eval-pi-runner"

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


def build_docker_image() -> bool:
    """Build the eval Docker image with pi + gateway extension. Returns True on success."""
    import tempfile
    import textwrap

    gateway_dir = Path(GATEWAY_EXTENSION)
    auth_file = Path(PI_AUTH_FILE)
    if not gateway_dir.exists():
        sys.stderr.write(f"error: gateway extension not found at {gateway_dir}\n")
        return False
    if not auth_file.exists():
        sys.stderr.write(f"error: pi auth.json not found at {auth_file}\n")
        return False

    build_ctx = Path(tempfile.mkdtemp(prefix="eval-docker-"))
    try:
        # Copy gateway extension and auth into build context
        shutil.copytree(gateway_dir, build_ctx / "gateway")
        shutil.copy2(auth_file, build_ctx / "auth.json")

        dockerfile = textwrap.dedent("""\
            FROM node:20-slim
            RUN apt-get update -qq && apt-get install -y -qq git python3 > /dev/null 2>&1 && rm -rf /var/lib/apt/lists/*
            RUN npm install -g --ignore-scripts @earendil-works/pi-coding-agent
            RUN mkdir -p /root/.pi/agent/extensions /root/.pi/agent/skills
            COPY gateway /root/.pi/agent/extensions/gateway
            COPY auth.json /root/.pi/agent/auth.json
            ENV PI_OFFLINE=1
            ENV PI_SKIP_VERSION_CHECK=1
            WORKDIR /workspace
            ENTRYPOINT ["pi"]
        """)
        (build_ctx / "Dockerfile").write_text(dockerfile, encoding="utf-8")

        print("  Building Docker image (this happens once)...")
        proc = subprocess.run(
            ["docker", "build", "-t", DOCKER_IMAGE_TAG, str(build_ctx)],
            capture_output=True, text=True, timeout=300,
        )
        if proc.returncode != 0:
            sys.stderr.write(f"docker build failed: {proc.stderr[:500]}\n")
            return False
        print(f"  Image built: {DOCKER_IMAGE_TAG}")
        return True
    finally:
        shutil.rmtree(build_ctx, ignore_errors=True)


def run_pi_docker(
    prompt: str,
    model: str,
    output_dir: Path,
    skill_paths: list[Path] | None,
    eval_files: list[Path],
    timeout: int = 600,
) -> dict[str, Any]:
    """Run pi inside a Docker container with full isolation."""
    output_dir.mkdir(parents=True, exist_ok=True)
    prompt_file = output_dir / "prompt.txt"
    prompt_file.write_text(prompt, encoding="utf-8")

    cmd = [
        "docker", "run", "--rm",
        "-v", f"{output_dir.resolve()}:/output",
    ]

    # Mount skill files read-only
    if skill_paths:
        for i, sp in enumerate(skill_paths):
            mount = f"{sp.resolve()}:/skills/skill-{i}/SKILL.md:ro"
            cmd.extend(["-v", mount])

    # Mount eval fixture files read-only
    for i, ef in enumerate(eval_files):
        mount = f"{ef.resolve()}:/fixtures/file-{i}/{ef.name}:ro"
        cmd.extend(["-v", mount])

    # Build the pi command that runs inside the container
    pi_cmd = [
        "--no-skills", "--no-extensions",
        "-e", "/root/.pi/agent/extensions/gateway",
        "--no-context-files", "--no-session",
        "--model", model,
        "-p", prompt,
    ]
    if skill_paths:
        for i in range(len(skill_paths)):
            pi_cmd.extend(["--skill", f"/skills/skill-{i}/SKILL.md"])

    cmd.append(DOCKER_IMAGE_TAG)
    cmd.extend(pi_cmd)

    start = time.monotonic()
    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout,
        )
        elapsed_ms = int((time.monotonic() - start) * 1000)
        result: dict[str, Any] = {"exit_code": proc.returncode, "duration_ms": elapsed_ms}
        if proc.stdout.strip():
            result["output"] = proc.stdout.strip()
        if proc.stderr.strip():
            result["stderr"] = proc.stderr.strip()[:3000]
    except subprocess.TimeoutExpired:
        elapsed_ms = int((time.monotonic() - start) * 1000)
        result = {"exit_code": -1, "duration_ms": elapsed_ms, "output": "", "stderr": "TIMEOUT"}
    except Exception as e:
        elapsed_ms = int((time.monotonic() - start) * 1000)
        result = {"exit_code": -2, "duration_ms": elapsed_ms, "output": "", "stderr": str(e)[:2000]}

    result_file = output_dir / "raw_result.json"
    save_json(result_file, result)
    return result


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
    trials: int = 1,
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
        for trial in range(1, trials + 1):
            trial_prefix = f"trial-{trial}/" if trials > 1 else ""
            workdir = skill_dir / "eval-results" / iter_label / f"{trial_prefix}{case['name']}"

            specs.append({
                "label": f"{skill_dir.name}/{case['name']}/with_skill{f'/trial-{trial}' if trials > 1 else ''}",
                "prompt": build_prompt(case, read_skill_md(skill_dir)),
                "model": model,
                "output_dir": workdir / "with_skill" / "outputs",
                "skill_paths": with_skill_paths,
                "eval_files": evalfiles,
                "timeout": timeout,
                "skill_dir": skill_dir,
                "iter_label": iter_label,
            })
            specs.append({
                "label": f"{skill_dir.name}/{case['name']}/without_skill{f'/trial-{trial}' if trials > 1 else ''}",
                "prompt": build_prompt(case, None),
                "model": model,
                "output_dir": workdir / "without_skill" / "outputs",
                "skill_paths": None,
                "eval_files": evalfiles,
                "timeout": timeout,
                "skill_dir": skill_dir,
                "iter_label": iter_label,
            })
    return specs


def run_all(all_specs: list[dict], max_workers: int, provider: str = "local") -> list[dict]:
    total = len(all_specs)
    completed = 0
    results = []

    print(f"\n=== Running {total} eval cases across {max_workers} workers ({provider}) ===\n")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {}
        for spec in all_specs:
            if provider == "docker":
                future = executor.submit(
                    run_pi_docker,
                    spec["prompt"],
                    spec["model"],
                    spec["output_dir"],
                    spec["skill_paths"],
                    spec.get("eval_files", []),
                    spec["timeout"],
                )
            else:
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

    # Trial presets
    trials = 1
    if "--smoke" in args:
        trials = 5
        args = [a for a in args if a != "--smoke"]
    elif "--reliable" in args:
        trials = 15
        args = [a for a in args if a != "--reliable"]
    elif "--regression" in args:
        trials = 30
        args = [a for a in args if a != "--regression"]

    iterations = 1
    timeout = DEFAULT_TIMEOUT
    max_workers = DEFAULT_PARALLEL
    provider = "local"

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
        elif a == "--trials" and i + 1 < len(args):
            trials = int(args[i + 1])
            i += 2
        elif a == "--provider" and i + 1 < len(args):
            provider = args[i + 1]
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
        all_specs.extend(build_run_specs(skill_dir, model, iter_label, timeout, trials))
        n_evals = len(load_json(skill_dir / "evals" / "evals.json")["evals"])
        skill_names.append(f"{skill_dir.name} ({n_evals} evals)")
        print(f"Queued: {skill_dir.name} ({n_evals} evals) → {iter_label}")

    if not all_specs:
        sys.exit("Nothing to run.")

    print(f"\nModel: {model}")
    print(f"Skills: {', '.join(skill_names)}")
    print(f"Workers: {max_workers}, Timeout: {timeout}s, Trials: {trials}, Provider: {provider}")

    if provider == "docker":
        if not build_docker_image():
            sys.exit("Docker image build failed. Falling back: use --provider=local")
        # Docker containers have no global skill dirs — no isolation needed
        run_all(all_specs, max_workers, provider="docker")
    else:
        print("\nIsolating global skills...")
        isolate_global_skills()
        try:
            run_all(all_specs, max_workers, provider="local")
        finally:
            print("\nRestoring global skills...")
            restore_global_skills()

    print(f"\nDone. {len(all_specs)} runs across {len(skill_dirs)} skill(s).")
    print("Run eval-grade.py and eval-aggregate.py to complete the pipeline.")


if __name__ == "__main__":
    main()