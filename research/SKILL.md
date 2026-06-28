---
name: research
description: Research a technical or scientific topic on arXiv when explicitly instructed.
disable-model-invocation: true
---

# Research

## Overview

Use this skill to turn a topic or planning question into an evidence-grounded research brief. Prefer primary sources from arXiv, then connect the findings to the user's decision, design, or implementation context when relevant.

Treat "arvix" as a likely typo for "arXiv".

Do not invoke this skill just because a task involves planning, design, or implementation. Invoke it only when the user explicitly asks for research, arXiv/arvix, papers, prior art, or academic evidence.

## Workflow

1. Restate the user's topic or planning question as a research question.
2. Search arXiv for recent and foundational papers using multiple keyword variants.
3. Prioritize primary papers over blog posts, summaries, or secondary commentary.
4. Read enough of each selected paper to identify the problem, method, assumptions, empirical results, limitations, and implementation details.
5. Synthesize the findings into decisions that matter for the user's plan, design, experiment, or build task.
6. Return a concise, citation-backed brief that can inform planning or later implementation.

## Search Strategy

Use current web access when available. Good starting searches include:

```text
site:arxiv.org <topic> <method or domain>
site:arxiv.org <topic> survey
site:arxiv.org <topic> benchmark
site:arxiv.org <topic> implementation
```

If the topic has several names, search each name. Include related terms from the user's domain, such as model family, dataset, algorithm, architecture, metric, or application area.

Prefer papers that are:

- Directly relevant to the user's research question.
- Recent enough to reflect the current state of the field.
- Highly cited or clearly foundational when the area is established.
- Empirical, reproducible, or implementation-oriented when the user needs to build something.
- Surveys only when mapping the space or finding canonical references.

## Reading Checklist

For each useful paper, capture:

- Title, authors, year, and arXiv link.
- What problem the paper solves.
- The central method or design idea.
- Required inputs, assumptions, data, compute, or dependencies.
- Results that affect whether the method is worth implementing.
- Limitations, failure modes, or conditions where the method is inappropriate.
- Any details that translate directly into design choices, architecture, APIs, tests, evaluation metrics, or acceptance criteria.

Do not overfit to abstracts. Open the paper or arXiv page when possible, and inspect method sections, figures, ablations, appendices, or code links if they are important to implementation.

## Synthesis

Produce a compact research brief:

- `Question`: the topic or decision being researched.
- `Papers`: the most relevant papers with links.
- `Findings`: the ideas that should influence the user's plan.
- `Recommendation`: the chosen approach and why.
- `Risks`: assumptions, unknowns, and what to validate with tests or experiments.
- `Practical notes`: concrete code, API, data, model, evaluation, UX, or process implications when relevant.

If the research is inconclusive, say so plainly and recommend the next best query, experiment, or reversible planning step.

## Handoff

After the brief, continue with the user's requested planning, design, or implementation work if that is part of the same request. Preserve citations in the final answer when they materially justify a decision.

If arXiv does not contain enough relevant work, broaden to other primary sources such as official papers, conference proceedings, project repositories linked from papers, or standards documents. State that arXiv was insufficient and explain what sources filled the gap.
