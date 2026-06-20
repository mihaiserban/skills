---
name: init-agent-harness
description: |
  Initialize the pi agent harness in a new or existing repository. Sets up:
  agent definitions (worker + reviewers), coding standards, mechanical lint
  rules, pre-commit hooks, TypeScript strict config, and the AGENTS.md
  reference. Use when the user asks to "set up agents", "init harness",
  "bootstrap agent setup", or "add coding standards".
---

# Init Agent Harness

This skill initializes the full pi agent harness in a repository. The output is
a working setup: agent files, satellite docs, mechanical lint enforcement, git
gates, and session-start bootstrapping.

## Prerequisites

This skill is built for the **pi coding agent** and its extension ecosystem.
Without the environment-level dependencies below, the harness it creates will
produce agent files referencing non-existent APIs.

### Environment (must exist before running this skill)

| Dependency | Version check | Required for |
|---|---|---|
| [pi](https://pi-agent.dev) | `pi --version` | Agent file format, `.pi/` conventions, `subagent()` API |
| [context-mode](https://github.com/earendil-works/context-mode) | `ctx_doctor` | `ctx_search`, `ctx_execute`, `ctx_execute_file`, `ctx_stats` tools |
| [pi-subagents](https://github.com/earendil-works/pi-subagents) | `subagent({ action: "doctor" })` | Agent lifecycle, `.pi/settings.json` overrides, `subagent()` orchestration |
| Node.js ≥ 20 | `node --version` | `npx husky`, `npm install`, ESLint runtime |
| git ≥ 2.30 | `git --version` | Pre-commit hooks, conventional commits |

### Project (installed by this skill or must already exist)

| Dependency | How it's handled |
|---|---|
| TypeScript ≥ 5 | Skill hardens `tsconfig.json`; expects existing install |
| ESLint (flat config) | Skill merges standards into `eslint.config.js`; creates minimal config if missing |
| Prettier | Skill adds format scripts; expects existing install or adds it |
| `eslint-plugin-jsdoc` | Auto-installed by skill when creating `eslint.standards.config.js` |
| `husky`, `lint-staged` | Installed by Phase 7 |

### Quick environment check

Run these before Phase 0. If any fail, fix the environment first:

```bash
# pi itself
pi --version

# context-mode
ctx_doctor

# pi-subagents
subagent({ action: "doctor" })

# runtime
node --version  # ≥ 20
git --version   # ≥ 2.30
```

Do NOT proceed past Phase 0 if any environment check fails — the harness
will produce agent files that reference tools and APIs that don't exist.

## When to Use

- New repo: user wants agent-driven development from day one
- Existing repo without agents: user wants to add the harness retroactively
- The user asks to "set up agent harness", "init agents", "add coding
  standards", "add pre-commit gates"

## When NOT to Use

- The repo already has `.pi/agents/` populated — this is an init tool, not a
  migration tool
- The user only wants ONE piece (e.g., just ESLint) — do that directly

## What This Skill Creates

```
project-root/
├── .pi/
│   ├── agents/
│   │   ├── <package>.worker.md          # implementation worker
│   │   ├── <package>.reviewer.md        # general reviewer
│   │   └── <package>.ts-standards-reviewer.md  # TS semantic standards
│   ├── SESSION_START.md                 # bootstraps every session
│   └── skills/                          # (this skill lives here)
├── AGENTS.md                            # agent harness reference doc
├── CODE_STANDARDS.md                    # coding rules + conventions
├── eslint.standards.config.js           # mechanically-enforceable rules
├── .husky/pre-commit                    # pre-commit hook
└── (updated) package.json               # scripts + lint-staged config
```

Plus updates to existing files: `tsconfig.json` (strict mode flags),
`eslint.config.js` (merge standards), `package.json` (scripts, husky,
lint-staged).

## Step-by-Step Workflow

### Phase 0: Discover

Ask the user (or infer from codebase):

1. **Package name** — used as agent prefix (e.g., `toolbox`, `myapp`). Defaults
   to the directory name.
2. **Framework** — `effect` (Effect.ts), `next` (Next.js), `express`,
   `react-vite`, or `other`. Determines which sections of CODE_STANDARDS.md get
   written.
3. **TDD enforcement?** — Yes/no. If yes, CODE_STANDARDS.md §5 mandates TDD.
4. **Security review?** — Yes/no. If yes, adds a security-reviewer agent
   (framework-specific: Electron security, API auth, etc.).
5. **Design system?** — If the project has a DESIGN_SYSTEM.md already, note it.
   This skill does NOT create design systems.
6. **Model for agents?** — Which model to assign to each agent role. Models are
   configured centrally in `.pi/settings.json` `subagents.agentOverrides`, not
   in individual agent frontmatter. Default mapping:
   - Worker + reviewers (coding tier): `deepseek/deepseek-v4-pro`
   - Scout, researcher (explorer tier): `deepseek/deepseek-v4-flash`
   - Oracle, planner: inherit pi default

If the user doesn't know, use sensible defaults: package=dir-name, framework=infer
from package.json dependencies, TDD=yes, security=no, model=default.

### Phase 1: Create Agent Files

Create `.pi/agents/<package>.<role>.md` from the templates in
`templates/agents/`. Each template has `{{PACKAGE}}` placeholders — replace
them.

**Minimum set:**

| Agent | Template | Always? |
|---|---|---|
| `<package>.worker` | `templates/agents/worker.md` | ✅ |
| `<package>.reviewer` | `templates/agents/reviewer.md` | ✅ |
| `<package>.ts-standards-reviewer` | `templates/agents/ts-standards-reviewer.md` | ✅ |

**Conditional:**

| Agent | Template | When? |
|---|---|---|
| `<package>.security-reviewer` | Build from scratch | Only if user wants security review |

For the security reviewer, adapt the review angles to the framework:
- Electron → process isolation, IPC, contextBridge
- Next.js → API routes auth, SSR leaks, middleware
- Express → input validation, CORS, rate limiting
- Generic → secret handling, input validation, dependency audit

**Agent frontmatter rules:**

- `package: <package-name>`, `scope: project`
- Do NOT include `model:` — models are centralized in `.pi/settings.json`
- `tools: read, write, edit, bash, ctx_search, ctx_execute, ctx_execute_file` for worker
- `tools: read, bash, ctx_search, ctx_execute, ctx_execute_file` for reviewers (no write/edit)
- `systemPromptMode: replace`, `inheritProjectContext: false`, `inheritSkills: false`

**After creating agents, configure models in `.pi/settings.json`:**

Read or create `.pi/settings.json` and add `subagents.agentOverrides` entries
for every agent. Use the full runtime name (`<package>.<name>`) as the key:

```json
{
  "$schema": "https://pi-agent.dev/settings.schema.json",
  "subagents": {
    "agentOverrides": {
      "<package>.worker": { "model": "<coding-model>" },
      "<package>.reviewer": { "model": "<coding-model>" },
      "<package>.ts-standards-reviewer": { "model": "<coding-model>" },
      "scout": { "model": "deepseek/deepseek-v4-flash", "thinking": "off" },
      "researcher": { "model": "deepseek/deepseek-v4-flash", "thinking": "off" }
    }
  }
}
```

If `.pi/settings.json` already exists, merge into the existing `agentOverrides`
object — do not replace other settings. For the security reviewer (if created),
add its override too.

### Phase 2: Create AGENTS.md

Create `AGENTS.md` using `templates/AGENTS.md` as the base. This is the agent
harness reference doc — the central index of all agents and orchestration
patterns.

Replace `{{PACKAGE}}` with the package name. Add entries for any conditional
agents (security reviewer).

The AGENTS.md must include:
- Quick index table of all agents (builtin + project)
- Project agent descriptions (when to use each)
- Builtin strategy descriptions
- Orchestration patterns (implement→review→fix, parallel fanout, explore→plan→implement)
- Agent properties reference table
- Context hygiene rules (file-only output, handoff templates, budget thresholds)
- Troubleshooting section

### Phase 3: Create CODE_STANDARDS.md

Create `CODE_STANDARDS.md` from `templates/CODE_STANDARDS.base.md` as the
core, then append framework-specific sections.

**Sections that are ALWAYS included (framework-agnostic):**

| § | Content | Source |
|---|---|---|
| 1 | TypeScript strict rules (no `any`, no `!`, exhaustiveness, naming, file org) | `CODE_STANDARDS.base.md` |
| 4 | Import rules (order, no cycles) | `CODE_STANDARDS.base.md` |
| 6 | Git workflow (conventional commits, hooks, branching) | `CODE_STANDARDS.base.md` |
| 7 | What agents MUST know | `CODE_STANDARDS.base.md` |
| 8 | Quick reference (verify/lint/typecheck commands) | `CODE_STANDARDS.base.md` |

**Framework-specific sections:**

| Framework | Sections to add | Source |
|---|---|---|
| `effect` | §2 Effect.ts Patterns, §3 DRY, §5 Testing (TDD) | `CODE_STANDARDS.effect.md` |
| `next` | §2 React/Next.js Patterns, §3 API Routes, §5 Testing | Build from scratch |
| `express` | §2 Express Patterns, §3 Middleware, §5 Testing | Build from scratch |
| `react-vite` | §2 React Patterns, §3 State Management, §5 Testing | Build from scratch |
| `other` | §2 (user must fill), §3 (user must fill), §5 Testing | Skeleton only |

### Phase 4: Create ESLint Standards Config

Create `eslint.standards.config.js` from `templates/eslint.standards.config.js`.

This is **largely framework-agnostic**. The mechanical rules enforced:
- No `any` (except test files)
- No non-null assertions (`!`)
- No `as` casts (except `as const`)
- No `vi.mock` / `jest.mock` (TDD requires real seams)
- No `export *` (barrel re-exports)
- No `assertNever`/`absurd`/`unreachable` (use prelude helpers)
- `process.env` only in config/bootstrap
- JSDoc on all exported symbols (src only, not tests)

Customize the `files` globs to match the project structure. If the project
doesn't have `src/config/` or `src/bootstrap/`, adjust the `process.env`
allowlist paths.

### Phase 5: Merge ESLint Config

Read the existing `eslint.config.js` (flat config). Merge the standards configs
by spreading `...standardsConfigs` into the existing config array, AFTER any
project-specific overrides. If there's no existing config, create a minimal one:

```js
import { standardsConfigs } from "./eslint.standards.config.js"
export default [...standardsConfigs]
```

### Phase 6: Harden tsconfig.json

Ensure `tsconfig.json` has:

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitOverride": true,
    "exactOptionalPropertyTypes": true
  }
}
```

If the file doesn't exist, create it with these flags plus `module`, `target`,
`moduleResolution` appropriate for the framework.

### Phase 7: Set Up Git Hooks

1. Install `husky` and `lint-staged`:
   ```bash
   npm install -D husky lint-staged
   ```

2. Initialize husky:
   ```bash
   npx husky init
   ```

3. Create `.husky/pre-commit`:
   ```bash
   npx lint-staged
   ```

4. Add to `package.json`:
   ```json
   {
     "lint-staged": {
       "*.{ts,tsx}": ["eslint --fix --no-warn-ignored", "prettier --write"],
       "*.{json,md,yml,yaml}": ["prettier --write"]
     }
   }
   ```

### Phase 8: Add Verify/Lint Scripts

Ensure `package.json` has these scripts:

```json
{
  "scripts": {
    "typecheck": "tsc --noEmit",
    "lint": "eslint .",
    "lint:fix": "eslint . --fix",
    "format": "prettier --write .",
    "format:check": "prettier --check .",
    "verify": "npm run typecheck && npm run lint && npm run format:check",
    "prepare": "husky"
  }
}
```

If the project uses a different package manager, adjust accordingly.

### Phase 9: Create SESSION_START.md

Create `.pi/SESSION_START.md` from `templates/SESSION_START.md`. This is the
file every session reads to bootstrap context.

Customize §2 and §6 for the project — which satellite docs to read, which
phases exist, what file patterns matter.

### Phase 10: Validate

1. Run `npm run verify` — should pass (no code violates standards yet, just
   config validation)
2. Run `npm run prepare` — husky hook installed
3. Make a test commit — pre-commit hook should run lint-staged
4. Verify agents appear: `subagent({ action: "list" })`

### Phase 11: Commit

```bash
git add -A
git commit -m "chore: initialize agent harness with coding standards, lint gates, and agents"
```

## Customization Points

After running this skill, the user (or a follow-up session) should:

1. **Fill CODE_STANDARDS.md §2** if framework is `other` — add framework-specific
   patterns
2. **Add more agents** — tool-contract-reviewer, license-reviewer,
   design-reviewer as the project grows. When adding agents, do NOT put `model:`
   in their frontmatter — add their override to `.pi/settings.json` instead.
3. **Create DESIGN_SYSTEM.md** if the project has a UI
4. **Create acceptance contracts** in `acceptance/` if using task-group workflow
5. **Create MANIFEST.md** if using phased implementation
6. **Swap models later** — edit `.pi/settings.json` `agentOverrides` to change
   models across all agents in one place without touching any agent file.

## Anti-Patterns

- ❌ Don't copy Toolbox's Design System tokens — they're macOS-specific
- ❌ Don't copy Effect.ts patterns for non-Effect projects
- ❌ Don't create Electron security reviewers for web apps
- ❌ Don't create tool-contract-reviewers unless the project has a ToolDescriptor pattern
- ❌ Don't skip the user prompts in Phase 0 — framework choice matters
- ❌ Don't overwrite existing agent files — this is init-only, not repair
