#!/usr/bin/env python3
"""Aggregate grading results into a benchmark.

Usage:
    eval-aggregate.py <skill-path> [--iteration N] [--output html]
    eval-aggregate.py --all [--output html]
    eval-aggregate.py --all --ci --threshold 0.8

Reads grading.json files from eval-results/iteration-N/ and produces
benchmark.json, benchmark.md, and optionally review.html.
With --ci, exits non-zero if overall pass rate falls below --threshold.
"""
import json
import math
import statistics
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent

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


def get_score_from_grading(grading: Any) -> tuple[float, int, int, list[dict]]:
    """Extract score, passed count, total count, and assertions from grading.json.

    Handles both new format (weighted_score + grader_results) and
    old format (list of assertion results).
    """
    if isinstance(grading, list):
        # Old format: list of assertion results
        passed = sum(1 for g in grading if g.get("passed") is True)
        total = sum(1 for g in grading if g.get("passed") is not None)
        score = passed / total if total else 0.0
        return score, passed, total, grading

    # New format: dict with weighted_score, assertion_results, grader_results
    if isinstance(grading, dict):
        if grading.get("grader_results"):
            # Weighted grader format
            score = grading.get("weighted_score", 0.0)
            grader_results = grading.get("grader_results", [])
            passed = sum(1 for g in grader_results if g.get("score", 0) >= 0.5)
            total = len(grader_results)
            return score, passed, total, grader_results
        else:
            # Assertion-based format in new structure
            assertions = grading.get("assertion_results", [])
            passed = sum(1 for a in assertions if a.get("passed") is True)
            total = sum(1 for a in assertions if a.get("passed") is not None)
            score = passed / total if total else 0.0
            return score, passed, total, assertions

    return 0.0, 0, 0, []


def aggregate(skill_dir: Path, iteration: int) -> dict[str, Any]:
    it_dir = skill_dir / "eval-results" / f"iteration-{iteration}"
    evals_data = load_json(skill_dir / "evals" / "evals.json")

    with_scores: list[float] = []
    without_scores: list[float] = []
    with_times: list[int] = []
    without_times: list[int] = []
    eval_results = []

    for case in evals_data["evals"]:
        eval_name = case["name"]
        e_result = {"name": eval_name, "with_skill": {}, "without_skill": {}}

        for variant in ("with_skill", "without_skill"):
            # Handle trial directories
            trial_dir = it_dir / "trial-1" / eval_name
            if trial_dir.exists():
                grading_file = trial_dir / variant / "grading.json"
                timing_file = trial_dir / variant / "outputs" / "raw_result.json"
            else:
                grading_file = it_dir / eval_name / variant / "grading.json"
                timing_file = it_dir / eval_name / variant / "outputs" / "raw_result.json"

            grading = load_json(grading_file) if grading_file.exists() else []
            score, passed, total, details = get_score_from_grading(grading)

            if variant == "with_skill":
                with_scores.append(score)
            else:
                without_scores.append(score)

            e_result[variant]["score"] = round(score, 3)
            e_result[variant]["passed"] = passed
            e_result[variant]["total"] = total
            e_result[variant]["details"] = details

            timing = load_json(timing_file) if timing_file.exists() else {}
            dur = timing.get("duration_ms", 0)
            if variant == "with_skill":
                with_times.append(dur)
            else:
                without_times.append(dur)
            e_result[variant]["duration_ms"] = dur

        eval_results.append(e_result)

    with_rate = statistics.mean(with_scores) if with_scores else 0.0
    without_rate = statistics.mean(without_scores) if without_scores else 0.0
    with_std = statistics.stdev(with_scores) if len(with_scores) > 1 else 0.0
    without_std = statistics.stdev(without_scores) if len(without_scores) > 1 else 0.0

    # pass_at_k: probability of >=1 success in k trials = 1 - (1-p)^k
    k = len(with_scores)
    pass_at_k_with = 1 - math.pow(1 - with_rate, k) if k > 0 and with_rate < 1 else (1.0 if with_rate >= 1 else 0.0)
    pass_at_k_without = 1 - math.pow(1 - without_rate, k) if k > 0 and without_rate < 1 else (1.0 if without_rate >= 1 else 0.0)

    benchmark = {
        "skill_name": evals_data["skill_name"],
        "iteration": iteration,
        "num_evals": len(evals_data["evals"]),
        "num_trials": k,
        "summary": {
            "with_skill": {
                "pass_rate": round(with_rate, 3),
                "stddev": round(with_std, 3),
                "pass_at_k": round(pass_at_k_with, 3),
                "mean_duration_ms": int(statistics.mean(with_times)) if with_times else 0,
            },
            "without_skill": {
                "pass_rate": round(without_rate, 3),
                "stddev": round(without_std, 3),
                "pass_at_k": round(pass_at_k_without, 3),
                "mean_duration_ms": int(statistics.mean(without_times)) if without_times else 0,
            },
            "delta_pass_rate": round(with_rate - without_rate, 3),
            "delta_pass_at_k": round(pass_at_k_with - pass_at_k_without, 3),
            "delta_duration_ms": int(statistics.mean(with_times) - statistics.mean(without_times)) if with_times and without_times else 0,
        },
        "evals": eval_results,
    }

    save_json(it_dir / "benchmark.json", benchmark)
    return benchmark


