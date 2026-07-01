#!/usr/bin/env python3
"""Create a TASTE.md scaffold from reference text files."""

from __future__ import annotations

import argparse
from pathlib import Path

TEXT_SUFFIXES = {
    ".css",
    ".html",
    ".js",
    ".jsx",
    ".md",
    ".mdx",
    ".ts",
    ".tsx",
    ".txt",
}


def iter_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_dir():
            files.extend(
                child
                for child in sorted(path.rglob("*"))
                if child.is_file() and child.suffix.lower() in TEXT_SUFFIXES
            )
        elif path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
            files.append(path)
    return files


def excerpt(path: Path, max_chars: int) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    text = "\n".join(line.rstrip() for line in text.splitlines() if line.strip())
    return text[:max_chars]


def build_scaffold(files: list[Path], max_chars: int) -> str:
    source_lines = "\n".join(f"- `{path}`" for path in files) or "- No text references supplied."
    excerpts = []
    for path in files[:12]:
        content = excerpt(path, max_chars)
        excerpts.append(f"### {path}\n\n````text\n{content}\n````")
    excerpt_block = "\n\n".join(excerpts) or "_Add screenshots, links, notes, or DESIGN.md files._"

    return f"""# TASTE.md

## Product Context

- Product:
- Audience:
- Primary interface job:
- Category risks:

## Taste Values

- Prefer:
- Prefer:
- Prefer:

## Positive References

{source_lines}

## Anti-Patterns

- Avoid:
- Avoid:
- Avoid:

## Decision Rules

- Prefer X over Y when Z.
- Spend visual drama on one memorable element; keep surrounding UI disciplined.
- If the design feels generic, remove weak decoration before adding new effects.

## Execution Dials

- Layout variance: /10
- Motion intensity: /10
- Visual density: /10

## Design Locks

- Accent:
- Shape:
- Type:
- Theme:
- CTA language:
- Asset strategy:

## Critique Questions

- What is the visual thesis?
- What should become quieter?
- Could this belong to ten other products?
- Is typography, spacing, or imagery carrying the personality?
- What did we remove?

## Preflight Checks

- Hero or primary workspace fits its viewport and has one clear job.
- Accent, radius, type, and CTA language are consistent.
- Repeated sections do not reuse the same layout family without purpose.
- Buttons, forms, focus rings, and media overlays pass contrast checks.
- Mobile layout is explicitly handled for every multi-column section.
- Empty, loading, error, and active states exist where the product needs them.

## Workflow Modes

- Explore:
- Build:
- Audit:
- Refine:
- Ship:

## Playbooks To Load

- Selection:
- Implementation:
- Audit:

## Memory

- Recently used directions:
- Directions to avoid repeating:

## Reference Excerpts

{excerpt_block}
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path, help="Reference files or folders")
    parser.add_argument("--output", "-o", type=Path, default=Path("TASTE.md"))
    parser.add_argument("--max-chars", type=int, default=1600)
    args = parser.parse_args()

    files = iter_files(args.paths)
    args.output.write_text(build_scaffold(files, args.max_chars), encoding="utf-8")
    print(f"Wrote {args.output} from {len(files)} text reference file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
