---
name: clean-commits
description: Turn messy WIP into clean, atomic commits with messages that explain why. Use before opening a PR.
when_to_use: before a PR, messy history, "squash this", commit message help
---
# Clean Commits
- **Atomic** — one logical change per commit. Refactor and behavior change go in separate commits.
- **Message** — subject says WHAT in imperative ("Fix null pointer in user lookup"), body says WHY. "Fix bug" is useless.
- **Specific** — "Fix login failing when email has uppercase chars" tells the next person exactly what happened.
- Reorder/squash WIP and "fix typo" commits into the real changes (`git rebase -i`).
- Never mix an unrelated fix into a feature commit.
A good history is a debugging tool: `git bisect` and `git blame` only work if commits are atomic and messages explain intent.

## Common Rationalizations

| Excuse | Why it's wrong |
|--------|---------------|
| "I'll squash it all at the end" | Squashing loses intermediate intent. Atomic commits tell a story that a mega-squash hides. |
| "The diff is small, one commit is fine" | Small diffs can still mix unrelated changes. Refactor + fix in one commit breaks bisect. |
| "Commit messages are just overhead" | Messages are debugging tools. `git bisect` and `git blame` are useless with "fix bug" or "WIP". |
| "Nobody reads commit history anyway" | The person debugging a regression 6 months from now absolutely does. That person might be you. |
| "I'll clean it up in the next PR" | "Later" is a code word for "never." Messy history compounds — clean it now, while context is fresh. |
