# Agent Harness — {{PACKAGE}}

Central reference for all agents available to this project — builtin strategies,
project-specific agents, and the orchestration patterns they compose into.

---

## Quick Index

| Agent | Role | Context | Writes? | Use When |
|---|---|---|---|---|
| `{{PACKAGE}}.worker` | Implementation | fork | yes | Building ANY code |
| `{{PACKAGE}}.reviewer` | General review | fresh | no | Mixed-domain diffs |
| `{{PACKAGE}}.ts-standards-reviewer` | TS Coding Standards | fresh | no | Semantic standards: errors, parsing, branding, modules, workflows, tests, config |
{{SECURITY_ROW}}
| `worker` (builtin) | Generic implementation | fork | yes | Simple tasks, file ops |
| `reviewer` (builtin) | Generic review | fresh | no | Non-project-specific review |
| `oracle` (builtin) | Decision advisory | fork | no | Architecture, drift, tradeoffs |
| `scout` (builtin) | Codebase recon | fresh | no | Exploring, mapping modules |
| `researcher` (builtin) | Web research | fresh | no | Package eval, API docs |
| `planner` (builtin) | Plan creation | fork | no | Creating task plans |

---

## Project Agents

### {{PACKAGE}}.worker

**When**: any implementation session.

**What it knows**: project structure, CODE_STANDARDS, test patterns, framework
conventions. It reads acceptance contracts before starting, writes tests first,
then implements.

**Invocation**:

```ts
subagent({
  agent: "{{PACKAGE}}.worker",
  task: "Implement the user authentication service.",
  cwd: "/path/to/project",
})
```

**Properties**: fork context, single writer, enforces TDD, commits after completion.

---

### {{PACKAGE}}.reviewer

**When**: the diff spans 2+ domains and you need one reviewer that
auto-classifies changes and applies the right checks.

**What it checks**: classifies the diff by file pattern, then applies the
relevant review angle (TypeScript Standards, Domain Logic, Tests,
Config/Build).

**Invocation** (parallel review):

```ts
subagent({
  agent: "{{PACKAGE}}.reviewer",
  task: "Review the current diff. Classify changes and apply relevant checks.",
  context: "fresh",
  async: true,
})
```

---

### {{PACKAGE}}.ts-standards-reviewer

**When**: any diff touching domain/application code where the *semantic*
TypeScript Coding Standards apply — error modeling, parse-don't-validate,
branded types, state machines, module depth, adapter reuse audits,
functional-core/imperative-shell, workflow idempotency, test seams,
sensitive-data handling, config parsing, JSDoc/SAFETY-comment quality.

**What it checks**: only the SEMANTIC standards. The MECHANICAL rules (`any`,
`!`, `as` casts, `vi.mock`, `process.env`, `export *`, `assertNever`, missing
JSDoc) are already enforced by `eslint.standards.config.js` + `tsconfig.json` —
this reviewer does NOT re-report them.

**Invocation**:

```ts
subagent({
  agent: "{{PACKAGE}}.ts-standards-reviewer",
  task: "Review the current diff for TypeScript Coding Standards adherence (semantic rules).",
  context: "fresh",
  async: true,
})
```

{{SECURITY_AGENT_SECTION}}

---

## Builtin Strategies

For tasks that don't need project-specific knowledge, use the builtin agents.

### worker (builtin)

Generic implementation agent. Use for simple file operations, config tweaks, or
when the project agent would be overkill. Fork context, single writer.

### reviewer (builtin)

Generic review agent. Use when reviewing non-project-specific code (build
configs, CI scripts, READMEs). Fresh context, review-only.

### oracle (builtin)

Decision-consistency advisory. Use when the parent needs a second opinion on
architecture, model routing, merge conflicts, or context drift. Fork context —
inherits parent session history. Advisory only, never writes.

### scout (builtin)

Fast codebase recon. Use to map module structure, find patterns, or prepare
context docs for handoff. Fresh context.

### researcher (builtin)

Web research briefs. Use for npm package evaluation, API docs, ecosystem
comparisons. Fresh context.

### planner (builtin)

Creates structured implementation plans from context and requirements. Fork
context (inherits parent history). Use when a task is large enough to benefit
from a written plan before the worker starts.

---

## Orchestration Patterns

### 1. Implement → Review → Fix (the standard loop)

