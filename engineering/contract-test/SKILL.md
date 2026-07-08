---
name: contract-test
description: Test the boundary between two systems by the contract, not the implementation. Use for APIs, integrations, and shared interfaces.
when_to_use: an API endpoint, a service integration, a webhook, a shared schema
---
# Contract Test
Test what the two sides AGREED on, so either can change internals without breaking the other.
- Assert the **shape**: required fields, types, status codes, error format — not internal logic.
- Cover the contract's edges: missing optional fields, the documented error responses, pagination bounds, versioning.
- For consumers: test against the real contract (recorded/real responses), not a mock you wrote to match your assumptions — that mock drifts and lies.
- One source of truth for the schema; both sides validate against it.

Done when: every documented field, status code, and error format is covered by an assertion. Every documented error response has a test. Pagination bounds are verified at both ends.

## Gotchas
- A green unit test with a wrong mock is worse than no test — the mock drifts and lies. Pin the contract.
- Missing optional fields tests must assert the consumer handles absence, not just that the server allows it.
- Versioning: a contract test that pins v1 when v2 shipped catches drift late. Test the version the consumer actually uses.

## Common Rationalizations

| Excuse | Why it's wrong |
|--------|---------------|
| "I'll just write a mock that matches my expectations" | A mock you wrote to match your assumptions drifts and lies. Test against the real contract. |
| "A green unit test means the integration works" | Unit tests test YOUR code. Contract tests test the BOUNDARY — what the other side promises to deliver. |
| "The API is stable, contract tests are overkill" | Stable APIs change at the worst times — migrations, refactors, dependency bumps. Contract tests catch drift before production. |
| "Missing optional fields is an edge case" | Production systems send incomplete payloads constantly. If a missing field crashes the consumer, it's not an edge case. |
| "I'll add contract tests when the integration breaks" | By then you're firefighting. Contract tests prevent breakage, they don't diagnose it. |
