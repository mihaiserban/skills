# Audit Rubric

Use this to compare an implementation against a selected source `DESIGN.md`.

## Core Questions

- Does the first viewport communicate the same design posture as the source?
- Are typography, spacing, and density doing as much work as color?
- Is the source's signature element present in a product-specific form?
- Are repeated controls consistent across states and breakpoints?
- Does the design still serve the user's product rather than performing the source brand?
- Are accent, radius, type, theme, CTA language, and asset strategy locked consistently?

## Common Drift Patterns

- Accent-only styling: the UI uses source colors but generic type, cards, shadows, and layout.
- Token dilution: source colors are approximated with many nearby shades.
- Roundedness mismatch: pills, sharp edges, or card radii do not follow the source geometry.
- Density mismatch: a precise tool becomes a spacious landing page, or a cinematic brand becomes cramped cards.
- Wrong media strategy: a photography-first source gets icon cards, or a data-first source gets decorative images.
- Uncontrolled gradients: gradients appear where the source relies on solid surfaces, photography, or typography.
- Weak signature: the most memorable source move is absent or copied literally instead of translated.
- Default structure: centered hero, repeated cards, section eyebrows, or zigzags appear because no stronger layout decision was made.
- Missing states: the UI only shows the happy path and lacks loading, empty, error, focus, or active states.
- Asset gap: a media-led style is implemented with empty boxes, fake screenshots, or text-only placeholders.

## Fix Patterns

- Replace arbitrary colors with named source tokens and semantic roles.
- Rebuild type scale before adjusting spacing; hierarchy often starts there.
- Collapse decorative cards into stronger sections when the source uses full-bleed bands or editorial layouts.
- Add one source-faithful signature element, then remove weaker decorations.
- Audit mobile separately; many style systems fail when type and controls compress.
- Add or simplify states until the UI feels usable, not just presentational.
- Replace default section patterns with layout families justified by the content.
