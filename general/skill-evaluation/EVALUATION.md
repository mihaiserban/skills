# Skill Evaluation — skill-evaluation

> Evaluated: 2026-07-04
> Source: general/skill-evaluation/SKILL.md
> Evaluator: skill-evaluation v2.1.0 (self-evaluation)
> Framework: [Anthropic Skill Best Practices](https://claude.com/blog/lessons-from-building-claude-code-how-we-use-skills) + Matt Pocock's [writing-great-skills](https://www.youtube.com/watch?v=UNzCG3lw6O0)

## Summary

| Metric | Value |
|--------|-------|
| Overall Score | 81.00/100 |
| Grade | A |
| Category | code-quality-and-review |
| Invocation | model-invoked |
| Files | 5 |
| Criteria scored / N/A | 16 scored, 2 N/A |

## Scorecard

### Axis 1 — Trigger

| # | Criterion | Weight | Score | Notes |
|---|-----------|--------|-------|-------|
| 1 | Invocation design | 2x | 85/100 | Model-invoked is correct: the skill fires autonomously when a user asks about skill quality and must be reachable by other evaluation-chaining skills. Description carries ~4 lines of context load per turn — the right trade-off. Frontmatter is clean, no `disable-model-invocation`. Unchanged from prior eval. |
| 2 | Description quality | 2x | 82/100 | Model-invoked: two branches present (evaluate and compare). Now includes leading word "evidence-cited" up front (SKILL.md:6–7) — anchors invocation and is grep-able in traces. The parenthetical examples `("evaluate this skill", "skill scorecard", "review SKILL.md")` remain near-synonym restatements of the first branch — internal duplication within the description. Improved from 75: leading word fixes the prior gap of no anchoring term. |

### Axis 2 — Structure

| # | Criterion | Weight | Score | Notes |
|---|-----------|--------|-------|-------|
| 3 | Steps vs. reference clarity | 1x | 85/100 | Clean separation: Workflow (SKILL.md:115–150) is an ordered 8-step procedure; Criteria, Scoring Guide, and Gotchas are reference. Quality Checklist is now integrated into workflow steps inline (formerly a standalone section), eliminating a post-procedure checklist that the agent could treat as optional. Each criterion is co-located with its weight and key question in a single table row. Improved from 80: QC integration removes a structural ambiguity. |
| 4 | Branch-aware disclosure & pointers | 2x | 85/100 | Key fix applied: the mechanics.md pointer now reads "Read `references/mechanics.md` — the vocabulary and tests behind Axes 1, 3, and 4, including what makes a context pointer's wording effective" (SKILL.md:22) — mandatory wording for material Axes 1, 3, and 4 depend on. The prior phrasing ("If you need the vocabulary…") was a variance bug. categories.md pointer is strong; output-template.md pointer is adequate. Improved from 72: the critical variance bug is resolved. |
| 5 | Conciseness | 2x | 80/100 | 188 lines — well under the 500-line ceiling and down from ~218 in the prior eval. Removed: Source section (4 lines), Overall score formula (8 lines), standalone Quality Checklist (~10 lines). Grade Scale table shortened from 8-line table to 4-line pointer. Remaining candidates: Parameters table (SKILL.md:24–34, 11 lines) partially duplicates information in the workflow and CI paragraph. Improved from 60: ~30 lines of no-op and duplicated material removed. |
| 6 | Coherent scope | 1x | 85/100 | Single purpose: evaluate skills and produce evidence-cited scorecards. Comparison mode is a natural extension. Composes cleanly: score.py gates CI, EVALUATION.md is consumable by other tools. The CI mention (SKILL.md:36–41) stays within a reasonable boundary. Unchanged from prior eval. |

### Axis 3 — Steering

| # | Criterion | Weight | Score | Notes |
|---|-----------|--------|-------|-------|
| 7 | Leading words | 2x | 75/100 | "cite-or-cut" remains a strong original leading word — compact, distinctive, trace-checkable, repeated consistently (SKILL.md:124, 126). "evidence-cited" now anchors the description (SKILL.md:6–7). The skill still imports more vocabulary from mechanics.md than it introduces of its own. "scorecard" is functional but not distinctive. Improved from 65: the description gains a leading word, enabling trace-checkable invocation. |
| 8 | Completion criteria & legwork | 2x | 82/100 | Steps 4 and 5 have explicit "Done when…" criteria that are checkable and exhaustive ("every applicable criterion carries a score and a citation, and every N/A a reason"; "every mode… checked… and either cited or dismissed"). Steps 6–8 have implicit but clear criteria. The "cite-or-cut" principle provides a cross-cutting exhaustiveness bar. Former QC standalone section is now folded into step criteria (SKILL.md:125–128, 132–133), making its completion criteria unskippable. Unchanged overall: the structural fix was a conciseness/clarity win, not a new criteria win. |
| 9 | Gotchas section | 2x | 90/100 | Three specific, actionable gotchas (SKILL.md:179–188): tiny skills and N/A flooding, self-evaluation bias, and duplication in fresh rewrites. Each addresses an observed failure pattern. The self-evaluation bias gotcha remains operationally critical — it directly shapes how an evaluator approaches this exact skill. Unchanged from prior eval. |
| 10 | Grounded in expertise | 2x | 80/100 | Sources are concrete: Anthropic's Jun 2026 skill practices post and Matt Pocock's writing-great-skills skill. mechanics.md is explicitly a "deliberately self-contained condensation" (mechanics.md:4–5). Gotchas read like they come from experience. Minor gap: no concrete examples from actual evaluations to demonstrate battle-testing beyond theory. Unchanged from prior eval. |
| 11 | Avoids railroading | 1x | 78/100 | Good flexibility intact: conditional criteria table has an explicit override mechanism (SKILL.md:99–104), scoring guide provides ranges not exact numbers, defaults are offered but overridable. The workflow is 8 numbered steps but each leaves room for judgment. Unchanged from prior eval. |

### Axis 4 — Pruning

| # | Criterion | Weight | Score | Notes |
|---|-----------|--------|-------|-------|
| 12 | No-ops (deletion test) | 2x | 78/100 | Self-evaluation with extra skepticism applied. Three prior no-op candidates deleted: Source section (was SKILL.md:26–29), Overall score formula (was SKILL.md:106–113), standalone Quality Checklist (~10 lines). Remaining borderline candidate: Parameters table (SKILL.md:24–34, 11 lines) — its defaults are encoded in the workflow and CI paragraph; removing it would leave behavior essentially unchanged. The table does provide a convenient single-location reference, so it earns a soft pass. The prior no-op count of ~19 lines (~9%) is now reduced to at most 11 borderline lines (~6%). Improved from 50. |
| 13 | Single source of truth | 1x | 75/100 | Grade scale duplication between SKILL.md and score.py is resolved: SKILL.md now points to score.py as the authoritative source (SKILL.md:110–113). Remaining overlap: the failure-mode table (SKILL.md:160–176) and mechanics.md §5 (mechanics.md:83–111) share mode names and concepts — SKILL.md adds the distinct "Evidence to look for" column, while mechanics.md holds the definitive definitions and defenses. This is defensible layering rather than pure duplication. Improved from 60: the grade scale dedup is the high-impact fix. |
| 14 | Relevance & sediment | 1x | 88/100 | v2.1.0 dated 2026-07-03 — very fresh. Source section (prior version-history sediment) is removed. No stale layers detected. The mechanics.md maintenance note ("sync manually if the upstream GLOSSARY changes") is a living instruction, not sediment. Improved from 85: minor freshness gain from removing the Source section's forward-looking decay risk. |

### Conditional criteria

| # | Criterion | Weight | Score | Notes |
|---|-----------|--------|-------|-------|
| 15 | Setup flow | 1x | N/A | Not in applicable categories for code-quality-and-review. The skill is self-contained — drop in, no installation needed. No override warranted. |
| 16 | Memory mechanism | 1x | N/A | Not in applicable categories. Each evaluation is stateless; no cross-invocation state needed. No override warranted. |
| 17 | Scripts & libraries | 1x | 85/100 | `scripts/score.py` (66 lines) is a well-written CLI: handles N/A criteria correctly, validates score ranges, supports `--fail-below` gating, has clean docstring usage. Tightly integrated — workflow step 7 explicitly invokes it. Minor: error messages could be more specific for malformed input. Unchanged from prior eval. |
| 18 | On-demand hooks | 1x | 55/100 | The skill mentions CI gating (SKILL.md:36–41) and score.py `--fail-below` is designed for it, but no actual hook configuration exists — no pre-commit config, no GitHub Actions YAML, no Makefile target. The concept is present but the artifact is missing. Unchanged from prior eval. |

## Failure Modes Detected

| Mode | Evidence | Root cause | Defense |
|------|----------|------------|---------|
| Weak steering | SKILL.md:24–34 — Parameters table and workflow both encode defaults (output path, target); a change to one would be silently desynchronized | The Parameters table is reference material sitting before the workflow without a clear "this is the source" declaration | Collapse the Parameters table into the workflow's step descriptions, or declare one as authoritative |
| Duplication | mechanics.md:83–111 and SKILL.md:160–176 — failure-mode names and concepts appear in both files | SKILL.md adds "Evidence to look for" but re-states mode names that mechanics.md already defines | Keep definitions only in mechanics.md; SKILL.md should point to mechanics.md §5 and add only the evidence-to-look-for column |
| No-ops | SKILL.md:24–34 — Parameters table partially restates defaults the workflow already encodes | The table provides a convenient summary, but under the deletion test removing it would leave behavior essentially unchanged | Either merge the table's unique information into the workflow and delete it, or make it clearly non-duplicative by adding parameter-level details the workflow omits |
| Sediment (latent) | SKILL.md:143 — "the 4 carried over from v2.0, plus a fifth" | Version-history reference that will decay on next version bump | Replace with a description of what the 5 are without referencing their origin version |

## Prioritized Actions

### 1. Add CI hook artifact

**Evidence:** SKILL.md:36–41 describes CI gating; score.py supports `--fail-below`.

**Fix:** Ship a `.github/workflows/skill-check.yml` or `.pre-commit-config.yaml` entry that runs `score.py --fail-below 60` on changed SKILL.md files. This lifts criterion 18 from conceptual to operational.

### 2. Resolve Parameters table duplication

**Evidence:** SKILL.md:24–34 — the Parameters table restates defaults already encoded in workflow steps (target: "Ask user", output: "target/EVALUATION.md").

**Fix:** Either (a) delete the Parameters table and let the workflow be the single source, or (b) keep only the `compare` parameter in the table (it's the one detail not obvious from the workflow alone) and drop the rest.

### 3. Deduplicate failure-mode definitions with mechanics.md

**Evidence:** mechanics.md §5 defines all seven failure modes with defenses; SKILL.md:160–176 re-states mode names.

**Fix:** Replace the SKILL.md failure-mode table with a pointer to mechanics.md §5, keeping only the "Evidence to look for" column (which mechanics.md lacks).

### 4. Replace version-history language in Bonus Patterns

**Evidence:** SKILL.md:143 — "the 4 carried over from v2.0, plus a fifth".

**Fix:** Rewrite as "5 bonus patterns" described by what they are, not where they came from. Example: "5 bonus patterns covering self-check, structured output, procedural thinking, defaults, and trace-checkable steering."

## Bonus Patterns

| Pattern | Status | Notes |
|---------|--------|-------|
| Validation loops | Absent | No instruction for the agent to self-check its evaluation before finalizing. Consider: "Before writing, re-read each scored criterion and ask: would this evidence survive adversarial review?" |
| Output templates | Present | `references/output-template.md` provides exact Markdown structure for both single and comparison-mode scorecards, with placeholder variables. |
| Procedures over declarations | Present | The workflow teaches *how to evaluate* (classify → score → diagnose → compute → write), not *what score to give*. |
| Defaults over menus | Present | Default output path, default parameters, default scoring ranges. Alternatives mentioned briefly (comparison mode, CI gating). |
| Trace-checkable steering | Present | "evidence-cited" and "cite-or-cut" are distinctive enough to grep agent reasoning traces — the description-level leading word fixed the prior absence. |

## Grade Scale

The grade is computed by `scripts/score.py`. See the script for the authoritative grade mapping.

---

*Generated by [skill-evaluation](https://github.com/fabricioctelles/skills) v2.1.0, merging the [Anthropic skill quality framework](https://claude.com/blog/lessons-from-building-claude-code-how-we-use-skills) with Matt Pocock's [writing-great-skills](https://www.youtube.com/watch?v=UNzCG3lw6O0) methodology.*
