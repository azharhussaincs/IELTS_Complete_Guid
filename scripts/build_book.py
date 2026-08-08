#!/usr/bin/env python3
"""Commercial republish: merge + volume PDFs/DOCX/EPUB/HTML + combined outputs."""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output"
BOOK = ROOT / "book"
CSS = ROOT / "assets" / "book.css"
META = ROOT / "assets" / "metadata.yaml"
FMT = "markdown+pipe_tables+fenced_code_blocks-yaml_metadata_block"

VOLUMES = [
    ("Vol1_Front_Grammar", ["front_matter", "part01_introduction", "part02_grammar"]),
    ("Vol3_Skills", [
        "part04_listening",
        "part05_reading",
        "part06_writing_task1",
        "part07_writing_task2",
        "part08_speaking",
    ]),
    ("Vol4_Practice_Appendices", [
        "part09_practice_tests",
        "part10_band9_secrets",
        "appendices",
    ]),
]


def natural_key(path: Path):
    parts = re.split(r"(\d+)", path.name.lower())
    return [int(p) if p.isdigit() else p for p in parts]


def run(cmd: list[str]) -> None:
    print(">", " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True)


def merge_parts(part_names: list[str], out_path: Path) -> int:
    chunks: list[str] = []
    count = 0
    for part in part_names:
        folder = BOOK / part
        if not folder.exists():
            continue
        for f in sorted(folder.glob("*.md"), key=natural_key):
            text = f.read_text(encoding="utf-8").strip()
            if not text:
                continue
            chunks.append(text)
            chunks.append("\n\n\\newpage\n\n")
            count += 1
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(chunks).rstrip() + "\n", encoding="utf-8")
    return count


def merge_files(files: list[Path], out_path: Path) -> None:
    chunks = []
    for f in files:
        t = f.read_text(encoding="utf-8").strip()
        if t:
            chunks.append(t)
            chunks.append("\n\n\\newpage\n\n")
    out_path.write_text("\n".join(chunks).rstrip() + "\n", encoding="utf-8")


def pandoc(src: Path, dest: Path, extra: list[str] | None = None) -> None:
    cmd = [
        "pandoc",
        str(src),
        f"--from={FMT}",
        "--toc",
        "--toc-depth=3",
        "--resource-path",
        str(ROOT),
        "--metadata-file",
        str(META),
        "-o",
        str(dest),
    ]
    if extra:
        cmd.extend(extra)
    run(cmd)


def build_set(name: str, md: Path, do_pdf: bool = True) -> None:
    pandoc(md, OUTPUT / f"Ultimate_IELTS_Mastery_{name}.docx")
    pandoc(md, OUTPUT / f"Ultimate_IELTS_Mastery_{name}.epub")
    html = OUTPUT / f"Ultimate_IELTS_Mastery_{name}.html"
    pandoc(md, html, [f"--css={CSS}", "--standalone", "-V", "lang=en"])
    if do_pdf:
        pdf = OUTPUT / f"Ultimate_IELTS_Mastery_{name}.pdf"
        print(f"WeasyPrint {name}...", flush=True)
        run([sys.executable, "-m", "weasyprint", str(html), str(pdf)])


def merge_pdfs(parts: list[Path], dest: Path) -> int:
    try:
        from pypdf import PdfWriter, PdfReader
    except ImportError:
        run([sys.executable, "-m", "pip", "install", "--user", "pypdf"])
        from pypdf import PdfWriter, PdfReader

    writer = PdfWriter()
    pages = 0
    for p in parts:
        reader = PdfReader(str(p))
        pages += len(reader.pages)
        for page in reader.pages:
            writer.add_page(page)
    with open(dest, "wb") as f:
        writer.write(f)
    return pages


