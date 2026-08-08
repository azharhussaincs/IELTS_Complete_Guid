# Ultimate IELTS Mastery

**Complete Preparation Guide for Band 8.0–9.0**

**Author:** Azhar Hussain  
**Email:** azharhussaincs@gmail.com · **Phone:** +92 300 8786258  
**YouTube:** Jamia Pakistan · **Edition:** First Edition, 2026

This repository contains the full Markdown source, assets, and build scripts for the *Ultimate IELTS Mastery* textbook.

## Project layout

```
IELTS_Complete_Guid/
├── MASTER_OUTLINE.md     # Full chapter map + status
├── PROGRESS.md           # Generation progress log
├── book/                 # All Markdown chapters
├── images/ diagrams/ tables/
├── references/
├── scripts/              # Build & content generators
├── assets/               # CSS, fonts, cover
└── output/               # PDF, DOCX, EPUB
```

## Build outputs

```bash
# Install deps (once)
pip3 install -r requirements.txt

# Merge markdown → single book
python3 scripts/merge_book.py

# Build PDF / DOCX / EPUB (requires pandoc)
python3 scripts/build_book.py
```

## Content generation workflow

1. Chapters are written one file at a time under `book/`.
2. Update `MASTER_OUTLINE.md` status when a chapter is finished.
3. Large banks (vocabulary, cue cards, mocks) may be produced by scripts in `scripts/generators/`.
4. Final commercial PDF is produced only after all chapters are complete.

## Quality rules

- Original wording; no copyrighted Cambridge/British Council passages copied.
- Every teaching chapter includes objectives, theory, examples, exercises, solutions, quiz, tips.
- Facts aligned with publicly documented IELTS formats from IELTS.org / British Council / IDP / Cambridge English (paraphrased).
