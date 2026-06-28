#!/usr/bin/env bash
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"

fail() {
  echo "error: $*" >&2
  exit 1
}

published_prefix() {
  case "$1" in
    design/*|engineering/*|research|research/*) return 0 ;;
    *) return 1 ;;
  esac
}

manifest_file=".claude-plugin/plugin.json"
[ -f "$manifest_file" ] || fail "missing $manifest_file"

published_skills=()
while IFS= read -r line; do
  published_skills+=("$line")
done < <(
  find design engineering research -name SKILL.md -not -path '*/.git/*' 2>/dev/null \
    | sed 's#/SKILL.md$##' \
    | sort
)

manifest_skills=()
while IFS= read -r line; do
  manifest_skills+=("$line")
done < <(python3 - "$manifest_file" <<'PY'
import json
import sys
from pathlib import Path

manifest = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
for entry in sorted(item.removeprefix("./") for item in manifest.get("skills", [])):
    print(entry)
PY
)

if [ "${published_skills[*]}" != "${manifest_skills[*]}" ]; then
  echo "Published skills and manifest entries differ." >&2
  comm -23 <(printf "%s\n" "${published_skills[@]}") <(printf "%s\n" "${manifest_skills[@]}") | sed 's/^/missing from manifest: /' >&2
  comm -13 <(printf "%s\n" "${published_skills[@]}") <(printf "%s\n" "${manifest_skills[@]}") | sed 's/^/extra in manifest: /' >&2
  exit 1
fi

for skill in "${manifest_skills[@]}"; do
  published_prefix "$skill" || fail "manifest includes non-published skill: $skill"
  [ -f "$skill/SKILL.md" ] || fail "manifest entry has no SKILL.md: $skill"
done

while IFS= read -r skill_md; do
  python3 - "$skill_md" <<'PY'
import re
import sys
from pathlib import Path

path = Path(sys.argv[1])
text = path.read_text(encoding="utf-8")
match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
if not match:
    raise SystemExit(f"error: {path}: missing YAML frontmatter")
frontmatter = match.group(1)
if not re.search(r"^name:\s*\S+", frontmatter, re.M):
    raise SystemExit(f"error: {path}: missing name")
if not re.search(r"^description:\s*.+", frontmatter, re.M):
    raise SystemExit(f"error: {path}: missing description")
PY
done < <(find . -name SKILL.md -not -path './.git/*' | sort)

readme="README.md"
[ -f "$readme" ] || fail "missing README.md"

for skill in "${published_skills[@]}"; do
  name="$(python3 - "$skill/SKILL.md" <<'PY'
import re
import sys
from pathlib import Path
text = Path(sys.argv[1]).read_text(encoding="utf-8")
print(re.search(r"^name:\s*(\S+)", text, re.M).group(1))
PY
)"
  rg -q "/$name|\\[$name\\]|$skill/SKILL.md" "$readme" || fail "README missing published skill: $name ($skill)"
done

if [ -d in-progress ] || [ -d deprecated ]; then
  while IFS= read -r draft_skill; do
    rel="${draft_skill#./}"
    rel="${rel%/SKILL.md}"
    if printf "%s\n" "${manifest_skills[@]}" | grep -qx "$rel"; then
      fail "draft/deprecated skill appears in manifest: $rel"
    fi
  done < <(find in-progress deprecated -name SKILL.md 2>/dev/null | sort)
fi

if find . \( -name .DS_Store -o -name __pycache__ -o -name '*.pyc' \) -not -path './.git/*' | grep -q .; then
  find . \( -name .DS_Store -o -name __pycache__ -o -name '*.pyc' \) -not -path './.git/*' >&2
  fail "generated files present"
fi

rg -n "init-agent-harness|\\.agents/skills/design-md-style|design-md-style-(picker|apply|audit)/scripts|grill-with-docs|improve-codebase-architecture" \
  --glob '!**/.git/**' \
  --glob '!scripts/check-pack.sh' \
  . && fail "stale references found"

echo "Pack check passed: ${#published_skills[@]} published skill(s)."
