# {{PACKAGE}} – Coding Standards

> **Every agent and human contributor MUST follow these rules.** Enforced by ESLint +
> TypeScript strict mode + git hooks. Violations block commit. No exceptions, no
> suppressions without documented reason.

---

## 1. TypeScript

### 1.1 Strict Mode Only

`strict: true` with these additions:

- `noUncheckedIndexedAccess: true` – every array/record access is potentially undefined
- `noUnusedLocals: true` – zero dead code
- `noUnusedParameters: true` – no unused args (prefix with `_` if intentionally unused)
- `noImplicitOverride: true` – explicit `override` keyword on class overrides
- `exactOptionalPropertyTypes: true` – no `undefined` leakage through optional properties

### 1.2 No `any` – Ever

```typescript
// ❌ FORBIDDEN
function parse(data: any): any { ... }
const config: any = loadConfig()

// ✅ REQUIRED
function parse(data: unknown): ParsedResult { ... }
const config: unknown = loadConfig()
// ... validate with Schema before using
```

ESLint blocks: `@typescript-eslint/no-explicit-any`, `no-unsafe-assignment`,
`no-unsafe-member-access`, `no-unsafe-call`, `no-unsafe-return`, `no-unsafe-argument`.

**Test files only**: `any` is allowed for mock flexibility. This is the ONLY exception.

### 1.3 No Non-Null Assertions (`!`)

```typescript
// ❌ FORBIDDEN
const value = maybeNull!;

// ✅ REQUIRED
if (maybeNull === null) return errorResult
const value = maybeNull
```

ESLint blocks: `@typescript-eslint/no-non-null-assertion`.

### 1.4 Exhaustiveness Checking

All `switch` statements and `if/else` chains must be exhaustive for discriminated unions:

```typescript
type Status = "active" | "inactive" | "pending"

// ❌ FORBIDDEN: missing "pending"
switch (status) {
  case "active": return <ActiveBadge />
  case "inactive": return <InactiveBadge />
  default: return <DefaultBadge /> // MISSING: pending
}

// ✅ REQUIRED: every variant handled
switch (status) {
  case "active": return <ActiveBadge />
  case "inactive": return <InactiveBadge />
  case "pending": return <PendingBadge />
}
```

### 1.5 Naming

| Construct   | Convention               | Example                        |
| ----------- | ------------------------ | ------------------------------ |
| Classes     | PascalCase               | `class UserService`            |
| Interfaces  | PascalCase, NO `I` prefix | `interface User`, NOT `IUser` |
| Type aliases| PascalCase               | `type UserStatus = ...`        |
| Functions   | camelCase                | `function formatName(...)`     |
| Variables   | camelCase                | `const activeUser = ...`       |
| Constants   | UPPER_CASE               | `const MAX_RETRIES = 3`        |
| Parameters  | camelCase, `_` if unused | `(_event, data) => ...`        |
| Type params | PascalCase, descriptive  | `<TInput>`, NOT `<T>`          |

### 1.6 File Organization

```
File max: 300 lines (ESLint warns). Split if longer.
One primary export per file.
Group imports: node builtins → external → internal aliases → relative.
Empty line between groups.
```

---

## 2. [FRAMEWORK-SPECIFIC PATTERNS]

> **Fill this section with your framework's conventions.** Examples:
> - Effect.ts: Context.Tag services, Layer composition, Schema validation
> - Next.js: Server Components vs Client Components, data fetching patterns
> - Express: middleware ordering, error handling, route organization
> - React: component patterns, hooks rules, state management
>
> Delete this placeholder after filling.

---

## 3. Code Duplication Prevention

### 3.1 Extract Shared Logic

If 3+ files share the same logic, extract it to a shared utility:

```typescript
// ✅ If multiple modules need string truncation:
// src/shared/utils/string.ts
export function truncate(s: string, max: number): string { ... }

// ❌ Copy-pasting truncate() into 5 files
```

### 3.2 One Concern Per File

Each file does exactly one thing. Never put two unrelated exports in one file.

---

## 4. Import Rules

### 4.1 Import Order (Auto-fixed by ESLint)

```typescript
// 1. Node built-ins
import { Buffer } from "node:buffer"

// 2. External packages
import { z } from "zod"

// 3. Internal aliases
import { User } from "@shared/types/user.js"

// 4. Relative imports
import { formatName } from "./utils.js"
```

### 4.2 No Circular Imports

ESLint blocks: `import/no-cycle`. If you hit this, extract shared types to a
separate file.

---

## 5. Testing Standards

### 5.1 Test-First Development (TDD)

**Write the test BEFORE the implementation. No exceptions.**

| Step | Action | Check |
|------|--------|-------|
| 1 | Write the unit test | Run tests → RED (test fails — code doesn't exist yet) |
| 2 | Write minimal implementation | Run tests → GREEN (test passes) |
| 3 | Refactor (if needed) | Run tests → GREEN (stays green) |
| 4 | Commit | Pre-commit hook verifies lint + typecheck |

**Why TDD:**
- The test IS the specification. It's more precise than prose.
- Reviewers verify tests exist and pass; they can't verify prose acceptance criteria.
- Prevents "the code works, I'll write tests later" which means never.

### 5.2 Test File Location

```
tests/unit/<mirror-source-path>/<name>.test.ts
```

Example: `src/shared/utils/string.ts` → `tests/unit/shared/utils/string.test.ts`

### 5.3 Test Coverage Requirements

| Test case                    | Required?     | Example                                   |
| ---------------------------- | ------------- | ----------------------------------------- |
| Valid input → correct output | ✅ Always     | `process("hello") → expected`             |
| Empty input → error          | ✅ Always     | `process("") → throws`                    |
| Boundary values              | ✅ Always     | Max length, min length, zero              |
| Error paths                  | ✅ Always     | Invalid input produces typed error         |
| Edge cases                   | ✅ If relevant| Unicode, special chars, null bytes        |

---

## 6. Git Workflow

### 6.1 Commit Messages

Conventional commits format:

```
feat: add user authentication
fix: handle empty input in formatter
refactor: extract string utils to shared module
test: add edge case tests for parser
chore: update dependencies
docs: add API documentation
```

### 6.2 Pre-Commit Hook

Runs automatically. Blocks commit if:

- ESLint finds errors
- TypeScript finds type errors
- Prettier check fails

### 6.3 Branching

```
main        – production, protected
feat/*      – feature branches
fix/*       – bug fixes
```

---

## 7. What Agents MUST Know

### 7.1 Before Writing Code

1. Read `AGENTS.md` — agent reference and orchestration patterns
2. Read `CODE_STANDARDS.md` (this file) — mechanical rules enforced by lint
3. Read existing files in the area you're modifying
4. If acceptance contracts exist (`acceptance/`), read the relevant one

### 7.2 While Writing Code

- No `any`, no `!`, no `as` casts (except `as const`)
- No `throw` for expected errors — use typed error returns
- Parse, don't validate at boundaries
- Imports follow the order: node → external → internal → relative
- File max 300 lines

### 7.3 Before Committing

- `npm run typecheck` passes
- `npm run lint` passes
- `npm test` passes (for changed code)
- Pre-commit hook will catch violations anyway – better to run first

---

## 8. Quick Reference

```bash
# Check everything
npm run verify

# Individual checks
npm run typecheck      # TypeScript
npm run lint           # ESLint
npm run format:check   # Prettier
npm test               # Tests

# Auto-fix
npm run lint:fix       # Fix ESLint issues
npm run format         # Fix formatting
```
