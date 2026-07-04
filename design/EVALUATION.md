# Skill Evaluation — design

> Evaluated: 2026-07-04
> Source: design/SKILL.md
> Evaluator: skill-evaluation v2.1.0
> Framework: [Anthropic Skill Best Practices](https://claude.com/blog/lessons-from-building-claude-code-how-we-use-skills) + Matt Pocock's [writing-great-skills](https://www.youtube.com/watch?v=UNzCG3lw6O0)

## Summary

| Metric | Value |
|---|---|
| Overall Score | 82.12/100 |
| Grade | A |
| Category | business-process-automation |
| Invocation | model-invoked |
| Files | 1 |
| Criteria scored / N/A | 15 scored, 3 N/A |

## Scorecard

### Axis 1 — Trigger

| # | Criterion | Weight | Score | Notes |
|---|---|---|---|---|
| 1 | Invocation design | 2x | 85/100 | Model-invoked is correct: orchestrator must fire autonomously on "design a website" etc. Sub-skills are reachable. No `disable-model-invocation`. |
| 2 | Description quality | 2x | 90/100 | Leading word "Route" anchors invocation. Trigger phrases ("design a website, landing page, dashboard, app shell, or UI") cover primary entry points. Pipeline compressed to "picker → apply → audit". Distiller alternative included. Dense and complete. |

### Axis 2 — Structure

| # | Criterion | Weight | Score | Notes |
|---|---|---|---|---|
| 3 | Steps vs. reference clarity | 1x | 88/100 | Pipeline section is clearly ordered steps (1→2→3, each with "Done when:"). Routing guide table is clearly reference. Taste capture is secondary reference. Completion criteria solidify the step/reference boundary. |
| 4 | Branch-aware disclosure & pointers | 2x | 82/100 | Routing guide covers 5 distinct branches (default pipeline, skip picker, picker-only, audit-only, taste capture). Sub-skill instructions live behind pointers. TASTE.md conflict addressed in gotchas. TASTE.md vs pipeline priority still unresolved when both apply. |
| 5 | Conciseness | 2x | 92/100 | 36 lines including frontmatter. Body no-ops removed. Pipeline is 3 bullets + gate. Routing guide compact. Gotchas added without bloat. Exemplary density for an orchestrator. |
| 6 | Coherent scope | 1x | 85/100 | Tightly scoped to routing design requests. Does not drift into teaching design principles, duplicating sub-skill instructions, or adding configuration. |

### Axis 3 — Steering

| # | Criterion | Weight | Score | Notes |
|---|---|---|---|---|
| 7 | Leading words | 2x | 85/100 | "Route" threaded through description ("Route every design request"), section title ("Routing guide"), and table rows ("route to"). "Done when:" consistent across all three pipeline steps. Both are trace-checkable. Strong anchoring from a compact vocabulary. |
| 8 | Completion criteria & legwork | 2x | 80/100 | Each pipeline step has a checkable "Done when:" — picker returned a DESIGN.md path, apply produced code and stated verification results, audit returned pass or findings block. "If any step fails, stop and report" is the cross-check gate. Solid for a delegated orchestrator. |
| 9 | Gotchas section | 2x | 85/100 | Three well-chosen gotchas: picker fallback to general-purpose DESIGN.md, audit remediation loop (apply→audit up to 3x), TASTE.md check before picker. Covers the three main edge cases for this orchestrator. Compact and actionable. |
| 10 | Grounded in expertise | 2x | 72/100 | References concrete `voltagent/awesome-design-md` catalog. Pick→apply→audit is a defensible design workflow. Gotchas reflect earned experience (3-retry loop, TASTE.md priority). Thin embedded expertise — depth lives in sub-skills, which is expected for an orchestrator. |
| 11 | Avoids railroading | 1x | 80/100 | "Default path"/"Default pipeline" signals suggestion. Routing guide lists alternatives (skip picker, individual sub-skills). Taste capture is a separate, optional path. Agent adapts the procedure. |

### Axis 4 — Pruning

| # | Criterion | Weight | Score | Notes |
|---|---|---|---|---|
| 12 | No-ops (deletion test) | 2x | 88/100 | Previous borderline no-ops removed (old "single entry point" line, "gives every project a distinct identity" framing). Remaining line "Orchestrate the end-to-end design workflow" is borderline — signals orchestrator role to the model but partially restates description. All other lines are essential. |
| 13 | Single source of truth | 1x | 85/100 | Pipeline in description (compressed) and body (detailed with completion criteria) is progression, not duplication. No cross-file duplication. Single source maintained. |
| 14 | Relevance & sediment | 1x | 90/100 | All content serves the orchestrator role. `awesome-design-md` link is current. Skill's small size prevents sediment accumulation. No stale layers. |

### Conditional criteria

| # | Criterion | Weight | Score | Notes |
|---|---|---|---|---|
| 15 | Setup flow | 1x | N/A | Category `business-process-automation` is not in the conditional set for setup flow. |
| 16 | Memory mechanism | 1x | 25/100 | `business-process-automation` qualifies. TASTE.md (via distiller) is persistent memory, and the gotcha "Check for existing TASTE.md before running the picker" is weak memory awareness. No session-tracking, log file, or state persistence across invocations. |
| 17 | Scripts & libraries | 1x | N/A | Category `business-process-automation` is not in the conditional set for scripts & libraries. |
| 18 | On-demand hooks | 1x | N/A | Category `business-process-automation` is not in the conditional set for on-demand hooks. |

## Failure Modes Detected

| Mode | Evidence | Root cause | Defense |
|---|---|---|---|
| Thin expertise | Grounded in expertise score 72 | Orchestrator delegates domain depth to sub-skills; its own expertise is routing decisions only | Acceptable for an orchestrator — increase if sub-skill quality depends on orchestrator knowing more |
| Memory mechanism weak | Memory mechanism score 25; no log file or session tracking | Business-automation benefits from recording pipeline runs for future context | Add a one-line log instruction: "After completing the pipeline, append to `.design-log`: project, DESIGN.md, audit result" |
| Borderline no-op | Body line: "Orchestrate the end-to-end design workflow." partially restates description | Description already signals orchestrator role | Remove or replace with additive framing: "Think of this as a router — it dispatches and stays out of the way" |

## Prioritized Actions

### 1. Add memory mechanism for orchestrator state

**Evidence:** Memory mechanism score 25; no tracking across design sessions.

**Fix:** Add instruction to log each pipeline run: "After completing the pipeline, append a one-line entry to `.design-log` with the project, chosen DESIGN.md, and audit result. This gives future design sessions context on past choices."

### 2. Trim borderline no-op from body

**Evidence:** "Orchestrate the end-to-end design workflow" partially restates the description.

**Fix:** Replace with "This is a router — it dispatches to the right sub-skill and stays out of the way."

### 3. Resolve TASTE.md vs pipeline priority

**Evidence:** Gotcha says "Check for existing TASTE.md before running the picker" but routing guide doesn't integrate this into branch logic.

**Fix:** Add a routing guide row: "TASTE.md exists + 'design X'" → skip picker, route to apply → audit with TASTE.md preferences.

## Bonus Patterns

| Pattern | Status | Notes |
|---|---|---|
| Validation loops | Present | "If audit finds issues, loop apply → audit up to 3 times" (gotchas) |
| Output templates | Absent | No structured output format defined for the orchestrator |
| Procedures over declarations | Present | Pipeline is procedural (1 → 2 → 3), not declarative |
| Defaults over menus | Present | "Default path" with brief alternatives in routing guide |
| Trace-checkable steering | Present | "Route" and "Done when:" are distinctive enough to confirm in agent traces |

## Grade Scale

| Grade | Range |
| A | 80-100 | B | 60-79 | C | 40-59 | D | 20-39 | F | 0-19 |

---

*Generated by [skill-evaluation](https://github.com/fabricioctelles/skills) v2.1.0, merging the [Anthropic skill quality framework](https://claude.com/blog/lessons-from-building-claude-code-how-we-use-skills) with Matt Pocock's [writing-great-skills](https://www.youtube.com/watch?v=UNzCG3lw6O0) methodology.*
