# Definition of Done

Every change must clear this bar before it's considered complete. These gates
apply regardless of which skill was used to produce the change.

## Gates

| Gate | Check |
|------|-------|
| Tests pass | All existing tests pass. New behavior has tests. |
| No regressions | Existing functionality intact. No test removals without explicit approval. |
| Behavior verified | Code works at runtime, not just "looks correct." Run it. |
| Lint/typecheck | Clean output from the project's lint and typecheck commands. |
| Docs updated | ADRs, READMEs, or inline docs updated if the change shifts behavior or intent. |
| Scope matched | Only the intended changes. No unrelated "cleanup" snuck in. |

## Per-Skill Verification

Each skill defines its own verification evidence. For example:
- `kill-dead-code`: grep finds no remaining references to removed symbols.
- `secret-scan`: no hardcoded credentials in the diff.
- `systematic-debugging`: bug reproduced before fix; fix confirmed by the
  reproduction case.

The per-skill bar sits ON TOP of this baseline. If a skill has a specific
verification step, it runs after the gates above.

## Anti-Patterns

| Excuse | Reality |
|--------|---------|
| "Seems right to me" | "Seems right" is how bugs ship. Prove it. |
| "I checked it mentally" | Run it. Every time. Without exception. |
| "The tests pass locally" | Also check lint, typecheck, and that you didn't break docs. |
| "It's a tiny change" | Tiny changes cause big outages. Same bar. |