def sync_assets() -> None:
    """WeasyPrint resolves relative image paths from the HTML file location (output/)."""
    for name in ("images", "diagrams", "assets"):
        src = ROOT / name
        dst = OUTPUT / name
        if not src.exists():
            continue
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        print(f"Synced {name}/ → output/{name}/", flush=True)


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    sync_assets()

    # Full markdown
    run([sys.executable, str(ROOT / "scripts" / "merge_book.py")])
    full_md = OUTPUT / "Ultimate_IELTS_Mastery.md"

    # Full DOCX / EPUB / HTML (screen)
    pandoc(full_md, OUTPUT / "Ultimate_IELTS_Mastery.docx")
    pandoc(full_md, OUTPUT / "Ultimate_IELTS_Mastery.epub")
    pandoc(
        full_md,
        OUTPUT / "Ultimate_IELTS_Mastery.html",
        [f"--css={CSS}", "--standalone", "-V", "lang=en"],
    )
    shutil.copy2(OUTPUT / "Ultimate_IELTS_Mastery.html", OUTPUT / "Ultimate_IELTS_Mastery_Screen.html")

    pdf_parts: list[Path] = []

    # Volumes 1,3,4
    for name, parts in VOLUMES:
        md = OUTPUT / f"Ultimate_IELTS_Mastery_{name}.md"
        n = merge_parts(parts, md)
        print(f"Merged {n} → {md.name}", flush=True)
        build_set(name, md, do_pdf=True)
        pdf_parts.append(OUTPUT / f"Ultimate_IELTS_Mastery_{name}.pdf")

    # Vocabulary in 3 parts
    vocab_files = sorted((BOOK / "part03_vocabulary").glob("*.md"), key=natural_key)
    chunks = [vocab_files[i : i + 9] for i in range(0, len(vocab_files), 9)]
    for idx, files in enumerate(chunks, 1):
        name = f"Vol2_Vocabulary_Part{idx}"
        md = OUTPUT / f"Ultimate_IELTS_Mastery_{name}.md"
        merge_files(files, md)
        build_set(name, md, do_pdf=True)
        pdf_parts.insert(idx, OUTPUT / f"Ultimate_IELTS_Mastery_{name}.pdf")  # after vol1

    # Correct order: Vol1, Vocab1-3, Vol3, Vol4
    ordered = [
        OUTPUT / "Ultimate_IELTS_Mastery_Vol1_Front_Grammar.pdf",
        OUTPUT / "Ultimate_IELTS_Mastery_Vol2_Vocabulary_Part1.pdf",
        OUTPUT / "Ultimate_IELTS_Mastery_Vol2_Vocabulary_Part2.pdf",
        OUTPUT / "Ultimate_IELTS_Mastery_Vol2_Vocabulary_Part3.pdf",
        OUTPUT / "Ultimate_IELTS_Mastery_Vol3_Skills.pdf",
        OUTPUT / "Ultimate_IELTS_Mastery_Vol4_Practice_Appendices.pdf",
    ]

    pages = merge_pdfs(ordered, OUTPUT / "Ultimate_IELTS_Mastery.pdf")
    shutil.copy2(OUTPUT / "Ultimate_IELTS_Mastery.pdf", OUTPUT / "Ultimate_IELTS_Mastery_Print.pdf")
    shutil.copy2(OUTPUT / "Ultimate_IELTS_Mastery.pdf", OUTPUT / "Ultimate_IELTS_Mastery_Screen.pdf")

    # Full vocab package
    merge_files(vocab_files, OUTPUT / "Ultimate_IELTS_Mastery_Vol2_Vocabulary.md")
    pandoc(OUTPUT / "Ultimate_IELTS_Mastery_Vol2_Vocabulary.md", OUTPUT / "Ultimate_IELTS_Mastery_Vol2_Vocabulary.docx")
    pandoc(OUTPUT / "Ultimate_IELTS_Mastery_Vol2_Vocabulary.md", OUTPUT / "Ultimate_IELTS_Mastery_Vol2_Vocabulary.epub")

    print(f"COMPLETE — combined PDF pages: {pages}")
    for p in sorted(OUTPUT.glob("Ultimate_IELTS_Mastery*.pdf")):
        print(f"  {p.name}: {p.stat().st_size/1e6:.1f} MB")


if __name__ == "__main__":
    main()
