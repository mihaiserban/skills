---
name: design-md-style-picker
description: Choose an appropriate source aesthetic from voltagent/awesome-design-md DESIGN.md profiles for a product, app, landing page, dashboard, or redesign brief. Use when the user wants design direction, asks what style to use, or gives a product brief without a clear visual system and needs a DESIGN.md profile selected before building.
---

# DESIGN.md Style Picker

## Overview

Use the local checkout of `https://github.com/voltagent/awesome-design-md` to choose a source aesthetic that fits the product brief. Return a decisive recommendation, the selected `DESIGN.md` path, and the design moves that should survive translation into the new product.

## Prerequisites

Requires Python 3 and the scripts bundled with this skill pack. Find the catalog script:

```bash
# Preferred: environment variable
python3 "$SKILLS_SCRIPTS/design_md_catalog.py" ensure

# Fallback: relative to skill pack root
python3 scripts/design_md_catalog.py ensure
```

## Catalog Workflow

1. Find the catalog:

```bash
python3 "$SKILLS_SCRIPTS/design_md_catalog.py" ensure
python3 "$SKILLS_SCRIPTS/design_md_catalog.py" list
```

2. Search by product category, mood, or named style:

```bash
python3 "$SKILLS_SCRIPTS/design_md_catalog.py search "developer tool dark precise"
```

3. Inspect only the strongest candidates:

```bash
python3 "$SKILLS_SCRIPTS/design_md_catalog.py show vercel --lines 140
```

4. Read `references/selection-rubric.md` before making the final pick when the brief is ambiguous or more than one style could work.

5. Look for a local `TASTE.md` in the project root or design docs. If present, read it before recommending a source.

## Selection Rules

- Prefer product fit over surface similarity. A fintech app can borrow Stripe's precision, Wise's friendly clarity, or Kraken's trading density depending on the job.
- Let `TASTE.md` override catalog novelty. If taste says "precise, quiet, low ornament," do not pick an expressive media-led source just because it is visually exciting.
- Pick one primary source style. Use a second source only to fill a missing interaction or density pattern, and name it as secondary.
- Treat brand aesthetics as inspiration, not affiliation. Do not copy logos, protected marks, proprietary names, or exact marketing claims.
- Choose a style whose structure fits the product's real workflow. For example, use Linear/Superhuman/Raycast for keyboard-first tools, Runway/Pinterest/Nike for media-first products, and ClickHouse/Supabase/Stripe for developer-facing technical surfaces.
- Preserve the source's decisive constraints: palette discipline, typography rhythm, spacing density, component geometry, motion behavior, and signature visual gesture.

## Gotchas

- Don't pick a style solely for its accent color — a cohesive translation needs typography, spacing, and component geometry too.
- Matching a marketing-heavy source to a data-dense product produces a shallow skin, not a design.
- Exhaust one source before reaching for a second — mixed styles usually feel less designed than a single strong source.

## Recommendation Format

Give the future builder enough to act without re-deciding the direction. Done when every DNA category is filled with at least one concrete design move from the source. Mark any category you cannot fill and explain why in "Avoid."

```markdown
Selected style: <slug>
Source: <absolute path to DESIGN.md>
Taste: <TASTE.md path, or none>
Why it fits: <1-3 concrete reasons tied to the product brief>
Design DNA to preserve:
- Color:
- Typography:
- Layout:
- Components:
- Signature gesture:
Avoid:
- <brand copying or style mismatch risk>
```

If the user asks you to build immediately after choosing, invoke or follow `$design-md-style-apply` with the chosen source path.
