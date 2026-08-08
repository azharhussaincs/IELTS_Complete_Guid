#!/usr/bin/env python3
"""Helpers for consistent chapter scaffolding."""

from __future__ import annotations


def header(chapter_no: int, title: str, part: str) -> str:
    return f"""# Chapter {chapter_no}: {title}

**Part:** {part}

---
"""


def learning_objectives(items: list[str]) -> str:
    bullets = "\n".join(f"- {i}" for i in items)
    return f"""## Learning Objectives

By the end of this chapter, you will be able to:

{bullets}
"""


def section(title: str, body: str) -> str:
    return f"## {title}\n\n{body.strip()}\n"


def exam_tip(text: str) -> str:
    return f"""> **Exam Tip:** {text.strip()}
"""


def band9(text: str) -> str:
    return f"""> **Band 9 Insight:** {text.strip()}
"""
