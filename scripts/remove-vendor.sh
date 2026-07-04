#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

usage() {
  echo "Usage: $0 <name>"
  echo ""
  echo "Remove a vendored skill pack (git submodule) from vendor/"
  echo ""
  echo "Example:"
  echo "  $0 agent-browser"
}

if [ $# -eq 0 ] || [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
  usage
  exit 1
fi

NAME="$1"
VENDOR_PATH="vendor/$NAME"

if [ ! -d "$REPO_ROOT/$VENDOR_PATH" ]; then
  echo "Error: $VENDOR_PATH does not exist" >&2
  exit 1
fi

echo "Removing vendor skill: $NAME"

git -C "$REPO_ROOT" submodule deinit -f "$VENDOR_PATH"
git -C "$REPO_ROOT" rm -f "$VENDOR_PATH"

MODULES_PATH="$REPO_ROOT/.git/modules/$VENDOR_PATH"
if [ -d "$MODULES_PATH" ]; then
  rm -rf "$MODULES_PATH"
fi

echo ""
echo "Done. Run 'bash scripts/setup.sh' to update the plugin manifest."
