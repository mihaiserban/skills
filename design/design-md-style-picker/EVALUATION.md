# Skill Evaluation — design-md-style-picker
> Evaluated: 2026-07-04
> Source: design/design-md-style-picker/SKILL.md
> Evaluator: skill-evaluation v2.1.0
> Framework: [Anthropic Skill Best Practices](https://claude.com/blog/lessons-from-building-claude-code-how-we-use-skills) + Matt Pocock's [writing-great-skills](https://www.youtube.com/watch?v=UNzCG3lw6O0)

## Summary
| Metric | Value |
|---|---|
| Overall Score | 84.17/100 |
| Grade | A |
| Category | library-and-api-reference |
| Invocation | model-invoked |
| Files | 3 (SKILL.md, agents/openai.yaml, references/selection-rubric.md) |
| Criteria scored / N/A | 15 scored, 3 N/A |

## Scorecard
### Axis 1 — Trigger
| # | Criterion | Weight | Score | Notes |
|---|---|---|---|---|
| 1 | Invocation design | 2x | 85/100 | Model-invoked is the correct choice. Composes with `design-md-style-apply` (explicit handoff at line 83), reached by parent `design` skill. No `disable-model-invocation` present. |
| 2 | Description quality | 2x | 75/100 | Leading word "Choose" up front. Trigger branches still have some synonym overlap ("design direction" / "what style to use" / "product brief without a clear visual system" all describe lacking direction). Final clause "Codex should select a DESIGN.md profile before building" is functional but partly restates purpose. |

### Axis 2 — Structure
| # | Criterion | Weight | Score | Notes |
|---|---|---|---|---|
| 3 | Steps vs. reference clarity | 1x | 90/100 | Clean separation: Prerequisites (lines 12-22) → Catalog Workflow (numbered steps, lines 24-47) → Selection Rules (lines 49-56) → Gotchas (lines 58-62) → Recommendation Format (lines 64-82). Material is well co-located within each section. Prerequisites addition improves navigability. |
| 4 | Branch-aware disclosure & pointers | 2x | 85/100 | Two conditional context pointers: `references/selection-rubric.md` ("when the brief is ambiguous or more than one style could work", line 45), and TASTE.md ("If present", line 47). Prerequisites section (lines 12-22) adds explicit pointer to script location with environment-variable fallback. Minor: rubric pointer wording ("Read") could be stronger ("Must read"). |
| 5 | Conciseness | 2x | 90/100 | 83 lines total — well under the 500-line ceiling. Prerequisites (+10 lines) and Gotchas (+5 lines) are earned additions. No sprawl. |
| 6 | Coherent scope | 1x | 90/100 | Single purpose: pick a DESIGN.md source aesthetic. Composes with `design-md-style-apply` (line 83). Does not apply, build, or audit — clean boundary unchanged. |

### Axis 3 — Steering
| # | Criterion | Weight | Score | Notes |
|---|---|---|---|---|
| 7 | Leading words | 2x | 70/100 | Domain vocabulary present ("source aesthetic", "Design DNA to preserve", "signature gesture"). Gotchas section adds concrete behavioral terms ("accent color", "shallow skin", "mixed styles"). DNA categories (Color, Typography, Layout, Components, Signature gesture) now double as completion anchors. Still lacks compact trace-checkable terms in core Selection Rules. |
| 8 | Completion criteria & legwork | 2x | 90/100 | Previously scored 60 — now sharpened: "Done when every DNA category is filled with at least one concrete design move from the source. Mark any category you cannot fill and explain why in 'Avoid'" (lines 66-67). Checkable, exhaustive, and self-verifying. Individual workflow steps remain checkable (`ensure` → `search` → `show` → read rubric → look for TASTE.md). |
| 9 | Gotchas section | 2x | 85/100 | Previously scored 30 — now has an explicit Gotchas section (lines 58-62) with three concrete footguns: accent-color-only trap, marketing-to-data mismatch, mixed-styles pitfall. Complements the rubric's "Red Flags" section (references/selection-rubric.md:27-33) with condensed actionable guidance. |
| 10 | Grounded in expertise | 2x | 85/100 | Strong domain expertise: concrete category-to-source mappings (lines 55), practical decision heuristics ("If the product sells trust, prefer disciplined palette", rubric lines 22-26), and product-fit reasoning drawn from real design practice. Unchanged from prior evaluation. |
| 11 | Avoids railroading | 1x | 80/100 | Procedures over declarations: steps guide exploration rather than prescribe answers. Allows secondary sources (line 53), conditional TASTE.md override (lines 50-51), and multiple valid style-source matches. The output template remains a recommendation format, not a rigid structure. |

### Axis 4 — Pruning
| # | Criterion | Weight | Score | Notes |
|---|---|---|---|---|
| 12 | No-ops (deletion test) | 2x | 85/100 | Previously scored 65 — TASTE.md duplication removed from Overview (line 10: no longer mentions TASTE.md). Step 5 (line 47) is now the single operative instruction. Overview summary ("Return a decisive recommendation, the selected DESIGN.md path, and the design moves...") is a reasonable top-level framing, not duplication of the output template. |
| 13 | Single source of truth | 1x | 85/100 | Previously scored 75 — TASTE.md now lives in one place (Step 5, line 47). Gotchas content in SKILL.md is condensed guidance; rubric's "Red Flags" is deeper reference — appropriate abstraction layers. No new duplications introduced. |
| 14 | Relevance & sediment | 1x | 90/100 | Previously scored 70 — hardcoded machine-local path `/Users/mitzuuuu/.agents/skills/scripts/design_md_catalog.py` replaced with `$SKILLS_SCRIPTS/design_md_catalog.py` with a `scripts/` relative fallback (lines 18-21). All content is current and relevant. No sediment risk. |

### Conditional criteria
| # | Criterion | Weight | Score | Notes |
|---|---|---|---|---|
| 15 | Setup flow | 1x | 85/100 | Previously scored 40 — now has an explicit Prerequisites section (lines 12-22) documenting Python 3 requirement, the catalog script location with environment-variable and fallback, and how to run `ensure`. The `ensure` subcommand implies first-run setup exists in the script. |
| 16 | Memory mechanism | 1x | N/A | Not applicable to library-and-api-reference. |
| 17 | Scripts & libraries | 1x | N/A | Not applicable to library-and-api-reference. |
| 18 | On-demand hooks | 1x | N/A | Not applicable to library-and-api-reference. |

## Failure Modes Detected
| Mode | Evidence | Root cause | Defense |
|---|---|---|---|
| Weak steering | No compact trace-checkable leading words in Selection Rules; agent execution on "Design DNA to preserve" depends on model interpretation (lines 66-82) | Reliance on domain vocabulary rather than behavioral anchors | Introduce stronger leading words ("precise", "quiet", "dense") inside Selection Rules that would confirm in traces the skill fired |
| Description overlap | Trigger branches "design direction" = "what style to use" = "product brief without a clear visual system" are near-duplicates (description field, line 3) | Expanding trigger coverage through synonyms | Collapse to 2-3 distinct trigger scenarios rather than 4 variants of the same need |

## Resolved from Prior Evaluation
| Mode | Fix applied | Where |
|---|---|---|
| TASTE.md duplication | Removed from Overview (was line 10). Step 5 is sole source of truth. | SKILL.md:47 |
| Premature completion | Replaced "enough to act" with "every DNA category is filled" criterion. | SKILL.md:66-67 |
| Missing Gotchas | Three-item Gotchas section added. | SKILL.md:58-62 |
| Missing Prerequisites | Prerequisites section with Python 3, script location, fallback. | SKILL.md:12-22 |
| Hardcoded script paths | Replaced with `$SKILLS_SCRIPTS` + `scripts/` fallback. | SKILL.md:17-21 |

## Bonus Patterns
| Pattern | Status | Notes |
|---|---|---|
| Validation loops | Absent | No self-check mechanism before delivering the recommendation |
| Output templates | Present | Recommendation Format block (lines 68-82) provides clear output structure |
| Procedures over declarations | Present | Steps teach how to explore and decide, not what answer to give |
| Defaults over menus | Present | Selection Rules provide defaults (prefer product fit, prefer one source) with brief alternatives (second source only to fill gaps) |
| Trace-checkable steering | Absent | No distinctive behavioral anchor terms that would confirm the skill fired in agent traces |

## Grade Scale
| Grade | Range | Meaning |
| A | 80-100 | Production-quality |
| B | 60-79 | Good, minor improvements |
| C | 40-59 | Functional but significant gaps |
| D | 20-39 | Needs substantial rework |
| F | 0-19 | Skeleton only |

---

*Generated by [skill-evaluation](https://github.com/fabricioctelles/skills) v2.1.0, merging the [Anthropic skill quality framework](https://claude.com/blog/lessons-from-building-claude-code-how-we-use-skills) with Matt Pocock's [writing-great-skills](https://www.youtube.com/watch?v=UNzCG3lw6O0) methodology.*
