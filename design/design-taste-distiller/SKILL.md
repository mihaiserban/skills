---
name: design-taste-distiller
description: Distill visual taste from references, screenshots, prior designs, notes, DESIGN.md files, brand examples, workflow preferences, or user feedback into a compact TASTE.md for future design agents. Use when the user asks how to capture taste, create taste guidelines, make agents design with better judgment, define aesthetic preferences, avoid generic AI design, capture critique loops, or build a reusable design judgment layer alongside DESIGN.md.
---

# Design Taste Distiller

## Overview

Create a `TASTE.md` that captures design judgment: values, preferences, anti-patterns, critique questions, and decision rules. Use `DESIGN.md` for concrete visual systems; use `TASTE.md` for what to choose when several design moves are possible.

## Inputs

Accept any mix of:

- screenshots, mockups, or implemented UI
- links or named references
- existing `DESIGN.md` files
- prior project notes
- user comments like "this feels too generic" or "more like Linear but warmer"
- workflow preferences such as "audit before rebuilding", "show variants first", or "use the design-system skill when applying a known style"
- folders of markdown, images, or product artifacts

If inputs are files, inspect them directly. If the reference set is text-heavy, use:

```bash
python3 /Users/mitzuuuu/.agents/skills/design/design-taste-distiller/scripts/taste_scaffold.py --output TASTE.md <paths...>
```

The scaffold is only a starting point. Fill it with real judgment from the references.

## Distillation Workflow

1. Identify the product context:
   - subject
   - audience
   - primary job of the interface
   - design risks for this category

2. Separate signals:
   - `Observed`: what the references visibly do
   - `Valued`: why those choices are good for this product
   - `Rejected`: what should be avoided even if it is fashionable
   - `Conditional`: where taste changes by context, such as landing page vs. dense tool

3. Write the taste profile as decisions, not decoration:
   - "Prefer one strong visual thesis over many small flourishes."
   - "Use cards only when items repeat or need containment."
   - "Let typography carry personality before adding decorative effects."
   - "Make premium mean control, spacing, and material confidence, not generic dark gloss."

4. Add a critique loop:
   - questions the agent must ask before building
   - questions the agent must ask after seeing screenshots
   - what to remove when the design feels generic
   - which mode the agent is in: explore, build, audit, refine, or ship

5. Capture reusable playbooks:
   - which skills, design-system docs, style guides, or TASTE.md/DESIGN.md files to load for each mode
   - what to load first by default, and what to load only when the task needs it
   - when to use screenshots, visual audits, or side-by-side comparisons before changing code
   - when to stop adding new visual ideas and instead refine spacing, hierarchy, copy, responsiveness, and states

6. Keep it compact:
   - target 1 to 3 pages
   - use bullets and short imperatives
   - include concrete positive and negative examples
   - avoid long theory

## TASTE.md Shape

Use this structure unless the project already has a taste document:

```markdown
# TASTE.md

## Product Context

## Taste Values

## Positive References

## Anti-Patterns

## Decision Rules

## Critique Questions

## Workflow Modes

## Playbooks To Load

## Memory
```

Use `Workflow Modes` to encode how design work should proceed, such as explore, build, audit, refine, or ship. Use `Playbooks To Load` to name the reusable skills or documents a future agent should reach for, without loading everything for every task.

## Quality Bar

- Make taste falsifiable. A future agent should know when a design violates it.
- Include negative examples. Anti-taste is often more useful than preference.
- Name tradeoffs. For example: "Prefer density for expert tools, but never at the cost of scan order."
- Avoid copying a famous brand's identity. Capture judgment and posture, not trademarked expression.
- Preserve user voice. If the user has strong phrasing, include it directly in short quotes.
- Make the workflow opinionated. Good taste often comes from critique loops and mode-specific playbooks, not a single generation pass.

## Using With DESIGN.md

When a product has both files:

- `DESIGN.md` defines the visual system.
- `TASTE.md` defines judgment, selection pressure, critique, and what to avoid.
- If they conflict, respect the user's explicit latest instruction first, then `TASTE.md`, then `DESIGN.md`.

After creating or updating `TASTE.md`, suggest using `$design-md-style-picker`, `$design-md-style-apply`, or `$design-md-style-audit` when the next step is selecting, building, or reviewing a concrete UI.
