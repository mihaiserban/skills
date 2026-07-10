---
name: skill-eval-runner
description: Run runtime evals on a skill to measure whether it actually improves agent behavior. Use when the user asks to run evals, evaluate a skill's effectiveness, benchmark a skill, or measure skill impact. Also use to iterate on a skill after making changes — rerun evals to see if pass rates improved.
---

# Skill Eval Runner

Measure a skill's impact by running the same task with and without the
skill, grading outputs against defined assertions, and aggregating
results into a benchmark. Complements `/skill-evaluation` (static
SKILL.md audit) with runtime measurement.

Read `references/review.html` for the output template.

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `target` | Path to skill directory with `evals/evals.json` | Ask user |
| `iterations` | Number of eval runs per case (for variance) | 1 |

## Workflow

### 1. Load evals

Read `<target>/evals/evals.json`. If it doesn't exist, tell the user
and offer to create example evals. The schema:

```json
{
  "skill_name": "...",
  "evals": [
    {
      "id": 1,
      "name": "descriptive-name",
      "prompt": "Realistic user task prompt",
      "files": ["fixtures/file.ts"],
      "assertions": [
        {"id": "unique-id", "text": "What to check", "type": "quality|format|behavior"}
      ]
    }
  ]
}
```

### 2. Determine iteration

New iteration every run. Check `<target>/eval-results/`:
if `iteration-1/` exists, use `iteration-2/`, etc. Create the iteration
directory. Run all evals in this order:

### 3. Run evals in parallel

For each eval case, spawn **two `task` subagents in the same turn**:

**With-skill worker:**
```
Execute this task:
- Skill: <full SKILL.md content>
- Task: <eval prompt>
- Input files: <eval files, or "none">
- Save your final output to: <target>/eval-results/iteration-N/<eval-name>/with_skill/outputs/
- Also save a summary of your approach to <target>/eval-results/iteration-N/<eval-name>/with_skill/approach.md
```

**Without-skill worker:**
```
Execute this task:
- Task: <eval prompt>
- Input files: <eval files, or "none">
- Save your final output to: <target>/eval-results/iteration-N/<eval-name>/without_skill/outputs/
- Also save a summary of your approach to <target>/eval-results/iteration-N/<eval-name>/without_skill/approach.md
```

The without-skill variant gets the bare prompt with no skill context.
The with-skill variant gets the full SKILL.md content prepended.

Use `subagent_type: "worker"` and give each a descriptive task name
like `"eval-N-with-skill"`. Launch all workers for all evals in the
same turn so they complete in parallel.

### 4. Grade as runs complete

As worker notifications arrive, save timing data (tokens, duration)
from the notification. Write `timing.json` in each run directory:

```json
{"total_tokens": 84852, "duration_ms": 23332}
```

When all runs for an eval are done, grade outputs against assertions.
Spawn a grader subagent that reads both outputs + the assertion list
and produces `grading.json` in the eval directory:

```json
{
  "with_skill": [
    {"id": "max-depth-2", "text": "No nesting deeper than 2 levels", "passed": true, "evidence": "..."}
  ],
  "without_skill": [
    {"id": "max-depth-2", "text": "No nesting deeper than 2 levels", "passed": false, "evidence": "..."}
  ]
}
```

For deterministic checks (file patterns, regex, structure), write
a quick script rather than asking the LLM to eyeball it.

### 5. Aggregate benchmark

When all evals are graded, produce `benchmark.json` and `benchmark.md`
in the iteration directory. Compute:
- Pass rate per variant (% of assertions passed)
- Mean tokens ± stddev per variant
- Mean duration ms ± stddev per variant
- Delta: with_skill minus without_skill for each metric

```json
{
  "skill_name": "...",
  "iteration": 1,
  "summary": {
    "with_skill": {"pass_rate": 0.85, "mean_tokens": 12000, "mean_duration_ms": 15000},
    "without_skill": {"pass_rate": 0.60, "mean_tokens": 8000, "mean_duration_ms": 10000},
    "delta_pass_rate": 0.25
  },
  "evals": [...]
}
```

### 6. Show results

Write `review.html` to `<target>/eval-results/iteration-N/review.html`
using `references/review.html` as the template. Populate it with all
eval data: prompts, outputs, grading, benchmark. Tell the user:

"I've written results to `<target>/eval-results/iteration-N/review.html`.
Here's the summary: [pass rates, token/time deltas]. The full breakdown
with per-eval outputs is in review.html."

### 7. Iterate

After the user reviews results and gives feedback:
1. Apply changes to the skill
2. Run `scripts/check-pack.sh` to verify the skill still passes
3. Rerun evals into a new `iteration-N+1/` directory
4. Compare against previous iteration

Stop when the user is satisfied or pass rates plateau.

## Gotchas

- Assertions must be objectively verifiable. "The code is clean" is not
  an assertion. "No function exceeds 20 lines" is.
- Without-skill runs can sometimes outperform with-skill runs on simple
  tasks. That's valid data — the skill may add noise for trivial cases.
- Small N: 3 evals × 1 iteration = noisy results. For real confidence,
  run 5+ evals across 3+ iterations. Treat single-run results as
  directional, not definitive.
- Worker subagents have fresh context and don't know about the eval
  setup. Give them only the task, not meta-instructions about the eval.
- The task tool's timing notification is the only source of token/duration
  data — save `timing.json` as soon as each worker completes.
- Skills without `evals/evals.json` can't be runtime-evaluated. Tell
  the user to create evals first or use `/skill-evaluation` for a
  static audit instead.

## Common Rationalizations

| Excuse | Why it's wrong |
|--------|---------------|
| "This skill is too subjective for evals" | Subjective skills (writing style, design) need qualitative review, not runtime assertions. But most workflow skills have objectively checkable outputs. |
| "I ran the skill manually and it works" | Author-blindness. Two parallel runs (with/without) surface what the skill actually changes vs. what the model does by default. |
| "3 evals is enough" | 3 evals catch obvious bugs. 10+ evals across 3+ iterations approach statistical significance. Start small, expand as the skill stabilizes. |
| "The without-skill baseline is unfair — the model figured it out anyway" | That's exactly the signal: if pass rates are identical, the skill adds tokens without changing outcomes. Sharpen the evals or the skill. |
