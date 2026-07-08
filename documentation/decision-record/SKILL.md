---
name: decision-record
description: Capture an architectural decision so the next session (or engineer) knows WHY. Use after any non-obvious technical choice.
when_to_use: picked a library/pattern/schema, a tradeoff was made, a hard-to-reverse choice
---
# Decision Record (ADR)
Write a short file `docs/decisions/NNN-<slug>.md`:
- **Context** — what forced a decision. The constraints.
- **Options** — the 2-3 real candidates, one line each.
- **Decision** — what you picked, dated.
- **Why** — the tradeoff. What you gave up. "We picked Postgres over Mongo because we need real joins; we accept heavier ops."
- **Consequences** — what this now makes easy and hard.

Done when: every section is filled with concrete detail (no "TBD"), the tradeoff is named explicitly, and the date + slug are set.

## Gotchas
- Vague "why": "better performance" without the metric and the benchmark is a guess. Name the constraint (e.g. "500ms page load with 10K records").
- Straw-man options: listing candidates you'd never pick to make the real choice look better. Only list genuine runners-up.
- Hard-to-reverse choices (schema, auth, data store, language) MUST get an ADR. Skip it for reversible ones like a library swap with a clean interface.

## Common Rationalizations

| Excuse | Why it's wrong |
|--------|---------------|
| "The decision is obvious" | "Obvious" depends on context. The next engineer won't have your context — that's what the ADR provides. |
| "I'll write it up after the PR merges" | Decisions fade from memory. Write the ADR while the tradeoffs are still sharp in your mind. |
| "A one-line commit message is enough" | Commit messages explain WHAT. ADRs explain WHY — the constraints, the rejected options, the consequences. |
| "Nobody reads ADRs" | The engineer debugging a design flaw 6 months from now will. ADRs are for explaining why the obvious fix is wrong. |
| "This library swap is reversible, skip the ADR" | Correct — for cleanly-abstracted dependencies, skip. For anything that touches schema, data, or auth: write it. |
