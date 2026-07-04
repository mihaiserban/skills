#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}  Skills update${NC}"
echo -e "${CYAN}  Repo: ${REPO_ROOT}${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# ── Pull repo ─────────────────────────────────────────────────────────

echo -e "${CYAN}Pulling latest changes...${NC}"
git -C "$REPO_ROOT" pull
echo ""

# ── Update submodules ──────────────────────────────────────────────────

if [ -f "$REPO_ROOT/.gitmodules" ]; then
  echo -e "${CYAN}Updating vendored skill packs...${NC}"
  git -C "$REPO_ROOT" submodule update --init --recursive --remote
  echo ""
else
  echo -e " ${YELLOW}⊘${NC}  No submodules to update"
  echo ""
fi

# ── Regenerate manifests ───────────────────────────────────────────────

echo -e "${CYAN}Regenerating harness manifests...${NC}"
bash "$REPO_ROOT/scripts/setup.sh"
