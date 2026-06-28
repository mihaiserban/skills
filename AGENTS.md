# Agent Instructions

This repository is a personal skill pack. Keep the package small, explicit, and
boring to install.

## Buckets

Published buckets:

- `design/` — frontend design, DESIGN.md translation, visual taste.
- `engineering/` — engineering workflows and reusable engineering discipline.
- `research/` — explicit research workflows.

Non-published buckets, if created later:

- `in-progress/` — drafts and experiments.
- `deprecated/` — retained only for history or migration.

Only published buckets may appear in `.claude-plugin/plugin.json` and the
top-level README skill tables.

## Manifest Rules

Every `SKILL.md` under `design/`, `engineering/`, or `research/` must have:

- a README entry
- a `.claude-plugin/plugin.json` entry
- valid frontmatter with `name` and `description`

Skills under `in-progress/` and `deprecated/` must not appear in the README
skill tables or plugin manifest.

Run `scripts/check-pack.sh` after moving, adding, deleting, or renaming skills.

## Invocation Rules

Use the vocabulary in `docs/invocation.md`.

- User-invoked skills set `disable-model-invocation: true`.
- Model-invoked skills omit `disable-model-invocation`.
- Avoid ambiguous categories like "explicit model skill" in docs. If a skill
  should only run when the user asks, make it user-invoked.

## Structure Rules

- Keep workflow skills thin. Put reusable shared logic in scripts or references.
- Do not duplicate helper scripts across skills. Prefer `scripts/`.
- Avoid hardcoded machine-local paths in `SKILL.md` instructions unless there is
  a fallback or environment variable.
- Do not commit generated files such as `.DS_Store`, `__pycache__/`, or `*.pyc`.
- If a skill is adapted from another repo, keep attribution in the skill file.

## Documentation Rules

The top-level README is the public index. It should explain:

- setup
- published skills
- invocation groups
- external resources such as the DESIGN.md catalog
- file structure

Bucket READMEs are optional while the pack is small. Add them only when a bucket
grows large enough that the top-level README becomes hard to scan.
