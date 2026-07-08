---
name: rebase-safely
description: Rebase, squash, or rewrite history without losing work or breaking shared branches. Use before any history rewrite.
when_to_use: rebase, squash, "update my branch", interactive rebase, force-push
---
# Rebase Safely
1. **Backup first** — `git branch backup/<name>` before any rewrite. Free undo.
2. Rebase onto the latest base: `git fetch; git rebase origin/main`.
3. Resolve conflicts one commit at a time. Test after the rebase, not just that it "completed".
4. **Never rewrite shared history** — if others pulled the branch, rebasing it forces them into pain. Rewrite only your own un-pushed/un-shared commits.
5. Push with `--force-with-lease`, never bare `--force` (lease refuses if someone else pushed).
If anything goes sideways: `git reflog` finds the pre-rebase state; `git reset --hard backup/<name>` restores it.

## Common Rationalizations

| Excuse | Why it's wrong |
|--------|---------------|
| "I don't need a backup branch, I know what I'm doing" | Rebase mistakes are silent until you force-push. A backup branch costs 10 bytes and saves hours. |
| "`--force` is easier to type than `--force-with-lease`" | `--force` overwrites anyone else's push without warning. `--force-with-lease` refuses if the remote diverged. |
| "I'll just resolve all conflicts at once" | Resolving per-commit catches conflicts introduced by intermediate commits. Bulk resolution hides which change broke what. |
| "It's a private branch, rebasing shared history won't matter" | Branches stop being private the moment someone pulls them. Check before rewriting. |
| "I'll test after the rebase finishes" | Testing after the rebase means you don't know which conflict resolution introduced a regression. Test incrementally. |
