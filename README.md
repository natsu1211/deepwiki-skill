# deepwiki-skill

**deepwiki-skill** is an agent skill for Claude Code (and any other AI agent that supports agent skills) that automatically generates comprehensive, wiki-style documentation for any codebase.

## Why use deepwiki-skill

- **Standard Agent Skill**: Not another standalone agent, but a reusable skill that works across multiple AI agents
- **Zero Configuration Hassle**: Leverage your existing subscription without complex setup
- **Evidence-Based & Hallucination-Free**: Every key statement includes precise line-level citations from source code
- **Manual Structure Control**: Available to take full control of document structure, solving the problem of uncontrollable auto-generated content
- **CI/CD Ready**: Built-in incremental updates feature makes it easy to deploy in CI/CD pipelines, keeping docs synchronized with code changes

## Features

- **Evidence-Based Documentation**: Every statement traced back to source files with line numbers
- **Mermaid Diagram Support**: Generate and validate flowcharts, sequence diagrams, class diagrams, and more
- **Flexible Execution Modes**: Fully automatic, TOC-file-based, or incremental updates
- **Parallel Processing**: Subagents for faster documentation generation and better context isolation
- **Smart Code Analysis**: Detects multiple programming languages, handles encoding detection, filters binary files
- **Multi-Language & Markdown-Based Output**: Output as Markdown, simple control over output language

## Quick Start

### Prerequisites
- Python >=3.12
- Node.js and Mermaid CLI (for diagram validation)
   ```bash
   npm install -g @mermaid-js/mermaid-cli
   ```

### Installation

> **Note**: While deepwiki-skill works with any coding agent that supports agent skills, Claude Code currently offers the best subagent support for optimal documentation generation. Claude Code is recommended for the best experience.

#### Claude Code

In Claude Code, register the marketplace and install this plugin

```
/plugin marketplace add natsu1211/deepwiki-skill
/plugin install deepwiki-skill@deepwiki-skill-marketplace
```

Execute `/skills` command in Claude Code then you should see `wiki` skill in the list.

#### Gemini CLI
> **Note**: Version >=0.24.0 is required to use agent skills. Manual installation will not install subagents, and generation quality may degrade due to the limited context window.

<b>via Gemini CLI Extension</b>

`coming soon...`

<b>manual</b>

Copy the skills folder into `~/.gemini` (user scope) or `project_dir/.gemini`(workspace scope)

```
git clone https://github.com/natsu1211/deepwiki-skill && cd deepwiki-skill
cp -R skills ~/.gemini
```

Execute `/skills` command in Gemini CLI then you should see `wiki` skill in the list.

#### Codex
> **Note**: Generation quality may degrade due to limited context window.

Copy the skills folder into `~/.codex` (user scope) or `project_dir/.codex`(workspace scope)

```
git clone https://github.com/natsu1211/deepwiki-skill && cd deepwiki-skill
cp -R skills ~/.codex
```

Execute `/skills` command in Codex then you should see `wiki` skill in the list.

### Usage

Just write something like `Use wiki skill to generate wiki documentation` or `Invoke wiki skill to update documents at docs/wiki based on docs/wiki/toc.yaml` to tell agent to invoke skill.

Custom command `gen` is also provided to parse the arguments and explicitly invoke the skill. This allows you to use the skill like a regular CLI tool, making inputs more concise while expressing intent more precisely.

#### Basic Usage

Fully automatic wiki document generation:
```bash
/deepwiki-skill:gen
```

Generate TOC file only:
```bash
/deepwiki-skill:gen --structure
```

Generate from existing TOC:
```bash
/deepwiki-skill:gen docs/wiki/toc.yaml
```

Update documentation after manually changing `toc.yaml` and/or code changes:
```bash
/deepwiki-skill:gen docs/wiki/toc.yaml --update
```

Specify output directory:
```bash
/deepwiki-skill:gen --output ./documentation/wiki
```

Generate documentation in Chinese:
```bash
/deepwiki-skill:gen --language zh-CN
```

Include only specific files:
```bash
/deepwiki-skill:gen --include "src/**/*.ts"
```

Exclude test files:
```bash
/deepwiki-skill:gen --exclude "**/*.test.js"
```

Combined arguments:
```bash
/deepwiki-skill:gen --language zh-CN --output ./docs --exclude "**/*.test.js"
```

Run from CLI (yolo mode / headless mode):
```bash
claude -p "/deepwiki-skill:gen" --dangerously-skip-permissions
```

#### Use Cases

1. Quickly understand a new project
   - Use fully automatic mode: `/deepwiki-skill:gen`

