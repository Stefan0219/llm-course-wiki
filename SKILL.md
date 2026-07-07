---
name: llm-course-wiki
description: Build and maintain an Obsidian Markdown course wiki from lecture transcripts, slide PDFs or PPTs, and existing course notes. Use when the user wants video-to-notes upgraded from one-off LaTeX PDF output into a reusable course knowledge base with per-lecture note.md files, shared concept pages, lecture_summary.md, concept_summary.md, pending_links.md, Obsidian wikilinks, callouts, and source-grounded concept maintenance.
---

# LLM Course Wiki

Use this skill to turn lecture materials into a durable Obsidian course wiki.
The core workflow is:

```text
transcript + slides + existing summaries -> lecture note -> concept pages -> summary updates -> pending decisions
```

Prefer a maintainable Markdown knowledge base over a polished one-off PDF.

## Directory Contract

Use this minimal structure:

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

Treat `material/` as the source of truth. Read raw files there, but do not edit,
overwrite, move, or normalize them unless the user explicitly asks. Store derived
slide images, crops, and generated figures outside `material/`, usually in
`figures/`.

Use `scripts/init_course_wiki.py` to create the structure and starter files:

```bash
python3 scripts/init_course_wiki.py --root . --course course-name --lecture lecture-01 --title "Lecture title"
```

## Source Preparation

Accept these input combinations:

- local transcript TXT plus local slide PDF
- local transcript TXT plus local PPT or PPTX after conversion to PDF
- subtitle SRT or VTT converted to transcript TXT
- YouTube URL plus cookies for subtitle-only download, when the user provides them

If there are multiple plausible source files, choose conservatively from names and
paths. Ask only when ambiguity would materially change the output.

For subtitles, convert to TXT with:

```bash
python3 scripts/srt_to_txt.py lecture.srt transcript.txt
```

For slide images, render the slide PDF into the lecture's `figures/` directory:

```bash
python3 scripts/prepare_slide_images.py --pdf courses/course-name/lectures/lecture-01/material/slides.pdf --output courses/course-name/lectures/lecture-01/figures
```

If the user gives a YouTube URL and `cookies.txt`, download subtitles only with
`yt-dlp --skip-download`; do not download video unless explicitly asked. Prefer
human subtitles over automatic captions. After download, convert SRT or VTT to
TXT and place or copy the TXT into the lecture `material/` folder.

## Ingest Workflow

Follow this order for each lecture.

1. Inspect the course folder, lecture folder, source files, existing summaries,
   and relevant concept pages.
2. Ensure `lecture_summary.md`, `concept_summary.md`, and `pending_links.md`
   exist. Use `assets/*-template.md` or `scripts/init_course_wiki.py` when
   creating them.
3. Generate or refresh slide page images in `figures/` only when needed.
4. Write `courses/course-name/lectures/lecture-id/note.md`.
5. Extract new or updated concepts from `note.md`.
6. Reuse existing concept pages where definitions and context match.
7. Create or update `concepts/*.md` only for concepts important beyond the
   current paragraph.
8. Update `lecture_summary.md` and `concept_summary.md`.
9. Add uncertain duplicates, naming conflicts, or unverified links to
   `pending_links.md` instead of forcing a merge.
10. Run `scripts/check_wiki.py` and fix reported errors before delivery.

## Lecture Note Pass

Write `note.md` in Chinese by default, preserving necessary English terms.
Use the lecture's real teaching logic rather than a mechanical transcript order.

Each lecture note should:

- use Markdown headings, not LaTeX commands
- include YAML frontmatter for course, lecture, source paths, and status when useful
- link important concepts on first meaningful mention with `[[Concept Name]]`
- reuse existing concept names from `concept_summary.md`
- explain how this lecture uses a concept, not repeat the entire concept page
- embed useful slide images with relative Markdown image links such as
  `![说明](figures/page_12.png)`
- end every major section with `### 本章小结`
- end the file with `## 总结与延伸`

Use Obsidian callouts deliberately:

- `> [!important]` for core definitions, central claims, mechanisms, and algorithms
- `> [!note]` for background, comparisons, prerequisites, and design tradeoffs
- `> [!warning]` for common mistakes, hidden assumptions, notation traps, and conflicts
- `> [!quote]` only for high-value exact quotes, Q&A, or dialogue

Do not write model guesses as course facts. If a point is inferred, label it as
inference or send it to `pending_links.md`.

## Concept Update Pass

After `note.md` is coherent, maintain the reusable wiki layer.

For each important concept:

1. Search `concept_summary.md` first.
2. Search existing files in `concepts/` when the summary is insufficient.
3. Reuse an existing page if definition, aliases, and course context match.
4. Create a new page from `assets/concept-template.md` when the concept is
   reusable or will likely recur.
5. Update the concept's `出现位置` with a link to the lecture note and a short
   statement of how the lecture uses it.
6. Update `concept_summary.md` with aliases, scope, courses, date, and notes.

Use stable names:

| Case | Naming pattern | Example |
| --- | --- | --- |
| General concept | Plain concept name | `Recursion` |
| Course-specific concept | Course prefix | `CS61A - Environment Diagram` |
| Same name, different domain | Domain qualifier | `Graph Traversal (ML)` |
| Same name, different course meaning | Course qualifier | `Graph Traversal (CS61B)` |

Default to a general concept name. Add qualifiers only when needed for
disambiguation.

## Pending Decisions

Use `pending_links.md` as the safety valve. Add an entry when:

- two concept pages may be duplicates but the source material is not enough to merge
- the same term has conflicting meanings across courses or domains
- a candidate concept name is unstable
- a slide or transcript reference suggests a link but does not confirm it

Do not block the lecture note on uncertain links. Use a stable candidate link in
the note only when it is useful for later review, and record the uncertainty in
`pending_links.md`.

## Validation

Before delivery:

- confirm `material/` raw files were not modified
- confirm `note.md` exists and uses Markdown, Obsidian links, and callouts
- confirm `note.md` contains `## 总结与延伸`
- confirm new or changed concepts appear in `concept_summary.md`
- confirm the lecture appears in `lecture_summary.md`
- confirm unresolved ambiguity is in `pending_links.md`
- run:

```bash
python3 scripts/check_wiki.py --root .
```

## Resources

- `scripts/init_course_wiki.py`: create wiki folders and starter Markdown files.
- `scripts/check_wiki.py`: validate required structure and common note issues.
- `scripts/prepare_slide_images.py`: render slide PDF pages to `page_N.png`.
- `scripts/srt_to_txt.py`: convert SRT or VTT subtitles to transcript TXT.
- `assets/lecture-note-template.md`: starter structure for `note.md`.
- `assets/concept-template.md`: starter structure for concept pages.
- `assets/*summary-template.md`: starter summary and pending files.
