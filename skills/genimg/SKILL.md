---
name: genimg
description: >
  AI 图片生成。关键词: "生成图片", "画", "generate image"
allowed-tools: Bash, Read, Write
---

# GenImg - AI Image Generation

使用 Gemini 生成图片。

## 适用场景

- 抽象概念可视化（"创新"、"协作"、"增长"）
- 场景/氛围营造（产品使用场景、团队照片）
- 装饰性元素（图标、背景、徽章）
- 情感连接（讲故事时的配图）

**不适合**：逻辑流程图、系统架构图、数据图表（这些用代码生成更精确）

## 配置

复制 `.env.example` 到 `.env` 并填入 API key：

```bash
cp ~/.claude/skills/genimg/.env.example ~/.claude/skills/genimg/.env
# Edit .env and add your GEMINI_API_KEY
```

## 使用

```bash
SCRIPT=~/.claude/skills/genimg/scripts/generate.py

# 基本生成（uv run 自动读取脚本内 PEP 723 依赖声明）
uv run $SCRIPT "a futuristic city" -o city.png

# 带风格
uv run $SCRIPT "landscape" -s photo -o photo.png

# 图标
uv run $SCRIPT "cloud" -s icon -r 1:1 -o icon.png

# 编辑图片
uv run $SCRIPT "add rainbow" -e source.png -o edited.png

# 查看风格
uv run $SCRIPT --list-styles
```

## 风格

| 风格 | 描述 |
|------|------|
| `photo` | 真实照片 |
| `illustration` | 数字插画 |
| `flat` | 扁平设计 |
| `3d` | 3D 渲染 |
| `minimalist` | 极简 |
| `corporate` | 商务风 |
| `tech` | 科技感 |
| `sketch` | 手绘 |
| `isometric` | 等轴测 |
| `icon` | 图标 |

## 参数

```plain
-o, --output    输出路径
-s, --style     风格
-r, --ratio     比例 (16:9, 9:16, 4:3, 1:1)
-n, --negative  避免的内容
-e, --edit      编辑已有图片
--json          JSON 输出
```

## Slide/Presentation Integration

`genimg` + `slide` + `typst` 配合使用，为技术演示增加视觉吸引力。

### 演示文稿推荐配置

| 用途 | Prompt 示例 | Style | Ratio |
|------|-------------|-------|-------|
| 封面 | "futuristic logistics network" | `tech`, `corporate` | 16:9 |
| 章节分隔 | "abstract data flow" | `minimalist` | 16:9 |
| 概念图 | "AI agents collaborating" | `isometric`, `illustration` | 4:3 |
| 图标 | "shipping container" | `icon`, `flat` | 1:1 |
| 背景 | "subtle tech pattern" | `minimalist` + `-n "text, logo"` | 16:9 |

### 工作流

```bash
# 1. 在 slide 项目目录生成
cd /path/to/slide/project
SCRIPT=~/.claude/skills/genimg/scripts/generate.py

# 2. 生成封面图
uv run $SCRIPT "AI agents in supply chain network, abstract, professional" \
  -s tech -r 16:9 -o images/cover.png

# 3. 生成概念图
uv run $SCRIPT "three pillars supporting platform, integration communication authentication" \
  -s isometric -r 4:3 -o images/pillars.png

# 4. 在 Typst 中导入
# #image("images/cover.png", width: 100%)
```

### 与 Diagraph 分工

| 图类型 | 工具 | 原因 |
|--------|------|------|
| 流程图 | Diagraph | 精确控制节点和连接 |
| 架构图 | Diagraph/D2 | 需要精确标签和层次 |
| 数据图表 | Typst native | 数据准确性 |
| 抽象概念 | **GenImg** | 视觉冲击力 |
| 情感连接 | **GenImg** | 引起共鸣 |
| 装饰元素 | **GenImg** | 增加设计感 |

### Prompt 技巧（演示文稿专用）

```bash
# 避免文字（Typst 添加文字更精确）
-n "text, words, letters, labels"

# 保持简洁
"concept, minimal, clean, professional"

# 配色一致
"blue accent color, #1565C0, corporate style"
```
