# Skill Evaluation — design-taste-distiller

> Evaluated: 2026-07-04
> Source: design/design-taste-distiller/SKILL.md
> Evaluator: skill-evaluation v2.1.0
> Framework: [Anthropic Skill Best Practices](https://claude.com/blog/lessons-from-building-claude-code-how-we-use-skills) + Matt Pocock's [writing-great-skills](https://www.youtube.com/watch?v=UNzCG3lw6O0)

## Summary

| Metric | Value |
|--------|-------|
| Overall Score | 85.00/100 |
| Grade | A |
| Category | code-scaffolding-and-templates |
| Invocation | model-invoked |
| Files | 4 (SKILL.md, agents/openai.yaml, references/taste-rubric.md, scripts/taste_scaffold.py) |
| Criteria scored / N/A | 15 scored, 3 N/A |

## Scorecard

### Axis 1 — Trigger

| # | Criterion | Weight | Score | Notes |
|---|-----------|--------|-------|-------|
| 1 | Invocation design | 2x | 85/100 | Model-invoked, correctly omits `disable-model-invocation`. Reachable by other design skills (picker, apply, audit). Description is model-facing with dense trigger phrases. |
| 2 | Description quality | 2x | 90/100 | Names the output (TASTE.md), lists 6+ trigger patterns, specifies input types. Slightly long but every phrase earns its context cost. |

### Axis 2 — Structure

| # | Criterion | Weight | Score | Notes |
|---|-----------|--------|-------|-------|
| 3 | Steps vs. reference clarity | 1x | 88/100 | Seven-step workflow is sequential and clean. Reference material (TASTE.md Shape, Quality Bar) is partitioned after steps. Step 4 now defer to rubric with one-liner bullets — improved separation. |
| 4 | Branch-aware disclosure & pointers | 2x | 85/100 | Both previous issues resolved: hardcoded path replaced with `$SKILLS_SCRIPTS` (line 27), and taste-rubric.md has two explicit pointers — step 4 "Add execution controls as defined in the taste rubric (see `references/taste-rubric.md`)" (line 52) and Quality Bar "For the full rubric and execution control definitions, see `references/taste-rubric.md`" (line 121). Pointers are well-worded: each tells the agent why to follow the link. |
| 5 | Conciseness | 2x | 82/100 | 131 lines. Step 4 execution controls now one-liners pointing to rubric (was ~6 lines of duplicate detail). Mild redundancy between Quality Bar and workflow steps persists (e.g., "falsifiable" in both). |
| 6 | Coherent scope | 1x | 92/100 | Single clear job: distill references into TASTE.md. "Using With DESIGN.md" integrates cleanly into the broader skill pack without scope creep. |

### Axis 3 — Steering

| # | Criterion | Weight | Score | Notes |
|---|-----------|--------|-------|-------|
| 7 | Leading words | 2x | 90/100 | Strong vocabulary: "distill", "falsifiable", "anti-taste", "critique loop", "Execution Dials", "Design Locks", "Preflight Checks". Trace-checkable in agent reasoning. |
| 8 | Completion criteria & legwork | 2x | 76/100 | Improved from prior evaluation: "A strong TASTE.md lets another agent decide whether to pick Linear or Runway for a brief — aim for that level of decision guidance" (line 119) is a strong benchmark. "Target 1 to 3 pages" (line 71) is measurable. Still no explicit stop-check — "Fill it with real judgment" (line 30) remains soft. The rubric pointer (line 121) lets the agent self-audit against the "Good Output" section of taste-rubric.md. |
| 9 | Gotchas section | 2x | 80/100 | Good gotchas embedded in Quality Bar: "don't copy a famous brand's identity", "make taste falsifiable", "mechanical where possible". taste-rubric.md is now correctly cross-referenced, making its anti-default patterns and weak-rule examples (e.g., "Make it modern" vs. "Prefer X over Y when Z") accessible during execution. |
| 10 | Grounded in expertise | 2x | 92/100 | Concrete taste axes, specific anti-patterns, executable dial guidance per brief type. Genuine design judgment via taste-rubric.md, not generic advice. |
| 11 | Avoids railroading | 1x | 85/100 | "Use this structure unless the project already has a taste document" (line 78). Flexible input acceptance. Template is default, not mandate. |

### Axis 4 — Pruning

| # | Criterion | Weight | Score | Notes |
|---|-----------|--------|-------|-------|
| 12 | No-ops (deletion test) | 2x | 80/100 | Step 4 one-liners (lines 53-56) are now index-like references to rubric sections — they guide without repeating. Mild overlap: "Make taste falsifiable" appears in both Quality Bar (line 112) and workflow step 2's implicit signals. "If inputs are files, inspect them directly" (line 24) is borderline — agents do this by default but the explicit instruction improves reliability. |
| 13 | Single source of truth | 1x | 82/100 | Step 4 (lines 52-56) now defers to taste-rubric.md instead of repeating execution control definitions. The one-liner bullets name controls without duplicating the rubric's detailed definitions. Mild SSOT variance: "Design Read" in SKILL.md is called "a one-line" (line 53) while taste-rubric.md defines it as "one sentence" — inconsequential but distinct phrasing. |
| 14 | Relevance & sediment | 1x | 88/100 | No sediment. Every section is actively used. Last line (line 131) suggesting other design skills is mildly tangential but serves workflow integration. |

### Conditional criteria

| # | Criterion | Weight | Score | Notes |
|---|-----------|--------|-------|-------|
| 15 | Setup flow | 1x | N/A | Not applicable for code-scaffolding-and-templates. |
| 16 | Memory mechanism | 1x | N/A | Not applicable for code-scaffolding-and-templates. |
| 17 | Scripts & libraries | 1x | 85/100 | `taste_scaffold.py` is well-structured: argparse, clean function decomposition, handles empty inputs, filters by text suffixes. Self-contained with no external deps. The bash invocation in SKILL.md (line 27) now uses `$SKILLS_SCRIPTS` instead of a hardcoded machine path — the previous evaluation's primary defect is resolved. |
| 18 | On-demand hooks | 1x | N/A | Not applicable for code-scaffolding-and-templates. |

## Failure Modes Detected

| Mode | Evidence | Root cause | Defense |
|------|----------|------------|---------|
| Mild duplication (Quality Bar / workflow) | SKILL.md:112 "Make taste falsifiable" and SKILL.md:41-44 step 2's Separated signals both address falsifiability of taste rules | Quality Bar restates principles from the workflow's generated output shape | Accept as reinforcing echo — the Quality Bar is an audit checklist, not redundant instruction |

All four failure modes from the prior evaluation (hardcoded machine path, buried reference, weak completion criteria, duplication across pointer) are resolved in this version.

## Prioritized Actions

### 1. Add an explicit stop-check to the workflow

**Evidence:** SKILL.md line 30 ("Fill it with real judgment from the references") — the agent has no mechanical gate to self-assess completeness.

**Fix:** Add a step 8 after "Keep it compact": "8. Self-audit against taste-rubric.md §Good Output: can a generic design agent decide Linear vs. Runway, card existence, and color/type/imagery leadership from this TASTE.md? If not, iterate on sections 2–4."

### 2. Consider an env-var fallback for `$SKILLS_SCRIPTS`

**Evidence:** SKILL.md line 27 uses `$SKILLS_SCRIPTS` which is acceptable per repo AGENTS.md but has no fallback if unset.

**Fix:** Either document `SKILLS_SCRIPTS` in the README setup section, or add a fallback: `"${SKILLS_SCRIPTS:-$(dirname "$0")/..}"`.

## Bonus Patterns

| Pattern | Status | Notes |
|---------|--------|-------|
| Validation loops | Present | Quality Bar and critique loop create self-check. "Make taste falsifiable" and "mechanical where possible" enforce auditability. taste-rubric.md §Good Output provides concrete audit criteria. |
| Output templates | Present | TASTE.md Shape section provides a complete output template with 11 pre-filled sections. |
| Procedures over declarations | Present | Seven-step workflow is procedural. Template is offered as default, not mandate. |
| Defaults over menus | Present | "Use this structure unless the project already has a taste document." No exhaustive menus. |
| Trace-checkable steering | Present | Leading words ("falsifiable", "anti-taste", "Design Locks", "Preflight Checks") are distinctive and would appear verbatim in agent reasoning. |

## Grade Scale

| Grade | Range |
|-------|-------|
| A | 80-100 |
| B | 60-79 |
| C | 40-59 |
| D | 20-39 |
| F | 0-19 |

---

*Generated by [skill-evaluation](https://github.com/fabricioctelles/skills) v2.1.0, merging the [Anthropic skill quality framework](https://claude.com/blog/lessons-from-building-claude-code-how-we-use-skills) with Matt Pocock's [writing-great-skills](https://www.youtube.com/watch?v=UNzCG3lw6O0) methodology.*
