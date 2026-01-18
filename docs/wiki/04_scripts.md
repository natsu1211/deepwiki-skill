<!-- PAGE_ID: deepwiki-skill_04_scripts -->
<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [collect_context.py:1-769](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/collect_context.py#L1-L769)
- [collect_sync_context.py:1-326](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/collect_sync_context.py#L1-L326)
- [collect_update_context.py:1-595](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/collect_update_context.py#L1-L595)
- [collect_git_diff.py:1-370](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/collect_git_diff.py#L1-L370)
- [read_files.py:1-391](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/read_files.py#L1-L391)
- [validate_docs_structure.py:1-597](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/validate_docs_structure.py#L1-L597)
- [validate_mermaid.py:1-826](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/validate_mermaid.py#L1-L826)
- [generate_summary.py:1-502](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/generate_summary.py#L1-L502)

</details>

# Python Scripts

> **Related Pages**: [[Workflow Phases|03_workflow.md]], [[Reference Policies|05_policies.md]]

---

<!-- BEGIN:AUTOGEN deepwiki-skill_04_scripts_overview -->
## Scripts Overview

This section provides an overview of the Python utility scripts that power the deepwiki-skill workflow. These scripts handle repository scanning, file reading, documentation validation, and summary generation.

The scripts are located in `skills/wiki/scripts/` and can be categorized into three main groups:

| Category | Scripts | Purpose |
|----------|---------|---------|
| Context Collection | `collect_context.py`, `collect_sync_context.py`, `collect_update_context.py`, `collect_git_diff.py` | Gather repository structure, TOC synchronization status, and git change information ([collect_context.py:2-6](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/collect_context.py#L2-L6)) |
| File Reading | `read_files.py` | Read source files with line numbers for accurate citation ([read_files.py:2-6](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/read_files.py#L2-L6)) |
| Validation | `validate_docs_structure.py`, `validate_mermaid.py` | Validate documentation structure against TOC and Mermaid diagram syntax ([validate_docs_structure.py:2-10](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/validate_docs_structure.py#L2-L10)) |
| Summary Generation | `generate_summary.py` | Generate SUMMARY.md report with generation statistics ([generate_summary.py:2-9](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/generate_summary.py#L2-L9)) |

All scripts follow a consistent CLI pattern with `argparse` for argument handling and JSON output for structured data exchange between workflow phases.

Sources: [collect_context.py:2-17](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/collect_context.py#L2-L17), [read_files.py:2-20](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/read_files.py#L2-L20), [validate_docs_structure.py:2-28](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/validate_docs_structure.py#L2-L28), [generate_summary.py:2-25](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/generate_summary.py#L2-L25)
<!-- END:AUTOGEN deepwiki-skill_04_scripts_overview -->

---

<!-- BEGIN:AUTOGEN deepwiki-skill_04_scripts_context-collection -->
## Context Collection Scripts

This section covers the scripts that collect various types of context information for wiki generation.

### collect_context.py

The primary context collection script scans a repository and collects project structure and README content for initial wiki generation ([collect_context.py:2-6](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/collect_context.py#L2-L6)).

**Usage:**

```bash
python collect_context.py --repo-path /path/to/repo [options]
```

**Key Parameters:**

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--repo-path` | Yes | - | Repository path ([collect_context.py:12](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/collect_context.py#L12)) |
| `--max-depth` | No | 10 | Maximum scan depth ([collect_context.py:13](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/collect_context.py#L13)) |
| `--include` | No | - | Include patterns (repeatable) ([collect_context.py:14](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/collect_context.py#L14)) |
| `--exclude` | No | - | Exclude patterns (repeatable) ([collect_context.py:15](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/collect_context.py#L15)) |
| `--output` | No | stdout | Output file path ([collect_context.py:16](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/collect_context.py#L16)) |

The script implements budget allocation to manage output size, reserving 80% for structure and 20% for README content ([collect_context.py:34-36](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/collect_context.py#L34-L36)). It supports automatic depth reduction when output exceeds the budget limit ([collect_context.py:617-651](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/collect_context.py#L617-L651)).

The script detects programming languages from file extensions using a comprehensive mapping table ([collect_context.py:66-127](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/collect_context.py#L66-L127)).

### collect_sync_context.py

Compares TOC structure with existing documentation to determine what needs to be synchronized during incremental updates ([collect_sync_context.py:2-6](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/collect_sync_context.py#L2-L6)).

**Usage:**

```bash
python collect_sync_context.py --repo-path /path/to/repo --toc-file toc.yaml --doc-dir ./docs/wiki/
```

**Key Functions:**

The script extracts PAGE_ID markers from existing documentation using regex pattern matching ([collect_sync_context.py:28-32](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/collect_sync_context.py#L28-L32)) and identifies empty sections by checking the content between AUTOGEN markers ([collect_sync_context.py:41-65](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/collect_sync_context.py#L41-L65)).

The output includes lists of new pages, pages to update, and unchanged pages along with metadata about the synchronization state ([collect_sync_context.py:251-268](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/collect_sync_context.py#L251-L268)).

### collect_update_context.py

Analyzes git changes between commits to determine which documentation sections need regeneration for incremental updates ([collect_update_context.py:2-6](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/collect_update_context.py#L2-L6)).

**Key Parameters:**

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--repo-path` | Yes | - | Repository path |
| `--toc-file` | Yes | - | TOC YAML file path |
| `--doc-dir` | Yes | - | Documentation directory |
| `--target-commit` | No | HEAD | Target commit reference ([collect_update_context.py:16](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/collect_update_context.py#L16)) |
| `--include-diff` | No | false | Include line-numbered patch data ([collect_update_context.py:17](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/collect_update_context.py#L17)) |

The script converts patch data to a format with line numbers for easier reference ([collect_update_context.py:103-156](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/collect_update_context.py#L103-L156)).

### collect_git_diff.py

Collects git diff data between commits with optional line numbers and context for change analysis ([collect_git_diff.py:2-6](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/collect_git_diff.py#L2-L6)).

**Key Parameters:**

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--repo-path` | Yes | - | Repository path |
| `--base-ref` | No | origin/main | Base reference ([collect_git_diff.py:14](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/collect_git_diff.py#L14)) |
| `--head-ref` | No | HEAD | Head reference ([collect_git_diff.py:15](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/collect_git_diff.py#L15)) |
| `--include-uncommitted` | No | false | Include staged/unstaged changes ([collect_git_diff.py:16](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/collect_git_diff.py#L16)) |
| `--context` | No | 3 | Context lines for diff ([collect_git_diff.py:17](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/collect_git_diff.py#L17)) |

Sources: [collect_context.py:2-17](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/collect_context.py#L2-L17), [collect_sync_context.py:2-16](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/collect_sync_context.py#L2-L16), [collect_update_context.py:2-20](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/collect_update_context.py#L2-L20), [collect_git_diff.py:2-19](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/collect_git_diff.py#L2-L19)
<!-- END:AUTOGEN deepwiki-skill_04_scripts_context-collection -->

---

<!-- BEGIN:AUTOGEN deepwiki-skill_04_scripts_file-reading -->
## File Reading

The `read_files.py` script reads source files and adds line numbers for accurate citations in wiki documentation ([read_files.py:2-6](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/read_files.py#L2-L6)).

**Usage:**

```bash
python read_files.py --repo-path /path/to/repo --files '["file1.py", "src/**/*.cs"]'
```

**Key Parameters:**

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--repo-path` | Yes | - | Repository path ([read_files.py:319](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/read_files.py#L319)) |
| `--files` | Yes | - | JSON array of file paths or glob patterns ([read_files.py:323](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/read_files.py#L323)) |
| `--line-numbers` | No | true | Add line numbers ([read_files.py:327-329](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/read_files.py#L327-L329)) |
| `--max-size` | No | 1MB | Maximum file size in bytes ([read_files.py:339-342](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/read_files.py#L339-L342)) |

**Glob Pattern Support:**

The script supports glob patterns for flexible file selection ([read_files.py:30-68](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/read_files.py#L30-L68)):

| Pattern | Description |
|---------|-------------|
| `*` | Matches any characters except `/` |
| `**` | Matches any characters including `/` (recursive) |
| `?` | Matches a single character |

**Line Number Format:**

Lines appear with the format `{spaces}{line_num}{arrow}{content}` where `{arrow}` is the delimiter, making it easy to extract exact line numbers for citations ([read_files.py:238-241](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/read_files.py#L238-L241)).

**Language Detection:**

The script automatically detects programming languages from file extensions using a comprehensive mapping table ([read_files.py:72-87](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/read_files.py#L72-L87)).

**Binary File Detection:**

Files are checked for binary content by examining null bytes and attempting UTF-8 decoding ([read_files.py:120-151](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/read_files.py#L120-L151)).

Sources: [read_files.py:2-20](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/read_files.py#L2-L20), [read_files.py:179-248](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/read_files.py#L179-L248)
<!-- END:AUTOGEN deepwiki-skill_04_scripts_file-reading -->

---

<!-- BEGIN:AUTOGEN deepwiki-skill_04_scripts_validation -->
## Validation Scripts

This section covers the two validation scripts used to ensure documentation quality.

### validate_docs_structure.py

Validates wiki documentation structure against the TOC specification ([validate_docs_structure.py:2-10](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/validate_docs_structure.py#L2-L10)).

**Usage:**

```bash
python validate_docs_structure.py --doc-dir docs/wiki --toc-file docs/wiki/toc.yaml
```

**Validation Checks:**

| Check | Description |
|-------|-------------|
| PAGE_ID markers | Presence and correctness of page identifiers ([validate_docs_structure.py:106-118](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/validate_docs_structure.py#L106-L118)) |
| AUTOGEN markers | BEGIN/END pairs with no overlaps ([validate_docs_structure.py:155-248](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/scripts/validate_docs_structure.py#L155-L248)) |
| TOC alignment | All pages/sections defined in TOC exist ([validate_docs_structure.py:433-524](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/validate_docs_structure.py#L433-L524)) |
| Internal links | Valid markdown link targets ([validate_docs_structure.py:251-296](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/validate_docs_structure.py#L251-L296)) |
| Basic structure | H1 headings, file size checks ([validate_docs_structure.py:299-342](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/validate_docs_structure.py#L299-L342)) |

The script uses an `Issue` dataclass to represent validation problems with file, line, severity, category, message, and fix hint fields ([validate_docs_structure.py:46-63](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/validate_docs_structure.py#L46-L63)).

### validate_mermaid.py

Extracts and validates Mermaid diagram syntax using mermaid-cli (mmdc) ([validate_mermaid.py:2-7](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/validate_mermaid.py#L2-L7)).

**Usage:**

```bash
# Validate all diagrams in a directory
python validate_mermaid.py --input ./docs/wiki/ --invalid-only

# Validate a single file
python validate_mermaid.py --input diagram.mmd

# Validate code string directly
python validate_mermaid.py --code "graph TD\n    A-->B"
```

**Key Parameters:**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--input` | One of input/code/blocks | File (.mmd) or directory (scans .md files) ([validate_mermaid.py:689-691](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/validate_mermaid.py#L689-L691)) |
| `--code` | One of input/code/blocks | Mermaid code string ([validate_mermaid.py:693-695](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/validate_mermaid.py#L693-L695)) |
| `--invalid-only` | No | Only output invalid blocks ([validate_mermaid.py:717-719](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/validate_mermaid.py#L717-L719)) |
| `--extract-only` | No | Only extract blocks, skip validation ([validate_mermaid.py:720-722](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/validate_mermaid.py#L720-L722)) |

**Diagram Type Detection:**

The script detects diagram types (flowchart, sequence, class, state, er, gantt, pie, journey, gitgraph) from the first line of the code ([validate_mermaid.py:144-168](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/validate_mermaid.py#L144-L168)).

**Error Classification:**

Errors are classified into types for better diagnosis ([validate_mermaid.py:376-394](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/validate_mermaid.py#L376-L394)):

| Error Type | Description |
|------------|-------------|
| `lexical_error` | Unrecognized text or character issues |
| `syntax_error` | General syntax issues |
| `node_error` | Problems with node definitions |
| `edge_error` | Problems with arrows/edges |
| `graph_structure_error` | Issues with diagram structure |
| `cli_unavailable` | mmdc not installed |

The script provides fix hints based on error patterns to help users correct issues ([validate_mermaid.py:397-443](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/validate_mermaid.py#L397-L443)).

Sources: [validate_docs_structure.py:2-28](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/validate_docs_structure.py#L2-L28), [validate_mermaid.py:2-29](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/validate_mermaid.py#L2-L29)
<!-- END:AUTOGEN deepwiki-skill_04_scripts_validation -->

---

<!-- BEGIN:AUTOGEN deepwiki-skill_04_scripts_summary-generation -->
## Summary Generation

The `generate_summary.py` script creates a SUMMARY.md report that analyzes generated documentation and provides statistics on completion status ([generate_summary.py:2-9](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/generate_summary.py#L2-L9)).

**Usage:**

```bash
python generate_summary.py --doc-dir docs/wiki --toc-file docs/wiki/toc.yaml
```

**Key Parameters:**

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--doc-dir` | Yes | - | Directory containing generated .md docs ([generate_summary.py:421-424](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/generate_summary.py#L421-L424)) |
| `--toc-file` | Yes | - | Path to toc.yaml file ([generate_summary.py:425-428](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/generate_summary.py#L425-L428)) |
| `--structure-report` | No | - | Path to structure_validation.json ([generate_summary.py:429-431](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/generate_summary.py#L429-L431)) |
| `--mermaid-report` | No | - | Path to mermaid_invalid.json ([generate_summary.py:432-434](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/generate_summary.py#L432-L434)) |
| `--output` | No | `{doc_dir}/_reports/SUMMARY.md` | Output path for SUMMARY.md ([generate_summary.py:435-437](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/generate_summary.py#L435-L437)) |

**Report Contents:**

The summary report includes the following sections ([generate_summary.py:290-413](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/generate_summary.py#L290-L413)):

1. **Generation Status**: Overall completion metrics for pages, sections, citations, and diagrams
2. **Page Details**: Per-page breakdown with section counts, citations, and status indicators
3. **Source Coverage**: Lists covered and uncovered source files
4. **Issues**: Errors that must be fixed and warnings
5. **Recommendations**: Actionable suggestions for improvement

**Page Statistics:**

The script tracks statistics for each page using the `PageStats` dataclass ([generate_summary.py:44-63](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/generate_summary.py#L44-L63)):

| Field | Description |
|-------|-------------|
| `filename` | Output filename |
| `expected_sections` | Number of sections defined in TOC |
| `found_sections` | Number of AUTOGEN sections found |
| `citations` | Count of source citations |
| `diagrams` | Count of Mermaid diagrams |
| `has_page_id` | Whether PAGE_ID marker exists |

**Citation Extraction:**

Citations are extracted from markdown using pattern matching for formats like `[file.ext:N](url)` or `[file.ext:N-M](url)` ([generate_summary.py:134-145](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/generate_summary.py#L134-L145)).

Sources: [generate_summary.py:2-25](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/generate_summary.py#L2-L25), [generate_summary.py:173-287](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/scripts/generate_summary.py#L173-L287)
<!-- END:AUTOGEN deepwiki-skill_04_scripts_summary-generation -->

---
