---
name: video-to-notes
description: Generate a professional, detailed, figure-rich Chinese LaTeX course note and final PDF from a local transcript TXT plus PPT/PDF lecture slides, optionally first downloading a YouTube subtitle TXT from a URL using cookies.txt. Use when the user wants the prompt.py-style TXT+PPT/PDF workflow upgraded with wdkns-style teaching structure, slide/page figure selection, final synthesis, and successful PDF rendering.
---

# TXT + PPT Video Render PDF

Use this skill to turn lecture source material into a complete `.tex` note and a rendered PDF.

The core workflow is `transcript TXT + PPT/PDF slides -> LaTeX notes -> compiled PDF`.
If the user gives a YouTube URL and `cookies.txt`, first download subtitles only and convert them to TXT; do not download the video unless the user explicitly asks.

## Goal

Produce professional Chinese lecture notes that combine:

- the transcript's spoken explanations, examples, emphasis, and closing synthesis
- the slide deck's structure, diagrams, formulas, tables, code, and visual sequence
- high-value slide screenshots or generated/redrawn teaching figures
- a final synthesis section that distills the course logic rather than merely ending with a summary

Deliver the final `.tex`, compiled `.pdf`, and every referenced asset.

## Inputs

Accept any of these source combinations:

- local `*.txt` transcript plus local `*.pdf` slides
- local `*.txt` transcript plus local `*.ppt` or `*.pptx` slides
- `url.txt` plus `cookies.txt`, then downloaded subtitle TXT plus local slides
- direct YouTube URL plus `cookies.txt`, then downloaded subtitle TXT plus local slides

When the directory contains multiple candidate TXT/PDF/PPT files, identify them and choose conservatively from names, or ask if ambiguity would change the output.

## Optional URL to TXT Workflow

Use this only to obtain the transcript TXT. It downloads subtitles only.

Required local files:

- `cookies.txt`: Netscape-format browser cookie export for a YouTube account allowed to view the video
- `url.txt`: one YouTube video URL, optionally including playlist parameters

Check the downloader and inputs without exposing cookie values:

```bash
yt-dlp --version
sed -n '1p' url.txt
wc -l cookies.txt
awk 'NR==1{print $0} NR>1 && $0 !~ /^#/ {print $1, $6; if (++n==5) exit}' cookies.txt
```

List subtitle tracks with `--no-playlist`, because URLs may include playlist parameters:

```bash
yt-dlp \
  --cookies cookies.txt \
  --no-playlist \
  --list-subs \
  --skip-download \
  --no-warnings \
  --ignore-config \
  "$(sed -n '1p' url.txt)"
```

Prefer human-uploaded subtitles when available:

```bash
yt-dlp \
  --cookies cookies.txt \
  --no-playlist \
  --skip-download \
  --write-subs \
  --sub-langs en \
  --sub-format srt \
  --no-warnings \
  --ignore-config \
  -o '%(title).80B [%(id)s].%(ext)s' \
  "$(sed -n '1p' url.txt)"
```

If there are no human subtitles, use automatic captions. Prefer the original-language track, such as `en-orig`, when available:

```bash
yt-dlp \
  --cookies cookies.txt \
  --no-playlist \
  --skip-download \
  --write-auto-subs \
  --sub-langs en-orig \
  --sub-format srt \
  --no-warnings \
  --ignore-config \
  -o '%(title).80B [%(id)s].%(ext)s' \
  "$(sed -n '1p' url.txt)"
```

After downloading, convert the subtitle file to TXT with:

```bash
python3 scripts/srt_to_txt.py "downloaded.srt" "transcript.txt"
```

Use the TXT for long-form note writing.

Troubleshooting:

- If playlist authentication fails, retry with `--no-playlist`.
- If access fails, refresh and re-export `cookies.txt` from a browser session that can view the video.
- If YouTube JavaScript challenge errors occur, update `yt-dlp`.

## Source Preparation

1. Inspect source files first.
   Record slide filename, transcript filename, and slide page count.

2. Convert PPT/PPTX to PDF before figure extraction when needed.
   Prefer LibreOffice or another available local converter.

3. Convert slide PDF pages into images in `pic/`.
   Follow the `prompt.py` convention: `pic/page_1.png`, `pic/page_2.png`, etc.
   If `pic/` already exists and contains suitable page images, reuse it unless stale or mismatched.
   A helper is available:

```bash
python3 scripts/prepare_slide_images.py --pdf "slides.pdf" --output pic
```

   If the working directory contains exactly one PDF and one TXT, the helper can discover them:

```bash
python3 scripts/prepare_slide_images.py --auto
```

4. Use `assets/notes-template.tex` as the starting point.
   Fill the title if needed and replace the body block. Keep the title page simple: title, author `Codex`, and date only.

5. Keep generated or extracted assets local.
   Typical artifacts are the transcript TXT, slide PDF, `pic/page_N.png`, optional generated vector figures, final `.tex`, and final `.pdf`.

## Long Material Strategy

Do not rely on a single monolithic pass for long lectures.

