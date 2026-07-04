#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

usage() {
  echo "Usage: $0 <repo-url> [--name <name>]"
  echo ""
  echo "Add an external skill pack as a git submodule under vendor/"
  echo ""
  echo "Options:"
  echo "  --name, -n   Submodule name (default: derived from repo URL)"
  echo ""
  echo "Examples:"
  echo "  $0 https://github.com/vercel-labs/agent-browser"
  echo "  $0 https://github.com/vercel-labs/agent-browser --name agent-browser"
  echo ""
  echo "After adding, run 'bash scripts/setup.sh' to update the plugin manifest."
}

NAME=""
URL=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --name|-n)
      NAME="$2"; shift 2 ;;
    --help|-h)
      usage; exit 0 ;;
    -*)
      echo "Unknown option: $1" >&2; usage; exit 1 ;;
    *)
      if [ -z "$URL" ]; then
        URL="$1"; shift
      else
        echo "Unexpected argument: $1" >&2; usage; exit 1
      fi
      ;;
  esac
done

if [ -z "$URL" ]; then
  echo "Error: repo URL is required" >&2
  usage
  exit 1
fi

if [ -z "$NAME" ]; then
  NAME="${URL##*/}"
  NAME="${NAME%.git}"
fi

VENDOR_PATH="vendor/$NAME"

if [ -d "$REPO_ROOT/$VENDOR_PATH" ]; then
  echo "Error: $VENDOR_PATH already exists" >&2
  exit 1
fi

echo "Adding vendor skill: $NAME"
echo "  URL:  $URL"
echo "  Path: $VENDOR_PATH"
echo ""

git -C "$REPO_ROOT" submodule add "$URL" "$VENDOR_PATH"

echo ""
echo "Done. Run 'bash scripts/setup.sh' to update the plugin manifest and symlinks."
