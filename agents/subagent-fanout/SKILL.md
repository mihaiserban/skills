---
name: subagent-fanout
description: Parallelize independent sub-jobs across fresh-context subagents instead of one bloated context. Use when a goal branches into many independent pieces.
when_to_use: analyze N items, fix M files, search K sources, anything embarrassingly parallel
---
# Subagent Fan-out
One context loaded with ten jobs' worth of material is the exact shape that triggers context rot. Ten small contexts don't.
- Spawn one subagent per independent unit (one file, one source, one check). Each gets a fresh context window.
- An **orchestrator** synthesizes their results — it never does the per-unit work itself.
- Give each worker a tight role and only the input it needs.
- Use ONLY when the pieces are genuinely independent. Sequential dependencies stay in one chain.

Done when: every unit has a completed result from a worker subagent, the orchestrator has synthesized them into a single summary, and no worker was blocked on another's output.

## Gotchas
- Hidden dependency trap: two units that look independent but one needs the other's output. Serialize them — the fan-out fails silently when worker B stalls.
- Orchestrator drift: the orchestrator starts doing per-unit work because it's "just one more". If it touches the work, refactor into a worker.
- Worker starvation: a worker with too broad a role recreates the original context-bloat problem. One file, one source, one check.
