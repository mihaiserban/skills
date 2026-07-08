---
name: changelog-from-diff
description: Turn a set of commits or a diff into a clean, user-facing changelog entry. Use before a release or PR description.
when_to_use: cutting a release, writing release notes, summarizing a branch
---
# Changelog from Diff
Read the actual diff/commits, not the commit messages (they lie).
Group into: **Added · Changed · Fixed · Removed · Security** (skip empty groups).
Each line: user-facing impact, not implementation. "Fixed login failing for emails with uppercase characters" — not "fixed bug in user lookup".
- Lead with what the user notices. Bury internals.
- Call out breaking changes loudly, with the migration step.
- Link the PR/issue. No marketing fluff.
Output: markdown ready to paste. If a change has no user impact, leave it out.

## Common Rationalizations

| Excuse | Why it's wrong |
|--------|---------------|
| "I'll just use the commit messages as the changelog" | Commit messages are for developers. Changelogs are for users. Internal refactors don't belong. |
| "There are no breaking changes, I can skip the changelog" | Breaking changes are the loudest thing to call out, but non-breaking improvements are still worth noting. |
| "The diff is too complex to summarize" | If the diff is too complex for a changelog entry, it might be too complex for a single release. Split it. |
| "I'll group by commit, not by impact" | Users don't care about your commit order. They care about what changed: Added, Changed, Fixed, Removed. |
| "Marketing fluff makes it sound better" | "Refactored the authentication middleware for improved maintainability" belongs in commit messages. Users want "Login no longer logs you out unexpectedly." |
