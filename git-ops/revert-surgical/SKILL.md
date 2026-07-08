---
name: revert-surgical
description: Undo a bad change without nuking unrelated work. Use when a specific commit or change broke something.
when_to_use: "revert this", a bad deploy, one commit broke prod, undo without losing other work
---
# Surgical Revert
Don't `git reset --hard` away three good commits to undo one bad one.
- **Single commit** — `git revert <sha>` creates an inverse commit; history stays intact and shared-branch-safe.
- **One file from a commit** — `git checkout <good-sha> -- path/to/file`.
- **Hunk-level** — `git checkout -p` to revert specific changes, keep the rest.
- **A merge** — `git revert -m 1 <merge-sha>` (pick the mainline parent).
On a shared branch, always revert (forward), never rewrite history. Reproduce the breakage first so you revert the RIGHT thing, then verify the revert actually fixes it.

## Common Rationalizations

| Excuse | Why it's wrong |
|--------|---------------|
| "I'll just `git reset --hard` back to the good commit" | That nukes every commit after it — including other people's work. On shared branches, that's irreversible damage. |
| "I know which commit broke it, I don't need to reproduce" | Without reproduction, you can't verify the revert fixes the breakage. Confirm before and after. |
| "Reverting a merge is the same as reverting a regular commit" | Merge reverts need `-m 1` to pick the mainline parent. Skip it and git reverts nothing useful. |
| "It's faster to hand-edit the broken file back to before" | Hand-editing loses the audit trail. `git revert` creates an explicit inverse commit that everyone can see and understand. |
| "Force-pushing my fix is cleaner than a revert commit" | Force-push on shared branches breaks everyone else's local copy. Revert forward — history stays intact. |
