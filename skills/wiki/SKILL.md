---
name: wiki
description: Generating comprehensive wiki-style documentation for any codebase. This skill can be used when 1. Generating documentation for a new project, 2. Update existing documentation after code changes, 3. Create or refine a wiki TOC for a codebase, 4. Obtain a comprehensive overview of an unfamiliar project.
---

**Your response MUST be written in the language specified by the locale code (default: en-US). This is crucial.**

# Wiki Document Generator
This skill provides a complete workflow for generating and updating wiki-style documentation for any codebase, with evidence-based citations and Mermaid diagram validation.

## Workflow
**Fully execute this workflow until completion. Do not ask for user confirmation.**

**IMPORTANT: If subagent is supported, spawn `deepwiki:workflow-runner` subagent with the corresponding `Phase_id` to execute each phase according to execution mode, otherwise read each phase spec file and reference file to understand the requirement and execute sequentially.**

### Workflow Phase Definitions

| Phase | Phase_id | Phase_spec | Purpose |
|-------|---------|-----------|---------|
| 1 | `repo-scan` | `/references/workflow/repo-scan.md` | Scan repository to get context for toc design |
| 2 | `toc-design` | `/references/workflow/toc-design.md` | Design TOC structure |
| 3 | `doc-write` | `/references/workflow/doc-write.md` | Generate documentation pages |
| 4 | `validate-docs` | `/references/workflow/validate-docs.md` | Validate diagrams and structure |
| 5 | `doc-summary` | `/references/workflow/doc-summary.md` | Generate SUMMARY.md report |
| 6 | `incremental-sync` | `/references/workflow/incremental-sync.md` | Detect TOC and source changes |.

### Execution Modes and Phases

This skill supports multiple execution modes and each mode has different execution phases and order.

| Mode | Phases | Description |
|------|--------|-------------|
| **Automatic** | 1 → 2 → 3 → 4 → 5 | Full pipeline for new documentation |
| **Structure-only** | 1 → 2 | Generate TOC only, stop before docs |
| **TOC-based** | 3 → 4 → 5 | Generate docs from existing `toc.yaml` |
| **Incremental** | 6 → 3 → 4 → 5 | Update docs after code changes |

### Subagent Invocation
**This section is available only when subagent is supported**

When spawning subagent, pass the required inputs:

```
subagent: deepwiki:workflow-runner
inputs:
  phase_id: "{phase_id}"
  phase_sepc: "absolute path of {phase_spec}"
  repo_path: "{repo_path}"
  output_dir: "{output_dir}"
  toc_file: "{toc_file}"
  page_id: "{page_id}"
  language: "{language}"
```

### Parallel Execution for doc-write (Phase 2)
**This section is available only when subagent is supported**

If subagent is supported, the `doc-write` phase should be executed parallelly to improve performance. Instead of generating all pages sequentially in a single subagent, spawn multiple subagents in **foreground** - one per page:

```
# Parse toc.yaml to get list of pages
pages = parse_toc("{toc_file}")

# Spawn one subagent per page IN PARALLEL
for each page in pages:
  spawn subagent: deepwiki:workflow-runner
    inputs:
      step_id: "{step_id}"
      repo_path: "{repo_path}"
      output_dir: "{output_dir}"
      toc_file: "{toc_file}"
      page_id: "{page.id}"
      language: "{language}"

# Wait for all subagents to complete
# Then proceed to phase 3 (validate-docs)
```

**Parallel Execution Rules**:
- Each subagent generates exactly one page (specified by `page_id`)
- All subagents should run at foreground, NOT background
- Wait for ALL page subagents to complete before proceeding to phase 3
- If any subagent fails, re-spawn a new subgent to finish the page generation