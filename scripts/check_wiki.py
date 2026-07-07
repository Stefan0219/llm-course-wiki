#!/usr/bin/env python3
"""Validate the minimal structure and common note issues for a course wiki."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")


def add_issue(issues: list[str], kind: str, message: str) -> None:
    issues.append(f"[{kind}] {message}")


def has_table_row(path: Path, needle: str) -> bool:
    if not path.exists():
        return False
    return needle in path.read_text(encoding="utf-8", errors="replace")


def concept_target_exists(root: Path, target: str) -> bool:
    target = target.split("|", 1)[0].split("#", 1)[0].strip()
    if not target or target.startswith(("http://", "https://")):
        return True
    if target.endswith(".md"):
        return (root / target).exists()
    return (root / "concepts" / f"{target}.md").exists() or (root / f"{target}.md").exists()


def validate_note(root: Path, note: Path, issues: list[str]) -> None:
    text = note.read_text(encoding="utf-8", errors="replace")
    rel = note.relative_to(root)

    if "## 总结与延伸" not in text:
        add_issue(issues, "ERROR", f"{rel} is missing '## 总结与延伸'")
    if "\\section{" in text or "\\subsection{" in text:
        add_issue(issues, "ERROR", f"{rel} contains LaTeX section commands")
    if "[cite]" in text:
        add_issue(issues, "ERROR", f"{rel} contains [cite] placeholder")
    if "> [!" not in text:
        add_issue(issues, "WARN", f"{rel} has no Obsidian callouts")

    material = note.parent / "material"
    if not material.exists():
        add_issue(issues, "ERROR", f"{rel.parent}/material is missing")

    for match in WIKILINK_RE.findall(text):
        if "/" in match:
            continue
        if not concept_target_exists(root, match):
            add_issue(issues, "WARN", f"{rel} links to missing concept candidate [[{match}]]")


def validate_course(root: Path, course_dir: Path, issues: list[str]) -> None:
    summary = course_dir / "summary"
    required = ["lecture_summary.md", "concept_summary.md", "pending_links.md"]
    for name in required:
        if not (summary / name).exists():
            add_issue(issues, "ERROR", f"{summary.relative_to(root)}/{name} is missing")

    lecture_summary = summary / "lecture_summary.md"
    for note in sorted((course_dir / "lectures").glob("*/note.md")):
        validate_note(root, note, issues)
        lecture_id = note.parent.name
        if lecture_summary.exists() and not has_table_row(lecture_summary, lecture_id):
            add_issue(
                issues,
                "WARN",
                f"{lecture_summary.relative_to(root)} does not mention {lecture_id}",
            )


def main() -> None:
    parser = argparse.ArgumentParser(description="Check an Obsidian course wiki.")
    parser.add_argument("--root", default=".", help="Wiki root directory")
    parser.add_argument("--course", help="Optional course folder to check")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    issues: list[str] = []

    if not (root / "concepts").exists():
        add_issue(issues, "ERROR", "concepts/ is missing")
    if not (root / "courses").exists():
        add_issue(issues, "ERROR", "courses/ is missing")

    course_dirs = []
    if args.course:
        course_dirs = [root / "courses" / args.course]
    elif (root / "courses").exists():
        course_dirs = sorted(path for path in (root / "courses").iterdir() if path.is_dir())

    for course_dir in course_dirs:
        if not course_dir.exists():
            add_issue(issues, "ERROR", f"{course_dir.relative_to(root)} is missing")
            continue
        validate_course(root, course_dir, issues)

    for issue in issues:
        print(issue)

    errors = [issue for issue in issues if issue.startswith("[ERROR]")]
    if errors:
        print(f"Found {len(errors)} error(s) and {len(issues) - len(errors)} warning(s).")
        sys.exit(1)

    if issues:
        print(f"Found {len(issues)} warning(s); no structural errors.")
    else:
        print("Wiki structure looks valid.")


if __name__ == "__main__":
    main()
