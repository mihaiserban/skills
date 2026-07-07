---
name: show-first
description: Plan a feature with a low-fidelity UI wireframe and a systems plan before writing any code.
disable-model-invocation: true
---

# Show First

## Overview

Show the feature before building it. Produce a plan and a low-fidelity artifact
showing how the UI will look and how the systems fit together. Keep them in sync
as we iterate.

Inspired by Dan Fein's workflow: "Create a plan and a low-fidelity artifact
showing how the UI will look and how the systems fit together. Keep them in sync as
we iterate. This moves more of the iteration from the code to the plan."

## Read Skills Locally

Read design sub-skills from this repository's local folder — not from
harness-specific symlink directories. Use paths relative to the skill pack root:

- `design/design-md-style-picker/SKILL.md`
- `design/design-md-style-apply/SKILL.md`
- `design/design-md-style-audit/SKILL.md`
- `design/design-taste-distiller/SKILL.md`

Do NOT reach into `~/.claude/skills/`, `~/.opencode/skills/`,
`~/.codex/skills/`, or `~/.agents/skills/` to read skill files.

## Workflow

### 1. Capture the feature brief

- What is being built? For whom? What job does it do?
- What are the key user actions?
- What existing screens or systems does it connect to?
- Read the project's `TASTE.md` if present — taste preferences shape the plan.

**Done when:** the brief is stated in 3-5 sentences and the success criteria are
listed.

### 2. Pick the visual language

Run the design picker to select the source aesthetic that will inform the
wireframe's component vocabulary, density, and layout rhythm:

```bash
python3 "$SKILLS_SCRIPTS/design_md_catalog.py" ensure
python3 "$SKILLS_SCRIPTS/design_md_catalog.py" search "<keywords from brief>"
```

Follow `design/design-md-style-picker/SKILL.md` for the full selection process.
Record the selected DESIGN.md path and its DNA dimensions (palette, typography,
layout, components, signature gesture). Do NOT build the full UI yet — use the
aesthetic only to inform the wireframe's component geometry and layout rhythm.

**Done when:** a DESIGN.md source is selected and its DNA dimensions are
recorded.

### 3. Write the systems plan

Capture the non-UI architecture — how the systems fit together:

- **Components/modules** involved and their responsibilities
- **Data flow** — where data comes from, how it moves, where it's stored
- **API surface** — endpoints, contracts, request/response shapes
- **State** — client state, server state, loading/error/success states
- **Edge cases** — empty, error, loading, permission denied, offline, conflict
- **Dependencies** — what existing code this touches, what's new

**Done when:** every subsection (Components, Data Flow, API Surface, State,
Edge Cases, Dependencies) has at least one concrete item tied to the feature
brief.

### 4. Produce the low-fidelity artifact

Draw ASCII wireframes in markdown showing:

- **Primary layout** — desktop (and mobile if the feature is responsive)
- **Key states** — default, loading, empty, error, success
- **Component vocabulary** informed by the selected DESIGN.md (e.g. card-based,
  split-pane, command palette, list-detail, sidebar+content)
- **Annotations** — notes connecting UI regions to systems plan sections

Use box-drawing characters for clarity. Keep it low-fidelity — no colors, no
real content, no code, no styling. The goal is layout, hierarchy, and flow. The
design-md-style-apply step handles fidelity later.

Example primary layout:

```
┌─────────────────────────────────────────────┐
│  Logo          [ search ]        [ + New ]  │
├──────────┬──────────────────────────────────┤
│ Filters  │  ┌────────────────────────────┐  │
│ · All    │  │ Item card                  │  │
│ · Active │  │ title · status · date      │  │
│ · Done   │  └────────────────────────────┘  │
│          │  ┌────────────────────────────┐  │
│          │  │ Item card                  │  │
│          │  └────────────────────────────┘  │
└──────────┴──────────────────────────────────┘
   sidebar          list (data: GET /items)
```

Empty state:

```
┌─────────────────────────────────────────────┐
│                                             │
│         No items yet                        │
│         [ Create your first item → ]        │
│                                             │
└─────────────────────────────────────────────┘
```

Error state:

```
┌─────────────────────────────────────────────┐
│  ⚠ Could not load items                     │
│  [ Retry ]                                  │
└─────────────────────────────────────────────┘
```

**Done when:** primary layout + at least loading, empty, and error states are
drawn and annotated.

### 5. Sync check

The plan and the artifact must agree. Before showing the user:

- Every UI region in the wireframe maps to a component in the systems plan.
- Every data flow annotation in the wireframe matches the API/state section of
  the plan.
- Every state in the wireframe (empty, error, loading) has a handling note in
  the plan's edge cases.
- No plan section describes something invisible in the wireframe, and no
  wireframe element is unexplained by the plan.

If they disagree, fix whichever is wrong. Do not show an unsynced pair.

**Done when:** every wireframe element traces to a plan section and vice versa.

### 6. Iterate on the plan, not the code

Present the synced plan + artifact to the user. When the user gives feedback:

- Update the plan AND the artifact together.
- Re-run the sync check.
- Do NOT write implementation code during this phase — not even a scaffold.

Loop until the user approves or says "build it". Do not cross the build gate
until the user approves.

**Done when:** the user approves the plan + wireframe.

### 7. Build gate

Cross the build gate only now — start writing code. Hand off to the design
build pipeline:

- Follow `design/design-md-style-apply/SKILL.md` to translate the DESIGN.md
  aesthetic into real product UI, using the wireframe as the layout spec.
- Implement the systems plan alongside the UI.
- After implementation, follow `design/design-md-style-audit/SKILL.md` to
  verify the result against the source aesthetic.

**Done when:** the handoff to `design-md-style-apply` and
`design-md-style-audit` is accepted and implementation has begun.

## Artifact File

Write the plan + wireframe to `FEATURE_PLAN.md` in the project root (or a
location the user specifies). Keep both halves in one file so they stay in
sync. Use this structure:

```markdown
# Feature Plan: <name>

## Brief
<3-5 sentences + success criteria>

## Visual Language
Selected source: <slug>
DESIGN.md: <path>
DNA: <palette, type, layout, components, signature>

## Systems Plan
### Components
### Data Flow
### API Surface
### State
### Edge Cases
### Dependencies

## Wireframes
### Primary Layout
### Loading State
### Empty State
### Error State

## Sync Notes
<mapping between wireframe regions and plan sections>
```

Update `FEATURE_PLAN.md` in place during iteration — do not create multiple
versions.

## Guardrails

- Do NOT skip the wireframe. "Show me the feature" means a visual artifact, not
  just a text plan.
- Do NOT skip the systems plan. "How the systems fit together" is half the
  artifact.
- If `TASTE.md` and the selected DESIGN.md conflict, follow the user's explicit
  instruction first, then `TASTE.md`, then `DESIGN.md`.
- If the user says "just build it" and skips the plan, respect that — but offer
  to save the brief into `FEATURE_PLAN.md` anyway for traceability.

## Final Response

State the feature name, the selected visual language, a one-line summary of the
systems plan, and point to `FEATURE_PLAN.md`. Ask the user to review and approve
before building. When approved, invoke or follow `$design-md-style-apply`.