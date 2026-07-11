#!/usr/bin/env python3
"""Grade eval outputs against assertions and deterministic graders.

Usage:
    eval-grade.py <skill-path> [--iteration N] [--parallel P] [--model M]
    eval-grade.py --all [--iteration N] [--parallel P] [--model M]

Supports two grader types:
    1. assertions (LLM-graded) — existing, backward compatible
    2. graders (deterministic + llm_rubric) — new, weighted combination

Deterministic graders run a script in the eval's output directory.
The script outputs JSON: {"score": 0.67, "details": "...", "checks": [...]}
LLM rubric graders evaluate the output against qualitative criteria.

When both assertions and graders are present, graders take precedence.
Default grader model is gateway/coder. Use --model to override.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_GRADER_MODEL = "gateway/coder"
DEFAULT_PARALLEL = 8

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


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def discover_skills() -> list[Path]:
    skills = []
    for prefix in SKILL_SCAN_PREFIXES:
        scan_dir = REPO_ROOT / prefix
        if not scan_dir.is_dir():
            continue
        if (scan_dir / "SKILL.md").exists() and (scan_dir / "eval-results").exists():
            skills.append(scan_dir)
        for skill_dir in sorted(scan_dir.iterdir()):
            if not skill_dir.is_dir() or skill_dir.name.startswith("."):
                continue
            if (skill_dir / "SKILL.md").exists() and (skill_dir / "eval-results").exists():
                skills.append(skill_dir)
    return skills


def latest_iteration(skill_dir: Path) -> int | None:
    results = skill_dir / "eval-results"
    if not results.exists():
        return None
    existing = sorted(
        int(d.name.split("-")[1])
        for d in results.iterdir()
        if d.is_dir() and d.name.startswith("iteration-")
    )
    return existing[-1] if existing else None


def find_outputs(run_dir: Path) -> str:
    raw = run_dir / "raw_result.json"
    has_raw = raw.exists()
    if has_raw:
        data = load_json(raw)
        if data.get("exit_code", 0) != 0:
            return "OPENCODE_RUN_FAILED"
        text_output = data.get("output", "")
        if isinstance(text_output, str) and len(text_output) > 20:
            return text_output
    candidates = []
    for f in run_dir.rglob("*"):
        if f.is_file() and f.name not in ("prompt.txt", "raw_result.json"):
            candidates.append(f)
    if candidates:
        return "\n\n".join(read_text(c) for c in sorted(candidates))
    if has_raw:
        return data.get("output", "")
    return ""


def heuristic_grade(assertion: dict, output: str) -> tuple[bool | None, str]:
    aid = assertion["id"]
    text = assertion["text"].lower()

    if aid == "max-depth-2" or "no nesting" in text or "deeper than" in text:
        return check_nesting_depth(output)
    if "guard clauses" in text or "early return" in text or "inverted" in text:
        return check_guard_clauses(output)
    if "flags" in text.lower() or "catch" in text.lower() or "detect" in text.lower():
        return check_flag(output, assertion["text"])

    return None, ""


def check_nesting_depth(output: str) -> tuple[bool, str]:
    max_depth = 0
    for line in output.splitlines():
        stripped = line.rstrip()
        if stripped:
            depth = (len(line) - len(line.lstrip())) // 2
            max_depth = max(max_depth, depth)
    passed = max_depth <= 2
    return passed, f"max indent depth: {max_depth} levels (threshold: 2)"


def check_guard_clauses(output: str) -> tuple[bool, str]:
    lines = output.strip().splitlines()
    if not lines:
        return False, "empty output"
    first_10 = lines[:10]
    early_return = any(
        "return" in line and ("if" in line.lower() and "!" in line or "if not" in line.lower())
        for line in first_10
    )
    return_pattern = any("return" in line for line in first_10)
    return early_return or return_pattern, f"early return pattern {'found' if early_return or return_pattern else 'not found'}"


def check_flag(output: str, assertion_text: str) -> tuple[bool, str]:
    m = re.search(r"Flags\s+(.+)", assertion_text)
    if not m:
        return None, ""
    flagged = m.group(1).lower().rstrip(".")
    output_lower = output.lower()
    passed = flagged in output_lower
    return passed, f"'{flagged}' {'found' if passed else 'not found'} in output"


def batch_llm_grade(
    assertions: list[dict],
    output: str,
    grader_model: str,
    workdir: Path,
) -> list[tuple[bool, str]]:
    if not assertions:
        return []

    lines = ["Grade each assertion below against the model output."]
    lines.append("For each assertion, reply with EXACTLY one line:")
    lines.append('"N. PASS: brief reason" or "N. FAIL: brief reason"')
    lines.append("Do NOT use markdown formatting. Plain text only.")
    lines.append("")
    lines.append("<model_output>")
    lines.append(output[:10000])
    lines.append("</model_output>")
    lines.append("")
    lines.append("Assertions:")
    for i, a in enumerate(assertions, 1):
        lines.append(f"{i}. {a['text']}")

    prompt = "\n".join(lines)
    prompt_file = workdir / "grading_prompt.txt"
    prompt_file.write_text(prompt, encoding="utf-8")

    try:
        import tempfile
        grade_workdir = Path(tempfile.mkdtemp(prefix="grade-"))
        gateway_ext = str(Path.home() / ".pi" / "agent" / "extensions" / "gateway")
        proc = subprocess.run(
            ["pi", "--no-skills", "--no-extensions", "-e", gateway_ext,
             "--no-context-files", "--no-session",
             "--model", grader_model, "-p", prompt],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(grade_workdir),
        )
        response = proc.stdout.strip()
        shutil.rmtree(grade_workdir, ignore_errors=True)
    except Exception as e:
        return [(False, f"grader failed: {str(e)[:200]}") for _ in assertions]

    results = []
    for i, assertion in enumerate(assertions, 1):
        num = re.escape(str(i))
        pattern = re.compile(
            rf"^\s*{num}\.\s*\**\s*(PASS|FAIL)\s*\**\s*:?\s*(.*)$",
            re.M | re.I,
        )
        match = pattern.search(response)
        if match:
            verdict = match.group(1).upper()
            reason = match.group(2).strip().strip("*").strip()
            results.append((verdict == "PASS", reason))
        else:
            fallback = re.search(
                rf"\b\**\s*(PASS|FAIL)\s*\**\b.*{re.escape(assertion['text'][:20])}",
                response, re.I,
            )
            if fallback:
                verdict = fallback.group(1).upper().strip("*")
                results.append((verdict == "PASS", "fallback parse: " + response[:200].strip().replace("\n", " ")))
            else:
                results.append((False, "grader did not return numbered verdict; response excerpt: " + response[:300].strip().replace("\n", " ")))

    return results


def run_deterministic_grader(
    grader_config: dict,
    output_dir: Path,
    output: str,
) -> dict[str, Any]:
    run_cmd = grader_config.get("run", "")
    if not run_cmd:
        return {"score": 0.0, "details": "no run command in deterministic grader", "checks": []}

    grader_script = output_dir / "_grader_script.sh"
    grader_script.write_text(run_cmd, encoding="utf-8")
    grader_script.chmod(0o755)

    try:
        proc = subprocess.run(
            ["bash", str(grader_script)],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=str(output_dir),
            input=output,
        )
        grader_output = proc.stdout.strip()
        result = json.loads(grader_output)
        return {
            "score": float(result.get("score", 0.0)),
            "details": result.get("details", ""),
            "checks": result.get("checks", []),
        }
    except subprocess.TimeoutExpired:
        return {"score": 0.0, "details": "deterministic grader timed out (30s)", "checks": []}
    except json.JSONDecodeError:
        return {"score": 0.0, "details": f"grader output not valid JSON: {grader_output[:200]}", "checks": []}
    except Exception as e:
        return {"score": 0.0, "details": f"grader error: {str(e)[:200]}", "checks": []}


def run_llm_rubric_grader(
    grader_config: dict,
    output: str,
    grader_model: str,
    workdir: Path,
) -> dict[str, Any]:
    rubric = grader_config.get("rubric", "")

    rubric_file = workdir / "_rubric.txt"
    rubric_path = Path(rubric)
    if rubric_path.exists():
        rubric = rubric_path.read_text(encoding="utf-8")

    prompt = f"""You are grading a model's output against a rubric. Return a JSON object with "score" (0.0-1.0) and "details" (one sentence).

