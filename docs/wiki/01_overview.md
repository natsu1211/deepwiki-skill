<!-- PAGE_ID: deepwiki-skill_01_overview -->
<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [README.md:1-290](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/README.md#L1-L290)
- [SKILL.md:1-83](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/SKILL.md#L1-L83)
- [plugin.json:1-8](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/.claude-plugin/plugin.json#L1-L8)

</details>

# Overview

> **Related Pages**: [[Architecture|02_architecture.md]], [[Workflow Phases|03_workflow.md]]

---

<!-- BEGIN:AUTOGEN deepwiki-skill_01_overview_introduction -->
## Introduction

deepwiki-skill is an agent skill for Claude Code and other AI agents that automatically generates comprehensive, wiki-style documentation for any codebase ([README.md:3](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/README.md#L3)). It is designed as a reusable skill that works across multiple AI agents, not as a standalone agent ([README.md:7](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/README.md#L7)).

The skill provides a complete workflow for generating and updating wiki-style documentation with evidence-based citations and Mermaid diagram validation ([SKILL.md:9](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/SKILL.md#L9)).

### Why Use deepwiki-skill

The project addresses several key documentation challenges:

| Benefit | Description |
|---------|-------------|
| Standard Agent Skill | Works across multiple AI agents as a reusable skill ([README.md:7](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/README.md#L7)) |
| Zero Configuration | Leverages existing subscriptions without complex setup ([README.md:8](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/README.md#L8)) |
| Evidence-Based | Every key statement includes precise line-level citations from source code ([README.md:9](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/README.md#L9)) |
| Manual Structure Control | Full control of document structure, solving the problem of uncontrollable auto-generated content ([README.md:10](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/README.md#L10)) |
| CI/CD Ready | Built-in incremental updates feature for easy deployment in CI/CD pipelines ([README.md:11](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/README.md#L11)) |

Sources: [README.md:1-11](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/README.md#L1-L11), [SKILL.md:8-9](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/SKILL.md#L8-L9)
<!-- END:AUTOGEN deepwiki-skill_01_overview_introduction -->

---

<!-- BEGIN:AUTOGEN deepwiki-skill_01_overview_key-features -->
## Key Features

deepwiki-skill provides a comprehensive set of features for documentation generation:

| Feature | Description |
|---------|-------------|
| Evidence-Based Documentation | Every statement traced back to source files with line numbers ([README.md:15](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/README.md#L15)) |
| Mermaid Diagram Support | Generate and validate flowcharts, sequence diagrams, class diagrams, and more ([README.md:16](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/README.md#L16)) |
| Flexible Execution Modes | Fully automatic, TOC-file-based, or incremental updates ([README.md:17](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/README.md#L17)) |
| Parallel Processing | Subagents for faster documentation generation and better context isolation ([README.md:18](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/README.md#L18)) |
| Smart Code Analysis | Detects multiple programming languages, handles encoding detection, filters binary files ([README.md:19](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/README.md#L19)) |
| Multi-Language Output | Output as Markdown with simple control over output language ([README.md:20](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/README.md#L20)) |

### Execution Modes

The skill supports multiple execution modes to fit different use cases ([SKILL.md:29-36](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/SKILL.md#L29-L36)):

| Mode | Phases | Use Case |
|------|--------|----------|
| Automatic | 1 - 2 - 3 - 4 - 5 | Generate complete documentation from scratch ([README.md:268](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/README.md#L268)) |
| Structure-only | 1 - 2 | Design TOC without generating content ([README.md:269](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/README.md#L269)) |
| TOC-based | 3 - 4 - 5 | Generate docs from existing TOC yaml file ([README.md:270](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/README.md#L270)) |
| Incremental | 6 - 3 - 4 - 5 | Update docs after code changes ([README.md:271](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/README.md#L271)) |

Sources: [README.md:13-21](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/README.md#L13-L21), [README.md:264-271](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/README.md#L264-L271), [SKILL.md:27-36](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/SKILL.md#L27-L36)
<!-- END:AUTOGEN deepwiki-skill_01_overview_key-features -->

---

<!-- BEGIN:AUTOGEN deepwiki-skill_01_overview_installation -->
## Installation

### Prerequisites

Before installing deepwiki-skill, ensure you have the following:

- Python >=3.12 ([README.md:25](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/README.md#L25))
- Node.js and Mermaid CLI for diagram validation ([README.md:26-29](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/README.md#L26-L29))

```bash
npm install -g @mermaid-js/mermaid-cli
```

### Claude Code

Claude Code currently offers the best subagent support for optimal documentation generation and is recommended for the best experience ([README.md:33](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/README.md#L33)).

To install in Claude Code, register the marketplace and install the plugin ([README.md:37-42](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/README.md#L37-L42)):

```
/plugin marketplace add natsu1211/deepwiki-skill
/plugin install deepwiki-skill@deepwiki-skill-marketplace
```

After installation, execute `/skills` command in Claude Code to verify the `wiki` skill appears in the list ([README.md:44](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/README.md#L44)).

### Gemini CLI

For Gemini CLI, version >=0.24.0 is required to use agent skills. Manual installation will not install subagents, and generation quality may degrade due to the limited context window ([README.md:47](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/README.md#L47)).

Manual installation ([README.md:55-60](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/README.md#L55-L60)):

```bash
git clone https://github.com/natsu1211/deepwiki-skill && cd deepwiki-skill
cp -R skills ~/.gemini
```

### Codex

For Codex, generation quality may degrade due to limited context window ([README.md:65](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/README.md#L65)).

Copy the skills folder into `~/.codex` (user scope) or `project_dir/.codex` (workspace scope) ([README.md:67-72](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/README.md#L67-L72)):

```bash
git clone https://github.com/natsu1211/deepwiki-skill && cd deepwiki-skill
cp -R skills ~/.codex
```

Sources: [README.md:22-75](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/README.md#L22-L75)
<!-- END:AUTOGEN deepwiki-skill_01_overview_installation -->

---

<!-- BEGIN:AUTOGEN deepwiki-skill_01_overview_quick-start -->
## Quick Start

### Basic Usage

You can invoke the skill by writing natural language prompts like "Use wiki skill to generate wiki documentation" or "Invoke wiki skill to update documents at docs/wiki based on docs/wiki/toc.yaml" ([README.md:78](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/README.md#L78)).

A custom command `gen` is also provided to parse arguments and explicitly invoke the skill, allowing CLI-style usage with more concise inputs ([README.md:80](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/README.md#L80)).

### Command Examples

**Fully automatic wiki document generation** ([README.md:82-85](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/README.md#L82-L85)):
```bash
/deepwiki-skill:gen
```

**Generate TOC file only** ([README.md:87-90](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/README.md#L87-L90)):
```bash
/deepwiki-skill:gen --structure
```

**Generate from existing TOC** ([README.md:92-95](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/README.md#L92-L95)):
```bash
/deepwiki-skill:gen docs/wiki/toc.yaml
```

**Update documentation after changes** ([README.md:97-100](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/README.md#L97-L100)):
```bash
/deepwiki-skill:gen docs/wiki/toc.yaml --update
```

**Specify output directory** ([README.md:102-105](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/README.md#L102-L105)):
```bash
/deepwiki-skill:gen --output ./documentation/wiki
```

**Generate documentation in a specific language** ([README.md:107-110](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/README.md#L107-L110)):
```bash
/deepwiki-skill:gen --language zh-CN
```

**Include or exclude specific files** ([README.md:112-120](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/README.md#L112-L120)):
```bash
/deepwiki-skill:gen --include "src/**/*.ts"
/deepwiki-skill:gen --exclude "**/*.test.js"
```

**Run from CLI in headless mode** ([README.md:127-130](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/README.md#L127-L130)):
```bash
claude -p "/deepwiki-skill:gen" --dangerously-skip-permissions
```

### Available Arguments

| Argument | Description |
|----------|-------------|
| `<toc.yaml>` | Path to existing TOC file ([README.md:138](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/README.md#L138)) |
| `--structure` | Generate only TOC structure, stop before generating docs ([README.md:139](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/README.md#L139)) |
| `--update` | Incremental update mode, requires TOC file path ([README.md:140](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/README.md#L140)) |
| `--output <dir>` | Output directory, default: `./docs/wiki/` ([README.md:141](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/README.md#L141)) |
| `--language <locale>` | Output language, default: `en-US`, supports almost any locale code ([README.md:142](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/README.md#L142)) |
| `--include <pattern>` | Include files matching pattern, can use multiple times ([README.md:143](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/README.md#L143)) |
| `--exclude <pattern>` | Exclude files matching pattern, can use multiple times ([README.md:144](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/README.md#L144)) |

Sources: [README.md:76-145](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/README.md#L76-L145)
<!-- END:AUTOGEN deepwiki-skill_01_overview_quick-start -->

---