```
SESSION A (IMPLEMENT)
  parent picks next task
  parent launches {{PACKAGE}}.worker (fork, async)
  worker writes tests (RED) → implements (GREEN) → commits

SESSION B (REVIEW)
  parent launches 1-3 fresh-context reviewers in parallel (async)
  parent waits for all → synthesizes findings

  BLOCKER + FIX-WORTH-DOING → {{PACKAGE}}.worker (fix-worker, apply only accepted fixes)
  OPTIONAL → backlog note
  DEFER → discuss later
  CONFLICT → parent decides or escalates to user
```

### 2. Parallel Review Fanout

```ts
subagent({
  tasks: [
    { agent: "{{PACKAGE}}.reviewer", task: "Review the current diff." },
    { agent: "{{PACKAGE}}.ts-standards-reviewer", task: "Review for TS semantic standards." },
  ],
  concurrency: 2,
  context: "fresh",
  async: true,
})
```

### 3. Oracle → Worker (decision-gated implementation)

```ts
// Step 1: Oracle challenges direction (advisory, fork context)
subagent({ agent: "oracle", task: "Review my approach to the data layer." })

// Step 2: After parent approves direction, worker implements
subagent({
  agent: "{{PACKAGE}}.worker",
  task: "Implement the approved data layer approach.",
})
```

### 4. Explore → Plan → Implement (greenfield task)

```ts
// Step 1: Scout maps territory, researcher finds evidence
subagent({
  tasks: [
    { agent: "scout", task: "Map the src/ directory structure." },
    { agent: "researcher", task: "Research best practices for the chosen framework." },
  ],
  concurrency: 2,
  context: "fresh",
  async: true,
})

// Step 2: Planner creates structured plan from findings
subagent({ agent: "planner", task: "Create implementation plan from {previous}." })

// Step 3: After parent approves plan, worker implements
subagent({ agent: "{{PACKAGE}}.worker", task: "Implement the approved plan." })
```

---

## Agent Properties Reference

| Property | {{PACKAGE}}.worker | {{PACKAGE}}.reviewer | builtin worker | builtin reviewer | oracle | scout |
|---|---|---|---|---|---|---|
| Context | fork | fresh | fork | fresh | fork | fresh |
| Writes files | yes | no | yes | no | no | no |
| Knows project | yes | yes | no | no | partial | no |
| TDD-enforcing | yes | — | no | — | — | — |
| Async default | yes | yes | yes | yes | yes | yes |
| Output mode | inline (compact) | file-only | inline (compact) | file-only | inline | file-only |

---

## Context Hygiene

**The parent orchestrator's context window is the scarcest resource.** Every
byte of agent output that enters the parent's context burns budget that should
go to synthesis, architecture, and decision-making.

### Parent rules (non-negotiable)

1. **All reviewers output `file-only`.** Never let reviewer findings inline.
   Query sections with ctx_search.
2. **All scout/researcher/planner output `file-only`.** Only the handoff summary
   (5 lines) comes inline.
3. **Worker handoffs are 10 lines max.** Files changed, verification status,
   undone items, decisions.
4. **Check budget before launching.** `ctx_stats` at session start. If >70%,
   switch to file-only for everything.
5. **If >85%, stop.** Commit WIP. Hand off via MANIFEST.md. Never start new
   work past 85%.

### Sub-agent output contract

Every agent invocation that could produce >500 chars of output MUST use:

```ts
output: "reviews/<session>-<agent>.md",
outputMode: "file-only"
```

The parent sees only:

```
Output saved to: /tmp/.../review.md (4.2 KB, 87 lines)
```

Then queries specific findings:

```ts
ctx_search(queries: ["blocker", "type-design"], source: "review")
```

### Compact handoff template

```markdown
## Handoff

**Done**: [one sentence]
**Files**: [list with line counts]
**Verification**: typecheck ✅ lint ✅ tests N/N ✅
**Undone**: [none, or list]
**Decisions**: [none, or list]
```

Anti-patterns:

- Narrative ("I then read...") — never
- Vague ("some issues exist") — be specific or omit
- Full file contents — use file-only

## Troubleshooting

**Agent not found in `subagent list`?** Files must follow the
`{package}.{name}.md` naming convention. Example: `.pi/agents/{{PACKAGE}}.worker.md`.
Check with `subagent({ action: "doctor" })`.

**Agent created but empty?** `subagent create` writes only the frontmatter
skeleton. The system prompt body must be added manually or via `subagent update`
with a `systemPrompt` field.
