[English](./README.md) | [简体中文](./README_CN.md)

# video-to-notes

`video-to-notes` 是一个 Codex skill 和配套工具集，用于把课程转录文本与幻灯片材料整理成专业的中文 LaTeX 课程笔记，并编译为 PDF。

核心流程是：

```text
转录 TXT + 幻灯片 PDF/PPT/PPTX -> 幻灯片截图 -> LaTeX 笔记 -> PDF 成品
```

如果提供 YouTube URL 和 `cookies.txt`，工作流也可以先只下载字幕，把字幕转换为 TXT，再与本地幻灯片一起生成笔记。

## 目录结构

- `SKILL.md`：Codex skill 的主说明文件，也是写作规范、图像选择、字幕下载、LaTeX 生成与校验流程的事实来源。
- `assets/notes-template.tex`：默认中文 LaTeX 笔记模板，包含简洁封面、强调框、代码块、图片和 TikZ。
- `scripts/prepare_slide_images.py`：把幻灯片 PDF 渲染成 `pic/page_N.png` 图片；支持在当前目录中自动识别唯一的 PDF 和 TXT。
- `scripts/srt_to_txt.py`：把 `.srt` 或 `.vtt` 字幕转换成可读的 `.txt` 转录文本。
- `clean.sh`：在一节课笔记完成后，把当前工作区归档到指定文件夹。
- `agents/openai.yaml`：面向 agent 的简短入口配置。
- `demo/`：用于测试图片准备脚本的示例幻灯片 PDF。

## 支持的输入

- 本地 TXT 转录文本 + 本地 PDF 幻灯片。
- 本地 TXT 转录文本 + 本地 PPT/PPTX 幻灯片，需先转换为 PDF。
- YouTube URL 或 `url.txt` + `cookies.txt`，先下载字幕，再与本地幻灯片合成笔记。

如果目录中有多份候选转录文本或多份候选幻灯片，请显式指定文件，不要依赖自动识别。

## 环境依赖

字幕转换脚本只依赖 Python 标准库。PDF 渲染建议安装：

```bash
python3 -m pip install pdf2image
```

还需要安装 Poppler 以渲染 PDF 页面。macOS：

```bash
brew install poppler
```

Ubuntu/Debian：

```bash
sudo apt-get install poppler-utils
```

如需从 YouTube 下载字幕，安装 `yt-dlp`：

```bash
python3 -m pip install yt-dlp
```

如需编译最终 PDF，请安装带 XeLaTeX 的 LaTeX 发行版，并确保包含 `ctex`、`tcolorbox`、`listings`、`tikz`、`pgfplots` 等常用宏包。

## 快速开始

### 1. 准备源文件

把课程转录文本和幻灯片放到工作目录。如果转录材料是字幕文件，先转换为 TXT：

```bash
python3 scripts/srt_to_txt.py lecture.srt transcript.txt
```

### 2. 生成幻灯片截图

如果工作目录中正好有一个 `.pdf` 和一个 `.txt`，可以使用自动识别：

```bash
python3 scripts/prepare_slide_images.py --auto
```

否则，请显式指定幻灯片 PDF：

```bash
python3 scripts/prepare_slide_images.py --pdf slides.pdf --output pic
```

脚本会生成 `pic/page_1.png`、`pic/page_2.png` 等图片。如果 `pic/` 中已经存在页面图片，默认会复用；需要重新渲染时加上 `--force`。

使用示例文件测试：

```bash
python3 scripts/prepare_slide_images.py --pdf demo/karpathy_llm_intro.pdf --output pic --force
```

### 3. 生成课程笔记

让 Codex 使用 `video-to-notes` skill 处理转录文本和幻灯片。该 skill 会：

1. 检查源文件和幻灯片截图；
2. 以 `assets/notes-template.tex` 为基础模板；
3. 选择或生成有教学价值的图；
4. 写出完整中文课程笔记；
5. 将 `.tex` 编译为 PDF；
6. 校验引用资源是否存在，并确认 PDF 可成功生成。

如果手动使用，可以从 `assets/notes-template.tex` 开始，替换正文区域，并按 `pic/page_N.png` 约定引用幻灯片截图。

### 4. 手动编译

```bash
xelatex notes.tex
xelatex notes.tex
```

目录和交叉引用通常需要运行两遍 XeLaTeX。

### 5. 归档已完成课程

```bash
chmod +x clean.sh
./clean.sh Lec_01_Intro
```

`clean.sh` 会创建目标文件夹，并移动 `pic/`、根目录下所有 `*.pdf`、`*.txt`、`*.tex` 文件。它目前不会移动 `.srt` 或 `.vtt` 文件。

## 输出约定

- 默认使用中文写作，除非用户明确要求其他语言。
- 幻灯片截图使用 `pic/page_N.png`；图注只说明教学作用，不额外注明来源页码。
- 图片不要放在 `importantbox`、`knowledgebox`、`warningbox` 或 `dialoguebox` 内部。
- 每个主要章节应以 `本章小结` 收束。
- 文档最后应包含顶层章节 `总结与延伸`。
- 最终交付物应包含生成的 `.tex`、编译后的 `.pdf` 以及所有被引用的资源文件。
