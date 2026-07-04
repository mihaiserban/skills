# Skill Evaluation — research

> Evaluated: 2026-07-04 (Round 3 — final)
> Source: research/SKILL.md
> Evaluator: skill-evaluation v2.1.0
> Framework: [Anthropic Skill Best Practices](https://claude.com/blog/lessons-from-building-claude-code-how-we-use-skills) + Matt Pocock's [writing-great-skills](https://www.youtube.com/watch?v=UNzCG3lw6O0)

## Summary

| Metric | Value |
|--------|-------|
| Overall Score | 84.04/100 |
| Grade | A |
| Category | data-fetching-and-analysis |
| Invocation | user-invoked |
| Files | 1 |
| Criteria scored / N/A | 17 scored, 1 N/A |

## Scorecard

### Axis 1 — Trigger

| # | Criterion | Weight | Score | Notes |
|---|-----------|--------|-------|-------|
| 1 | Invocation design | 2x | 85/100 | User-invoked is correct: the skill should only fire when the user explicitly asks for research, arXiv papers, or academic evidence. Zero context load, and the human-index trade-off is appropriate — research is a deliberate request, not an autonomous trigger. `disable-model-invocation: true` (L5). |
| 2 | Description quality | 2x | 85/100 | User-invoked description: "Research a technical or scientific topic on arXiv when explicitly instructed." (L3) — human-facing one-liner, concise, no unnecessary trigger list. Clean. |

### Axis 2 — Structure

| # | Criterion | Weight | Score | Notes |
|---|-----------|--------|-------|-------|
| 3 | Steps vs. reference clarity | 1x | 82/100 | Six ordered workflow steps (L27–32), followed by reference sections (Search Strategy, Reading Checklist, Gotchas, Synthesis, Memory, Handoff). Clear separation. Synthesis (L84–93) doubles as an output template. Memory (L93–96) sits between Synthesis and Handoff — well-positioned as a post-brief action. Minor: Reading Checklist (L64–74) sits between Search Strategy and Gotchas — conceptually it's a reference appendix, not a step, but it flanks the workflow rather than living clearly within or after it. |
| 4 | Branch-aware disclosure & pointers | 2x | 85/100 | Single-file skill, single branch (arXiv research). All material is inline — appropriate when there's only one branch and the file is 101 lines. No external references to disclose, no variance risk from weak pointers. |
| 5 | Conciseness | 2x | 85/100 | 101 lines — lean, well under the 500-line ceiling. Every section earns its place: Setup (5 lines), Workflow (6 lines), Search Strategy (18 lines), Reading Checklist (10 lines), Gotchas (4 lines), Synthesis (11 lines), Memory (3 lines), Handoff (5 lines). No filler paragraphs. |
| 6 | Coherent scope | 1x | 88/100 | Single, focused purpose: search arXiv, filter papers, synthesize into a primary-source brief. Composes cleanly with design and engineering skills via Handoff (L99–100). The Handoff section explicitly enables downstream work. |

### Axis 3 — Steering

| # | Criterion | Weight | Score | Notes |
|---|-----------|--------|-------|-------|
| 7 | Leading words | 2x | 82/100 | "primary-source brief" (L11, L32, L84) is a compact, distinctive anchor — trace-checkable via grep and repeated across Overview, Workflow step 6, and Synthesis heading. "evidence-grounded" (L11) reinforces the same idea. These recruit priors around rigor and sourcing. The description (L3) lacks a leading word, but user-invoked descriptions don't need one for invocation — the leading words work in the body to steer behavior. |
| 8 | Completion criteria & legwork | 2x | 85/100 | Step 2: "≥3 keyword variants, ≥5 candidates" (L28) — checkable, exhaustive floor. Step 3: "Tag each candidate as primary/secondary/irrelevant before proceeding" (L29) — checkable, prevents skipping. Reading Checklist (L64–74) provides an exhaustiveness bar ("For each useful paper, capture:"). Synthesis (L84–93) defines the output shape with labeled fields. Memory (L93–96) adds a concrete completion action: append to `.research-log`. Strong and now end-to-end. |
| 9 | Gotchas section | 2x | 88/100 | Dedicated Gotchas section (L76–80) with three actionable items: (1) don't overfit to abstracts — open the paper, (2) "arvix" typo handling, (3) be honest about inconclusive results. Each addresses a specific failure pattern, not a generic warning. |
| 10 | Grounded in expertise | 2x | 72/100 | Search patterns (`site:arxiv.org` queries, `arxiv` Python package) are concrete and practical. Reading checklist is realistic (problem, method, assumptions, limitations). However, the skill lacks cited methodology sources — the research workflow (search → filter → synthesize) is presented as self-evident rather than grounded in research-methods literature or observed evaluation outcomes. No external anchor like Pocock/Anthropic for the workflow design itself. |
| 11 | Avoids railroading | 1x | 80/100 | Six-step procedure leaves judgment room: "≥3 keyword variants" is a floor, not a ceiling; "Prefer papers that are:" (L56–62) gives preferences, not mandates; Handoff says "if that is part of the same request" (L99). Fallback search (L45–52) acknowledges constrained environments. Memory is a lightweight suggestion ("append a one-line entry") rather than a mandate. Good balance of structure and flexibility. |

### Axis 4 — Pruning

| # | Criterion | Weight | Score | Notes |
|---|-----------|--------|-------|-------|
| 12 | No-ops (deletion test) | 2x | 88/100 | Clean. The "arvix" typo line that was previously duplicated in Overview has been removed — it lives only in Gotchas (L79) where it belongs. No remaining lines that can be deleted without changing behavior. Search Strategy code blocks, Reading Checklist fields, Synthesis template, and Memory mechanism all add new behavior the model wouldn't default to. |
| 13 | Single source of truth | 1x | 85/100 | "arvix" typo handling was moved from Overview to Gotchas only (L79) — duplication fixed. The Overview's "Prefer primary sources from arXiv" (L11) and the "Prefer papers that are:" list (L56–62) overlap conceptually but serve different purposes (overview vs. search guidance) — acceptable. Single file, no external duplication risk. |
| 14 | Relevance & sediment | 1x | 90/100 | Fresh skill — no stale layers visible. Setup uses current `pip install arxiv` (L19). All sections align with the skill's purpose. No version-history sediment, no outdated references. The fallback from `arxiv` package to web search (L23) is forward-looking, not stale. Memory section (.research-log) is a fresh, well-scoped addition. |

### Conditional criteria

| # | Criterion | Weight | Score | Notes |
|---|-----------|--------|-------|-------|
| 15 | Setup flow | 1x | 85/100 | Setup section (L17–23) with `pip install arxiv` and a fallback note ("If `arxiv` is unavailable, use web access…"). Clean, actionable, covers both happy and degraded paths. |
| 16 | Memory mechanism | 1x | 80/100 | Memory section added (L93–96): "After producing a primary-source brief, append a one-line entry to `.research-log` with the topic, date, and key finding. Future invocations can reference past briefs." Provides cross-invocation continuity without heavyweight infrastructure — a file-based log that future sessions can read. The mechanism is lightweight but sufficient: one-line entries are easy to write, easy to scan, and non-disruptive. |
| 17 | Scripts & libraries | 1x | 85/100 | Integrates the `arxiv` Python package (L36–43) with a concrete usage example — `arxiv.Search`, `arxiv.SortCriterion.Relevance`, iteration over results. Fallback to `site:arxiv.org` web searches (L45–52) provides a degraded path. Library is directly tied to the skill's core workflow. |
| 18 | On-demand hooks | 1x | N/A | Not in applicable categories for data-fetching-and-analysis. Research is an interactive, human-triggered workflow — no CI/CD or review hook applies. |

## Failure Modes Detected

| Mode | Evidence | Root cause | Defense |
|------|----------|------------|---------|
| Methodology grounding | SKILL.md lacks external citation for the research workflow design | Workflow is presented as self-evident rather than grounded in research-methods literature | Add a brief methodology note: "This workflow adapts evidence-synthesis patterns from systematic review methodology — search broadly, filter strictly, synthesize with citations." |

## Prioritized Actions

### 1. Ground the methodology with a citation

**Evidence:** Criterion #10 — workflow lacks external methodology grounding

**Fix:** Add a brief methodology note: "This workflow adapts evidence-synthesis patterns from systematic review methodology — search broadly, filter strictly, synthesize with citations." One sentence anchors the approach without bloating the file.

## Changes Since Round 2

| Change | Criterion impacted | Score delta | Notes |
|--------|-------------------|-------------|-------|
| "arvix" typo deduplication (removed from Overview, kept in Gotchas) | #12 No-ops, #13 SSOT | #12: 72→88 (+16), #13: 68→85 (+17) | Both axes improved — no remaining no-ops, single source of truth restored |
| Memory section added (.research-log) | #16 Memory | 0→80 (+80) | Cross-invocation continuity via file-based log — lightweight and sufficient |
| Memory section positioning | #3 Steps, #8 Completion | #3: 80→82 (+2), #8: 82→85 (+3) | Memory sits cleanly between Synthesis and Handoff; adds a concrete completion step |

## Bonus Patterns

| Pattern | Status | Notes |
|---------|--------|-------|
| Validation loops | Absent | No explicit instruction for the agent to self-check the brief before finalizing. The Reading Checklist and Synthesis template provide structure but no verification step. Consider adding: "Before returning, re-read the brief against each question field — is every field substantive?" |
| Output templates | Present | Synthesis (L84–93) defines a structured output with named fields: `Question`, `Papers`, `Findings`, `Recommendation`, `Risks`, `Practical notes`. Field labels are concrete and self-checking. |
| Procedures over declarations | Present | The workflow teaches *how to research* (restate question → search variants → tag → read → synthesize), not *what to conclude*. The "Prefer papers that are:" list gives criteria, not a fixed paper selection. |
| Defaults over menus | Present | Defaults: arXiv as primary source, arxiv Python package, 10 results, sort by relevance. Fallback: web search with `site:arxiv.org`. Alternatives mentioned briefly without overwhelming menus. |
| Trace-checkable steering | Present | "primary-source brief" and "evidence-grounded" are distinctive enough to grep in agent reasoning traces and confirm the skill steered behavior. The compound phrase "primary-source brief" is unlikely to appear by default. |
| Cross-invocation memory | Present | `.research-log` file-based persistence — one-line entries with topic, date, and key finding. Future invocations can reference past briefs. |

## Grade Scale

| Grade | Range | Meaning |
|-------|-------|---------|
| A | 80–100 | Production-quality, reference skill |
| B | 60–79 | Good skill, minor improvements needed |
| C | 40–59 | Functional but significant gaps |
| D | 20–39 | Needs substantial rework |
| F | 0–19 | Skeleton only, not production-ready |

---

*Generated by [skill-evaluation](https://github.com/fabricioctelles/skills) v2.1.0, merging the [Anthropic skill quality framework](https://claude.com/blog/lessons-from-building-claude-code-how-we-use-skills) with Matt Pocock's [writing-great-skills](https://www.youtube.com/watch?v=UNzCG3lw6O0) methodology.*
