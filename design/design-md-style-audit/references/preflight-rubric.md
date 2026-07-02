# Preflight Rubric

Use this after comparing the UI to `DESIGN.md` and `TASTE.md`. It catches common generated-UI failures that can exist even when the palette is correct.

## Design Read

- Is the page or workspace clearly designed for the named audience?
- Does the visual language match the product category and risk level?
- Did the implementation choose one posture instead of mixing several half-directions?

## Locks

- Accent: one accent system, with only semantic exceptions.
- Shape: radii follow one grammar or a documented component rule.
- Type: display, body, and utility roles are stable.
- Theme: neutral temperature and surface logic do not drift section to section.
- CTA language: one label per intent.
- Assets: image-led styles use real, generated, or explicitly requested assets.

## Layout

- Hero or primary workspace fits its viewport and has one job.
- Navigation is not wrapped or oversized at desktop.
- Repeated sections do not reuse the same split, grid, or card family without purpose.
- Bento grids have exactly as many cells as content requires.
- Mobile collapse is explicit for every multi-column section.

## Interaction And States

- Buttons have hover, active, focus, and disabled states where relevant.
- Forms use labels above fields, not placeholders as labels.
- Loading, empty, and error states match the product surface.
- Motion respects reduced-motion preferences and does not distract from the primary task.

## Accessibility And Copy

- Buttons and form controls pass contrast checks.
- CTA text fits on one line at desktop.
- Headline scale does not clip glyphs or force awkward wrapping.
- Eyebrows and small uppercase labels are used sparingly.
- Trust logos, customer marks, and social proof do not contain filler labels.
