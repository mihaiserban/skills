---
name: governance-fanout
description: Fan out independent sub-jobs across fresh-context workers using file-based task specs and results. Use when a goal branches into many independent pieces.
when_to_use: analyze N items, fix M files, search K sources, anything embarrassingly parallel
---
# Governance Fan-out

One context loaded with ten jobs' worth of material triggers context rot. Ten small contexts with file-based handoffs don't.

## Workflow

1. **PLAN:** Write a task spec for each independent unit to `.agent-state/tasks/<id>.yaml`:
   ```yaml
   goal: what to accomplish
   constraints: any limits
   expected_output_path: .agent-state/results/<id>.yaml
   context_files: [files to read first]
   blocked_on: [dependent task IDs, or null]
   ```

2. **FAN OUT:** Spawn one worker per independent unit. Each worker brief is minimal:
   `Read .agent-state/tasks/<id>.yaml. Do the work. Write result to .agent-state/results/<id>.yaml. Return confirmation.`

3. **COLLECT:** Workers return short confirmations. Collect them. Do NOT read result files — workers write results to disk, not your context.

4. **SYNTHESIZE:** When all workers confirm completion, spawn a fresh synthesis agent:
   `Read all .agent-state/results/*.yaml files. Synthesize. Return final answer.`

## Rules

- Governance NEVER does per-unit work. If you start reading a file a worker should read, stop and spawn a worker.
- Governance NEVER synthesizes. That is the synthesis agent's job.
- Each worker gets a FRESH context window containing only its task spec + needed files.
- Use `.agent-state/` for ALL task specs and results. Keep it in `.gitignore`.
- Sequential dependencies: if task B depends on task A, fan out A first, wait for completion, then fan out B.

## Done When

Every worker confirmed completion. Synthesis agent produced final output. No worker was blocked on another's incomplete output.

## Gotchas

- Hidden dependency trap: two units that look independent but one needs the other's output. Serialize them.
- Governance drift: governance starts doing per-unit work because "it's just one more." If it touches the work, refactor into a worker.
- Worker starvation: a worker with too broad a role recreates the context-bloat problem. One goal, one result file.
- Result bloat: a worker returns full results in its confirmation instead of writing to file. If confirmation exceeds 3 lines, ask the worker to truncate and write to file instead.
