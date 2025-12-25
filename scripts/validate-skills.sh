#!/bin/bash
# Validate skills using skill-creator's quick_validate.py
# Checks both internal (~/.claude) and external (~/.config/claude) paths

set -e

# Find skill-creator validate script
VALIDATE_SCRIPT=""
if [ -f "$HOME/.claude/skills/skill-creator/scripts/quick_validate.py" ]; then
    VALIDATE_SCRIPT="$HOME/.claude/skills/skill-creator/scripts/quick_validate.py"
elif [ -f "$HOME/.config/claude/skills/skill-creator/scripts/quick_validate.py" ]; then
    VALIDATE_SCRIPT="$HOME/.config/claude/skills/skill-creator/scripts/quick_validate.py"
fi

if [ -z "$VALIDATE_SCRIPT" ]; then
    echo "skill-creator not found, skipping validation"
    exit 0
fi

# Find skills directory
SKILLS_DIR="./skills"
if [ ! -d "$SKILLS_DIR" ]; then
    echo "No skills/ directory found"
    exit 0
fi

# Validate each skill
FAILED=0
for skill in "$SKILLS_DIR"/*/; do
    if [ -f "$skill/SKILL.md" ]; then
        if ! python3 "$VALIDATE_SCRIPT" "$skill"; then
            FAILED=1
        fi
    fi
done

exit $FAILED
