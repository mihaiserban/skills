---
name: pr-from-diff
description: Write a PR description a reviewer can approve fast. Use when opening any pull request.
when_to_use: opening a PR, "write the PR body", review prep
---
# PR from Diff
A reviewer should understand the change without reading every line. Structure:
- **What & why** — the problem and the approach, 2-3 sentences.
- **Changes** — bullet the meaningful ones (skip noise like formatting).
- **How to verify** — the exact steps/commands the reviewer runs to confirm it works.
- **Risks / out of scope** — what could break, what you deliberately didn't do.
- **Screenshots** for UI.
Flag any decision the reviewer should weigh in on. Keep the PR small — if the diff is huge, say what could be split out. No "fixes stuff".

## Common Rationalizations

| Excuse | Why it's wrong |
|--------|---------------|
| "The diff speaks for itself" | It doesn't. A PR description gives the reviewer a map before they start reading 200 lines of diff. |
| "The commit messages are enough" | Commit messages are for bisect. PR descriptions are for review — different audience, different format. |
| "I'm the only one reviewing, I know what I did" | You wrote it 2 hours ago. In 2 weeks, you won't remember WHY you changed the auth middleware. |
| "Risk section is just boilerplate" | "No known risks" is better than skipping it. Explicitly stating there are no edge cases forces you to check. |
| "Verification steps aren't needed for a small PR" | "Run the tests" is more useful than silence. Give the reviewer the exact command. |
