---
name: kill-dead-code
description: Find and remove unreachable/unused code safely. Use during cleanup or before a refactor.
when_to_use: cleanup, "remove unused", before refactoring, dead branches
---
# Kill Dead Code
1. **Prove it's dead** — no references (grep the symbol across the repo, including dynamic/string usage and tests). Unused export ≠ dead if it's a public API.
2. Check it's not feature-flagged off (dead today, alive when the flag flips).
3. Delete it AND its now-orphaned tests, imports, and config.
4. Run the full suite + a build. Dead code removal should change behavior in exactly zero ways.
Bias to delete: every line someone has to read is a cost. But never delete what you can't prove is unreachable — say "I think X is unused, confirm?" instead of guessing.

## Common Rationalizations

| Excuse | Why it's wrong |
|--------|---------------|
| "It's not hurting anything" | Dead code inflates grep results, search, and false confidence. Someone WILL try to use it. |
| "Someone might need it later" | Git history exists. Dead code rots silently — assumptions drift, APIs change, it becomes actively wrong. |
| "I'm not sure it's unused — let me delete it anyway" | False positives are worse than leaving dead code. Flag it and ask. Never delete what you can't prove is unreachable. |
| "The tests still pass, so it's fine" | Tests that exercise dead code are also dead tests. Removing code without removing its tests leaves zombie tests. |
| "It's just a few lines" | Those few lines get copied, refactored around, and imported. Dead code spawns dead patterns. |