2. Generate wiki documentation for your project with control over chapter structure
   - First use structure-only mode to generate initial `toc.yaml`: `/deepwiki-skill:gen --structure`
   - Modify `docs/wiki/toc.yaml` according to your needs
   - Then use TOC-based mode to regenerate documentation: `/deepwiki-skill:gen docs/wiki/toc.yaml`

3. Sync documentation when TOC file or code is updated
   - Use Incremental Update mode: `/deepwiki-skill:gen docs/wiki/toc.yaml --update`

**Available Arguments:**

| Argument | Description |
|----------|-------------|
| `<toc.yaml>` | Path to existing TOC file |
| `--structure` | Generate only TOC structure, stop before generating docs |
| `--update` | Incremental update mode (requires TOC file path) |
| `--output <dir>` | Output directory (default: `./docs/wiki/`) |
| `--language <locale>` | Output language (default: `en-US`, supports almost any locale code) |
| `--include <pattern>` | Include files matching pattern (can use multiple times) |
| `--exclude <pattern>` | Exclude files matching pattern (can use multiple times) |


### CI/CD Integration

#### Claude Code

If you have a Pro/Max subscription, create an OAuth token first (if you prefer to use an API key, save the API key instead of an OAuth token to GitHub secrets).

Open your terminal and input
```
claude setup-token
```

Record the token output in your terminal and save it to GitHub secrets for your repository, giving it a name like `CLAUDE_CODE_OAUTH_TOKEN`.

Then create the GitHub Actions workflow file.
Here is a GitHub Actions workflow example that can be triggered manually to incrementally update existing documentation:
```
name: Wiki Doc Update

on:
  workflow_dispatch:

jobs:
  generate:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
      issues: write
      id-token: write
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 1

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install mermaid-cli
        run: npm install -g @mermaid-js/mermaid-cli

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install Python dependencies
        run: |
          if [ -f skills/wiki/scripts/requirements.txt ]; then
            pip install -r skills/wiki/scripts/requirements.txt
          fi

      - name: Run Wiki Doc Update
        id: deepwiki-skill
        uses: anthropics/claude-code-action@v1
        with:
          plugin_marketplaces: 'https://github.com/natsu1211/deepwiki-skill.git'
          plugins: 'deepwiki-skill@deepwiki-skill-marketplace'
          claude_code_oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
          prompt: '/deepwiki-skill:gen docs/wiki/toc.yaml --update'
          additional_permissions: |
            actions: read

```

#### Gemini CLI
Refer to https://github.com/google-github-actions/run-gemini-cli

#### Codex
Refer to https://github.com/openai/codex-action

## Technical Details

Check out the detailed documents generated by deepwiki-skill itself: [docs](./docs/wiki)

### Workflow

deepwiki-skill operates through six distinct phases:

#### 1. Repository Scan (`repo-scan`)
- Analyzes repository structure and file organization
- Detects programming languages and file types
- Counts files and generates project statistics
- Reads existing README and documentation

#### 2. TOC Design (`toc-design`)
- Designs wiki structure based on code analysis
- Generates hierarchical Table of Contents
- Creates `toc.yaml` with page definitions
- Supports nested sections and auto-generation flags

#### 3. Document Writing (`doc-write`)
- Generates actual documentation pages
- Includes evidence-based citations
- Creates Mermaid diagrams for visualizations
- Supports parallel page generation

#### 4. Document Validation (`validate-docs`)
- Validates document structure and markers
- Checks Mermaid diagram syntax
- Provides error reports with fix suggestions
- Ensures TOC compliance

#### 5. Summary Generation (`doc-summary`)
- Creates `SUMMARY.md` report
- Lists all generated pages
- Includes validation results
- Provides documentation statistics

#### 6. Incremental Sync (`incremental-sync`)
- Detects code changes via git diff
- Identifies impacted documentation pages
- Updates only affected sections
- Maintains documentation consistency

### Execution Modes

| Mode | Phases | Use Case |
|------|--------|----------|
| **Automatic** | 1→2→3→4→5 | Generate complete documentation from scratch |
| **Structure-only** | 1→2 | Design TOC without generating content |
| **TOC-based** | 3→4→5 | Generate docs from existing TOC yaml file |
| **Incremental Update** | 6→3→4→5 | Update docs after code changes |

### Output Structure

```
docs/wiki/
├── toc.yaml                  # Table of Contents definition
├── 01_overview.md            # Generated pages
├── 02_architecture.md
├── 03_workflow.md
├── _context/
│   └── context_pack.json     # Context data for generation
└── _reports/
    ├── SUMMARY.md            # Documentation summary report
    ├── mermaid_invalid.json  # Mermaid diagram validation
    └── structure_validation.json
```

## LICENSE
MIT
