# LLM Course Wiki

English | [中文](README_CN.md)

Turn lecture transcripts, slide decks, and existing notes into a maintainable Obsidian course wiki.

## Overview

This project turns lecture materials into a reusable Markdown/Obsidian knowledge base instead of a one-off summary artifact. The intended outputs include:

- per-lecture `note.md`
- reusable `concepts/*.md` pages
- course-level summaries: `lecture_summary.md`, `concept_summary.md`, and `pending_links.md`

Core flow:

```text
transcript + slides + existing summaries
-> lecture note
-> concept pages
-> summary updates
-> pending decisions
```

## Inspiration

This project is influenced by two directions:

- Karpathy's `llm-wiki` idea: continuously turning raw material into a searchable, linkable, and updatable knowledge base.
- [decopy.ai](https://decopy.ai/), especially its approach to summarizing YouTube videos into structured notes, summaries, and key concepts.

This repository focuses more on a local workflow and a maintainable course wiki than on a consumer-facing web product.

## What Is in the Repo

- `SKILL.md`: the Codex skill spec that defines the end-to-end wiki workflow
- `scripts/init_course_wiki.py`: initializes course folders and starter Markdown files
- `scripts/srt_to_txt.py`: converts `.srt` / `.vtt` subtitles into plain-text transcripts
- `scripts/prepare_slide_images.py`: renders slide PDFs into `page_N.png` images
- `scripts/check_wiki.py`: validates wiki structure and common note issues
- `assets/`: templates for course indexes, lecture notes, concept pages, and summaries

## Directory Contract

```text
.
├── concepts/
│   └── Concept Name.md
└── courses/
    └── course-name/
        ├── lectures/
        │   └── lecture-01/
        │       ├── material/
        │       │   ├── slides.pdf
        │       │   └── transcript.txt
        │       ├── figures/
        │       │   └── page_1.png
        │       └── note.md
        └── summary/
            ├── lecture_summary.md
            ├── concept_summary.md
            └── pending_links.md
```

Treat `material/` as the source of truth. Raw inputs should remain unchanged; derived outputs belong in `figures/` or other generated files.

## Quick Start

1. Initialize a course structure:

```bash
python3 scripts/init_course_wiki.py --root . --course course-name --lecture lecture-01 --title "Lecture title"
```

2. Convert subtitles into a transcript when needed:

```bash
python3 scripts/srt_to_txt.py lecture.srt transcript.txt
```

3. Render slide images from a PDF when needed:

```bash
python3 scripts/prepare_slide_images.py --pdf courses/course-name/lectures/lecture-01/material/slides.pdf --output courses/course-name/lectures/lecture-01/figures
```

4. Validate the wiki before delivery:

```bash
python3 scripts/check_wiki.py --root .
```

## Good Fit

- video-to-notes workflows for courses
- transcript + slides note synthesis
- incremental knowledge capture for long lecture series
- managing lecture notes, concepts, and cross-links in Obsidian

## License

This repository is licensed under the [MIT License](LICENSE).

MIT is a permissive open source license and allows commercial use,
modification, and redistribution.
