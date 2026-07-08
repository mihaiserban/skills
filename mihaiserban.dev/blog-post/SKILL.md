---
name: blog-post
description: Distill a conversation or completed task into a mihaiserban.dev blog post.
disable-model-invocation: true
argument-hint: "[topic or session summary]"
---
# Blog Post

Distill a chat session or completed body of work into a polished blog post for mihaiserban.dev. The blog is a Gatsby site; posts live in `content/blog/` as Markdown.

## Blog conventions

### Frontmatter schema

```yaml
---
slug: url-friendly-slug
title: "Post Title in Title Case"
description: "One sentence summary of the post. Used for SEO and social cards."
date: "YYYY-MM-DDTHH:MM+03:00"
hidden: false
tags: ["lowercase", "kebab-or-single-word"]
---
```

### Tone and structure

First-person, conversational. Lead with the problem or motivation — no warm-up fluff. Alternate between concrete examples and the principles they illustrate. Separate major sections with `---` horizontal rules. Use `##` level-2 section headings (no level-1 after the title).

End with a "Bottom line" or "What's next" section. Reference external sources with inline Markdown links. No footnote-style citations.

### Code and visuals

- Code blocks: fenced triple backticks with language identifier (`yaml`, `sql`, `javascript`, `text`).
- ASCII architecture diagrams in `text` blocks.
- Inline code for file paths, variable names, commands.
- Tables for comparison data (before/after, dimensions, selection rules).
- Images go in `/static/images/blog/` and are referenced as `![alt](/images/blog/filename.ext)`.
- No walls of text: short paragraphs, every claim followed by evidence.

### Repository

Posts go in the blog repo at `~/code/personal/projects/mihaiserban.dev/content/blog/`. The filename is the slug with `.md` extension. Do not prefix with a date.

## Workflow

1. **Identify the post.** What was done? What was learned? What pattern or insight emerged? A good post has one clear thesis, not a diary of everything that happened.

2. **Gather evidence.** From the session: key decisions, code snippets, architecture decisions, performance numbers, before/after comparisons, cited papers. Only include what supports the thesis.

3. **Draft the frontmatter.** Slug from the one-line summary. Date in `+03:00` timezone, current date. Tags as lowercase short strings.

4. **Write the post.** Follow the structure: hook paragraph → evidence/narrative sections separated by `---` → summary section → references (if citing papers).

5. **Write to the blog repo.** Output the file to `~/code/personal/projects/mihaiserban.dev/content/blog/<slug>.md`. Do not git commit or push unless asked.

## Stop conditions

- If the session doesn't contain enough concrete material for a post, say so. A post needs at least one of: a pattern discovered, a problem solved, performance numbers, an architecture decision, or research findings.
- Only write one post per invocation. If the session contains material for multiple posts, ask which to write first.
- Do not fabricate evidence. If a claim wasn't demonstrated in the session, don't include it.

## Common Rationalizations

| Excuse | Why it's wrong |
|--------|---------------|
| "This session wasn't blog-worthy" | Small insights compound. A pattern you noticed, a problem you solved, a decision you made — write it while it's fresh. |
| "I'll write it up when the work is fully complete" | The best posts are written from active context. By "completion," the details have faded. |
| "I don't have enough material for a full post" | A 300-word post with one concrete insight beats 3000 words of filler. The blog rewards precision, not length. |
| "Nobody reads blog posts about this kind of work" | The audience is future-you. Blog posts are cached reasoning you can link to instead of re-explaining. |
| "Writing takes too long, I have other things to do" | Structured workflow + frontmatter template = 15 minutes. You'll spend longer re-explaining the same thing next week. |

## Output

A single `.md` file in the blog repo with valid frontmatter, written in the blog's voice and structure. Inform the user of the path and whether it's ready to commit.
