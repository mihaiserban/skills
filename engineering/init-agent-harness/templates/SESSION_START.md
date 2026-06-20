# Session Start Checklist

> **Read this at the start of every {{PACKAGE}} implementation or review
> session.** It bootstraps context without re-reading the entire project.

---

## 1. Quick Status (2 min)

```bash
git log --oneline -5
git status --short
```

Note what changed in the last session. The commit message IS the summary.

## 2. Know Your Agents

Read `AGENTS.md` — it lists all project + builtin agents, when to use each, and
the orchestration patterns (implement→review→fix, review fanout,
explore→plan→implement). Prefer `{{PACKAGE}}.*` project agents for any
project-specific work.

### 2.1. Check Context Budget

Run `ctx_stats`. Note the context savings ratio.

| Budget | Mode |
| ------ | ---- |
| <50%   | Normal — read files, launch agents, synthesize inline |
| 50-70% | Caution — all agent outputs must be file-only. Use ctx_search, not inline reads. |
| 70-85% | Restricted — stop reading satellite docs (ctx_search only). Stop launching new agents. |
| >85%   | **HARD STOP** — commit WIP, hand off to next session. |

## 3. Determine Session Type

### If IMPLEMENTATION session:

- Find the next task to implement
- Read the acceptance contract if one exists
- Launch ONE worker with a thin task:

```ts
subagent({
  agent: "{{PACKAGE}}.worker",
  task: "Implement the user authentication service.",
  async: true,
})
```

The worker bootstraps its own context (reads satellite docs, source files,
acceptance contracts itself). Do NOT pre-read files for the worker — that burns
parent context.

### If REVIEW session:

- Check what files changed since the implementation commit:
  ```bash
  git diff --name-only HEAD~1 HEAD
  ```
- Pick relevant reviewers based on what changed
- Launch parallel reviewers:

```ts
subagent({
  tasks: [
    {
      agent: "{{PACKAGE}}.reviewer",
      task: "Review the current diff. Classify changes and inspect files directly.",
      output: false,
    },
    // add a specialized reviewer (security/license) in parallel only for a
    // genuinely-distinct high-stakes domain — not for TS standards, which the
    // general reviewer's checklist already covers
  ],
  context: "fresh",
  async: true,
})
```

## 4. While Waiting for Subagents

Do useful parallel work:

- Read the next task's context (prep for next session)
- Run verification commands
- Review docs or research notes relevant to upcoming work
- Do NOT edit the active worktree while a worker is running

## 5. After Subagents Return

### If worker completed:

- Check the worker handoff (the 10-line status signal)
- Verify acceptance criteria against the changed files
- If a verify log exists, inspect it with ctx_search
- Commit if worker didn't already

### If reviewers completed:

- Synthesize findings
- Categorize: blockers → fix now, fix-worth-doing → fix now, optional → backlog
- If blockers or fix-worth-doing items exist → launch fix-worker:
  ```ts
  subagent({
    agent: "{{PACKAGE}}.worker",
    task: "Apply only the blocker and fix-worth-doing items from the review.",
    async: true,
  })
  ```
- If no actionable findings → mark task as done

## 6. Close Session

- Update any tracking documents with new statuses
- If changes were made, commit
- Note what the next session should do

---

## Quick Reference: Key Files

| File | Purpose |
|------|---------|
| `AGENTS.md` | Agent harness reference + orchestration patterns |
| `CODE_STANDARDS.md` | Coding rules, enforced by lint + TS strict |
| `eslint.standards.config.js` | Mechanical lint rules (no `any`, `!`, `as`, etc.) |
| `.pi/agents/{{PACKAGE}}.worker.md` | Worker agent definition |
| `.pi/agents/{{PACKAGE}}.reviewer.md` | Reviewer agent definition |
| `.pi/agents/{{PACKAGE}}.ts-standards-reviewer.md` | TS standards reviewer (optional) |