def generate_markdown(benchmark: dict, it_dir: Path) -> None:
    s = benchmark["summary"]
    k = benchmark.get("num_trials", 1)
    md = f"""# Benchmark: {benchmark['skill_name']} (iteration {benchmark['iteration']})

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|-----------|---------------|-------|
| Pass rate | {s['with_skill']['pass_rate']:.0%} ±{s['with_skill'].get('stddev', 0):.0%} | {s['without_skill']['pass_rate']:.0%} ±{s['without_skill'].get('stddev', 0):.0%} | {s['delta_pass_rate']:+.0%} |
| pass@{k} | {s['with_skill'].get('pass_at_k', 0):.0%} | {s['without_skill'].get('pass_at_k', 0):.0%} | {s.get('delta_pass_at_k', 0):+.0%} |
| Mean duration | {s['with_skill']['mean_duration_ms']:,}ms | {s['without_skill']['mean_duration_ms']:,}ms | {s['delta_duration_ms']:+,}ms |

## Per-Eval Breakdown

"""
    for e in benchmark["evals"]:
        wp = e["with_skill"]
        wo = e["without_skill"]
        md += f"""### {e['name']}

| Variant | Score | Duration |
|---------|-------|----------|
| With skill | {wp.get('score', 0):.0%} | {wp.get('duration_ms', 0)}ms |
| Without skill | {wo.get('score', 0):.0%} | {wo.get('duration_ms', 0)}ms |

"""
    (it_dir / "benchmark.md").write_text(md, encoding="utf-8")


