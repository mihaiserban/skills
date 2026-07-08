---
name: sql-review
description: Review SQL and ORM queries for correctness, safety, and performance before they ship.
when_to_use: new query, a migration, an N+1 suspicion, a slow endpoint
---
# SQL Review
- **Injection** — parameterized, always. No string interpolation into SQL.
- **N+1** — a query inside a loop? Replace with a join or a batched IN.
- **Missing index** — does the WHERE/JOIN/ORDER BY hit an indexed column? If not, the table scan will surface at scale.
- **Unbounded** — SELECT with no LIMIT on a growing table; a JOIN that fans out rows.
- **Transactions** — multi-write operations wrapped so a partial failure can't corrupt state.
- **Migrations** — reversible (up AND down), and safe on a live table (no blocking lock on a hot table at peak).

Output: each issue with the line and the rewrite. Show the EXPLAIN if performance is the concern. Done when every query in the diff has been checked against all six bullets.

## Common Rationalizations

| Excuse | Why it's wrong |
|--------|---------------|
| "This query is simple, no review needed" | Simple queries become problematic at scale. A missing LIMIT on a growing table is a time bomb. |
| "The ORM handles injection" | ORMs prevent injection, not N+1, missing indexes, or unbounded result sets. Check the generated SQL. |
| "Performance doesn't matter yet" | Schema decisions (indexes, column types) are expensive to change later. Picking the right index now costs nothing. |
| "I tested it with a few rows and it's fast" | Queries that are fast on 100 rows can table-scan at 100K. Test with production-scale data or an EXPLAIN. |
| "The migration is backwards-compatible" | A migration that runs without errors can still lock tables for minutes on a hot production database. |

## Gotchas
- ORM magic: an ORM that looks like a loop-free attribute access may still generate N+1 queries. Check the generated SQL, not the surface code.
- Index blind spot: a column that is indexed but wrapped in a function (`WHERE LOWER(name)`) bypasses the index. Watch for function calls in WHERE/JOIN.
- Migration safety: `ALTER TABLE ... ADD COLUMN` with a default on a hot table can lock for minutes at scale. Split into ADD + backfill + SET DEFAULT.
