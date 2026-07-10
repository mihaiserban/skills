---
name: secret-scan
description: Catch hardcoded secrets, keys, and tokens before they get committed. Use before any commit and on any file with credentials.
when_to_use: before commit, files with API keys, .env handling, config, connection strings
---
# Secret Scan
Grep the diff for: `api[_-]?key`, `secret`, `token`, `password`, `BEGIN PRIVATE KEY`, `AKIA[0-9A-Z]{16}`, `sk-`, `ghp_`, bearer values, and long base64/hex blobs.
For each hit: is it a real secret or a placeholder? Real secrets:
1. **Move it** — to env vars or a secrets manager. Never the repo. Say: "Move this to an environment variable."
2. **Rotate it** — if already committed, it is COMPROMISED. Say: "Rotate this key now — it's in git history." Deleting the line doesn't help.
3. **Prevent recurrence** — add the pattern to `.gitignore` or a pre-commit secret scanner.
Output format: for each real secret, print `file:line — SECRET TYPE — Action: <move|rotate|prevent>`. End with a one-line summary: "N secrets found. M need rotation."

## What to say explicitly
- If a secret is committed: **"ROTATE immediately — it's in the reflog."**
- If a secret is in a config file: **"Move to environment variable: KEY_NAME"**
- If a secret looks like a test/mock: **"Treat as live — test keys often grant real staging access."**

## Common Rationalizations

| Excuse | Why it's wrong |
|--------|---------------|
| "It's a private repo" | Private repos get forked, mirrored, made public, or accessed by contractors. Assume zero trust. |
| "I'll rotate it before I push" | Humans forget. Rotate it first, then use the new value. Once committed, it's in the reflog forever. |
| "It's just a test/mock key" | Test keys often grant real access to staging environments and CI systems. Treat all keys as live. |
| "The CI will catch it" | CI scan delays make rotation harder — the secret is already in git history by the time it's caught. |
| "No one reads the git history that deep" | Automated scanners read ALL history. A secret committed and deleted is still visible in the reflog. |