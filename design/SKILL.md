---
name: design
description: Route every design request to the right sub-skill. Use when the user asks to design a website, landing page, dashboard, app shell, or UI. Pipeline: picker → apply → audit. For taste capture, use /design-taste-distiller.
---

# Design

Orchestrate the end-to-end design workflow.

## Pipeline

The default path uses proven design systems from
`https://github.com/voltagent/awesome-design-md`:

1. **Pick a style** — `/design-md-style-picker` selects the best-fitting
   DESIGN.md profile for the product brief.
   Done when: picker returned a DESIGN.md path.

2. **Apply the style** — `/design-md-style-apply` translates the chosen
   DESIGN.md DNA into real product UI code.
   Done when: apply produced code and stated verification results.

3. **Audit the result** — `/design-md-style-audit` checks the implementation
   against the source aesthetic and produces concrete fixes.
   Done when: audit returned pass or a findings block.

If any step fails, stop and report — do not advance blindly.

## Taste capture

Use `/design-taste-distiller` to distill references, screenshots, critiques,
or user feedback into a reusable `TASTE.md` for future design work.

## Routing guide

| User says | Route |
|---|---|
| "Design a website/dashboard/app" | Default pipeline: picker → apply → audit |
| "Show me the feature before building it" | route to `/show-first` → apply → audit |
| "Plan before building" / "wireframe first" | route to `/show-first` |
| "Build X in the style of Y" | skip picker, route to apply → audit |
| "What style fits my project?" | route to `/design-md-style-picker` |
| "Does this match the DESIGN.md?" | route to `/design-md-style-audit` |
| "Capture my design preferences" | route to `/design-taste-distiller` |

## Gotchas

- If the picker returns no strong match, fall back to a general-purpose
  DESIGN.md (e.g. "minimal") rather than stalling.
- If audit finds issues, loop apply → audit up to 3 times before surfacing
  to the user.
- Check for an existing TASTE.md before running the picker — taste
  preferences override DESIGN.md defaults.

Log pipeline results to `~/.design-log.md` with date, DESIGN.md source, and audit outcome for comparison across iterations.
