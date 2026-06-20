# Effect.ts Patterns (append to CODE_STANDARDS.md §2 after base template)

---

## 2. Effect.ts Patterns

### 2.1 Services Use Context.Tag

```typescript
// ✅ REQUIRED
export class Logger extends Context.Tag("{{PACKAGE}}/Logger")<
  Logger,
  { readonly info: (msg: string) => Effect.Effect<void> }
>() {}

// ❌ FORBIDDEN: plain classes as services
export class Logger {
  info(msg: string) { ... }
}
```

### 2.2 Layers for Construction, Not Services

Services NEVER mention their dependencies. Dependencies go in Layers:

```typescript
// ✅ REQUIRED: Service has no dependency awareness
class Database extends Context.Tag("{{PACKAGE}}/Database")<
  Database,
  { readonly query: (sql: string) => Effect.Effect<unknown> }
>() {}

// ✅ REQUIRED: Layer handles construction with dependencies
const DatabaseLive = Layer.effect(Database, Effect.gen(function* () {
  const config = yield* AppConfig  // dependency resolved HERE
  const logger = yield* Logger     // not leaked into service type
  return { query: (sql) => ... }
}))

// ❌ FORBIDDEN: leaking dependencies into service type
class Database extends Context.Tag("{{PACKAGE}}/Database")<
  Database,
  { readonly query: (sql: string) => Effect.Effect<unknown, never, AppConfig | Logger> }
>() {}
```

### 2.3 Errors Are Typed, Never Thrown

```typescript
// ✅ REQUIRED: Effect.fail with typed error
process: (input) =>
  Effect.gen(function* () {
    if (!input) {
      return yield* Effect.fail(new AppError("empty", "INVALID_INPUT"))
    }
    try {
      return compute(input)
    } catch (e) {
      return yield* Effect.fail(new AppError(e.message, "PROCESS_ERROR"))
    }
  })

// ❌ FORBIDDEN: throw in Effect code
process: (input) => {
  if (!input) throw new Error("empty") // WRONG
  return Effect.succeed(compute(input))
}
```

### 2.4 Schema Validation Before Processing

Every input MUST be validated via Schema before processing:

```typescript
// ✅ REQUIRED
const InputSchema = Schema.Struct({
  text: Schema.String.pipe(Schema.minLength(1)),
  options: Schema.optional(Schema.Struct({ indent: Schema.Number })),
})
```

### 2.5 ManagedRuntime Assembly

```typescript
const MainLayer = Layer.mergeAll(
  AppConfigLive,
  LoggerLive,
  DatabaseLive,
  // ... all layers
)

const runtime = ManagedRuntime.make(MainLayer)
```
