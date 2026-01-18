<!-- PAGE_ID: deepwiki-skill_03_workflow-phases -->
<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [repo-scan.md:1-94](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/repo-scan.md#L1-L94)
- [toc-design.md:1-116](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/toc-design.md#L1-L116)
- [doc-write.md:1-127](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/doc-write.md#L1-L127)
- [validate-docs.md:1-202](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/validate-docs.md#L1-L202)
- [doc-summary.md:1-127](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/doc-summary.md#L1-L127)
- [incremental-sync.md:1-162](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/incremental-sync.md#L1-L162)

</details>

# Workflow Phases

> **Related Pages**: [[Architecture|02_architecture.md]], [[Python Scripts|04_python-scripts.md]]

---

<!-- BEGIN:AUTOGEN deepwiki-skill_03_workflow-phases_repo-scan -->
## Phase 1: Repository Scan

The repository scan phase collects project context needed for TOC design and documentation generation ([repo-scan.md:3-5](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/repo-scan.md#L3-L5)).

### Inputs and Outputs

**Input Parameters**:

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `repo_path` | Yes | - | Absolute path to the target repository (git repo root preferred) ([repo-scan.md:11](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/repo-scan.md#L11)) |
| `output_dir` | No | `docs/wiki` | Documentation output directory ([repo-scan.md:12](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/repo-scan.md#L12)) |
| `include` | No | - | Include patterns (forwarded to script) ([repo-scan.md:13](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/repo-scan.md#L13)) |
| `exclude` | No | - | Exclude patterns (forwarded to script) ([repo-scan.md:14](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/repo-scan.md#L14)) |
| `max_depth` | No | `10` | Max scan depth ([repo-scan.md:15](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/repo-scan.md#L15)) |

**Output**:

| Path | Description |
|------|-------------|
| `{output_dir}/_context/context_pack.json` | Project context JSON for `toc-design` ([repo-scan.md:21](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/repo-scan.md#L21)) |

### Script: collect_context.py

The phase uses `collect_context.py` to collect project context ([repo-scan.md:25](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/repo-scan.md#L25)).

```bash
python3 /scripts/collect_context.py \
  --repo-path "{repo_path}" \
  --max-depth 10 \
  --output "{output_dir}/_context/context_pack.json"
```

The output JSON structure contains ([repo-scan.md:45-67](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/repo-scan.md#L45-L67)):
- **structure**: Directory tree, file counts, total size, and detected languages
- **readme**: README content if available
- **metadata**: Repository path and truncation flags

### Workflow Steps

1. **Validate repository**: Verify `repo_path` exists and is a directory, check if it is a git repository ([repo-scan.md:72-74](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/repo-scan.md#L72-L74))

2. **Collect git metadata**: Run git commands to get repo root, remote URL, and commit hash ([repo-scan.md:76-81](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/repo-scan.md#L76-L81))

3. **Run context collection**: Execute the `collect_context.py` script ([repo-scan.md:83-88](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/repo-scan.md#L83-L88))

### Validation Criteria

- `{output_dir}/_context/` directory exists
- `{output_dir}/_context/context_pack.json` is valid JSON ([repo-scan.md:91-94](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/repo-scan.md#L91-L94))

Sources: [repo-scan.md:1-94](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/repo-scan.md#L1-L94)
<!-- END:AUTOGEN deepwiki-skill_03_workflow-phases_repo-scan -->

---

<!-- BEGIN:AUTOGEN deepwiki-skill_03_workflow-phases_toc-design -->
## Phase 2: TOC Design

The TOC design phase analyzes the project context and creates a logical wiki structure in a `toc.yaml` file ([toc-design.md:3-5](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/toc-design.md#L3-L5)).

### Inputs and Outputs

**Input Parameters**:

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `repo_path` | Yes | - | Absolute repository path ([toc-design.md:11](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/toc-design.md#L11)) |
| `output_dir` | No | `docs/wiki` | Documentation output directory ([toc-design.md:12](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/toc-design.md#L12)) |
| `context_pack` | No | `{output_dir}/_context/context_pack.json` | Context JSON from `repo-scan` ([toc-design.md:13](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/toc-design.md#L13)) |
| `language` | No | `en-US` | Output language/locale ([toc-design.md:14](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/toc-design.md#L14)) |

**Output**:

| Path | Description |
|------|-------------|
| `{output_dir}/toc.yaml` | TOC definition following schema ([toc-design.md:20](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/toc-design.md#L20)) |

### Workflow: Generate Wiki Structure

The TOC design workflow involves a deep analysis of the codebase ([toc-design.md:46-72](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/toc-design.md#L46-L72)):

1. **Review Context**: Examine the project structure to identify main source directories and read README to understand project purpose

2. **Deep Dive into Code**: Identify representative files from main source directories, use `/scripts/read_files.py` to read these files, understand classes/modules and their organization

3. **Identify Logical Groupings**: Group related functionality based on actual code content (e.g., `Engine.cs`, `Renderer.cs`, `Physics.cs` -> "Core Systems" page)

4. **Design Wiki Structure**: Create pages based on logical groupings, map actual source files to each page, design sections covering different aspects

5. **Write toc.yaml**: Generate following the schema from `/references/toc_schema.md`

### Structure Design Principles

The phase provides guidelines for understanding project types and mapping them to appropriate documentation structures ([toc-design.md:76-97](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/toc-design.md#L76-L97)):

| Project Type | Recommended Sections |
|--------------|----------------------|
| Web application | Frontend, Backend, API, Deployment |
| Library/Framework | Architecture, Core APIs, Usage Guide, Extension |
| Data pipeline | Data Sources, Processing, Storage, Orchestration |
| Unity game | Gameplay, Systems, UI, Assets, Performance |
| DevOps tool | Configuration, Workflow, Integration, Monitoring |

**Page Count Guidelines** ([toc-design.md:99-105](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/toc-design.md#L99-L105)):

| Project Size | Files | Recommended Pages |
|--------------|-------|-------------------|
| Small | < 10 | 3-5 pages |
| Medium | 10-50 | 5-8 pages |
| Large | 50-200 | 8-12 pages |
| Very Large | > 200 | 10-15 pages |

### Validation Criteria

- TOC file generated successfully with all fields having valid values
- All page/section IDs are unique
- IDs use kebab-case with no special characters
- Each page has at least 1 `source_files` entry
- Nesting depth is at most 3 levels ([toc-design.md:110-116](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/toc-design.md#L110-L116))

Sources: [toc-design.md:1-116](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/toc-design.md#L1-L116)
<!-- END:AUTOGEN deepwiki-skill_03_workflow-phases_toc-design -->

---

<!-- BEGIN:AUTOGEN deepwiki-skill_03_workflow-phases_doc-write -->
## Phase 3: Document Writing

The document writing phase generates evidence-based wiki pages from the `toc.yaml` file with stable PAGE_ID markers, AUTOGEN markers for all generated sections, strict source citations with line numbers, and Mermaid diagrams where requested ([doc-write.md:3-9](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/doc-write.md#L3-L9)).

### Script: read_files.py

The phase uses `read_files.py` to read source files with line numbers for accurate citations ([doc-write.md:19-21](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/doc-write.md#L19-L21)).

```bash
python3 /scripts/read_files.py \
  --repo-path "{repo_path}" \
  --files '["path/to/file1", "src/**/*.cs"]' \
  --line-numbers
```

**Parameters** ([doc-write.md:31-39](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/doc-write.md#L31-L39)):

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--repo-path` | Yes | - | Absolute repository root path |
| `--files` | Yes | - | JSON array of file paths or glob patterns |
| `--line-numbers` | No | `true` | Include line numbers for citations |
| `--max-size` | No | `1048576` | Max bytes per file (1MB default) |
| `--output` | No | stdout | Output JSON path |

The script supports glob patterns: `*` matches characters except `/`, `**` matches recursively, `?` matches a single character ([doc-write.md:41-45](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/doc-write.md#L41-L45)).

### Workflow: Page Generation

For each page in `toc.yaml`, the phase follows this process ([doc-write.md:67-127](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/doc-write.md#L67-L127)):

**Step 1: Parse TOC Structure**
- Read page definition from YAML
- Extract page-level source_files (shared by all sections)
- Extract all sections with their titles, autogen flags, and optional source_files

**Step 2: Collect Evidence for Each Section**
- Merge page-level and section-level source files
- Resolve glob patterns and collect files using `read_files.py`
- Process nested sections recursively ([doc-write.md:77-114](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/doc-write.md#L77-L114))

**Step 3: Generate Page Content**
- Add source citations following the evidence citation policy
- Generate Mermaid diagrams where `diagrams_needed: true`
- Combine all sections following the page template
- Output Markdown files in `{output_dir}/` ([doc-write.md:122-127](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/doc-write.md#L122-L127))

### Reference Policies

The phase references several policies for content generation ([doc-write.md:11-15](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/doc-write.md#L11-L15)):
- `toc_schema.md`: Schema of toc file for parsing
- `page_template.md`: Format of wiki page to generate
- `evidence_citation_policy.md`: Citation requirements
- `mermaid_policy.md`: Mermaid diagram requirements

Sources: [doc-write.md:1-127](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/doc-write.md#L1-L127)
<!-- END:AUTOGEN deepwiki-skill_03_workflow-phases_doc-write -->

---

<!-- BEGIN:AUTOGEN deepwiki-skill_03_workflow-phases_validate-docs -->
## Phase 4: Document Validation

The validation phase verifies the generated documentation and applies safe fixes, ensuring Mermaid diagrams compile correctly and document structure is consistent with PAGE_ID markers and AUTOGEN markers ([validate-docs.md:3-8](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/validate-docs.md#L3-L8)).

### Inputs and Outputs

**Input Parameters**:

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `doc_dir` | No | `{output_dir}` | Directory containing generated `.md` docs ([validate-docs.md:13](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/validate-docs.md#L13)) |
| `output_dir` | No | `docs/wiki` | Base output dir for reports ([validate-docs.md:14](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/validate-docs.md#L14)) |
| `toc_file` | No | `{output_dir}/toc.yaml` | TOC file for validation ([validate-docs.md:15](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/validate-docs.md#L15)) |
| `repo_path` | No | `.` | Repository root path ([validate-docs.md:16](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/validate-docs.md#L16)) |

**Outputs**:

| Path | Description |
|------|-------------|
| `{output_dir}/_reports/mermaid_invalid.json` | Invalid Mermaid blocks report ([validate-docs.md:22](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/validate-docs.md#L22)) |
| `{output_dir}/_reports/structure_validation.json` | Document structure validation report ([validate-docs.md:23](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/validate-docs.md#L23)) |
| `{doc_dir}/*.md` | In-place fixes for Mermaid blocks and structural markers ([validate-docs.md:24](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/validate-docs.md#L24)) |

### Script: validate_docs_structure.py

Validates document structure against TOC specification including PAGE_ID markers, AUTOGEN markers, and internal links ([validate-docs.md:28-30](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/validate-docs.md#L28-L30)).

```bash
python scripts/validate_docs_structure.py \
    --doc-dir "{doc_dir}" \
    --toc-file "{toc_file}"
```

**Issue Categories** ([validate-docs.md:75-84](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/validate-docs.md#L75-L84)):

| Category | Description |
|----------|-------------|
| `page_id` | PAGE_ID marker missing or incorrect |
| `autogen` | AUTOGEN marker issues (missing, mismatched, orphaned) |
| `structure` | Basic structure issues (H1 headings, file size) |
| `link` | Internal link issues (broken or undefined targets) |
| `toc` | TOC alignment issues (missing pages, extra files) |

### Script: validate_mermaid.py

Extracts and validates Mermaid diagrams using the Mermaid CLI (`mmdc`) ([validate-docs.md:85-87](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/validate-docs.md#L85-L87)).

```bash
python3 scripts/validate_mermaid.py \
    --input "{doc_dir}" \
    --invalid-only
```

**Error Types** ([validate-docs.md:139-149](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/validate-docs.md#L139-L149)):

| Type | Description | Common Fix |
|------|-------------|------------|
| `lexical_error` | Unrecognized text/characters | Quote node text with special characters |
| `syntax_error` | General syntax issues | Check diagram type and arrow syntax |
| `node_error` | Node definition problems | Balance brackets, quote labels |
| `edge_error` | Arrow/edge problems | Use valid arrows (-->, ---) |
| `cli_unavailable` | mmdc not installed | Install @mermaid-js/mermaid-cli |
| `timeout` | Validation timeout | Simplify diagram |

### Workflow

**Mermaid Diagram Validation** ([validate-docs.md:152-171](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/validate-docs.md#L152-L171)):
1. Run `validate_mermaid.py` to find invalid diagrams
2. If Mermaid CLI is unavailable, record the limitation and leave diagrams unchanged
3. Fix each invalid diagram (max 3 attempts per diagram)
4. If still invalid after 3 attempts, comment out the diagram block with a TODO

**Document Structure Validation** ([validate-docs.md:173-197](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/validate-docs.md#L173-L197)):
1. Run `validate_docs_structure.py` to check structure
2. Fix issues based on `fix_hint`: add missing PAGE_ID markers, fix AUTOGEN markers
3. Re-run to confirm all errors are fixed

**Safe auto-fixes allowed** ([validate-docs.md:199-202](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/validate-docs.md#L199-L202)):
- Add missing PAGE_ID/AUTOGEN markers
- Fix mismatched section_id to match TOC
- Do NOT rewrite page content

Sources: [validate-docs.md:1-202](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/validate-docs.md#L1-L202)
<!-- END:AUTOGEN deepwiki-skill_03_workflow-phases_validate-docs -->

---

<!-- BEGIN:AUTOGEN deepwiki-skill_03_workflow-phases_doc-summary -->
## Phase 5: Summary Generation

The summary generation phase creates a `SUMMARY.md` report containing generation status, citation statistics and source coverage, diagram count summary, and issues from validation reports ([doc-summary.md:3-9](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/doc-summary.md#L3-L9)).

### Script: generate_summary.py

Generates the SUMMARY.md report by analyzing documentation and validation results ([doc-summary.md:13-15](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/doc-summary.md#L13-L15)).

```bash
python3 /scripts/generate_summary.py \
  --doc-dir "{doc_dir}" \
  --toc-file "{toc_file}" \
  --output "{output_dir}/_reports/SUMMARY.md"
```

**Parameters** ([doc-summary.md:25-33](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/doc-summary.md#L25-L33)):

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--doc-dir` | Yes | - | Directory containing generated .md docs |
| `--toc-file` | Yes | - | Path to toc.yaml file |
| `--structure-report` | No | `{doc_dir}/_reports/structure_validation.json` | Structure validation report (auto-detected) |
| `--mermaid-report` | No | `{doc_dir}/_reports/mermaid_invalid.json` | Mermaid validation report (auto-detected) |
| `--output` | No | `{doc_dir}/_reports/SUMMARY.md` | Output path for SUMMARY.md |

### Output Report Structure

The script generates a markdown report with these sections ([doc-summary.md:35-82](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/doc-summary.md#L35-L82)):

- **Generation Status**: Overall completion status with metrics table
- **Page Details**: Per-page section counts, citations, diagrams, and status
- **Source Coverage**: Lists covered and uncovered source files
- **Issues**: Errors, warnings, and recommendations

### Workflow

The script automatically performs these steps ([doc-summary.md:97-104](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/doc-summary.md#L97-L104)):
1. Parses `toc.yaml` to enumerate expected pages and sections
2. Scans generated docs to check completion status
3. Extracts and counts citations from each page
4. Counts Mermaid diagrams in each page
5. Analyzes source file coverage (cited vs uncited)
6. Reads validation reports (if present) to include errors/warnings
7. Generates the SUMMARY.md report

### Status Indicators

| Status | Meaning |
|--------|---------|
| Complete | All pages/sections generated, no errors ([doc-summary.md:118](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/doc-summary.md#L118)) |
| Incomplete | Some sections missing or has warnings ([doc-summary.md:119](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/doc-summary.md#L119)) |
| Has Errors | Validation errors present ([doc-summary.md:120](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/doc-summary.md#L120)) |

Sources: [doc-summary.md:1-127](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/doc-summary.md#L1-L127)
<!-- END:AUTOGEN deepwiki-skill_03_workflow-phases_doc-summary -->

---

<!-- BEGIN:AUTOGEN deepwiki-skill_03_workflow-phases_incremental-sync -->
## Phase 6: Incremental Sync

The incremental sync phase collects context needed to update existing documentation safely after changes, consisting of two sub-phases: detecting TOC structure changes (Phase A) and detecting source code changes relevant to TOC mappings (Phase B) ([incremental-sync.md:3-8](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/incremental-sync.md#L3-L8)).

This phase does not rewrite docs; it produces change context that `doc-write` uses to regenerate only affected pages/sections ([incremental-sync.md:9](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/incremental-sync.md#L9)).

### Inputs and Outputs

**Input Parameters**:

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `repo_path` | Yes | - | Absolute repository path ([incremental-sync.md:15](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/incremental-sync.md#L15)) |
| `output_dir` | No | `docs/wiki` | Documentation output directory ([incremental-sync.md:16](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/incremental-sync.md#L16)) |
| `doc_dir` | No | `{output_dir}` | Documentation directory containing existing `.md` ([incremental-sync.md:17](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/incremental-sync.md#L17)) |
| `toc_file` | No | `{output_dir}/toc.yaml` | Existing TOC ([incremental-sync.md:18](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/incremental-sync.md#L18)) |
| `target_commit` | No | `HEAD` | Target commit for change detection ([incremental-sync.md:19](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/incremental-sync.md#L19)) |
| `include_diff` | No | `false` | Whether to include patch data ([incremental-sync.md:20](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/incremental-sync.md#L20)) |

**Outputs**:

| Path | Description |
|------|-------------|
| `{output_dir}/_context/sync_context.json` | TOC sync result (Phase A) ([incremental-sync.md:27](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/incremental-sync.md#L27)) |
| `{output_dir}/_context/update_context.json` | Source update context (Phase B) ([incremental-sync.md:28](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/incremental-sync.md#L28)) |

### Phase A: collect_sync_context.py

Detects structural differences between `toc.yaml` and existing documentation files ([incremental-sync.md:36-38](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/incremental-sync.md#L36-L38)).

```bash
python3 /scripts/collect_sync_context.py \
  --repo-path "{repo_path}" \
  --toc-file "{toc_file}" \
  --doc-dir "{doc_dir}" \
  --output "{output_dir}/_context/sync_context.json"
```

**Output JSON Structure** ([incremental-sync.md:58-71](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/incremental-sync.md#L58-L71)):
- `status`: `sync_needed`, `up_to_date`, or `full_rebuild_needed`
- `changes`: Lists added/removed/modified pages and sections
- `recommendation`: Action guidance

### Phase B: collect_update_context.py

Detects source code changes and maps them to affected wiki pages/sections ([incremental-sync.md:73-75](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/incremental-sync.md#L73-L75)).

```bash
python3 /scripts/collect_update_context.py \
  --repo-path "{repo_path}" \
  --toc-file "{toc_file}" \
  --doc-dir "{doc_dir}" \
  --target-commit "{target_commit}" \
  --output "{output_dir}/_context/update_context.json"
```

**Output JSON Structure** ([incremental-sync.md:100-121](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/incremental-sync.md#L100-L121)):
- `base_commit` and `target_commit`: Commit range analyzed
- `affected_pages`: List of pages requiring updates with affected sections and changed files
- `unaffected_pages`: List of pages not requiring updates

### Optional: get_section_update_diff.py

Gets focused diffs for a specific set of files, useful for detailed section updates ([incremental-sync.md:123-125](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/incremental-sync.md#L123-L125)).

### Workflow

1. Run Phase A (`collect_sync_context.py`): If it indicates TOC drift requiring a full rebuild, stop and recommend rerunning full generation ([incremental-sync.md:151-152](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/incremental-sync.md#L151-L152))

2. Run Phase B (`collect_update_context.py`): Map code changes to pages/sections ([incremental-sync.md:153](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/incremental-sync.md#L153))

3. Hand off to `doc-write`: Regenerate only affected pages/sections, do not touch manual sections or content outside AUTOGEN markers ([incremental-sync.md:154-156](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/incremental-sync.md#L154-L156))

### Validation Criteria

- `{output_dir}/_context/sync_context.json` exists and is valid JSON
- `{output_dir}/_context/update_context.json` exists and is valid JSON
- Each output explicitly lists changes or states "no changes" ([incremental-sync.md:160-162](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/incremental-sync.md#L160-L162))

Sources: [incremental-sync.md:1-162](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/workflow/incremental-sync.md#L1-L162)
<!-- END:AUTOGEN deepwiki-skill_03_workflow-phases_incremental-sync -->

---
