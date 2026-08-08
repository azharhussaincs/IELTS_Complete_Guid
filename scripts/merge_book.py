#!/usr/bin/env python3
"""Merge all book Markdown files into a single manuscript."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "book"
OUT = ROOT / "output" / "Ultimate_IELTS_Mastery.md"

PART_ORDER = [
    "front_matter",
    "part01_introduction",
    "part02_grammar",
    "part03_vocabulary",
    "part04_listening",
    "part05_reading",
    "part06_writing_task1",
    "part07_writing_task2",
    "part08_speaking",
    "part09_practice_tests",
    "part10_band9_secrets",
    "appendices",
]


def natural_key(path: Path):
    parts = re.split(r"(\d+)", path.name.lower())
    return [int(p) if p.isdigit() else p for p in parts]


def collect_files() -> list[Path]:
    files: list[Path] = []
    for part in PART_ORDER:
        folder = BOOK / part
        if not folder.exists():
            continue
        md_files = sorted(folder.glob("*.md"), key=natural_key)
        files.extend(md_files)
    return files


def main() -> None:
    files = collect_files()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    chunks: list[str] = []
    for f in files:
        text = f.read_text(encoding="utf-8").strip()
        if not text:
            continue
        chunks.append(text)
        chunks.append("\n\n\\newpage\n\n")
    OUT.write_text("\n".join(chunks).rstrip() + "\n", encoding="utf-8")
    print(f"Merged {len(files)} files → {OUT}")
    print(f"Approximate characters: {OUT.stat().st_size:,}")


if __name__ == "__main__":
    main()
