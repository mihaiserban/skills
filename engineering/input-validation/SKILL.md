---
name: input-validation
description: Validate and constrain untrusted input at the boundary. Use on any handler that accepts external data.
when_to_use: request bodies, query params, file uploads, webhook payloads, form data
---
# Input Validation
Validate at the edge, before the data touches logic or storage.
- **Schema** — type, required fields, allowed values. Reject unknown fields rather than ignoring them.
- **Bounds** — string length, number ranges, array size. An unbounded input is a DoS and a memory bomb.
- **Format** — emails, UUIDs, dates parsed and re-validated, not trusted as strings.
- **Files** — size limit, type allowlist (check content, not just extension), no path traversal in names.
- Reject with a clear 4xx and a message that says what's wrong — without leaking internals.
Never trust "it comes from our own frontend". The request can come from anywhere.

## Common Rationalizations

| Excuse | Why it's wrong |
|--------|---------------|
| "It comes from our own frontend" | The request can come from anywhere — curl, a script, a compromised client. Backend is the only trust boundary. |
| "I'll add validation later" | Once invalid data is in the database, cleanup is exponentially harder than rejecting it at the edge. |
| "The ORM/library handles it" | Frameworks protect against injection, not bounds, duplicate keys, format violations, or business logic constraints. |
| "The schema already validates types" | Type validation catches null vs string. It doesn't catch 10MB strings, negative ages, or future dates. |
| "Rejecting unknown fields breaks the client" | Accepting unknown fields silently drops data. The client doesn't know its payload was partially ignored. |
