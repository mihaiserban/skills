# Skill Evaluation — setup-skills

> Evaluated: 2026-07-04
> Source: engineering/setup-skills/SKILL.md
> Evaluator: skill-evaluation v2.1.0
> Framework: [Anthropic Skill Best Practices](https://claude.com/blog/lessons-from-building-claude-code-how-we-use-skills) + Matt Pocock's [writing-great-skills](https://www.youtube.com/watch?v=UNzCG3lw6O0)

## Summary

| Metric | Value |
|--------|-------|
| Overall Score | 80.88/100 |
| Grade | A |
| Category | code-scaffolding-and-templates |
| Invocation | user-invoked |
| Files | 4 |
| Criteria scored / N/A | 15 scored, 3 N/A |

## Scorecard

### Axis 1 — Trigger

| # | Criterion | Weight | Score | Notes |
|---|-----------|--------|-------|-------|
| 1 | Invocation design | 2x | 90/100 | User-invoked (`disable-model-invocation: true`) is correct. This is a one-time setup wizard that runs by hand; no other skill needs to reach it autonomously. Zero context load, human-indexed — exactly the right trade-off for a run-once configurator. |
| 2 | Description quality | 2x | 90/100 | A clean human-facing one-liner: names the action ("configure this repo"), lists what gets configured (issue tracker, triage labels, domain docs), and signals when to use it ("once before first use of other engineering skills"). No trigger list scaffolding (it's user-invoked). |

### Axis 2 — Structure

| # | Criterion | Weight | Score | Notes |
|---|-----------|--------|-------|-------|
| 3 | Steps vs. reference clarity | 1x | 85/100 | Clean separation: 5 numbered procedural steps under "Process," with explainer blocks (A, B, C) co-located beside each decision. Reference material — file-picking rules, template block, Gotchas — is placed after the ordered workflow. Minor: "Pick the file to edit" rules (lines 82–88) are nested inside step 4 rather than given their own step number, but they read naturally as sub-steps of "Write." |
| 4 | Branch-aware disclosure & pointers | 2x | 78/100 | Seed templates (triage-labels.md, domain.md, issue-tracker-github.md) are correctly behind context pointers in step 4, not inflated inline. Pointer wording is instructional ("use the seed template at X as a starting point") — strong, not weakly conditional. The triage-labels pointer at line 58 says "see the seed template at…" — slightly passive but still directive. No variance bug of note; all pointers sit in the single branch that needs them. |
| 5 | Conciseness | 2x | 80/100 | 125 lines — lean for a skill that walks through 3 interactive configuration decisions, each with an explainer. The explainer blocks (lines 40, 50, 56, 64) earn their keep: the Gotchas section mandates "Assume the user does not know what these terms mean." Minor duplication: file-picking rules appear in step 4 (lines 82–88) and in Gotchas (line 122) — the Gotcha framing is deliberate consolidation but costs a few redundant tokens. |
| 6 | Coherent scope | 1x | 88/100 | Exactly one thing: scaffold the 3-item per-repo config (tracker, labels, domain docs) that engineering skills consume. Composes cleanly — other engineering skills read `docs/agents/*.md`, and `domain-modeling` creates CONTEXT.md/ADRs the domain docs section configures. No scope creep. |

### Axis 3 — Steering

| # | Criterion | Weight | Score | Notes |
|---|-----------|--------|-------|-------|
| 7 | Leading words | 2x | 55/100 | No distinctive, consistently repeated anchoring terms. "Explainer" (lines 40, 50, 56, 64) labels decision sections but is a structural tag, not a behavioral leading word. "Default posture" (line 42) is close but only fires once. The skill's prose does the steering ("Explore, present what you found, confirm with the user, then write" — line 17) without compact vocabulary to anchor it. A term like "walk-through" or "scaffold" repeated across steps could collapse several descriptive lines. |
| 8 | Completion criteria & legwork | 2x | 72/100 | Steps have implicit criteria adequate for an interactive, user-invoked skill: the human confirms at each decision (line 34: "get the user's answer, then move to the next"), then reviews a draft (line 78: "Let them edit before writing"). Step 4's directive "Then write the three docs files" is explicit enough. Step 1 ("Look at the current repo") and step 5 ("Tell the user the setup is complete") have no "Done when" bar — the interactive human gate fills the gap. |
| 9 | Gotchas section | 2x | 92/100 | Four specific, actionable constraints (lines 120–125): (1) never create AGENTS.md when SESSION_START.md exists, (2) don't overwrite surrounding sections, (3) assume the user doesn't know the terms, (4) only ask PRs-as-request-surface for GitHub. Each addresses a concrete footgun, not a generic warning. The recent consolidation into one section is a structural improvement. |
| 10 | Grounded in expertise | 2x | 82/100 | Adapted from mattpocock/skills (line 7). Battle-tested patterns: one-decision-at-a-time flow, specific `gh` CLI commands with `jq` filtering in the GitHub seed template (issue-tracker-github.md:9–28), the SESSION_START.md vs AGENTS.md precedence logic. The file-picking rules read like they came from real collision cases. |
| 11 | Avoids railroading | 1x | 82/100 | Good flexibility: "Default posture" (line 42) presents defaults without mandating them. Three tracker options with "Other" escape hatch (line 46). Labels default to canonical names with explicit override permission (line 60). "If neither exists, ask the user which one to create — don't pick for them" (line 86). User confirms a draft before writing (line 78). |

### Axis 4 — Pruning

| # | Criterion | Weight | Score | Notes |
|---|-----------|--------|-------|-------|
| 12 | No-ops (deletion test) | 2x | 78/100 | Sentence-by-sentence deletion test applied. One no-op candidate: attribution line (line 7) — removing it changes no behavior. The "prompt-driven skill" framing (lines 16–17) is borderline; it sets interaction expectations but the steps already encode the mode. Everything else carries behavioral weight: explainer blocks teach the user, seed-template pointers drive file creation, Gotchas guard against known footguns. |
| 13 | Single source of truth | 1x | 82/100 | Strong SSOT discipline: the triage labels table lives only in the seed template (triage-labels.md) — SKILL.md points to it (line 58: "see the seed template at…") rather than duplicating. This is the user-cited SSOT fix. Minor: file-picking rules appear in both step 4 (lines 82–88) and Gotchas (line 122) — intentional consolidation but each carries its own framing (procedural rule vs. footgun). The domain.md and issue-tracker-github.md templates are the sole sources for their respective content. |
| 14 | Relevance & sediment | 1x | 90/100 | Fresh skill with intentional recent improvements: Gotchas section added, triage labels table replaced with SSOT pointer, explainer blocks trimmed. No stale layers, no accumulated cruft. The mattpocock/skills adaptation is recent and all content aligns with the current skill's purpose. |

### Conditional criteria

| # | Criterion | Weight | Score | Notes |
|---|-----------|--------|-------|-------|
| 15 | Setup flow | 1x | N/A | Not in applicable categories for `code-scaffolding-and-templates`. The skill is a setup wizard itself — it configures other skills, rather than requiring external installation. No override warranted. |
| 16 | Memory mechanism | 1x | N/A | Not in applicable categories. Each invocation is a fresh, stateless walk-through; no cross-invocation state needed. No override warranted. |
| 17 | Scripts & libraries | 1x | 80/100 | Three seed template files (triage-labels.md, domain.md, issue-tracker-github.md) serve as reusable starting points the agent fills in. Well-structured: each is self-contained, clearly separated from SKILL.md, and includes concrete content (label table, directory structure diagrams, `gh` command conventions). Decent but no executable scripts — the "script" here is the templates themselves. |
| 18 | On-demand hooks | 1x | N/A | Not in applicable categories. This is a run-once setup wizard, not a gate or enforcement mechanism. No override warranted. |

## Failure Modes Detected

| Mode | Evidence | Root cause | Defense |
|------|----------|------------|---------|
| Weak steering | SKILL.md: body-wide — no distinctive leading word repeated across steps. The prose is functional but generic ("Explainer," "Default posture," "walk through") | No compact anchoring vocabulary; the skill relies on full sentences to steer where one word could anchor the same instruction | Introduce a leading word ("scaffold" or "walk-through") in the preamble and repeat it at section boundaries — SKILL.md:9, 21, 34, 119 |
| Duplication | SKILL.md:84–88 vs. SKILL.md:122 — file-picking rules appear in both step 4 and Gotchas | Intentional consolidation: Gotchas collects footguns, step 4 gives procedural instructions. Each frame adds distinct value but the tokens are redundant | Collapse: keep the procedural rule in step 4 (where the agent acts), and in Gotchas reference it ("File-picking rule: see step 4 rule") — the Gotcha becomes a pointer, not a restatement |
| No-ops | SKILL.md:7 — attribution line "Adapted from mattpocock/skills" | Attribution doesn't change agent behavior | Move to a metadata footer or the evaluation header; keep the credit but shrink its context cost |

## Prioritized Actions

### 1. Introduce a leading word to anchor steering

**Evidence:** SKILL.md — no distinctive term repeated across the body; "Explainer" is a label, not a behavioral anchor

**Fix:** Adopt "walk-through" at the preamble (line 17: "This is a prompt-driven walk-through — explore, present, confirm, then write") and repeat it at step boundaries. More distinctive options: "three-decision scaffold" or "config wizard."

### 2. Collapse gotcha-to-procedure duplication on file-picking rules

**Evidence:** SKILL.md:84–88 and SKILL.md:122 — same rule in two places

**Fix:** Keep the procedural form in step 4. In Gotchas, replace: "Follow the file-picking rule in step 4 — never create the wrong file." One less line, one source of truth, still flagged as a footgun.

### 3. Move attribution to a footer

**Evidence:** SKILL.md:7 — attribution line that changes no behavior

**Fix:** Drop line 7. Add "Adapted from mattpocock/skills" to the evaluation header or as a footnote in the file's closing line. Saves one line of context load without losing credit.

### 4. Sharpen step 1's completion criterion

**Evidence:** SKILL.md:21–30 — step 1 lists items to check but has no "Done when" gate

**Fix:** Add at line 30: "Done when all six items have been checked and findings are ready to present." Gives the agent an explicit exit condition for the exploration step.

## Bonus Patterns

| Pattern | Status | Notes |
|---------|--------|-------|
| Validation loops | Absent | No explicit self-check before finalizing. The draft preview (line 73–78, "Let them edit before writing") is a human validation loop — distinct from an agent self-check. |
| Output templates | Present | The `## Agent skills` markdown block (lines 94–108) and the three seed templates (triage-labels.md, domain.md, issue-tracker-github.md) provide exact structure for the generated output. |
| Procedures over declarations | Present | Teaches *how to configure* (explore → present → confirm → write), not *what to produce* for one specific repo. Decisions are parameterized, not hardcoded. |
| Defaults over menus | Present | "Default posture" (line 42) picks GitHub when a remote exists. Label strings default to canonical names (line 60). File choice rules pick SESSION_START.md over AGENTS.md. Alternatives mentioned briefly, defaults clear. |
| Trace-checkable steering | Absent | No distinctive term that would appear in reasoning traces to confirm the skill fired. A leading word like "scaffold" or "walk-through" would enable trace-checkability. |

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
