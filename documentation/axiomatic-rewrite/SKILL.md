---
name: axiomatic-rewrite
description: Decompose a document into atomic axioms, get user approval on each, then reassemble a fresh document from only the approved axioms. Use when rewriting, distilling, or restructuring an existing document and every claim must be intentional.
disable-model-invocation: true
argument-hint: "[path or URL to source document]"
---
# Axiomatic Rewrite

Rewrite a document through Assembly Theory: the source document is a complex
object assembled from simpler parts. Break it down to its atomic axioms, let the
user select which survive, then build a fresh document from only the approved
parts.

The result is never a paraphrase of the original. It is a deliberately
assembled document where every sentence traces back to an approved axiom.

## Assembly Theory mapping

| Assembly Theory concept | In this workflow |
|---|---|
| Complex object | The source document |
| Atomic building blocks | Axioms — self-contained, verifiable propositions |
| Assembly operations | The user's approval, rejection, or edit of each axiom |
| Selection pressure | The approval gate — unsupported or irrelevant axioms die here |
| Reassembled object | The fresh document, built only from approved axioms |

## What counts as an axiom

An axiom is a single statement that:

1. **Stands alone** — a reader can judge it true or false without surrounding
   context.
2. **Is atomic** — it makes one claim, not two. "X is fast and Y is cheap" is
   two axioms.
3. **Is verifiable** — it references evidence, a source, or a concrete
   observation. "The API returns 200 in 12ms" is an axiom. "The API seems
   okay" is not.

## Workflow

### 1. Ingest the source

Read the document the user points to (file path, URL, or pasted text). If no
source is given, ask for one. Do not proceed without a real source document.

### 2. Decompose into axioms

Extract every claim, assertion, and factual statement from the document. Each
becomes a numbered axiom. Strip narrative connective tissue — transitions,
opener phrases, throat-clearing. Keep only the propositional content.

Present the full axiom list to the user in one block, numbered:

```
A1. <axiom text>
A2. <axiom text>
A3. <axiom text>
...
```

### 3. Approval gate (one axiom at a time)

Go through the axioms sequentially. For each axiom, present it and ask the
user for a verdict:

- **Approve** — the axiom is correct, supported, and belongs in the new document.
- **Reject** — the axiom is wrong, unsupported, or irrelevant. It will not appear.
- **Edit** — the axiom is partly right. The user provides a corrected version;
  the edited form becomes the approved axiom.

Use the `question` tool to present each axiom for approval. One axiom per
question — never batch approvals. The whole point is deliberate selection.

If the axiom list is long (>15), present them in small batches of 3-5 and
collect verdicts per batch, still one axiom at a time within each batch.

### 4. Assemble the fresh document

From the approved set (including edited versions), author a new document.

- **Do not copy sentences from the source.** Write fresh prose that carries
  the approved axioms.
- **Every claim in the new document must trace to an approved axiom.** If a
  sentence cannot be tagged with an axiom number, remove it or get approval
  for it as a new axiom.
- **Structure is your choice.** Group approved axioms into sections, order
  them logically, add transitions. The structure is new even though the
  content is approved.
- **Preserve the source document's intent.** If the source was a technical
  spec, the output is a technical spec. If it was a blog post, the output is
  a blog post. Match the genre, not the wording.

### 5. Present the result

Show the user:
1. The approved axiom list (with axiom numbers).
2. The fresh document.
3. A traceability note: for each paragraph in the new document, which axiom
   numbers it draws from.

Write the output file if the user provides a path. Do not write or overwrite
files unless asked.

## Stop conditions

- If the source document contains no extractable axioms (pure narrative, no
  claims), say so. The workflow needs propositional content to work.
- If the user rejects every axiom, do not author a document. Report that no
  approved axioms survived and stop.
- If the user adds new axioms during the approval gate (claims that were not
  in the source), accept them — mark them as `[NEW]` in the approved list and
  include them in the assembly.
- Do not invent axioms. If the source is thin, the output is thin. Better a
  short, honest document than a padded one.

## Common Rationalizations

| Excuse | Why it's wrong |
|--------|---------------|
| "The original is fine, I'll just clean it up" | Editing in place preserves structure-driven cruft. Decomposing forces you to justify every claim before it earns a place in the new document. |
| "I can approve all axioms at once to save time" | Bulk approval is no approval. The point is selection pressure — if every axiom survives, the gate added no value. |
| "I'll keep the good sentences from the original" | Sentences are not axioms. A sentence can carry three claims, two wrong. Decompose to the atomic level, then decide. |
| "The document is too short to bother decomposing" | Short documents have the highest ratio of unsupported claims per paragraph. They benefit most from the gate. |
| "I'll just write the new version and check it after" | Writing first, approving later reverses the workflow. The axioms must be approved before they enter the new document — otherwise the gate is decorative. |

## Output

1. The approved axiom list (numbered, with any `[NEW]` or `[EDITED]` markers).
2. The fresh document.
3. A traceability map: paragraph → axiom numbers.