def generate_html(benchmark: dict, it_dir: Path, skill_path: Path) -> None:
    template_path = REPO_ROOT / "general" / "skill-eval-runner" / "references" / "review.html"
    if not template_path.exists():
        sys.stderr.write("review.html template not found, skipping HTML generation\n")
        return

    template = template_path.read_text(encoding="utf-8")

    evals_json = json.dumps(benchmark["evals"], indent=2)
    summary_json = json.dumps(benchmark["summary"], indent=2)

    html = template.replace(
        "__BENCHMARK_DATA_PLACEHOLDER__",
        f"const BENCHMARK = {{summary: {summary_json}, evals: {evals_json}}};",
    )

    eval_outputs = {}
    for i, e in enumerate(benchmark["evals"]):
        eval_dir = it_dir / e["name"]
        outputs = {}
        for variant in ("with_skill", "without_skill"):
            out_dir = eval_dir / variant / "outputs"
            text = ""
            for f in sorted(out_dir.rglob("*")):
                if f.is_file() and f.name not in ("prompt.txt", "raw_result.json"):
                    text += f"\n\n=== {f.name} ===\n\n" + read_text(f)
            if not text:
                raw = load_json(out_dir / "raw_result.json") if (out_dir / "raw_result.json").exists() else {}
                text = str(raw.get("output", ""))
            outputs[variant] = text
        eval_outputs[e["name"]] = outputs

    html = html.replace(
        "__EVAL_OUTPUTS_PLACEHOLDER__",
        f"const EVAL_OUTPUTS = {json.dumps(eval_outputs)};",
    )

    evals_data = load_json(skill_path / "evals" / "evals.json")
    prompts = {e["name"]: e["prompt"] for e in evals_data["evals"]}
    html = html.replace(
        "__EVAL_PROMPTS_PLACEHOLDER__",
        f"const EVAL_PROMPTS = {json.dumps(prompts)};",
    )

    (it_dir / "review.html").write_text(html, encoding="utf-8")


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


def aggregate_skill(skill_path: Path, iteration: int | None = None, output_html: bool = False) -> dict | None:
    if iteration is None:
        iteration = latest_iteration(skill_path)
        if iteration is None:
            print(f"  {skill_path.name}: no eval-results, skipping")
            return None

    benchmark = aggregate(skill_path, iteration)
    it_dir = skill_path / "eval-results" / f"iteration-{iteration}"

    generate_markdown(benchmark, it_dir)
    if output_html:
        generate_html(benchmark, it_dir, skill_path)

    s = benchmark["summary"]
    print(f"  {skill_path.name}: with={s['with_skill']['pass_rate']:.0%} without={s['without_skill']['pass_rate']:.0%} delta={s['delta_pass_rate']:+.0%}")
    return benchmark


def main() -> None:
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return

    all_mode = "--all" in args
    args = [a for a in args if a != "--all"]

    ci_mode = "--ci" in args
    args = [a for a in args if a != "--ci"]

    threshold = 0.8
    iteration = None
    output_html = False
    positional = []

    i = 0
    while i < len(args):
        a = args[i]
        if a == "--iteration" and i + 1 < len(args):
            iteration = int(args[i + 1])
            i += 2
        elif a == "--threshold" and i + 1 < len(args):
            threshold = float(args[i + 1])
            i += 2
        elif a == "--output" and i + 1 < len(args) and args[i + 1] == "html":
            output_html = True
            i += 2
        elif not a.startswith("-"):
            positional.append(a)
            i += 1
        else:
            i += 1

    all_benchmarks = []

    if all_mode:
        skill_dirs = discover_skills()
        if not skill_dirs:
            sys.exit("No skills found with eval-results. Run eval-runner.py first.")
        print(f"Aggregating {len(skill_dirs)} skill(s)")
        for sd in skill_dirs:
            bm = aggregate_skill(sd, iteration, output_html)
            if bm:
                all_benchmarks.append(bm)
    elif positional:
        for p in positional:
            skill_path = Path(p).resolve()
            bm = aggregate_skill(skill_path, iteration, output_html)
            if bm:
                all_benchmarks.append(bm)
    else:
        print(__doc__)
        return

    print(f"\nAggregation complete.")

    if ci_mode and all_benchmarks:
        below = []
        for bm in all_benchmarks:
            rate = bm["summary"]["with_skill"]["pass_rate"]
            if rate < threshold:
                below.append((bm["skill_name"], rate))
        if below:
            print(f"\nCI FAIL: {len(below)} skill(s) below threshold {threshold:.0%}:")
            for name, rate in below:
                print(f"  {name}: {rate:.0%}")
            sys.exit(1)
        else:
            print(f"\nCI PASS: all skills above threshold {threshold:.0%}")


if __name__ == "__main__":
    main()
