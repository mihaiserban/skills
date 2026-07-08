---
name: using-skills
description: Maps incoming work to the right skill workflow and defines shared operating rules. Use when starting a session or when you need to discover which skill applies to the current task.
---

# Using Skills

## Overview

This is the meta-skill that governs skill discovery and shared behaviors. When
a task arrives, use the decision tree below to find the right workflow. This
skill is the single discovery layer — it covers all authored skills plus
vendored agent-skills and ponytail workflows. The
core operating behaviors in `references/operating-behaviors.md` apply at all
times, across all skills.

## Skill Discovery

```
Task arrives
    │
    ├── Don't know what to build? ────────→ design/show-first       (wireframe + plan first)
    │
    ├── Building or restyling UI? ─────────→ design                  (routes to picker → apply → audit)
    │   ├── Need a visual style? ──────────→ design/design-md-style-picker
    │   ├── Applying a known style? ──────→ design/design-md-style-apply
    │   ├── Auditing visual fit? ──────────→ design/design-md-style-audit
    │   └── Capturing taste? ─────────────→ design/design-taste-distiller
    │
    ├── Bug, crash, unexpected behavior? ──→ engineering/systematic-debugging
    │   ├── Regression, don't know which commit? → engineering/bisect-regression
    │   ├── Need to undo one commit? ─────→ git-ops/revert-surgical
    │   └── Browser runtime bug? ─────────→ vendor/agent-skills/skills/browser-testing-with-devtools
    │
    ├── Writing or changing code? ─────────→
    │   ├── Deeply nested logic? ─────────→ engineering/reduce-nesting
    │   ├── Dead or unused code? ─────────→ engineering/kill-dead-code
    │   ├── User/external input involved? → engineering/input-validation
    │   ├── Credentials in the diff? ─────→ engineering/secret-scan
    │   ├── SQL or ORM queries? ──────────→ engineering/sql-review
    │   ├── API boundary or integration? ─→ engineering/contract-test
    │   ├── Architectural decision made? ─→ documentation/decision-record
    │   ├── Need a spec before code? ─────→ vendor/agent-skills/skills/spec-driven-development
    │   ├── Test-first workflow? ─────────→ vendor/agent-skills/skills/test-driven-development
    │   ├── UI component engineering? ────→ vendor/agent-skills/skills/frontend-ui-engineering
    │   ├── Designing an API? ────────────→ vendor/agent-skills/skills/api-and-interface-design
    │   ├── High-stakes or unfamiliar code? → vendor/agent-skills/skills/doubt-driven-development
    │   └── Just finished coding? ────────→ engineering/adversarial-verify
    │
    ├── Clarifying requirements? ──────────→
    │   ├── Vague ask, need to extract? ──→ vendor/agent-skills/skills/interview-me
    │   └── Rough concept, need variants? → vendor/agent-skills/skills/idea-refine
    │
    ├── Planning work? ────────────────────→
    │   ├── Spec exists, need tasks? ─────→ vendor/agent-skills/skills/planning-and-task-breakdown
    │   └── Need better agent context? ───→ vendor/agent-skills/skills/context-engineering
    │
    ├── Git operations? ───────────────────→
    │   ├── Opening a PR? ────────────────→ git-ops/pr-from-diff
    │   ├── Messy WIP to clean commits? ──→ git-ops/clean-commits
    │   ├── Rebasing or squashing? ───────→ git-ops/rebase-safely
    │   └── Writing release notes? ───────→ documentation/changelog-from-diff
    │
    ├── Code review or quality? ───────────→
    │   ├── Multi-axis review? ───────────→ vendor/agent-skills/skills/code-review-and-quality
    │   ├── Too complex? ─────────────────→ vendor/agent-skills/skills/code-simplification
    │   ├── Security concerns? ───────────→ vendor/agent-skills/skills/security-and-hardening
    │   └── Performance problems? ────────→ vendor/agent-skills/skills/performance-optimization
    │
    ├── Shipping or deploying? ────────────→
    │   ├── Deploying to production? ─────→ vendor/agent-skills/skills/shipping-and-launch
    │   ├── CI/CD pipeline work? ─────────→ vendor/agent-skills/skills/ci-cd-and-automation
    │   ├── Adding logs/metrics/alerts? ──→ vendor/agent-skills/skills/observability-and-instrumentation
    │   ├── Git workflow strategy? ───────→ vendor/agent-skills/skills/git-workflow-and-versioning
    │   └── Deprecating or migrating? ────→ vendor/agent-skills/skills/deprecation-and-migration
    │
    ├── Laziest solution / simplify? ──────→
    │   ├── Shortest path to working? ────→ vendor/ponytail/skills/ponytail
    │   ├── Review for over-engineering? ─→ vendor/ponytail/skills/ponytail-review
    │   └── Full-repo over-engineering audit? → vendor/ponytail/skills/ponytail-audit
    │
    ├── Agent context problems? ───────────→
    │   ├── Session too long/big files? ──→ agents/context-budget
    │   └── Parallel independent work? ───→ agents/governance-fanout
    │
    ├── Fuzzy domain language? ───────────→ engineering/domain-modeling
    │
    ├── First time in this repo? ─────────→ engineering/setup-skills
    │
    ├── Evaluating or comparing a skill? ──→ general/skill-evaluation
    │
    ├── Writing a blog post? ─────────────→ mihaiserban.dev/blog-post
    │
    └── Researching a topic? ─────────────→ research
```

