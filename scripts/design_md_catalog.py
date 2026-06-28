#!/usr/bin/env python3
"""Find, clone, update, and inspect awesome-design-md DESIGN.md profiles."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

REPO_URL = "https://github.com/voltagent/awesome-design-md.git"
DEFAULT_CACHE_ROOT = Path.home() / ".cache" / "agents" / "awesome-design-md"
KNOWN_ROOTS = [
    DEFAULT_CACHE_ROOT,
    Path.home() / "code" / "personal" / "projects" / "design_skills" / "awesome-design-md",
]


def slugify(value: str) -> str:
    value = value.strip().lower().replace("&", "and")
    value = re.sub(r"[^a-z0-9.]+", "-", value)
    value = re.sub(r"-{2,}", "-", value)
    return value.strip("-")


def has_design_md(root: Path) -> bool:
    design_dir = root / "design-md"
    return design_dir.is_dir() and any(design_dir.glob("*/DESIGN.md"))


def candidate_roots() -> list[Path]:
    roots: list[Path] = []
    env_root = os.environ.get("DESIGN_MD_ROOT")
    if env_root:
        roots.append(Path(env_root).expanduser())

    cwd = Path.cwd().resolve()
    for parent in [cwd, *cwd.parents]:
        roots.extend(
            [
                parent,
                parent / "awesome-design-md",
                parent / "design_skills" / "awesome-design-md",
            ]
        )

    roots.extend(KNOWN_ROOTS)
    deduped: list[Path] = []
    seen: set[Path] = set()
    for root in roots:
        resolved = root.expanduser().resolve()
        if resolved not in seen:
            deduped.append(resolved)
            seen.add(resolved)
    return deduped


def find_root() -> Path:
    for root in candidate_roots():
        if has_design_md(root):
            return root
    raise SystemExit(
        "Could not find awesome-design-md. Run:\n"
        f"  python3 {Path(__file__).resolve()} ensure\n"
        "or set DESIGN_MD_ROOT=/path/to/awesome-design-md."
    )


def ensure_root(update: bool = False) -> Path:
    env_root = os.environ.get("DESIGN_MD_ROOT")
    target = Path(env_root).expanduser() if env_root else DEFAULT_CACHE_ROOT
    target = target.resolve()

    if not env_root:
        for root in candidate_roots():
            if has_design_md(root):
                if update and (root / ".git").is_dir():
                    subprocess.run(["git", "-C", str(root), "pull", "--ff-only"], check=True)
                return root

    if has_design_md(target):
        if update and (target / ".git").is_dir():
            subprocess.run(["git", "-C", str(target), "pull", "--ff-only"], check=True)
        return target

    if target.exists() and any(target.iterdir()):
        raise SystemExit(
            f"{target} exists but is not an awesome-design-md checkout. "
            "Set DESIGN_MD_ROOT to a valid checkout or choose an empty cache path."
        )

    target.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "clone", "--depth", "1", REPO_URL, str(target)], check=True)
    if not has_design_md(target):
        raise SystemExit(f"Cloned {REPO_URL}, but no design-md/*/DESIGN.md files were found.")
    return target


def read_text(path: Path, limit: int | None = None) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    return text if limit is None else "\n".join(text.splitlines()[:limit])


def read_collection_descriptions(root: Path) -> dict[str, str]:
    readme = root / "README.md"
    if not readme.exists():
        return {}
    descriptions: dict[str, str] = {}
    pattern = re.compile(r"^- \[\*\*(.+?)\*\*\]\((.+?)\) - (.+)$")
    for line in readme.read_text(encoding="utf-8", errors="replace").splitlines():
        match = pattern.match(line.strip())
        if not match:
            continue
        name, url, description = match.groups()
        url_slug = url.rstrip("/").split("/")[-2] if url.endswith("/design-md") else ""
        for key in {slugify(name), slugify(url_slug)}:
            if key:
                descriptions[key] = description.strip()
    return descriptions


def first_summary(path: Path) -> str:
    text = read_text(path, 80)
    desc_match = re.search(r"^description:\s*(.+)$", text, re.MULTILINE)
    if desc_match:
        return desc_match.group(1).strip().strip('"')
    for line in text.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and not stripped.startswith("---"):
            return stripped[:220]
    return "No summary found."


def entries(root: Path) -> list[dict[str, str]]:
    descriptions = read_collection_descriptions(root)
    result: list[dict[str, str]] = []
    for path in sorted((root / "design-md").glob("*/DESIGN.md")):
        slug = path.parent.name
        result.append(
            {
                "slug": slug,
                "path": str(path),
                "description": descriptions.get(slug, first_summary(path)),
            }
        )
    return result


def resolve(entries_: list[dict[str, str]], query: str) -> dict[str, str] | None:
    query_slug = slugify(query)
    for item in entries_:
        if item["slug"] == query_slug:
            return item
    for item in entries_:
        if query_slug and query_slug in slugify(item["slug"]):
            return item
    return None


def score(item: dict[str, str], terms: list[str]) -> int:
    haystack = f"{item['slug']} {item['description']}".lower()
    return sum(3 if term in item["slug"].lower() else 1 for term in terms if term in haystack)


def cmd_ensure(args: argparse.Namespace) -> int:
    root = ensure_root(update=args.update)
    print(root)
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    root = find_root()
    for item in entries(root):
        print(f"{item['slug']}\t{item['description']}")
    return 0


def cmd_search(args: argparse.Namespace) -> int:
    root = find_root()
    terms = [term.lower() for term in re.findall(r"[a-zA-Z0-9.]+", args.query)]
    ranked = sorted(
        ((score(item, terms), item) for item in entries(root)),
        key=lambda pair: (-pair[0], pair[1]["slug"]),
    )
    shown = 0
    for item_score, item in ranked:
        if item_score <= 0:
            continue
        print(f"{item['slug']}\t{item['description']}\n  {item['path']}")
        shown += 1
        if shown >= args.limit:
            break
    if shown == 0:
        print("No matches. Try broader terms or run the list command.", file=sys.stderr)
        return 1
    return 0


def cmd_path(args: argparse.Namespace) -> int:
    root = find_root()
    item = resolve(entries(root), args.slug)
    if not item:
        print(f"No DESIGN.md profile matched: {args.slug}", file=sys.stderr)
        return 1
    print(item["path"])
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    root = find_root()
    item = resolve(entries(root), args.slug)
    if not item:
        print(f"No DESIGN.md profile matched: {args.slug}", file=sys.stderr)
        return 1
    print(f"# {item['slug']}")
    print(f"Source: {item['path']}")
    print(f"Summary: {item['description']}")
    print()
    print(read_text(Path(item["path"]), args.lines))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    ensure_parser = subparsers.add_parser("ensure", help="Clone the catalog if missing")
    ensure_parser.add_argument("--update", action="store_true", help="git pull an existing checkout")
    ensure_parser.set_defaults(func=cmd_ensure)

    list_parser = subparsers.add_parser("list", help="List all available profiles")
    list_parser.set_defaults(func=cmd_list)

    search_parser = subparsers.add_parser("search", help="Search profile names and summaries")
    search_parser.add_argument("query")
    search_parser.add_argument("--limit", type=int, default=8)
    search_parser.set_defaults(func=cmd_search)

    path_parser = subparsers.add_parser("path", help="Print the DESIGN.md path for a slug")
    path_parser.add_argument("slug")
    path_parser.set_defaults(func=cmd_path)

    show_parser = subparsers.add_parser("show", help="Show a profile summary and first lines")
    show_parser.add_argument("slug")
    show_parser.add_argument("--lines", type=int, default=120)
    show_parser.set_defaults(func=cmd_show)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
