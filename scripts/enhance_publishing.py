#!/usr/bin/env python3
"""Enhance existing chapters with commercial opening meta + info-box markers (non-destructive)."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "book"

META_BLOCK = """
<div class="chapter-meta">

| | |
|---|---|
| **Estimated study time** | 45–120 minutes (adjust by level) |
| **Prerequisites** | Complete earlier chapters in this Part where marked |
| **Difficulty** | Progressive — core theory first, then Band 8–9 stretch tasks |
| **Key takeaways** | Finish Review, Quiz, and Exam Tips before advancing |

</div>

"""

INFO_REPLACEMENTS = [
    (re.compile(r"^> \*\*Exam Tip:\*\*", re.M), "> **Exam Strategy:**"),
    (re.compile(r"^> \*\*Band 9 Insight:\*\*", re.M), "> **Band 9 Secret:**"),
]


def enhance_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    if "chapter-meta" not in text and text.lstrip().startswith("#"):
        # Insert meta after first heading block (title + optional Part line)
        lines = text.splitlines(keepends=True)
        insert_at = 0
        # skip title
        if lines and lines[0].startswith("#"):
            insert_at = 1
            # skip blank and **Part:** lines
            while insert_at < len(lines) and (
                lines[insert_at].strip() == ""
                or lines[insert_at].startswith("**Part")
                or lines[insert_at].strip() in {"***", "---", "****"}
            ):
                insert_at += 1
        lines.insert(insert_at, META_BLOCK)
        text = "".join(lines)

    for pat, repl in INFO_REPLACEMENTS:
        text = pat.sub(repl, text)

    # Standardise common callout labels for CSS styling via markdown blockquotes
    # Already using blockquotes extensively.

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = 0
    # Skip cover-only short files? Enhance all instructional md under book except pure cover images pages optionally
    for path in sorted(BOOK.rglob("*.md")):
        if path.name in {"00_cover.md", "a99_back_cover.md"}:
            continue
        if enhance_file(path):
            changed += 1
    print(f"Enhanced {changed} chapter files")


if __name__ == "__main__":
    main()
