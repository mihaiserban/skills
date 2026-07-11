#!/usr/bin/env bash
set -euo pipefail
# Start the full eval pipeline.
#
# Usage:
#   scripts/start-evals.sh <skill-path> [--parallel N] [--timeout SECS] [--model M] [--provider docker|local] [--smoke|--reliable|--regression]
#   scripts/start-evals.sh --all [--parallel N] [--timeout SECS] [--model M] [--provider docker|local] [--smoke|--reliable|--regression]
#
# Runs: eval-runner.py → eval-grade.py → eval-aggregate.py --output html

REPO="$(cd "$(dirname "$0")/.." && pwd)"

ALL_MODE=false
for a in "$@"; do
  [ "$a" = "--all" ] && ALL_MODE=true && break
done

if $ALL_MODE; then
  echo "=== Running evals for ALL skills ==="
  python3 "$REPO/scripts/eval-runner.py" --all "$@"

  echo ""
  echo "=== Grading ALL results ==="
  python3 "$REPO/scripts/eval-grade.py" --all "$@"

  echo ""
  echo "=== Aggregating ALL benchmarks ==="
  python3 "$REPO/scripts/eval-aggregate.py" --all --output html

  echo ""
  echo "=== Pipeline complete ==="
  exit 0
fi

if [ $# -eq 0 ]; then
  echo "Usage: scripts/start-evals.sh <skill-path> [flags]" >&2
  echo "       scripts/start-evals.sh --all [flags]" >&2
  exit 1
fi

SKILL="$1"
shift
SKILL_FULL="${REPO}/${SKILL}"
if [ ! -f "$SKILL_FULL/evals/evals.json" ]; then
  echo "error: no evals/evals.json found at $SKILL_FULL" >&2
  exit 1
fi

echo "=== Running evals for $(basename "$SKILL_FULL") ==="
python3 "$REPO/scripts/eval-runner.py" "$SKILL_FULL" "$@"

echo ""
echo "=== Grading results ==="
python3 "$REPO/scripts/eval-grade.py" "$SKILL_FULL" "$@"

echo ""
echo "=== Aggregating benchmark ==="
python3 "$REPO/scripts/eval-aggregate.py" "$SKILL_FULL" --output html

echo ""
echo "=== Pipeline complete ==="
