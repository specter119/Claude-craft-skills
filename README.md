# Craft Skills

Craft your insights into content - research, report, slide, and more.

A collection of Agent Skills for Claude Code that help you research, write, and create professional documents.

## Installation

### Option 1: Install as Plugin (All Skills)

```bash
# Add marketplace
/plugin marketplace add specter119/claude-craft-skills

# Install plugin
/plugin install craft-skills@specter119-claude-craft-skills
```

### Option 2: Install Individual Skills

If you only need specific skills, you can install them directly to `~/.claude/skills/`:

```bash
# Install deep-research only
curl -fsSL https://github.com/specter119/claude-craft-skills/archive/main.tar.gz | \
  tar -xz --strip-components=2 -C ~/.claude/skills/ claude-craft-skills-main/skills/deep-research

# Install report only
curl -fsSL https://github.com/specter119/claude-craft-skills/archive/main.tar.gz | \
  tar -xz --strip-components=2 -C ~/.claude/skills/ claude-craft-skills-main/skills/report

# Install slide only
curl -fsSL https://github.com/specter119/claude-craft-skills/archive/main.tar.gz | \
  tar -xz --strip-components=2 -C ~/.claude/skills/ claude-craft-skills-main/skills/slide
```

Or clone the entire repo and copy what you need:

```bash
git clone https://github.com/specter119/claude-craft-skills.git /tmp/craft-skills
cp -r /tmp/craft-skills/skills/deep-research ~/.claude/skills/
```

## Available Skills

| Skill | Description | Trigger Keywords |
|-------|-------------|------------------|
| **deep-research** | Deep research with multi-source synthesis | "调研", "研究", "深入了解" |
| **wide-research** | Broad exploration across multiple topics | "广泛调研", "全面了解" |
| **report** | Generate professional reports | "报告", "report" |
| **slide** | Create presentation slides with Typst | "幻灯片", "slide", "演示" |
| **typst** | Typst technical foundation layer | Used by slide/report |
| **genimg** | Generate images for content | "生成图片", "配图" |

## Usage

Skills are **model-invoked** - Claude automatically uses them based on your request. Just describe what you need:

```plain
帮我调研一下 A2A 协议的商业落地案例
```

Claude will automatically activate the `deep-research` skill.

## Requirements

- Claude Code >= 1.0.33
- For `genimg`: Requires API key configuration (see `genimg/.env.example`)

## License

MIT License - see [LICENSE](LICENSE) for details.

## Author

[specter119](https://github.com/specter119)
