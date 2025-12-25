# Dotter Configuration

Local development setup using [dotter](https://github.com/SuperCuber/dotter) to symlink skills to `~/.config/claude/skills/`.

## Usage

```bash
# Install all skills
dotter deploy

# Install specific skill
dotter deploy -p typst

# Install skill groups
dotter deploy -p research-skills  # deep-research, wide-research
dotter deploy -p doc-skills       # report, slide, typst

# Overwrite existing files
dotter deploy --force
```
