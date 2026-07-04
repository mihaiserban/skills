---
name: design
description: Use when the user asks to design a website, landing page, dashboard, app shell, or UI. Orchestrates the design workflow: first run /design-md-style-picker to choose a DESIGN.md aesthetic, then /design-md-style-apply to translate it, then /design-md-style-audit to verify. For capturing visual taste, use /design-taste-distiller.
---

# Design

Orchestrate the end-to-end design workflow. This skill is the single entry point
for any "design a website" or "build a UI" request.

## Design pipeline

The default path uses proven design systems from
`https://github.com/voltagent/awesome-design-md`:

1. **Pick a style** — `/design-md-style-picker` selects the best-fitting
   DESIGN.md profile for the product brief.
2. **Apply the style** — `/design-md-style-apply` translates the chosen
   DESIGN.md DNA into real product UI code.
3. **Audit the result** — `/design-md-style-audit` checks the implementation
   against the source aesthetic and produces concrete fixes.

This pipeline gives every project a distinct, intentional visual identity
rather than a generic AI-generated default.

## Taste capture

Use `/design-taste-distiller` to distill references, screenshots, critiques,
or user feedback into a reusable `TASTE.md` for future design work.

## Decision guide

| User says | Use |
|---|---|
| "Design a website/dashboard/app" | Default pipeline: picker → apply → audit |
| "Build X in the style of Y" | skip picker, go to apply → audit |
| "What style fits my project?" | `/design-md-style-picker` |
| "Does this match the DESIGN.md?" | `/design-md-style-audit` |
| "Capture my design preferences" | `/design-taste-distiller` |
