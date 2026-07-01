# Taste Rubric

Use this rubric to turn references into judgment.

## Signals To Extract

- What repeats across good references?
- What is absent from good references?
- What would make the product feel generic?
- Which constraints create the taste?
- What does the user call good, bad, premium, warm, precise, playful, serious, or weird?

## Useful Taste Axes

- restraint vs. expression
- density vs. air
- editorial vs. operational
- cinematic vs. utilitarian
- warm vs. severe
- playful vs. exacting
- familiar conventions vs. authored surprise
- product imagery vs. abstract systems
- typography-led vs. media-led vs. data-led

## Judgment Forms

Good taste rules usually look like:

- Prefer X over Y when Z.
- Spend visual drama on X, keep Y quiet.
- Avoid X unless it directly supports Y.
- If the design feels generic, remove X before adding Y.
- This product should feel X, not Y.

Weak taste rules usually look like:

- Make it modern.
- Use a clean design.
- Add delightful interactions.
- Make it premium.
- Use nice gradients.

Rewrite weak rules into visible decisions.

## Execution Controls

Add these when the taste profile will guide frontend implementation:

- `Design Read`: one sentence that names page kind, audience, visual language, and implementation posture.
- `Execution Dials`: 1 to 10 values for layout variance, motion intensity, and visual density.
- `Design Locks`: constraints that must stay consistent across the whole UI.
- `Preflight Checks`: mechanical checks before shipping.

## Dial Guidance

- Layout variance: low means symmetrical and conventional; high means asymmetric and editorial.
- Motion intensity: low means static states and simple hovers; high means scroll choreography and physics-like interaction.
- Visual density: low means gallery-like air; high means cockpit-like information per viewport.

Let the brief set the dials:

- Trust-first or regulated product: lower variance, lower motion, medium density.
- Premium consumer page: medium variance, medium motion, low-medium density.
- Creative studio or campaign: higher variance, higher motion, low-medium density.
- Developer portfolio or technical product: medium variance, low-medium motion, medium density.
- Dense product workspace: lower spectacle, higher density, interaction clarity first.

## Design Locks

Capture locks as rules another agent can audit:

- Accent lock: choose one accent system and use it consistently.
- Shape lock: choose sharp, soft, or pill geometry and apply it by rule.
- Type lock: choose display, body, and utility roles; avoid random family mixing.
- Theme lock: do not switch between unrelated warm/cool neutral systems mid-page.
- CTA lock: one label per intent, reused consistently.
- Asset lock: if the visual direction depends on imagery, require real or generated assets.

## Anti-Default Patterns

Watch for these recurring weak moves:

- centered hero, three cards, and a vague gradient background
- decorative glass panels everywhere
- random purple-blue glow as personality
- tiny uppercase labels above every section
- fake product screenshots built from empty boxes
- alternating split sections repeated until the page feels automated
- placeholder-as-label forms
- white text on white or low-contrast buttons
- rounded buttons in an otherwise sharp system without a rule

## Good Output

A strong `TASTE.md` lets another agent decide:

- whether to pick Linear or Runway for a brief
- whether a card should exist
- whether color, type, or imagery should carry the page
- how to critique a screenshot
- what to remove when the design feels noisy
- which mechanical checks must pass before handoff
