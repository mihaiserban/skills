---
name: bisect-regression
description: Find the exact commit that introduced a bug. Use when something worked before and broke, and you don't know which change did it.
when_to_use: "it worked last week", a regression, unclear which commit broke it
---
# Bisect the Regression
1. Find a known-good commit and a known-bad one. Confirm both by actually checking out and testing.
2. `git bisect start; git bisect bad <bad>; git bisect good <good>`.
3. At each step, run the SMALLEST test that distinguishes good from bad. Mark `git bisect good/bad`.
4. When git names the first bad commit, read its diff. The bug is in those lines — don't guess elsewhere.
5. `git bisect reset`. Report: the commit, the line, the one-sentence cause.
Automate it: `git bisect run ./repro.sh` if you have a script that exits non-zero on the bug.

## Common Rationalizations

| Excuse | Why it's wrong |
|--------|---------------|
| "I think I know which commit broke it" | Guessing sends you down the wrong rabbit hole. Bisect names the EXACT commit and line. |
| "I'll just read the recent git log and find it" | Visual inspection of 50 commits misses interactions between changes. Bisect tests behavior, not appearance. |
| "Setting up bisect is slower than manually checking commits" | Bisect halves the search space each step. 100 commits → 7 steps. Manual checking: up to 100 steps. |
| "The reproduction script is too complicated to write" | It only needs to exit non-zero on the bug. A 5-line script beats 20 manual checkouts. |
| "The bug is probably in this one file, I'll just look there" | Bugs cross files. A seemingly innocent change in config can break logic in a handler. Trust bisect, not intuition. |