## Core Operating Behaviors

These apply at all times, across all skills. See
`references/operating-behaviors.md` for the full text.

1. **Surface assumptions** — state them explicitly before implementing.
2. **Manage confusion actively** — stop, name it, ask, wait.
3. **Push back when warranted** — sycophancy is a failure mode.
4. **Enforce simplicity** — the boring solution wins.
5. **Maintain scope discipline** — surgical precision, not renovation.
6. **Verify, don't assume** — evidence required, "seems right" never sufficient.

## Definition of Done

Every change must clear the gates in `references/definition-of-done.md`:

| Gate | Check |
|------|-------|
| Tests pass | All existing + new behavior tests |
| No regressions | Existing functionality intact |
| Behavior verified | Run it, don't just read it |
| Lint/typecheck | Clean output |
| Docs updated | ADRs/READMEs updated if intent changed |
| Scope matched | Only intended changes |

## Failure Modes to Avoid

1. Making wrong assumptions without checking
2. Plowing ahead when confused instead of asking
3. Not surfacing inconsistencies you notice
4. Not presenting tradeoffs on non-obvious decisions
5. Being sycophantic ("Of course!") to approaches with clear problems
6. Overcomplicating code — building 100 lines where 10 would suffice
7. Modifying code or comments orthogonal to the task
8. Removing things you don't fully understand
9. Skipping verification because "it looks right"
10. Not checking for an applicable skill before starting work

## Skill Rules

1. **Check for an applicable skill before starting work.** Skills encode
   processes that prevent common mistakes.

2. **Skills are workflows, not suggestions.** Follow the steps in order. Don't
   skip verification.

3. **Multiple skills can apply sequentially.** A feature might involve:
   `show-first` → `design` → `systematic-debugging` → `adversarial-verify` →
   `clean-commits` → `pr-from-diff`.

4. **When in doubt, start small.** If no skill clearly matches, pick the
   closest one and adapt. Better a partial workflow than no workflow.

## Quick Reference

