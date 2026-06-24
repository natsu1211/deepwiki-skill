# Phase: doc-write (Phase 3)

## Goal

Generate evidence-based wiki pages from `{toc_file}` with:
- stable PAGE_ID markers
- AUTOGEN markers for all generated sections
- strict source citations with line numbers
- Mermaid diagrams where requested by the TOC

## References
- `../references/toc_schema.md`: schema of toc file for parsing
- `../references/page_template.md`: format of wiki page you shoud generate 
- `../references/evidence_citation_policy.md`: citation requirement for generating wiki page
- `../references/mermaid_policy.md`: mermaid requirement for generating wiki page

## Scripts

### `read_files.py`

Use this script to read source files with line numbers for accurate citations. Never use ad-hoc file reads if citation is needed.

**Usage**:
```bash
python3 /scripts/read_files.py \
  --repo-path "{repo_path}" \
  --files '["path/to/file1", "src/**/*.cs"]' \
  --line-numbers
```

**Parameters**:

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--repo-path` | Yes | - | Absolute repository root path |
| `--files` | Yes | - | JSON array of file paths or glob patterns (e.g., `["src/**/*.cs"]`) |
| `--line-numbers` | No | `true` | Include line numbers for citations |
| `--max-size` | No | `1048576` | Max bytes per file (1MB default) |
| `--output` | No | stdout | Output JSON path |

**Glob Pattern Support**:
- `*` matches any characters except `/`
- `**` matches any characters including `/` (recursive)
- `?` matches a single character
- Example: `src/**/*.cs` matches all `.cs` files under `src/` recursively

**Output Format**:
```json
{
  "files": [
    {
      "path": "src/main.ts",
      "content": "     1→import { App } from './app';\n     2→...",
      "line_count": 150,
      "size": 4096
    }
  ],
  "metadata": {
    "total_files": 1,
    "total_size": 4096
  }
}
```

**Line Number Format**: Lines appear as `{spaces}{line_num}→{content}` where `→` is the delimiter.

## Workflow

For each page in toc.yaml, generate comprehensive Markdown documentation using project context and on-demand file loading.

**For each page:**
1. Parse TOC Structure and read page sections:
   - Read page definition from YAML
   - Extract page-level source_files (if defined)
   - Extract all sections with their titles, autogen flags, and optional source_files

2. Collect Evidence for each section (recursively):
Pseudo Code:
```
function process_page(page):
    # Get page-level source files (shared by all sections)
    page_source_files = page.get('source_files', [])

    for each section in page.sections:
        process_section(section, page_source_files, heading_level=2)

function process_section(section, page_source_files, heading_level):
    if section.autogen == true:
        # Merge page-level and section-level source files
        section_source_files = section.get('source_files', [])
        all_source_files = page_source_files + section_source_files

        # Resolve glob patterns and collect files
        resolved_paths = resolve_glob_patterns(all_source_files, repo_path)

        # Collect files for this section
        # This works for ALL file types: source code, dependencies, etc.
        section_files = read_files(
            repo_path=repo_path,
            file_paths=resolved_paths,
            include_line_numbers=True,
            max_file_size=100000
        )

        # **Note**:
        # source_files are the PRIMARY reference files. If you find that
        # understanding the code requires additional context (e.g., base classes,
        # interfaces, or referenced types), you MAY use read_files 
        # to read additional source files as needed.

    # Process nested sections recursively (pass page_source_files down)
    if section.sections exists:
        for each subsection in section.sections:
            process_section(subsection, page_source_files, heading_level + 1)
```

Generate section content based on the source files read:
- Add source citations strictly following `/references/evidence_citation_policy.md`
- Generate mermaid diagrams where `diagrams_needed: true`
- Repeat for nested sections

3. Generate Page Content

Combine all sections into the final page:
- Output format should strictly follow `/references/page_template.md`
- Ensure each section cites from its specific `source_files`
- Output Markdown files in `{output_dir}/`