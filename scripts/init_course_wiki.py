#!/usr/bin/env python3
"""Create the minimal Obsidian course wiki structure."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path


LECTURE_SUMMARY = """# Lecture Summary

| Lecture | Note | Source Materials | Main Topics | Key Concepts | Status |
| --- | --- | --- | --- | --- | --- |
"""

CONCEPT_SUMMARY = """# Concept Summary

| Concept | Aliases | Scope | Courses | Last Updated | Notes |
| --- | --- | --- | --- | --- | --- |
"""

PENDING_LINKS = """# Pending Links

## {today}

| Type | Candidate | Related Pages | Reason | Suggested Action |
| --- | --- | --- | --- | --- |
"""

COURSE_INDEX = """# {course}

## Lectures

- [[summary/lecture_summary|Lecture Summary]]

## Concepts

- [[summary/concept_summary|Concept Summary]]

## Pending

- [[summary/pending_links|Pending Links]]
"""

LECTURE_NOTE = """---
type: lecture
course: "{course}"
lecture: "{lecture}"
source:
  slides: "material/slides.pdf"
  transcript: "material/transcript.txt"
status: draft
---

# {title}

## 本节概览

- 主题：
- 关键问题：
- 主要材料：

## 课程主线

> [!note]
> 说明本节课要解决的问题，以及为什么这些概念按这个顺序出现。

### 本章小结

## 关键概念与机制

- Concept Name：

### 本章小结

## 例子、图示与推导

![图示说明](figures/page_1.png)

### 本章小结

## 总结与延伸

- 核心结论：
- 与前后课程的联系：
- 待确认问题：
"""


def write_if_missing(path: Path, content: str) -> str:
    if path.exists():
        return f"exists  {path}"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return f"created {path}"


def append_if_missing(path: Path, needle: str, row: str) -> str:
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    if needle in text:
        return f"exists  {path} row for {needle}"
    with path.open("a", encoding="utf-8") as handle:
        handle.write(row)
    return f"updated {path} row for {needle}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize an Obsidian course wiki.")
    parser.add_argument("--root", default=".", help="Wiki root directory")
    parser.add_argument("--course", required=True, help="Course folder name")
    parser.add_argument("--lecture", help="Optional lecture folder name, such as lecture-01")
    parser.add_argument("--title", help="Optional lecture title")
    args = parser.parse_args()

    root = Path(args.root)
    course = args.course
    today = date.today().isoformat()

    paths = [
        root / "concepts",
        root / "courses" / course / "lectures",
        root / "courses" / course / "summary",
    ]
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)
        print(f"dir     {path}")

    summary_dir = root / "courses" / course / "summary"
    print(write_if_missing(summary_dir / "lecture_summary.md", LECTURE_SUMMARY))
    print(write_if_missing(summary_dir / "concept_summary.md", CONCEPT_SUMMARY))
    print(write_if_missing(summary_dir / "pending_links.md", PENDING_LINKS.format(today=today)))
    print(write_if_missing(root / "courses" / course / "index.md", COURSE_INDEX.format(course=course)))

    if args.lecture:
        lecture_dir = root / "courses" / course / "lectures" / args.lecture
        (lecture_dir / "material").mkdir(parents=True, exist_ok=True)
        (lecture_dir / "figures").mkdir(parents=True, exist_ok=True)
        print(f"dir     {lecture_dir / 'material'}")
        print(f"dir     {lecture_dir / 'figures'}")
        title = args.title or args.lecture
        note = LECTURE_NOTE.format(course=course, lecture=args.lecture, title=title)
        print(write_if_missing(lecture_dir / "note.md", note))
        note_link = f"[[../lectures/{args.lecture}/note|{title}]]"
        row = f"| {args.lecture} | {note_link} | slides, transcript |  |  | draft |\n"
        print(append_if_missing(summary_dir / "lecture_summary.md", args.lecture, row))


if __name__ == "__main__":
    main()
