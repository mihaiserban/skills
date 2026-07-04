# Skill Evaluation — design-md-style-audit

> Evaluated: 2026-07-04
> Source: design/design-md-style-audit/SKILL.md
> Evaluator: skill-evaluation v2.1.0
> Framework: [Anthropic Skill Best Practices](https://claude.com/blog/lessons-from-building-claude-code-how-we-use-skills) + Matt Pocock's [writing-great-skills](https://www.youtube.com/watch?v=UNzCG3lw6O0)

## Summary

| Metric | Value |
|--------|-------|
| Overall Score | 82.29/100 |
| Grade | A |
| Category | product-verification |
| Invocation | model-invoked |
| Files | 4 |
| Criteria scored / N/A | 15 scored, 3 N/A |

## Scorecard

### Axis 1 — Trigger

| # | Criterion | Weight | Score | Notes |
|---|-----------|--------|-------|-------|
| 1 | Invocation design | 2x | 80/100 | Model-invoked without `disable-model-invocation`. Appropriate for a product-verification skill that other skills or the agent should reach autonomously. Pays modest context load (one-line description) for autonomous reachability. |
| 2 | Description quality | 2x | 85/100 | Leading word "Audit" up front. One trigger per branch: "reviewing visual consistency," "finding design drift," "producing concrete fixes." No redundant identity rehashing body content. Tight and scannable for the model. |

### Axis 2 — Structure

| # | Criterion | Weight | Score | Notes |
|---|-----------|--------|-------|-------|
| 3 | Steps vs. reference clarity | 1x | 75/100 | Clear separation: "Resolve Inputs" (steps, commands) then "Audit Pass" (reference dimensions). Material co-located — audit dimensions live together, findings format lives together. Minor: the Overview blends summary with reference-like advice that overlaps with audit dimensions. |
| 4 | Branch-aware disclosure & pointers | 2x | 70/100 | References disclosed behind pointers: `references/audit-rubric.md`, `references/preflight-rubric.md`, and `TASTE.md` when present. Pointer wording for TASTE.md is conditional ("if present") — good. But the two rubric references lack explicit branch-scoping ("if you need X, read Y") — a weak pointer to must-have material introduces variance. |
| 5 | Conciseness (no sprawl) | 2x | 90/100 | 65 lines total — well under the 500-line ceiling. Every heading earns its context cost. No sprawl. |
| 6 | Coherent scope | 1x | 90/100 | Does exactly one thing: audit visual consistency against a DESIGN.md source. Doesn't drift into building, fixing, or re-designing. Composes well with design-md-style-picker and design-md-style-apply. |

### Axis 3 — Steering

| # | Criterion | Weight | Score | Notes |
|---|-----------|--------|-------|-------|
| 7 | Leading words | 2x | 75/100 | Strong anchor: "Audit" in the description. Distinctive audit dimensions: "Source DNA," "Taste fit," "Product translation," "Execution discipline." Priority labels P1/P2/P3 are compact and actionable. Trace-checkable: a grep for "Source DNA" or "execution discipline" in traces confirms the skill fired. |
| 8 | Completion criteria & legwork | 2x | 85/100 | Exhaustiveness bar: "Score every dimension — do not skip any. If a dimension doesn't apply, state why." The findings format template is checkable (Findings list with priorities, Style Fit block). Each audit pass dimension drives legwork over the reference. |
| 9 | Gotchas section | 2x | 90/100 | Three concrete, non-obvious items: (1) screenshot-required insight about spacing/rhythm hiding from code inspection, (2) "accent-only styling" as the most common failure mode, (3) "token dilution" as a subtle consistency erosion. All read as experience-driven, not generic. |
| 10 | Grounded in expertise | 2x | 80/100 | Gotchas items and audit dimensions feel domain-specific (typography scaling, component geometry, density, motion appropriateness). Not generic "be thorough" advice. Minor: could cite specific projects or observed failures. |
| 11 | Avoids railroading | 1x | 80/100 | Provides a procedure (dimensions → score → findings), not rigid output declarations. Priority levels are guidelines. Leaves room for judgment in distinguishing P2 from P3. |

### Axis 4 — Pruning

| # | Criterion | Weight | Score | Notes |
|---|-----------|--------|-------|-------|
| 12 | No-ops (deletion test) | 2x | 85/100 | Line 10 ("Focus on visible design drift…") — the examples sharpen what "drift" means, not a restatement. Line 22 ("Inspect the implemented UI through code, screenshots, or a running app") — suggests inspection modes, not obvious by default since screenshot emphasis is a gotcha insight. No clear no-ops detected. |
| 13 | Single source of truth | 1x | 85/100 | `$SKILLS_SCRIPTS` replaced hardcoded path (post-improvement). TASTE.md reference collapsed to a single conditional read rather than duplicated across sections. Audit dimensions and findings format each live in one place. |
| 14 | Relevance & sediment | 1x | 90/100 | Fresh skill with no stale layers. All content directly serves the audit workflow. |

### Conditional criteria

| # | Criterion | Weight | Score | Notes |
|---|-----------|--------|-------|-------|
| 15 | Setup flow | 1x | N/A | product-verification is not in the applicable categories (library-and-api-reference, data-fetching-and-analysis, ci-cd-and-deployment, infrastructure-operations). |
| 16 | Memory mechanism | 1x | N/A | product-verification is not in the applicable categories (business-process-automation, data-fetching-and-analysis, runbooks). |
| 17 | Scripts & libraries | 1x | 75/100 | product-verification is in the applicable set. Uses `$SKILLS_SCRIPTS/design_md_catalog.py` to resolve style slugs — appropriate helper. Could be stronger by documenting the script's contract (expected output shape) inline rather than requiring the agent to run it blind. |
| 18 | On-demand hooks | 1x | N/A | product-verification is not in the applicable categories (code-quality-and-review, ci-cd-and-deployment). |

## Failure Modes Detected

| Mode | Evidence | Root cause | Defense |
|------|----------|------------|---------|
| Weak steering (mild) | SKILL.md:18–19 — `python3 "$SKILLS_SCRIPTS/design_md_catalog.py" ensure` then `path runwayml` — no inline guidance on what the output shape means | The agent may not know how to parse or act on script output | Add a one-line note: "Output is a single file path on stdout." |
| Weak steering (mild) | SKILL.md:22 — "Read the selected source file, `references/audit-rubric.md`, and `references/preflight-rubric.md`" without why | The agent may skip the rubric read or not know what to extract | Add branch-scoping: "read `references/audit-rubric.md` for the dimension scoring framework; read `references/preflight-rubric.md` for layout/state checks." |

## Prioritized Actions

### 1. Sharpen pointer wording for rubric references

**Evidence:** SKILL.md:22

**Fix:** Replace "Read the selected source file, `references/audit-rubric.md`, and `references/preflight-rubric.md`" with "Read `references/audit-rubric.md` — it defines how to score each dimension. Read `references/preflight-rubric.md` — it covers layout rules, component states, and the checks that make Execution discipline measurable."

### 2. Inline script contract for design_md_catalog.py

**Evidence:** SKILL.md:17–19

**Fix:** Add a one-line note: "Each variant resolves to a single file path printed to stdout. The `show` variant also dumps the source's frontmatter for quick scanning."

### 3. (Bonus) Consider a leading word for "drift"

**Evidence:** SKILL.md:10 — "Focus on visible design drift…" is descriptive but could be sharper.

**Fix:** Lift "design drift" into the audit dimensions as a checkable signal (e.g., under Execution discipline: "Every drift found gets a line in Findings") to make it trace-checkable.

## Bonus Patterns

| Pattern | Status | Notes |
|---------|--------|-------|
| Validation loops | Present | The "Audit Pass" dimensions serve as a checklist — "Score every dimension — do not skip any" is a validation loop. |
| Output templates | Present | "Findings Format" provides a concrete template with priority labels, Style Fit block, and structure. |
| Procedures over declarations | Present | Teaches _how to audit_ (dimension-by-dimension, with priorities) rather than what to produce for one case. |
| Defaults over menus | Present | Priority levels (P1/P2/P3) are defaults with judgment room — no exhaustive menu of severity categories. |
| Trace-checkable steering | Present | "Source DNA," "Taste fit," "Product translation," "Execution discipline" are distinctive enough to grep in traces and confirm the skill fired. |

## Grade Scale

| Score | Grade |
|-------|-------|
| 80–100 | A |
| 60–79 | B |
| 40–59 | C |
| 20–39 | D |
| 0–19 | F |

---

*Generated by [skill-evaluation](https://github.com/fabricioctelles/skills) v2.1.0, merging the [Anthropic skill quality framework](https://claude.com/blog/lessons-from-building-claude-code-how-we-use-skills) with Matt Pocock's [writing-great-skills](https://www.youtube.com/watch?v=UNzCG3lw6O0) methodology.*