Rubric:
{rubric}

<model_output>
{output[:10000]}
</model_output>

Return ONLY valid JSON: {{"score": 0.0, "details": "..."}}
"""

    try:
        import tempfile
        grade_workdir = Path(tempfile.mkdtemp(prefix="grade-"))
        gateway_ext = str(Path.home() / ".pi" / "agent" / "extensions" / "gateway")
        proc = subprocess.run(
            ["pi", "--no-skills", "--no-extensions", "-e", gateway_ext,
             "--no-context-files", "--no-session",
             "--model", grader_model, "-p", prompt],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(grade_workdir),
        )
        response = proc.stdout.strip()
        shutil.rmtree(grade_workdir, ignore_errors=True)

        json_match = re.search(r'\{[^{}]*"score"[^{}]*\}', response, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
            return {
                "score": float(result.get("score", 0.0)),
                "details": result.get("details", ""),
            }
        return {"score": 0.0, "details": f"could not parse rubric grade from response: {response[:200]}", "checks": []}
    except Exception as e:
        return {"score": 0.0, "details": f"rubric grader error: {str(e)[:200]}", "checks": []}


def grade_variant(
    eval_case: dict,
    output: str,
    grader_model: str,
    workdir: Path,
    output_dir: Path,
) -> dict[str, Any]:
    if output == "OPENCODE_RUN_FAILED":
        assertions = eval_case.get("assertions", [])
        return {
            "assertion_results": [{"id": a["id"], "text": a["text"], "passed": False,
                                   "evidence": "run failed"} for a in assertions],
            "grader_results": [],
            "weighted_score": 0.0,
        }

    graders = eval_case.get("graders", [])
    assertions = eval_case.get("assertions", [])

    if graders:
        grader_results = []
        for g in graders:
            gtype = g.get("type", "deterministic")
            weight = g.get("weight", 1.0)
            if gtype == "deterministic":
                result = run_deterministic_grader(g, output_dir, output)
            elif gtype == "llm_rubric":
                result = run_llm_rubric_grader(g, output, grader_model, workdir)
            else:
                result = {"score": 0.0, "details": f"unknown grader type: {gtype}", "checks": []}
            result["type"] = gtype
            result["weight"] = weight
            grader_results.append(result)

        total_weight = sum(g["weight"] for g in graders)
        weighted_score = sum(r["score"] * r["weight"] for r in grader_results) / total_weight if total_weight else 0.0

        return {
            "grader_results": grader_results,
            "weighted_score": round(weighted_score, 3),
            "assertion_results": [],
        }

    # Fall back to assertion-based grading (backward compatible)
    results = []
    llm_assertions = []
    for assertion in assertions:
        passed, evidence = heuristic_grade(assertion, output)
        if passed is not None:
            results.append({
                "id": assertion["id"],
                "text": assertion["text"],
                "passed": passed,
                "evidence": evidence,
            })
        else:
            llm_assertions.append(assertion)

    if llm_assertions:
        time.sleep(0.2)
        llm_results = batch_llm_grade(llm_assertions, output, grader_model, workdir)
        for assertion, (passed, evidence) in zip(llm_assertions, llm_results):
            results.append({
                "id": assertion["id"],
                "text": assertion["text"],
                "passed": passed,
                "evidence": evidence,
            })

    results = sorted(results, key=lambda r: r["id"])
    passed_count = sum(1 for r in results if r["passed"])
    total_count = len(results)
    weighted_score = passed_count / total_count if total_count else 0.0

    return {
        "assertion_results": results,
        "grader_results": [],
        "weighted_score": round(weighted_score, 3),
    }


def grade_skill(
    skill_path: Path,
    grader_model: str,
    max_workers: int,
    iteration: int | None = None,
) -> None:
    if iteration is None:
        iteration = latest_iteration(skill_path)
        if iteration is None:
            print(f"  {skill_path.name}: no eval-results, skipping")
            return

    evals_data = load_json(skill_path / "evals" / "evals.json")
    eval_cases = evals_data["evals"]
    it_dir = skill_path / "eval-results" / f"iteration-{iteration}"

    tasks = []
    for case in eval_cases:
        eval_name = case["name"]

        # Check for trial directories
        trial_dirs = []
        for item in sorted(it_dir.iterdir()):
            if item.is_dir() and item.name.startswith("trial-"):
                trial_dirs.append(item)

        if trial_dirs:
            for trial_dir in trial_dirs:
                eval_dir = trial_dir / eval_name
                if not eval_dir.exists():
                    continue
                for variant in ("with_skill", "without_skill"):
                    output_dir = eval_dir / variant / "outputs"
                    output = find_outputs(output_dir)
                    tasks.append({
                        "skill": skill_path.name,
                        "eval": eval_name,
                        "variant": variant,
                        "trial": trial_dir.name,
                        "workdir": eval_dir / variant,
                        "output_dir": output_dir,
                        "eval_case": case,
                        "output": output,
                    })
        else:
            eval_dir = it_dir / eval_name
            for variant in ("with_skill", "without_skill"):
                output_dir = eval_dir / variant / "outputs"
                output = find_outputs(output_dir)
                tasks.append({
                    "skill": skill_path.name,
                    "eval": eval_name,
                    "variant": variant,
                    "trial": None,
                    "workdir": eval_dir / variant,
                    "output_dir": output_dir,
                    "eval_case": case,
                    "output": output,
                })

    total_score = 0.0
    total_count = 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(
                grade_variant,
                t["eval_case"],
                t["output"],
                grader_model,
                t["workdir"],
                t["output_dir"],
            ): t for t in tasks
        }

        for future in as_completed(futures):
            t = futures[future]
            try:
                result = future.result()
                save_json(t["workdir"] / "grading.json", result)
                score = result["weighted_score"]
                total_score += score
                total_count += 1
            except Exception as e:
                sys.stderr.write(f"grading failed for {t['skill']}/{t['eval']}/{t['variant']}: {e}\n")

    avg_score = total_score / total_count if total_count else 0.0
    print(f"  {skill_path.name}: avg score {avg_score:.1%} ({total_count} variants)")


def main() -> None:
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return

    all_mode = "--all" in args
    args = [a for a in args if a != "--all"]

    iteration = None
    max_workers = DEFAULT_PARALLEL
    grader_model = os.environ.get("OPENCODE_GRADER_MODEL", DEFAULT_GRADER_MODEL)
    positional = []

    i = 0
    while i < len(args):
        a = args[i]
        if a == "--iteration" and i + 1 < len(args):
            iteration = int(args[i + 1])
            i += 2
        elif a == "--parallel" and i + 1 < len(args):
            max_workers = int(args[i + 1])
            i += 2
        elif a == "--model" and i + 1 < len(args):
            grader_model = args[i + 1]
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
            sys.exit("No skills found with eval-results. Run eval-runner.py first.")
        print(f"Grading {len(skill_dirs)} skill(s) with {grader_model} ({max_workers} workers)")
        for sd in skill_dirs:
            grade_skill(sd, grader_model, max_workers, iteration)
    elif positional:
        for p in positional:
            skill_path = Path(p).resolve()
            print(f"Grading {skill_path.name} with {grader_model} ({max_workers} workers)")
            grade_skill(skill_path, grader_model, max_workers, iteration)
    else:
        print(__doc__)
        return

    print("\nGrading complete. Run eval-aggregate.py to produce benchmarks.")


if __name__ == "__main__":
    main()