- If the transcript is longer than about 20 minutes, 300 subtitle entries, or 20,000 words, split by slide sections, chapter headings, or coherent time windows.
- Preserve a short overlap between neighboring segments when the explanation crosses section boundaries.
- For each segment, extract: teaching goal, core claims, important formulas/code, slide pages that must be shown, misconceptions, and links to later sections.
- Integrate segments into one unified narrative. The final PDF must read like one lecture note, not stitched summaries.

## Pedagogical Standard

The notes must read like a strong human teacher is guiding the reader.

- Build each major section around motivation, main idea, mechanism, example/evidence, and takeaway.
- Rewrite the transcript into a teaching sequence; do not dump subtitle content chronologically.
- Explain why a concept appears, what problem it solves, and how the next idea follows.
- Keep technical depth, but introduce formulas after plain-language intuition.
- Break dense ideas into progressive subsections instead of one compressed derivation.
- Skip greetings, small talk, class logistics, sponsorship, routine closing pleasantries, and other non-teaching content.
- Keep closing discussion when it includes synthesis, limitations, tradeoffs, future work, advice, or open questions.

## Writing Rules

1. Write in Chinese unless the user explicitly asks otherwise.

2. Organize the document with `\section{...}` and `\subsection{...}`.
   Prefer the lecture's real logic over transcript order.

3. Use figures whenever they materially improve explanation.
   Include necessary slide pages, crops, or generated figures; do not optimize for a low figure count.

4. Slide screenshots must use the `pic/page_N.png` convention unless a better named crop or generated figure is created.
   Captions should explain the figure's teaching role and should not include slide-page provenance such as "source: slide/page N".

5. Do not place images inside `importantbox`, `knowledgebox`, `warningbox`, or `dialoguebox`.

6. When a mathematical formula appears:
   first explain what the formula expresses and why it appears, then show it in display math, then immediately follow with a flat list explaining every symbol.

7. When code appears:
   explain its role before the listing, wrap it in `lstlisting`, and add a descriptive `caption`.

8. Use highlight boxes deliberately:
   - `importantbox`: core definitions, central claims, theorem-like facts, key mechanisms, algorithm steps
   - `knowledgebox`: background, historical context, prerequisite reminders, terminology comparisons, design tradeoffs
   - `warningbox`: common misunderstandings, hidden assumptions, notation traps, implementation mistakes
   - `dialoguebox`: only for short high-signal dialogue from interviews, panels, or Q&A when the exact wording adds teaching value

9. End every major section with `\subsection{本章小结}`.
   Add `\subsection{拓展阅读}` only when there are one or two genuinely useful external links.

10. End with a top-level `\section{总结与延伸}` containing:
    - the speaker's substantive closing discussion when present
    - a structured distillation of core claims, mechanisms, and practical implications
    - cross-links between earlier sections
    - concrete takeaways, open questions, or next steps when supported by the material

11. Do not emit `[cite]`-style placeholders anywhere in the LaTeX.

## Slide Figure Handling

Select slide images by teaching value, not by quota.

- Inspect slide pages visually before deciding what they show.
- Do not infer a slide's semantic content only from transcript text or filenames.
- For progressive PPT reveals, prefer the final fully populated readable state unless intermediate states teach distinct steps.
- If a full slide is too dense or too loose, crop or redraw the relevant region.
- Prefer several readable figures over one overloaded, unreadable figure.
- Omit repetitive title slides, logistics slides, and low-information decorative pages.
- When a visual relationship is clearer redrawn than screenshotted, use TikZ/PGFPlots or generate a vector PDF figure with Python.

For each inserted slide or crop:

- use a caption that states what the figure teaches
- do not append source slide/page numbers in the caption

Stable pattern:

```latex
\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{pic/page_12.png}
\caption{流水线阶段与关键控制信号的对应关系。}
\end{figure}
```

## Visualization

Add accurate visualizations when screenshots and prose are insufficient.

Use:

- TikZ or PGFPlots for LaTeX-native diagrams and plots
- Python `matplotlib`/`seaborn` for generated teaching figures
- vector `pdf` output for plots, charts, and schematics whenever possible

Use visualizations for pipelines, architecture overviews, curves, distributions, heatmaps, ablations, tables-as-charts, geometric intuition, or summary mechanism diagrams.
Do not add decorative graphics.

## Validation

Before delivery:

- confirm the `.tex` compiles successfully to PDF
- verify every referenced asset exists
- check that figures match the surrounding explanation
- check that no image is inside a custom box
- check that there are no `[cite]` placeholders
- check that the final note includes a substantive `总结与延伸`
- if URL subtitles were downloaded, report whether they were human subtitles or automatic captions

## Assets

- `assets/notes-template.tex`: default LaTeX template to copy and fill.
- `scripts/prepare_slide_images.py`: prepares `pic/page_N.png` slide images from a PDF, with an auto-discovery mode inspired by `prompt.py`.
- `scripts/srt_to_txt.py`: converts SRT/VTT subtitles into transcript TXT while preserving readable spacing.
