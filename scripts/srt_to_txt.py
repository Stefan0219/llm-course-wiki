#!/usr/bin/env python3
"""Convert SRT/VTT subtitles into a readable transcript TXT."""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path


TIMING_RE = re.compile(
    r"\d{2}:\d{2}:\d{2}[,.]\d{3}\s+-->\s+\d{2}:\d{2}:\d{2}[,.]\d{3}"
)
TAG_RE = re.compile(r"<[^>]+>")


def normalize_line(line: str) -> str:
    line = line.strip().lstrip("\ufeff")
    line = html.unescape(line)
    line = TAG_RE.sub("", line)
    line = re.sub(r"^\s*-\s+", "", line)
    line = re.sub(r"\s+", " ", line)
    return line.strip()


def subtitle_to_text(source: Path) -> str:
    chunks: list[str] = []
    seen_consecutive = ""

    for raw_line in source.read_text(encoding="utf-8", errors="replace").splitlines():
        line = normalize_line(raw_line)
        if not line:
            continue
        if line == "WEBVTT" or line.startswith("Kind:") or line.startswith("Language:"):
            continue
        if line.isdigit() or TIMING_RE.search(line):
            continue
        if line == seen_consecutive:
            continue
        chunks.append(line)
        seen_consecutive = line

    text = "\n".join(chunks)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert SRT/VTT subtitles to TXT.")
    parser.add_argument("input", help="Input .srt or .vtt file")
    parser.add_argument("output", nargs="?", help="Output .txt file")
    args = parser.parse_args()

    source = Path(args.input)
    if not source.exists():
        raise SystemExit(f"Input file not found: {source}")

    output = Path(args.output) if args.output else source.with_suffix(".txt")
    output.write_text(subtitle_to_text(source), encoding="utf-8")
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
