#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}  Skills setup${NC}"
echo -e "${CYAN}  Repo: ${REPO_ROOT}${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# ── Helpers ──────────────────────────────────────────────────────────

is_pi()     { command -v pi >/dev/null 2>&1 || [ -d "$HOME/.agents" ]; }
is_claude() { command -v claude >/dev/null 2>&1; }
is_opencode(){ command -v opencode >/dev/null 2>&1; }
is_codex()  { command -v codex >/dev/null 2>&1; }

link_harness() {
  local label="$1" parent="$2" name="$3" harness_id="$4"
  local target="${parent}/${name}"

  # pi special case: repo lives at its own target path → nothing to do
  if [ "$harness_id" = "pi" ] && [ "$REPO_ROOT" = "$target" ]; then
    echo " ⊘  $label (repo is already at $target)"
    return 1
  fi

  # Already a symlink to us
  if [ -L "$target" ] && [ "$(readlink "$target")" = "$REPO_ROOT" ]; then
    echo " ⊘  $label (already linked)"
    return 1
  fi

  # Something else at target → warn, skip
  if [ -e "$target" ]; then
    echo -e " ${YELLOW}⚠${NC}  $label: $target already exists (not our symlink) — skipping"
    return 1
  fi

  mkdir -p "$(dirname "$target")"
  ln -s "$REPO_ROOT" "$target"
  echo -e " ${GREEN}✓${NC}  $label → $target"
  return 0
}

# ── Phase 1: Symlink ─────────────────────────────────────────────────

SYMLINKED=0
SKIPPED=0
NOT_FOUND=0

if is_pi; then
  if link_harness "pi" "$HOME/.agents" "skills" "pi"; then ((SYMLINKED++)); else ((SKIPPED++)); fi
else
  echo -e " ${RED}✗${NC}  pi (not installed)"; ((NOT_FOUND++))
fi

if is_claude; then
  if link_harness "Claude Code" "$HOME/.claude" "skills/mihaiserban-skills" "claude"; then ((SYMLINKED++)); else ((SKIPPED++)); fi
else
  echo -e " ${RED}✗${NC}  Claude Code (not installed)"; ((NOT_FOUND++))
fi

if is_opencode; then
  if link_harness "OpenCode" "$HOME/.opencode" "skills/mihaiserban-skills" "opencode"; then ((SYMLINKED++)); else ((SKIPPED++)); fi
else
  echo -e " ${RED}✗${NC}  OpenCode (not installed)"; ((NOT_FOUND++))
fi

if is_codex; then
  if link_harness "Codex" "$HOME/.codex" "skills/mihaiserban-skills" "codex"; then ((SYMLINKED++)); else ((SKIPPED++)); fi
else
  echo -e " ${RED}✗${NC}  Codex (not installed)"; ((NOT_FOUND++))
fi

echo ""

# ── Phase 2: Generate Claude Code plugin.json ────────────────────────

PLUGIN_DIR="$REPO_ROOT/.claude-plugin"
PLUGIN_FILE="$PLUGIN_DIR/plugin.json"

echo -e "${CYAN}Generating Claude Code plugin manifest...${NC}"

SKILL_DIRS=()
while IFS= read -r -d '' skill_md; do
  skill_dir="$(dirname "$skill_md")"
  rel="${skill_dir#$REPO_ROOT/}"
  SKILL_DIRS+=("$rel")
done < <(find "$REPO_ROOT" -name "SKILL.md" -not -path "*/.git/*" -print0 | sort -z)

if [ ${#SKILL_DIRS[@]} -eq 0 ]; then
  echo -e " ${YELLOW}⚠${NC}  No SKILL.md files found — skipping plugin.json"
else
  mkdir -p "$PLUGIN_DIR"

  {
    echo "{"
    echo "  \"name\": \"mihaiserban-skills\","
    echo "  \"skills\": ["
    last_idx=$((${#SKILL_DIRS[@]} - 1))
    for i in "${!SKILL_DIRS[@]}"; do
      if [ "$i" -eq "$last_idx" ]; then
        echo "    \"./${SKILL_DIRS[$i]}\""
      else
        echo "    \"./${SKILL_DIRS[$i]}\","
      fi
    done
    echo "  ]"
    echo "}"
  } > "$PLUGIN_FILE"

  echo -e " ${GREEN}✓${NC}  $PLUGIN_FILE"
  for dir in "${SKILL_DIRS[@]}"; do
    echo "   • $dir"
  done
fi

echo ""

# ── Summary ──────────────────────────────────────────────────────────

echo -e "${CYAN}Summary${NC}"
echo ""
echo -e " Linked:  ${GREEN}${SYMLINKED}${NC}"
echo -e " Skipped: ${YELLOW}${SKIPPED}${NC}"
echo -e " Missing: ${RED}${NOT_FOUND}${NC}"
echo ""
echo -e "${CYAN}Verification${NC}"
echo ""
echo "  pi:      subagent({ action: \"list\" })"
echo "  claude:  /setup-skills    (or check ~/.claude/skills/)"
echo "  opencode: check ~/.opencode/skills/"
echo "  codex:   check ~/.codex/skills/"
echo ""
echo -e "${GREEN}Done.${NC}"
