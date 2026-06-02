#!/usr/bin/env python3
"""Prepare slide page images using the prompt.py-style pic/page_N.png convention."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def find_single(pattern: str, label: str) -> Path:
    matches = sorted(Path(".").glob(pattern))
    if not matches:
        raise SystemExit(f"No {label} file found in the current directory.")
    if len(matches) > 1:
        names = ", ".join(str(path) for path in matches)
        raise SystemExit(f"Multiple {label} files found; specify one explicitly: {names}")
    return matches[0]


def convert_with_pdf2image(pdf_path: Path, output_dir: Path, dpi: int) -> int:
    try:
        from pdf2image import convert_from_path
    except ImportError as exc:
        raise RuntimeError("pdf2image is not installed") from exc

    images = convert_from_path(str(pdf_path), dpi=dpi)
    for index, image in enumerate(images, start=1):
        image.save(output_dir / f"page_{index}.png", "PNG")
    return len(images)


def convert_with_pdftoppm(pdf_path: Path, output_dir: Path, dpi: int) -> int:
    prefix = output_dir / "page"
    subprocess.run(
        ["pdftoppm", "-png", "-r", str(dpi), str(pdf_path), str(prefix)],
        check=True,
    )

    generated = sorted(output_dir.glob("page-*.png"))
    for index, path in enumerate(generated, start=1):
        target = output_dir / f"page_{index}.png"
        path.replace(target)
    return len(generated)


def main() -> None:
    parser = argparse.ArgumentParser(description="Render slide PDF pages to pic/page_N.png.")
    parser.add_argument("--pdf", help="Input slide PDF")
    parser.add_argument("--output", default="pic", help="Output image directory")
    parser.add_argument("--dpi", type=int, default=200, help="Image render DPI")
    parser.add_argument("--auto", action="store_true", help="Find exactly one PDF and one TXT in cwd")
    parser.add_argument("--force", action="store_true", help="Render even if output directory already exists")
    args = parser.parse_args()

    pdf_path = Path(args.pdf) if args.pdf else None
    if args.auto:
        pdf_path = find_single("*.pdf", "PDF")
        transcript = find_single("*.txt", "TXT")
        print(f"Found PDF: {pdf_path}")
        print(f"Found TXT: {transcript}")
    if pdf_path is None:
        raise SystemExit("Provide --pdf slides.pdf, or use --auto.")
    if not pdf_path.exists():
        raise SystemExit(f"PDF not found: {pdf_path}")

    output_dir = Path(args.output)
    existing = sorted(output_dir.glob("page_*.png")) if output_dir.exists() else []
    if existing and not args.force:
        print(f"Reusing existing {output_dir}/ with {len(existing)} page images.")
        return

    output_dir.mkdir(parents=True, exist_ok=True)
    for stale in output_dir.glob("page_*.png"):
        stale.unlink()

    try:
        count = convert_with_pdf2image(pdf_path, output_dir, args.dpi)
    except Exception as pdf2image_error:
        try:
            count = convert_with_pdftoppm(pdf_path, output_dir, args.dpi)
        except Exception as pdftoppm_error:
            raise SystemExit(
                "Failed to render PDF pages. Install pdf2image + Poppler, or pdftoppm.\n"
                f"pdf2image error: {pdf2image_error}\n"
                f"pdftoppm error: {pdftoppm_error}"
            ) from pdftoppm_error

    print(f"Wrote {count} page images to {output_dir}/")


if __name__ == "__main__":
    main()
