#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}Uninstalling skills symlinks...${NC}"
echo ""

# Same harness paths as setup.sh
HARNESSES=(
  "pi|$HOME/.agents|skills|pi"
  "claude|$HOME/.claude|skills/mihaiserban-skills|Claude Code"
  "opencode|$HOME/.opencode|skills/mihaiserban-skills|OpenCode"
  "codex|$HOME/.codex|skills/mihaiserban-skills|Codex"
)

REMOVED=()
SKIPPED=()

for entry in "${HARNESSES[@]}"; do
  IFS='|' read -r harness parent name label <<< "$entry"
  target="${parent}/${name}"

  # pi special: if repo IS the actual skills dir, don't remove it
  if [ "$harness" = "pi" ] && [ "$REPO_ROOT" = "$target" ]; then
    SKIPPED+=("$label (repo IS ~/.agents/skills — not removing)")
    continue
  fi

  if [ -L "$target" ] && [ "$(readlink "$target")" = "$REPO_ROOT" ]; then
    rm "$target"
    echo -e " ${GREEN}✓${NC}  Removed $target"
    REMOVED+=("$label")
  elif [ -e "$target" ]; then
    SKIPPED+=("$label ($target exists but is not our symlink)")
  else
    SKIPPED+=("$label (nothing at $target)")
  fi
done

echo ""
if [ ${#REMOVED[@]} -gt 0 ]; then
  echo -e " ${GREEN}Removed:${NC}"
  for h in "${REMOVED[@]}"; do
    echo "   ✓ $h"
  done
fi

if [ ${#SKIPPED[@]} -gt 0 ]; then
  echo -e " ${YELLOW}Skipped:${NC}"
  for h in "${SKIPPED[@]}"; do
    echo "   ⊘ $h"
  done
fi

echo ""
echo -e "${GREEN}Done.${NC}"