| Phase | Skill | One-Line Summary |
|-------|-------|-----------------|
| Define | `/show-first` | Low-fi wireframe + systems plan before any code |
| Define | `/interview-me` (vendor) | Extract what the user actually wants, one question at a time |
| Define | `/idea-refine` (vendor) | Structured divergent/convergent thinking for rough concepts |
| Define | `/spec-driven-development` (vendor) | Requirements and acceptance criteria before code |
| Plan | `/planning-and-task-breakdown` (vendor) | Decompose specs into small, verifiable tasks |
| Plan | `/context-engineering` (vendor) | Right context at the right time |
| Design | `/design` | Route to picker → apply → audit pipeline |
| Design | `/design-md-style-picker` | Choose a DESIGN.md source aesthetic |
| Design | `/design-md-style-apply` | Translate a DESIGN.md into product UI |
| Design | `/design-md-style-audit` | Audit UI against a DESIGN.md source |
| Design | `/design-taste-distiller` | Distill references into a TASTE.md |
| Build | `/input-validation` | Validate untrusted input at the boundary |
| Build | `/kill-dead-code` | Find and remove unreachable code |
| Build | `/reduce-nesting` | Flatten deeply nested conditionals |
| Build | `/secret-scan` | Catch hardcoded secrets before commit |
| Build | `/sql-review` | Review SQL for correctness, safety, performance |
| Build | `/contract-test` | Test system boundaries by the contract |
| Build | `/domain-modeling` | Pin down domain terminology and ADRs |
| Build | `/test-driven-development` (vendor) | Red-green-refactor with test pyramid |
| Build | `/frontend-ui-engineering` (vendor) | Component architecture, design systems, accessibility |
| Build | `/api-and-interface-design` (vendor) | Contract-first API design, Hyrum's Law |
| Build | `/doubt-driven-development` (vendor) | Adversarial fresh-context review of in-flight decisions |
| Build | `/source-driven-development` (vendor) | Ground framework decisions in official docs |
| Build | `/incremental-implementation` (vendor) | Thin vertical slices, feature flags, safe defaults |
| Verify | `/adversarial-verify` | Review diff assuming code is BROKEN |
| Verify | `/systematic-debugging` | Reproduce-then-isolate before fixing |
| Verify | `/bisect-regression` | Find the commit that introduced a bug |
| Verify | `/browser-testing-with-devtools` (vendor) | Chrome DevTools MCP for runtime verification |
| Review | `/code-review-and-quality` (vendor) | Five-axis review: correctness, readability, architecture, security, performance |
| Review | `/code-simplification` (vendor) | Chesterton's Fence, reduce complexity while preserving behavior |
| Review | `/security-and-hardening` (vendor) | OWASP Top 10, auth patterns, secrets management |
| Review | `/performance-optimization` (vendor) | Measure-first, Core Web Vitals, bundle analysis |
| Git | `/clean-commits` | WIP into atomic commits |
| Git | `/pr-from-diff` | Write a reviewable PR description |
| Git | `/rebase-safely` | Rebase without losing work |
| Git | `/revert-surgical` | Undo one commit without touching others |
| Git | `/git-workflow-and-versioning` (vendor) | Trunk-based development, atomic commits |
| Ship | `/shipping-and-launch` (vendor) | Pre-launch checklists, feature flags, rollback procedures |
| Ship | `/ci-cd-and-automation` (vendor) | Shift Left, quality gate pipelines, failure feedback |
| Ship | `/observability-and-instrumentation` (vendor) | Structured logging, RED metrics, OpenTelemetry tracing |
| Ship | `/deprecation-and-migration` (vendor) | Code-as-liability, safe migration patterns |
| Docs | `/decision-record` | Capture WHY a technical choice was made |
| Docs | `/changelog-from-diff` | Turn commits into a changelog entry |
| Docs | `/documentation-and-adrs` (vendor) | ADRs, API docs, inline documentation standards |
| Agent | `/context-budget` | Keep agent context lean |
| Agent | `/governance-fanout` | Parallel sub-jobs with file-based handoff |
| Ponytail | `/ponytail` (vendor) | Laziest solution that works, simplest path |
| Ponytail | `/ponytail-review` (vendor) | Code review for over-engineering |
| Ponytail | `/ponytail-audit` (vendor) | Whole-repo audit for over-engineering |
| Ponytail | `/ponytail-debt` (vendor) | Harvest ponytail: comments into a debt ledger |
| Ponytail | `/ponytail-gain` (vendor) | Ponytail's measured impact scoreboard |
| Ponytail | `/ponytail-help` (vendor) | Quick-reference for all ponytail commands |
| Meta | `/skill-evaluation` | Evaluate a skill across 4 axes |
| Meta | `/setup-skills` | Bootstrap issue tracker, labels, domain layout |
| Meta | `/using-agent-skills` (vendor) | (Suppressed — `/using-skills` supersedes) |
| Personal | `/research` | Research a topic on arXiv |
| Personal | `/blog-post` | Distill a conversation into a blog post |
