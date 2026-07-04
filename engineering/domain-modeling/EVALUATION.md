# Skill Evaluation — domain-modeling

> Evaluated: 2026-07-04
> Source: engineering/domain-modeling/SKILL.md
> Evaluator: skill-evaluation v2.1.0
> Framework: [Anthropic Skill Best Practices](https://claude.com/blog/lessons-from-building-claude-code-how-we-use-skills) + Matt Pocock's [writing-great-skills](https://www.youtube.com/watch?v=UNzCG3lw6O0)

## Summary

| Metric | Value |
|--------|-------|
| Overall Score | 85.00/100 |
| Grade | A |
| Category | code-quality-and-review |
| Invocation | model-invoked |
| Files | 3 (SKILL.md, ADR-FORMAT.md, CONTEXT-FORMAT.md) |
| Criteria scored / N/A | 14 scored, 4 N/A |

## Scorecard

### Axis 1 — Trigger

| # | Criterion | Weight | Score | Notes |
|---|-----------|--------|-------|-------|
| 1 | Invocation design | 2x | 85/100 | No `disable-model-invocation`, so model-invoked. Justified: description names "when another skill needs to maintain the domain model" — cross-skill reachability is the canonical reason for model-invocation. |
| 2 | Description quality | 2x | 80/100 | Covers three distinct triggers (pin down terms, record ADR, other-skill maintenance). Minor friction: frontmatter says "Build and sharpen" while body uses "Interrogate" as the anchoring leading word — slight identity drift. |

### Axis 2 — Structure

| # | Criterion | Weight | Score | Notes |
|---|-----------|--------|-------|-------|
| 3 | Steps vs. reference clarity | 1x | 80/100 | "File structure" (reference) and "During the session" (trigger-style reference) are cleanly separated. Each subsection co-locates definition, example quote, and rule. Not ordered steps, but the trigger→action pattern is consistent. |
| 4 | Branch-aware disclosure & pointers | 2x | 85/100 | Format files behind pointers with strong wording: "Use the format in [CONTEXT-FORMAT.md]" (line 64), ADR criteria behind "[ADR-FORMAT.md]" (line 71). File-structure examples inline (every branch needs to know where files live). |
| 5 | Conciseness | 2x | 90/100 | 80 lines — well under the 500-line ceiling. Every section carries its weight. No sprawl. |
| 6 | Coherent scope | 1x | 90/100 | One tight discipline: domain model interrogation (glossary + ADRs). Composes cleanly with other skills. No scope creep. |

### Axis 3 — Steering

| # | Criterion | Weight | Score | Notes |
|---|-----------|--------|-------|-------|
| 7 | Leading words | 2x | 85/100 | "Interrogate" (line 10) is a strong, trace-checkable anchor — a sharp upgrade from the prior "actively build and sharpen." "Canonical term" (line 52), "sparingly" (line 69), "glossary and nothing else" (line 66), "stress-test" (line 56) reinforce the tone. |
| 8 | Completion criteria & legwork | 2x | 85/100 | Sharpened: "A term conflicts when it either (a) is absent from CONTEXT.md, or (b) has a different meaning assigned in the glossary" (line 48). "When a term is resolved — the user has confirmed the canonical term and its definition" (line 64). ADR gate is explicit "all three criteria in ADR-FORMAT.md are all met" (line 71). Each trigger has a checkable boundary. |
| 9 | Gotchas section | 2x | 85/100 | Dedicated "Gotchas" section (lines 72-76): three concrete failure patterns — cross-context term collision, code/glossary drift, borderline ADRs. Actionable and grounded. |
| 10 | Grounded in expertise | 2x | 85/100 | Adapted from mattpocock/skills (line 6). Uses DDD concepts (ubiquitous language, context map, bounded contexts). Example quotes are concrete: "Your code cancels entire Orders, but you just said partial cancellation is possible" (line 60). |
| 11 | Avoids railroading | 1x | 85/100 | Procedures with example phrasing, not rigid templates. "Create files lazily" (line 42). ADR gate is judgment-based with a pointer. Doesn't over-prescribe. |

### Axis 4 — Pruning

| # | Criterion | Weight | Score | Notes |
|---|-----------|--------|-------|-------|
| 12 | No-ops (deletion test) | 2x | 80/100 | Most lines change behavior. Line 10's "Interrogate" is a genuine steer upgrade. Line 42 "only when you have something to write" is borderline — the model would default to laziness, but it restates the obvious. One minor candidate. |
| 13 | Single source of truth | 1x | 90/100 | ADR criteria now collapsed to a single pointer: SKILL.md line 71 references ADR-FORMAT.md only. No duplication across the three files. |
| 14 | Relevance & sediment | 1x | 90/100 | No stale layers or dead instructions. Skill is fresh and well-maintained. |

### Conditional criteria

| # | Criterion | Weight | Score | Notes |
|---|-----------|--------|-------|-------|
| 15 | Setup flow | 1x | N/A | Category (code-quality-and-review) not in applicable list. |
| 16 | Memory mechanism | 1x | N/A | Category not in applicable list. |
| 17 | Scripts & libraries | 1x | N/A | Category applies, but this is a pure reference/workflow skill with no scripts or libraries. Override: pattern doesn't fit. |
| 18 | On-demand hooks | 1x | N/A | Category applies, but no hooks to enforce. Override: pattern doesn't fit. |

## Failure Modes Detected

| Mode | Evidence | Root cause | Defense |
|------|----------|------------|---------|
| None detected | — | — | All four modes from the prior evaluation resolved: premature completion (sharpened criteria), duplication (ADR collapsed to pointer), weak steering ("Interrogate" replacement), no-ops (trimmed). |

## Prioritized Actions

### 1. Align frontmatter description with body leading word

**Evidence:** frontmatter line 3 "Build and sharpen" vs body line 10 "Interrogate the project's domain model"

**Fix:** Change frontmatter to `Interrogate a project's domain model as you design.` — matches the body's anchoring word and eliminates identity drift.

## Bonus Patterns

| Pattern | Status | Notes |
|---------|--------|-------|
| Validation loops | Present | Lines 78-80: "Before ending the session, confirm that CONTEXT.md reflects every term resolved this session." |
| Output templates | Present | CONTEXT-FORMAT.md and ADR-FORMAT.md provide concrete templates with examples. |
| Procedures over declarations | Present | Teaches how to approach domain modeling (challenge, sharpen, stress-test, cross-reference) rather than declaring exact output. |
| Defaults over menus | Present | Picks clear defaults: single CONTEXT.md at root unless CONTEXT-MAP.md exists; ADRs only when all three criteria met. |
| Trace-checkable steering | Present | "Interrogate" is distinctive and repeatable. "Canonical term" and "glossary and nothing else" reinforce. |

## Grade Scale

| Grade | Range |
|-------|-------|
| A | 80–100 |
| B | 60–79 |
| C | 40–59 |
| D | 20–39 |
| F | 0–19 |

---

*Generated by [skill-evaluation](https://github.com/fabricioctelles/skills) v2.1.0, merging the [Anthropic skill quality framework](https://claude.com/blog/lessons-from-building-claude-code-how-we-use-skills) with Matt Pocock's [writing-great-skills](https://www.youtube.com/watch?v=UNzCG3lw6O0) methodology.*
