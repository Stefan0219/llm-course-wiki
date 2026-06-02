[English](./README.md) | [简体中文](./README_CN.md)

# video-to-notes

`video-to-notes` is a Codex skill and helper toolkit for turning lecture source material into professional Chinese LaTeX course notes and a compiled PDF.

The main workflow is:

```text
transcript TXT + slide PDF/PPT/PPTX -> slide images -> LaTeX notes -> rendered PDF
```

If a YouTube URL and `cookies.txt` are provided, the workflow can first download subtitles only, convert them to TXT, and then use the transcript with the local slides.

## Repository Layout

- `SKILL.md`: the Codex skill instructions. This is the source of truth for the writing, figure-selection, subtitle-download, LaTeX, and validation workflow.
- `assets/notes-template.tex`: the default Chinese LaTeX note template, including a simple title page, highlight boxes, listings, figures, and TikZ.
- `scripts/prepare_slide_images.py`: renders a slide PDF into `pic/page_N.png` images. It can auto-discover one PDF and one TXT in the current directory.
- `scripts/srt_to_txt.py`: converts `.srt` or `.vtt` subtitles into a readable `.txt` transcript.
- `clean.sh`: archives the current lecture workspace into a named folder after notes are generated.
- `agents/openai.yaml`: a short agent-facing entry point for invoking the skill.
- `demo/`: sample slide PDFs for testing the image-preparation helper.

## Supported Inputs

- Local transcript TXT plus local slide PDF.
- Local transcript TXT plus local slide PPT/PPTX, after converting the deck to PDF.
- YouTube URL or `url.txt` plus `cookies.txt`, then downloaded subtitles plus local slides.

When there are multiple candidate transcripts or slide decks, choose the files explicitly instead of relying on auto-discovery.

## Prerequisites

Python helpers use only the standard library except for optional PDF rendering support:

```bash
python3 -m pip install pdf2image
```

Install Poppler so PDF pages can be rendered. On macOS:

```bash
brew install poppler
```

On Ubuntu/Debian:

```bash
sudo apt-get install poppler-utils
```

For optional YouTube subtitle download, install `yt-dlp`:

```bash
python3 -m pip install yt-dlp
```

For final PDF compilation, install a LaTeX distribution with XeLaTeX and common packages such as `ctex`, `tcolorbox`, `listings`, `tikz`, and `pgfplots`.

## Quick Start

### 1. Prepare Source Files

Place the lecture transcript and slide deck in the working directory. If the transcript is in subtitle format, convert it first:

```bash
python3 scripts/srt_to_txt.py lecture.srt transcript.txt
```

### 2. Render Slide Images

If the working directory contains exactly one `.pdf` and one `.txt`, use auto-discovery:

```bash
python3 scripts/prepare_slide_images.py --auto
```

Otherwise, pass the slide PDF explicitly:

```bash
python3 scripts/prepare_slide_images.py --pdf slides.pdf --output pic
```

The helper writes images as `pic/page_1.png`, `pic/page_2.png`, and so on. If `pic/` already contains page images, it reuses them by default. Add `--force` to re-render.

To test with a demo deck:

```bash
python3 scripts/prepare_slide_images.py --pdf demo/karpathy_llm_intro.pdf --output pic --force
```

### 3. Generate the Notes

Ask Codex to use the `video-to-notes` skill with your transcript and slides. The skill will:

1. inspect the sources and slide images,
2. use `assets/notes-template.tex` as the base document,
3. select or create teaching figures,
4. write a complete Chinese note,
5. compile the `.tex` file to PDF,
6. validate that referenced assets exist and the PDF builds.

For manual use, start from `assets/notes-template.tex`, replace the body block, and reference slide screenshots with the `pic/page_N.png` convention.

### 4. Compile Manually When Needed

```bash
xelatex notes.tex
xelatex notes.tex
```

Run XeLaTeX twice when the table of contents or references need a second pass.

### 5. Archive a Finished Lecture

```bash
chmod +x clean.sh
./clean.sh Lec_01_Intro
```

`clean.sh` creates the target folder and moves `pic/`, all root-level `*.pdf`, `*.txt`, and `*.tex` files into it. It does not currently move `.srt` or `.vtt` files.

## Output Conventions

- Notes are written in Chinese unless requested otherwise.
- Slide screenshots should use `pic/page_N.png`; captions should explain the teaching role without adding source page numbers.
- Figures should stay outside `importantbox`, `knowledgebox`, `warningbox`, and `dialoguebox`.
- Each major section should end with `本章小结`.
- The document should end with a top-level `总结与延伸` section.
- Final delivery should include the generated `.tex`, compiled `.pdf`, and every referenced asset.
