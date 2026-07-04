---
name: reduce-nesting
description: Flatten deeply nested conditionals into readable, early-return code. Use on any function with 3+ levels of indentation.
when_to_use: arrow-shaped code, 3+ nested ifs, a function that's hard to follow
---
# Reduce Nesting
Deep nesting hides bugs in the branches you didn't read.
- **Guard clauses** — handle the invalid/edge cases first and return early. The happy path drops to the left margin.
- **Invert conditions** — `if (!valid) return;` instead of wrapping the whole body in `if (valid) {...}`.
- **Extract** — a nested block doing one thing becomes a named function.
- **Replace flag-then-branch** — return the result directly instead of setting a variable to return later.

Done when: every function touched stays at 2-3 levels max. The diff is behavior-preserving (existing tests still pass).

## Gotchas
- Guard clause that changes behavior: `if (!x) return null` where the old code fell through to a side effect. Verify the old path end-to-end.
- Over-extraction: extracting a 3-line block into a function 40 lines away fragments the read. Extract only when the block has a clear, nameable purpose.
- If you still need more depth than 2-3 levels, split the function — forcing guard clauses onto a 200-line function just moves the complexity sideways.
