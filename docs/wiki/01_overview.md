<!-- PAGE_ID: deepwiki-skill_01_overview -->
<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [README.md:1-257](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/README.md#L1-L257)
- [SKILL.md:1-97](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/SKILL.md#L1-L97)
- [gen.md:1-27](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/commands/gen.md#L1-L27)

</details>

# Overview

> **Related Pages**: [[Architecture|02_architecture.md]], [[Workflow Phases|03_workflow-phases.md]]

---

<!-- BEGIN:AUTOGEN deepwiki-skill_01_overview_introduction -->
## Introduction

**deepwiki-skill** is an agent skill for Claude Code and other AI agents that supports agent skills, designed to automatically generate comprehensive, wiki-style documentation for any codebase ([README.md:3](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/README.md#L3)).

This skill provides a complete workflow for generating and updating wiki-style documentation with evidence-based citations and Mermaid diagram validation ([SKILL.md:9](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/SKILL.md#L9)).

### Why Use deepwiki-skill

The skill addresses several key documentation challenges ([README.md:5-11](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/README.md#L5-L11)):

| Benefit | Description |
|---------|-------------|
| Standard Agent Skill | Not another standalone agent, but a reusable skill that works across multiple AI agents ([README.md:7](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/README.md#L7)) |
| Zero Configuration Hassle | Leverage your existing subscription without complex setup ([README.md:8](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/README.md#L8)) |
| Evidence-Based & Hallucination-Free | Every key statement includes precise line-level citations from source code ([README.md:9](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/README.md#L9)) |
| Manual Structure Control | Available to take full control of document structure, solving the problem of uncontrollable auto-generated content ([README.md:10](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/README.md#L10)) |
| CI/CD Ready | Built-in incremental updates feature make it easy to deploy in CI/CD pipelines, keeping docs synchronized with code changes ([README.md:11](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/README.md#L11)) |

The skill can be used for generating documentation for a new project, updating existing documentation after code changes, creating or refining a wiki TOC for a codebase, and obtaining a comprehensive overview of an unfamiliar project ([SKILL.md:3](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/SKILL.md#L3)).

Sources: [README.md:1-11](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/README.md#L1-L11), [SKILL.md:1-9](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/SKILL.md#L1-L9)
<!-- END:AUTOGEN deepwiki-skill_01_overview_introduction -->

---

<!-- BEGIN:AUTOGEN deepwiki-skill_01_overview_key-features -->
## Key Features

The skill provides the following key capabilities ([README.md:13-20](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/README.md#L13-L20)):

| Feature | Description |
|---------|-------------|
| Evidence-Based Documentation | Every statement traced back to source files with line numbers ([README.md:15](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/README.md#L15)) |
| Mermaid Diagram Support | Generate and validate flowcharts, sequence diagrams, class diagrams, and more ([README.md:16](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/README.md#L16)) |
| Flexible Execution Modes | Full automatic, Table of Contents file based, or incremental updates ([README.md:17](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/README.md#L17)) |
| Parallel Processing | Subagents for faster documentation generation and better context isolation ([README.md:18](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/README.md#L18)) |
| Smart Code Analysis | Detects multiple programming languages, handles encoding detection, filters binary files ([README.md:19](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/README.md#L19)) |
| Multi-Language & Markdown-Based Output | Output as Markdown, simple control over output language ([README.md:20](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/README.md#L20)) |

### Execution Modes

The skill supports multiple execution modes, each tailored for different use cases ([README.md:208-215](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/README.md#L208-L215), [SKILL.md:29-36](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/SKILL.md#L29-L36)):

| Mode | Phases | Use Case |
|------|--------|----------|
| Automatic | 1 to 2 to 3 to 4 to 5 | Generate complete documentation from scratch ([README.md:212](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/README.md#L212)) |
| Structure-only | 1 to 2 | Design TOC without generating content ([README.md:213](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/README.md#L213)) |
| TOC-based | 3 to 4 to 5 | Generate docs from existing TOC yaml file ([README.md:214](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/README.md#L214)) |
| Incremental | 6 to 3 to 4 to 5 | Update docs after code changes ([README.md:215](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/README.md#L215)) |

### Workflow Phases

The documentation generation operates through six distinct phases ([README.md:168-206](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/README.md#L168-L206)):

| Phase | Name | Purpose |
|-------|------|---------|
| 1 | Repository Scan | Analyzes repository structure, detects programming languages, counts files, reads existing documentation ([README.md:172-176](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/README.md#L172-L176)) |
| 2 | TOC Design | Designs wiki structure based on code analysis, generates hierarchical Table of Contents ([README.md:178-182](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/README.md#L178-L182)) |
| 3 | Document Writing | Generates actual documentation pages with evidence-based citations and Mermaid diagrams ([README.md:184-188](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/README.md#L184-L188)) |
| 4 | Document Validation | Validates document structure, checks Mermaid diagram syntax, provides error reports ([README.md:190-194](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/README.md#L190-L194)) |
| 5 | Summary Generation | Creates SUMMARY.md report with all generated pages and validation results ([README.md:196-200](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/README.md#L196-L200)) |
| 6 | Incremental Sync | Detects code changes via git diff, identifies impacted pages, updates only affected sections ([README.md:202-206](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/README.md#L202-L206)) |

Sources: [README.md:13-20](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/README.md#L13-L20), [README.md:168-215](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/README.md#L168-L215), [SKILL.md:16-36](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/SKILL.md#L16-L36)
<!-- END:AUTOGEN deepwiki-skill_01_overview_key-features -->

---

<!-- BEGIN:AUTOGEN deepwiki-skill_01_overview_quick-start -->
## Quick Start

### Prerequisites

Before using deepwiki-skill, ensure you have the following installed ([README.md:24-29](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/README.md#L24-L29)):

- Python >= 3.12
- Node.js and Mermaid CLI (for diagram validation)

To install the Mermaid CLI:

```bash
npm install -g @mermaid-js/mermaid-cli
```

### Installation

While deepwiki-skill works with any coding agent that supports agent skills, Claude Code currently offers the best subagent support for optimal documentation generation ([README.md:33](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/README.md#L33)).

#### Claude Code

In Claude Code, register the marketplace and install the plugin ([README.md:35-42](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/README.md#L35-L42)):

```
/plugin marketplace add natsu1211/deepwiki-skill-marketplace
/plugin install deepwiki-skill@deepwiki-skill-marketplace
```

Execute `/skills` command in Claude Code to verify the `wiki` skill appears in the list ([README.md:44](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/README.md#L44)).

#### Gemini CLI

For Gemini CLI version >= 0.24.0, copy the skills folder into `~/.gemini` (user scope) or `project_dir/.gemini` (workspace scope) ([README.md:46-62](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/README.md#L46-L62)):

```bash
git clone https://github.com/natsu1211/deepwiki-skill && cd deepwiki-skill
cp -R skills ~/.gemini
```

#### Codex

Copy the skills folder into `~/.codex` (user scope) or `project_dir/.codex` (workspace scope) ([README.md:64-74](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/README.md#L64-L74)):

```bash
git clone https://github.com/natsu1211/deepwiki-skill && cd deepwiki-skill
cp -R skills ~/.codex
```

### Usage

You can invoke the skill by writing something like "Use wiki skill to generate wiki documentation" or "Invoke wiki skill" to tell the agent to invoke the skill ([README.md:78](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/README.md#L78)).

The custom command `gen` is also provided to parse arguments and explicitly invoke the skill, making inputs more concise while expressing intent more precisely ([README.md:80](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/README.md#L80)).

#### Command Examples

| Command | Description |
|---------|-------------|
| `/deepwiki-skill:gen` | Fully automatic wiki document generation ([README.md:83-85](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/README.md#L83-L85)) |
| `/deepwiki-skill:gen --structure` | Generate TOC file only ([README.md:87-89](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/README.md#L87-L89)) |
| `/deepwiki-skill:gen docs/wiki/toc.yaml` | Generate from existing TOC ([README.md:91-95](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/README.md#L91-L95)) |
| `/deepwiki-skill:gen docs/wiki/toc.yaml --update` | Update documentation after code changes ([README.md:97-100](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/README.md#L97-L100)) |
| `/deepwiki-skill:gen --output ./documentation/wiki` | Specify output directory ([README.md:102-105](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/README.md#L102-L105)) |
| `/deepwiki-skill:gen --language zh-CN` | Generate documentation in Chinese ([README.md:107-110](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/README.md#L107-L110)) |

#### Available Arguments

| Argument | Description |
|----------|-------------|
| `<toc.yaml>` | Path to existing TOC file ([gen.md:18](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/commands/gen.md#L18)) |
| `--structure` | Generate only TOC structure, stop before generating docs ([gen.md:19](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/commands/gen.md#L19)) |
| `--update` | Incremental update mode (requires TOC file path) ([gen.md:20](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/commands/gen.md#L20)) |
| `--output <dir>` | Output directory (default: `./docs/wiki/`) ([gen.md:21](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/commands/gen.md#L21)) |
| `--language <locale>` | Output language (default: `en-US`) ([gen.md:22](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/commands/gen.md#L22)) |
| `--include <pattern>` | Include files matching pattern ([gen.md:23](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/commands/gen.md#L23)) |
| `--exclude <pattern>` | Exclude files matching pattern ([gen.md:24](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/commands/gen.md#L24)) |

### Output Structure

The generated documentation follows this structure ([README.md:217-229](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/README.md#L217-L229)):

```
docs/wiki/
├── toc.yaml              # Table of Contents definition
├── SUMMARY.md            # Documentation summary report
├── 01_overview.md        # Generated pages
├── 02_architecture.md
├── 03_components/
│   ├── 01_module_a.md
│   └── 02_module_b.md
└── ...
```

Sources: [README.md:22-125](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/README.md#L22-L125), [README.md:217-229](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/README.md#L217-L229), [gen.md:14-24](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/commands/gen.md#L14-L24)
<!-- END:AUTOGEN deepwiki-skill_01_overview_quick-start -->

---
