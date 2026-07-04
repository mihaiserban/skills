# Skill Evaluation — design-md-style-apply

> Evaluated: 2026-07-04
> Source: design/design-md-style-apply/SKILL.md
> Evaluator: skill-evaluation v2.1.0
> Framework: [Anthropic Skill Best Practices](https://claude.com/blog/lessons-from-building-claude-code-how-we-use-skills) + Matt Pocock's [writing-great-skills](https://www.youtube.com/watch?v=UNzCG3lw6O0)

## Summary

| Metric | Value |
|--------|-------|
| Overall Score | 82.12/100 |
| Grade | A |
| Category | code-scaffolding-and-templates |
| Invocation | model-invoked |
| Files | 3 (SKILL.md, references/translation-workflow.md, references/execution-discipline.md) |
| Criteria scored / N/A | 15 scored, 3 N/A |

## Scorecard

### Axis 1 — Trigger

| # | Criterion | Weight | Score | Notes |
|---|-----------|--------|-------|-------|
| 1 | Invocation design | 2x | 70/100 | Model-invoked is correct: the skill must fire autonomously when a user says "build in the Linear style" or "apply Stripe's design". Context-load cost is justified — the parent `design` orchestrator and direct user requests both need automatic reach. |
| 2 | Description quality | 2x | 75/100 | Leading action "Apply" anchors the description. Four distinct branches (names a style/brand, provides a path, asks to build in same style, wants translation) — each a genuine trigger, not synonyms. Slightly verbose but no identity redundancy with the body. |

### Axis 2 — Structure

| # | Criterion | Weight | Score | Notes |
|---|-----------|--------|-------|-------|
| 3 | Steps vs. reference clarity | 1x | 85/100 | Translation Workflow (§) is unambiguously ordered steps. Guardrails (§) is reference/rules. Final Response (§) is an output spec. Clean distinction, co-located concepts. |
| 4 | Branch-aware disclosure & pointers | 2x | 78/100 | References correctly pushed behind pointers: "load … plus `references/translation-workflow.md` and `references/execution-discipline.md`". TASTE.md pointer is branch-conditional ("if present"). Catalog scripts disclosed only for resolve-source branch. `$SKILLS_SCRIPTS` improves portability from the previous hardcoded path. Minor weakness: reference-loading wording is unconditional-instruction, though the material is always needed, making this a style note rather than a variance bug. |
| 5 | Conciseness | 2x | 90/100 | SKILL.md is 86 lines — well under the 500-line ceiling. Heavy reference material (translation workflow details, execution discipline) lives in separate files. Every section earns its context cost. |
| 6 | Coherent scope | 1x | 90/100 | Single responsibility: translate a DESIGN.md into product UI code. Composes cleanly with siblings (`design-md-style-picker` picks source, `design-md-style-audit` validates output). |

### Axis 3 — Steering

| # | Criterion | Weight | Score | Notes |
|---|-----------|--------|-------|-------|
| 7 | Leading words | 2x | 75/100 | "DNA" is the primary leading word (appears in Overview, Step 1, Step 3) and anchors the design-translation concept. **Improvement:** "dials and locks" now serves as a compact leading-word pair — Step 2 title ("Set the dials and locks"), body (three execution dials, five design locks), and "Done when" criterion (line 44) all repeat it. This recruits a pretrained concept (adjustable design parameters vs. fixed constraints) that the model already holds. Beyond these, vocabulary remains thin — "signature element", "anti-default" appear once each. |
| 8 | Completion criteria & legwork | 2x | 85/100 | **Major improvement:** All 5 steps now carry explicit "Done when" criteria (lines 35, 44, 54, 62, 72). Step 1: "all 7 DNA dimensions … are recorded in your internal map" — exhaustive. Step 2: "the design read, three dials, and five locks are set" — checkable. Step 3: "every DNA dimension has a concrete product mapping" — exhaustive. Step 4: "code compiles and renders without errors" — binary check. Step 5: "all preflight checks pass" — exhaustive via delegation to execution-discipline.md. Step 5 remains the strongest (inspect screenshots, fix overflow/contrast/focus/responsive issues, run preflight). |
| 9 | Gotchas section | 2x | 85/100 | Guardrails (§) captures 7 concrete failure points: brand clones, style mixing, color-only styling, generic defaults, DESIGN.md pasting, domain mismatch, TASTE.md conflict resolution. execution-discipline.md Anti-Default Rules adds 9 more. Coverage is strong and specific. |
| 10 | Grounded in expertise | 2x | 90/100 | Content clearly comes from observed AI design failures: the "centered hero + three cards" anti-pattern, "vague purple-blue gradients", "fake product screenshots", "decorative glass panels". Execution dials (layout variance 1–10, motion intensity 1–10, visual density 1–10) reflect real design judgment. TASTE.md integration shows awareness of the broader design workflow. |
| 11 | Avoids railroading | 1x | 80/100 | "use existing framework, component structure, design tokens" adapts to the repo. "introduce CSS variables or token objects when the repo already uses tokens" is conditional. TASTE.md/DESIGN.md/user-instruction priority chain (Guardrails last rule) is explicit but leaves room. Execution dials teach a method rather than declaring exact output. |

### Axis 4 — Pruning

| # | Criterion | Weight | Score | Notes |
|---|-----------|--------|-------|-------|
| 12 | No-ops (deletion test) | 2x | 80/100 | **Improvement:** The previous hardcoded local path was borderline dead content; replaced with `$SKILLS_SCRIPTS` (line 17–19). Most lines survive the deletion test. Line 10 "responsive behavior, and implementation details that match the existing codebase" is borderline — a competent model would do this by default, but it reinforces against the specific failure mode of dropping an alien stylesheet. Line 60 "keep the edit scope tight" fights the model's natural tendency to broaden edits. Low overall no-op density. |
| 13 | Single source of truth | 1x | 90/100 | Clean layering: SKILL.md summarizes workflow steps; translation-workflow.md expands them with extraction notes, mapping rules, and implementation checks. No duplication across files. Preflight checklist lives in execution-discipline.md with a single pointer from SKILL.md. |
| 14 | Relevance & sediment | 1x | 90/100 | **Improvement:** The one past sediment concern (hardcoded path `/Users/mitzuuuu/.agents/skills/scripts/`) is now resolved with `$SKILLS_SCRIPTS`. All content is relevant to the current task. The `awesome-design-md` catalog reference is current. No stale layers or dead instructions. |

### Conditional criteria

| # | Criterion | Weight | Score | Notes |
|---|-----------|--------|-------|-------|
| 15 | Setup flow | 1x | N/A | Category `code-scaffolding-and-templates` is not in the applicability list for Setup flow. |
| 16 | Memory mechanism | 1x | N/A | Category `code-scaffolding-and-templates` is not in the applicability list for Memory mechanism. |
| 17 | Scripts & libraries | 1x | 80/100 | **Improvement:** References `$SKILLS_SCRIPTS/design_md_catalog.py` (lines 17–19) with `ensure`, `search`, and `path` subcommands for resolving DESIGN.md sources. The `$SKILLS_SCRIPTS` variable replaces the previous hardcoded local path, making the reference portable across machines. Functional and serves the skill's needs. Scripts remain external to the skill directory — acceptable for shared tooling. |
| 18 | On-demand hooks | 1x | N/A | Category `code-scaffolding-and-templates` is not in the applicability list for On-demand hooks. |

## What Changed Since Last Evaluation

| Issue | Before | After | Impact |
|-------|--------|-------|--------|
| Missing completion criteria (Steps 1–4) | No "done when" gates; premature completion risk | All 5 steps have explicit, checkable "Done when" criteria | #8: 65 → 85 |
| Weak leading-word vocabulary | Only "DNA" carried steering weight | "dials and locks" introduced as compact, repeated leading-word pair in Step 2 title, body, and completion criterion | #7: 60 → 75 |
| Hardcoded script path | `/Users/mitzuuuu/.agents/skills/scripts/` — broken on other machines | `$SKILLS_SCRIPTS` environment variable — portable | #12: 75 → 80, #14: 85 → 90, #17: 60 → 80 |
| Minor portability note | — | `$SKILLS_SCRIPTS` improves reference disclosure robustness | #4: 75 → 78 |

## Failure Modes Detected

| Mode | Evidence | Root cause | Defense |
|------|----------|------------|---------|
| Weak steering (mild) | SKILL.md:37–44 — "dials and locks" appears only in Step 2; Steps 1, 3, 4, 5 don't reuse it | Leading-word vocabulary beyond "DNA" and "dials/locks" remains thin; "signature element" and "anti-default" appear once each | Extend "dials" and "locks" into Steps 3 and 5 so the pairing carries through the full workflow |
| No-ops (mild) | SKILL.md:10 — "responsive behavior, and implementation details that match the existing codebase" is largely default model behavior | Reinforcing a default to prevent a specific failure pattern is a low-cost hedge | Keep — one sentence is cheap insurance against the "alien stylesheet" failure mode |

## Prioritized Actions

### 1. Extend "dials and locks" leading words beyond Step 2

**Evidence:** SKILL.md:37–44 — "dials and locks" is concentrated in Step 2 only.

**Fix:** Use "dials" in Step 4 (e.g., "honor the execution dials set in Step 2 when scoping the implementation") and Step 5 (e.g., "verify the design locks are visibly holding — the accent, shape, and type constraints should be legible in the rendered UI"). This carries the pretrained concept through the full workflow.

### 2. Consider whether reference-loading instruction should go conditional

**Evidence:** SKILL.md:22 — "Also load the project `TASTE.md` if present. Do not load the entire catalog unless selection is still unresolved." The second sentence is conditional; the first two reference loads are unconditional.

**Fix:** Reword as "load `references/translation-workflow.md` and `references/execution-discipline.md` **when executing translation**" to make the branch explicit, mirroring the catalog guard. Currently low-risk because the material is always needed for execution, but explicit branching is a minor hygiene win.

## Bonus Patterns

| Pattern | Status | Notes |
|---------|--------|-------|
| Validation loops | Present | Step 5 "Verify visually" plus execution-discipline.md Preflight checklist form a self-check loop before finalizing |
| Output templates | Partial | "Final Response" (§) specifies what to state (style, source file, changes, verification) but doesn't provide a concrete template format |
| Procedures over declarations | Present | Execution dials and design locks teach *how to approach* the translation — a method, not a fixed output spec |
| Defaults over menus | Present | "keep the edit scope tight unless a shared token layer is clearly needed" picks a default with an explicit escape hatch |
| Trace-checkable steering | Partial | "DNA" and "dials and locks" are traceable in reasoning traces; "dials" and "locks" are now distinctive enough to confirm the skill shaped behavior |

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
