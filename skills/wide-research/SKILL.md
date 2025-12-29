---
name: wide-research
description: >
  Process large volumes of local materials with parallel sub-agents. Features task decomposition,
  context isolation, parallel execution, and narrative synthesis. Use when processing multiple
  files, batch analysis, building narratives from existing materials, or when user mentions
  "wide research", "batch analysis", "批量分析", "整理材料", "构建叙事".
allowed-tools: Task, Read, Write, Edit, Bash, Glob, Grep
---

# Wide Research Skill

Inspired by Manus Wide Research and grapeot's Codex implementation.

## Knowledge Activation

**Core insight**: LLM context window limitations cause "lazy" behavior on long tasks (skipping items, premature completion). Apply **agentic decomposition patterns**: divide work into isolated sub-tasks with small output scope.

**Key principles** (Claude knows the theory):
- **Context isolation**: Prevent cross-contamination between sub-tasks
- **Parallel execution**: Fan-out pattern for independent tasks
- **Narrative synthesis**: Map-reduce pattern for final output

---

## When to Activate

- User wants to process multiple local files/documents
- Batch analysis of similar items (reports, emails, documents)
- Building narrative from existing materials
- Tasks that would produce very long output if done sequentially
- Chinese: "批量分析", "整理材料", "构建叙事", "汇总这些"

## When NOT to Use (Use Deep Research Instead)

- Need to search the internet for new information
- Single topic requiring deep investigation
- No existing local materials to process

---

## Workflow Overview

```plain
┌─────────────────────────────────────────────────────────────────┐
│  Phase 1: ANALYZE                                               │
│  ├── Inventory: List all materials to process                   │
│  ├── Classify: Group into independent sub-tasks                 │
│  └── Plan: Decide parallelization strategy                      │
├─────────────────────────────────────────────────────────────────┤
│  Phase 2: PARALLEL PROCESS                                      │
│  ├── Launch N sub-agents (one per sub-task group)               │
│  ├── Each sub-agent: read → process → write findings            │
│  └── Sub-agents write to isolated output files                  │
├─────────────────────────────────────────────────────────────────┤
│  Phase 3: SYNTHESIZE                                            │
│  ├── Collect all sub-agent outputs                              │
│  ├── Identify gaps → trigger Deep Research if needed            │
│  └── Generate final narrative/report                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Analyze

1. **Inventory**: Enumerate all materials (see `references/templates.md`)
2. **Classify**: Group by topic/file/section/batch (see `references/guidelines.md` for strategies)
3. **Plan**: Decide parallelization strategy

**Output structure**:
```plain
{working_dir}/wide-research/{task-slug}/
├── _inputs/                    # Symlinks or copies of inputs
├── group-a/findings.md
├── group-b/findings.md
├── group-c/findings.md
└── synthesis.md                # Final output
```

---

## Phase 2: Parallel Process

Launch sub-agents with Task tool. Each receives:
- Explicit item list (file paths, not patterns)
- Processing instructions
- Output path

**Critical rules for sub-agents**:
- Process EVERY item
- Do NOT skip any items
- Each item gets its own section

See `references/templates.md` for sub-agent prompt template.

---

## Phase 3: Synthesize

1. **Collect**: Read all findings.md files
2. **Gap check**: Missing items? Incomplete data?
3. **Deep Research**: Trigger for external info if needed
4. **Synthesize**: Generate final report

See `references/templates.md` for synthesis report template.

---

## Parallelization Guidelines

**Rule**: Keep 5-10 items per sub-agent to prevent slacking. See `references/guidelines.md` for detailed table.

---

## Integration with Deep Research

```plain
Wide Research → process local materials → identify gaps
       ↓
Deep Research → fill gaps from internet
       ↓
Wide Research → re-synthesize with new info
```

---

## Bundled Resources

| File | Purpose | Usage |
|------|---------|-------|
| `references/templates.md` | All templates | Read for guidance |
| `references/guidelines.md` | Tables & best practices | Reference as needed |
| `scripts/render_docx.py` | Word to images | `uv run scripts/render_docx.py <file.docx>` |

**Word files**: Use `render_docx.py` to convert DOCX → PNG images for reading. Requires LibreOffice and poppler-utils.

---

## Error Handling & Best Practices

See `references/guidelines.md` for detailed tables. Key rules:
- 5-10 items per sub-agent
- Explicit file paths, not patterns
- Verify output count = input count
