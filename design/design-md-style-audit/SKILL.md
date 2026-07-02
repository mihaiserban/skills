---
name: design-md-style-audit
description: Audit an implemented UI, screenshot, mockup, or code change against a selected voltagent/awesome-design-md DESIGN.md source aesthetic. Use when reviewing whether a product matches a chosen style, checking visual consistency after implementation, finding design drift, or producing concrete fixes to better apply a DESIGN.md design language.
---

# DESIGN.md Style Audit

## Overview

Compare the actual interface against the chosen source `DESIGN.md` and produce concrete fixes. Focus on visible design drift: missing hierarchy, weak signature gestures, wrong component geometry, generic palettes, inconsistent density, and source-inappropriate motion. If the project has `TASTE.md`, audit judgment and anti-patterns as well as source-style fidelity.

## Resolve Inputs

If the user gives a style slug or name, find the source:

```bash
python3 /Users/mitzuuuu/.agents/skills/scripts/design_md_catalog.py ensure
python3 /Users/mitzuuuu/.agents/skills/scripts/design_md_catalog.py path runwayml
python3 /Users/mitzuuuu/.agents/skills/scripts/design_md_catalog.py show runwayml --lines 160
```

Read the selected source file, `references/audit-rubric.md`, and `references/preflight-rubric.md`. Also read `TASTE.md` if present. Inspect the implemented UI through code, screenshots, or a running app. For frontend work, use screenshots whenever possible because design drift often hides in spacing, density, and rhythm.

## Audit Pass

Score the UI on five dimensions:

- Source DNA: palette, type, surfaces, geometry, and signature element feel like the selected source.
- Taste fit: the UI follows the project's values, anti-patterns, and critique questions.
- Product translation: the style supports the product's actual workflow rather than copying irrelevant source content.
- Execution discipline: design locks, layout rules, component states, and preflight checks hold.
- Consistency: repeated components share the same tokens, radii, borders, shadows, and interaction states.
- Responsiveness: mobile and desktop preserve the intended hierarchy without overlap or overflow.
- Accessibility: contrast, focus, labels, reduced motion, and touch targets are acceptable.

## Findings Format

Lead with fixes, not compliments:

```markdown
Findings
- [P1] <issue> — <file/screenshot area>. <why it breaks the source style or product use>. Fix: <specific change>.
- [P2] <issue> — ...

Style Fit
Selected source: <slug or path>
Taste source: <TASTE.md path, or none>
Fit: <strong / mixed / weak>
Most important missing move: <one sentence>
Preflight: <pass / partial / fail>
```

Use priorities:

- `P1`: breaks product use, accessibility, or the core source aesthetic.
- `P2`: noticeable design drift that should be fixed before shipping.
- `P3`: polish that would make the translation sharper.

If asked to fix issues, apply the changes directly and verify again.
