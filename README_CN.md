# LLM Course Wiki

[English](README.md) | 中文

把课程讲义、字幕、PDF 幻灯片和已有总结，整理成可长期维护的 Obsidian 课程知识库。

## 项目简介

这个项目用于把课程原始材料整理成一套可复用的 Markdown/Obsidian 知识库，而不是一次性的总结文档。目标产物包括：

- 每节课的 `note.md`
- 跨课程复用的 `concepts/*.md`
- 课程级汇总文件：`lecture_summary.md`、`concept_summary.md`、`pending_links.md`

核心流程：

```text
transcript + slides + existing summaries
-> lecture note
-> concept pages
-> summary updates
-> pending decisions
```

## 灵感来源

这个项目受到了两个方向的影响：

- Karpathy 的 `llm-wiki` 思路：把原始材料持续沉淀成可检索、可链接、可迭代更新的知识库，而不是一次性输出。
- [decopy.ai](https://decopy.ai/) 总结 YouTube 视频的产品形态：强调从视频内容中提炼结构化笔记、摘要和关键概念。

这个仓库更偏向本地工作流和可维护的课程 wiki，而不是面向终端用户的网页产品。

## 仓库内容

- `SKILL.md`：Codex skill 说明，定义了完整的课程 wiki 生成流程
- `scripts/init_course_wiki.py`：初始化课程目录和 Markdown 模板
- `scripts/srt_to_txt.py`：把 `.srt` / `.vtt` 字幕转成纯文本 transcript
- `scripts/prepare_slide_images.py`：把 PDF 幻灯片渲染成 `page_N.png`
- `scripts/check_wiki.py`：检查 wiki 结构和常见笔记问题
- `assets/`：课程索引、lecture note、concept summary 等模板

## 目录约定

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

`material/` 中的原始文件应被视为 source of truth，默认只读；派生内容放在 `figures/` 或其他生成文件中。

## 快速开始

1. 初始化课程结构：

```bash
python3 scripts/init_course_wiki.py --root . --course course-name --lecture lecture-01 --title "Lecture title"
```

2. 如果输入是字幕文件，先转成 transcript：

```bash
python3 scripts/srt_to_txt.py lecture.srt transcript.txt
```

3. 如果需要，把 PDF 幻灯片渲染成图片：

```bash
python3 scripts/prepare_slide_images.py --pdf courses/course-name/lectures/lecture-01/material/slides.pdf --output courses/course-name/lectures/lecture-01/figures
```

4. 完成笔记和概念页后，运行检查：

```bash
python3 scripts/check_wiki.py --root .
```

## 适用场景

- 课程视频转笔记
- 字幕 + 幻灯片联合整理
- 长课程的增量式知识沉淀
- 用 Obsidian 管理课程概念、lecture note 和交叉链接

## 许可证

本仓库采用 [MIT License](LICENSE)。

MIT 属于宽松型开源许可证，允许商业使用、修改和再分发。
