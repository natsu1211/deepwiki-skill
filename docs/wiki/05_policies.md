<!-- PAGE_ID: deepwiki-skill_05_policies -->
<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [evidence_citation_policy.md:1-134](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/evidence_citation_policy.md#L1-L134)
- [mermaid_policy.md:1-428](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/mermaid_policy.md#L1-L428)
- [page_template.md:1-282](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/page_template.md#L1-L282)
- [validation_policy.md:1-262](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/validation_policy.md#L1-L262)
- [doc_update_policy.md:1-389](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/doc_update_policy.md#L1-L389)
- [toc_schema.md:1-238](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/toc_schema.md#L1-L238)

</details>

# Documentation Policies

> **Related Pages**: [[Workflow Phases|03_workflow-phases.md]], [[CI/CD Integration|06_cicd.md]]

---

<!-- BEGIN:AUTOGEN deepwiki-skill_05_policies_evidence-citation -->
## Evidence Citation Policy

This section describes the rules for evidence-based writing and source citation requirements in wiki documentation.

### Core Principles

The evidence citation policy establishes that every major claim must be backed by citations from actual source files ([evidence_citation_policy.md:5-13](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/evidence_citation_policy.md#L5-L13)). The key requirements are:

- Never guess or infer information
- Never make up line numbers
- Only describe functionality present in source code
- If information is missing, state it explicitly

### Citation URL Structure

Citations use a specific URL format that includes the repository base URL, commit hash, file path, and line numbers ([evidence_citation_policy.md:16-28](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/evidence_citation_policy.md#L16-L28)):

```
{repo_base_url}/{ref_commit_hash}/{file_path}#L{start}
{repo_base_url}/{ref_commit_hash}/{file_path}#L{start}-L{end}
```

| Component | Description |
|-----------|-------------|
| `repo_base_url` | Base URL without commit hash (e.g., `https://github.com/owner/repo/blob`) |
| `ref_commit_hash` | Git commit hash for permanent links |
| `file_path` | Relative path from repository root |
| `start` / `end` | Line number(s) for the citation |

### Link Format Rules

The display text for citations follows specific rules ([evidence_citation_policy.md:42-48](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/evidence_citation_policy.md#L42-L48)):

| Component | Rule | Example |
|-----------|------|---------|
| Filename | Use only the filename (no directory path) | `Button.tsx` not `src/components/Button.tsx` |
| Line numbers | Use actual numbers from file content | `:42` or `:42-50` |
| Separator | Use colon between filename and lines | `Button.tsx:42` |

### Citation Placement

Inline citations must be placed immediately after the claim and wrapped in parentheses ([evidence_citation_policy.md:54-66](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/evidence_citation_policy.md#L54-L66)). The citation must come before the period as part of the sentence. Additionally, each section should end with a summary of sources used.

For tables, citations should also be wrapped in parentheses within table cells ([evidence_citation_policy.md:77-86](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/evidence_citation_policy.md#L77-L86)).

### What NOT to Cite

Certain items do not require citations ([evidence_citation_policy.md:102-107](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/evidence_citation_policy.md#L102-L107)):

- General programming concepts
- Standard library functions
- Well-known patterns
- Your own explanations and summaries

Sources: [evidence_citation_policy.md:1-134](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/evidence_citation_policy.md#L1-L134)
<!-- END:AUTOGEN deepwiki-skill_05_policies_evidence-citation -->

---

<!-- BEGIN:AUTOGEN deepwiki-skill_05_policies_mermaid -->
## Mermaid Diagram Policy

This section describes the rules and best practices for creating Mermaid diagrams in wiki documentation.

### Supported Diagram Types

The mermaid policy defines six supported diagram types ([mermaid_policy.md:7-14](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/mermaid_policy.md#L7-L14)):

| Type | Use Case | Syntax |
|------|----------|--------|
| `flowchart` | Process flows, data flow, decision trees | `graph TD` |
| `sequence` | Interaction sequences, API calls | `sequenceDiagram` |
| `class` | Class relationships, inheritance | `classDiagram` |
| `state` | State machines, status transitions | `stateDiagram-v2` |
| `er` | Entity relationships, database schema | `erDiagram` |
| `gantt` | Project timelines | `gantt` |

### Critical Rules

#### Rule 1: Vertical Orientation

Always use `graph TD` (top-down), never `graph LR` (left-right) ([mermaid_policy.md:18-20](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/mermaid_policy.md#L18-L20)).

#### Rule 2: Quote All Node Text

All node text must be wrapped in double quotes to prevent parse errors ([mermaid_policy.md:22-48](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/mermaid_policy.md#L22-L48)). This applies to all node types:

- Rectangles: `A["text"]`
- Rounded: `B("text")`
- Circles: `C(("text"))`
- Diamonds: `D{"text"}`
- Hexagons: `E{{"text"}}`

#### Rule 3: Subgraph Names

Subgraph names must NOT contain parentheses or special characters ([mermaid_policy.md:49-72](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/mermaid_policy.md#L49-L72)). Use alphanumeric characters and underscores only.

#### Rule 4: Sequence Diagram Messages

The colon in sequence diagrams must be followed by content. When there is no meaningful message, use `;` as a placeholder ([mermaid_policy.md:74-92](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/mermaid_policy.md#L74-L92)).

#### Rule 5: No Shorthand Activation

Do NOT use shorthand activation syntax (`->>+`, `-->>-`). Instead, use explicit `activate` and `deactivate` statements ([mermaid_policy.md:94-115](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/mermaid_policy.md#L94-L115)).

#### Rule 6: No Source Citations in Diagrams

Never include source file citations inside Mermaid diagrams. Place citations outside the diagram in the documentation text ([mermaid_policy.md:117-133](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/mermaid_policy.md#L117-L133)).

### Validation Process

Mermaid diagrams are validated using the `validate_mermaid.py` script ([mermaid_policy.md:249-263](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/mermaid_policy.md#L249-L263)):

```bash
python3 validate_mermaid.py --input {doc_dir} --invalid-only --output _reports/mermaid_invalid.json
```

The validation output includes fields such as `is_valid`, `error_message`, `error_type`, `error_line`, and `fix_hint` ([mermaid_policy.md:265-287](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/mermaid_policy.md#L265-L287)).

### Error Types

| Type | Description |
|------|-------------|
| `lexical_error` | Unrecognized text or character issues |
| `syntax_error` | General syntax issues |
| `node_error` | Problems with node definitions |
| `edge_error` | Problems with arrows/edges |
| `graph_structure_error` | Issues with diagram structure |
| `style_error` | Problems with style declarations |

Sources: [mermaid_policy.md:1-428](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/mermaid_policy.md#L1-L428)
<!-- END:AUTOGEN deepwiki-skill_05_policies_mermaid -->

---

<!-- BEGIN:AUTOGEN deepwiki-skill_05_policies_page-template -->
## Page Template

This section describes the page structure and marker conventions for wiki pages.

### Page Structure

Every wiki page must follow a specific structure with required markers ([page_template.md:7-46](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/page_template.md#L7-L46)):

1. `PAGE_ID` marker at the very beginning
2. Collapsible source files list
3. Page title (H1)
4. Related pages links
5. Horizontal rule separator
6. AUTOGEN-marked sections with content

### PAGE_ID Marker

The PAGE_ID marker uniquely identifies the page for incremental updates ([page_template.md:50-67](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/page_template.md#L50-L67)):

```html
<!-- PAGE_ID: {page_id} -->
```

Rules:
- Must be at the very beginning of the file
- page_id must match the ID in toc.yaml
- One PAGE_ID per file

### AUTOGEN Markers

AUTOGEN markers define auto-generated content boundaries for safe updates ([page_template.md:69-97](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/page_template.md#L69-L97)):

```
BEGIN:AUTOGEN {section_id}
{generated content}
END:AUTOGEN {section_id}
```

Rules:
- Every autogen section must have both BEGIN and END markers
- section_id must match the ID in toc.yaml
- Content outside markers is preserved during updates
- Include a `---` separator after each section

### Heading Levels

The template defines heading levels based on section depth ([page_template.md:130-138](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/page_template.md#L130-L138)):

| Section Depth | Heading | Markdown |
|---------------|---------|----------|
| Page title | H1 | `#` |
| Top-level section | H2 | `##` |
| Nested level 1 | H3 | `###` |
| Nested level 2 | H4 | `####` |
| Nested level 3 | H5 | `#####` |

### Section Content Guidelines

Each section should start with the heading and a brief 1-2 sentence introduction. The body should include explanatory text with source citations, code examples if relevant, tables for structured data, and diagrams if needed. Sections end with a source citations summary and the END:AUTOGEN marker followed by a horizontal rule ([page_template.md:165-199](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/page_template.md#L165-L199)).

Sources: [page_template.md:1-282](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/page_template.md#L1-L282)
<!-- END:AUTOGEN deepwiki-skill_05_policies_page-template -->

---

<!-- BEGIN:AUTOGEN deepwiki-skill_05_policies_validation -->
## Validation Policy

This section describes the validation rules for wiki documents during Phase 4.

### Overview

After all documents are generated, two types of validation are performed ([validation_policy.md:7-9](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/validation_policy.md#L7-L9)):

1. **Mermaid Diagram Validation** - Ensure all diagrams compile
2. **Document Structure Validation** - Ensure markers are correct

### PAGE_ID Validation

Every wiki page must have a PAGE_ID marker at the beginning ([validation_policy.md:13-35](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/validation_policy.md#L13-L35)):

| Check | Action if Failed |
|-------|------------------|
| PAGE_ID marker exists at file start | Add the marker |
| page_id matches TOC definition | Fix to match TOC |
| Only one PAGE_ID per file | Remove duplicates |

### AUTOGEN Marker Validation

Every auto-generated section must have matching BEGIN and END markers ([validation_policy.md:37-58](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/validation_policy.md#L37-L58)):

| Check | Action if Failed |
|-------|------------------|
| BEGIN marker exists for each `autogen: true` section | Add before section content |
| END marker exists for each `autogen: true` section | Add after section content |
| BEGIN section_id matches END section_id | Correct the mismatched ID |
| section_id matches TOC definition | Update to match TOC |
| No orphaned markers (BEGIN without END) | Add missing END or remove orphan |
| No duplicate markers (same ID multiple times) | Remove duplicates |
| No extra markers not in TOC | Remove extra markers |

### Marker Integrity Checks

The validation policy defines several marker integrity issues ([validation_policy.md:60-119](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/validation_policy.md#L60-L119)):

- **Orphaned Markers**: BEGIN without matching END, or vice versa
- **Duplicate Markers**: Same section_id appearing multiple times
- **Mismatched IDs**: BEGIN and END have different section_ids
- **Extra Markers**: AUTOGEN markers not defined in TOC

### Validation Workflow

The validation workflow uses two main tools ([validation_policy.md:121-198](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/validation_policy.md#L121-L198)):

1. **validate_docs_structure** - Validates document structure and markers
2. **get_invalid_mermaid_blocks** - Validates Mermaid diagrams

Issue categories include: `page_id`, `autogen`, `structure`, `link`, and `toc`.

### Fix Actions

Based on validation results, issues are fixed automatically ([validation_policy.md:200-216](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/validation_policy.md#L200-L216)):

| Category | Issue Type | Auto-Fix Action |
|----------|------------|-----------------|
| `page_id` | Missing marker | Insert at file start |
| `page_id` | Wrong ID | Replace with correct ID |
| `autogen` | Missing BEGIN | Insert before section heading |
| `autogen` | Missing END | Insert after section content |
| `autogen` | Mismatched ID | Update END to match BEGIN |
| `autogen` | Orphaned marker | Remove or add matching marker |
| `autogen` | Extra marker | Remove marker |
| `structure` | Missing H1 | Add H1 heading |
| `link` | Broken link | Fix or remove link |
| mermaid | Syntax error | Rewrite diagram |

Sources: [validation_policy.md:1-262](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/validation_policy.md#L1-L262)
<!-- END:AUTOGEN deepwiki-skill_05_policies_validation -->

---

<!-- BEGIN:AUTOGEN deepwiki-skill_05_policies_toc-schema -->
## TOC Schema

This section describes the YAML schema specification for toc.yaml files.

### Schema Structure

The TOC schema defines the structure for wiki documentation organization ([toc_schema.md:7-44](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/toc_schema.md#L7-L44)):

```yaml
project:
  name: string              # Required: Project name
  description: string       # Required: Brief project description
  repo_base_url: string     # Optional: Base web URL without commit hash
  ref_commit_hash: string   # Required: Git commit hash for permanent links
  updated_at: string        # Optional: Last update date (YYYY-MM-DD)

pages:                      # Required: Array of page definitions
  - id: string              # Required: Unique page identifier
    title: string           # Required: Page title
    filename: string        # Required: Output filename
    description: string     # Optional: Brief page description
    source_files: [string]  # Required: Page-level source files
    sections: [...]         # Required: Array of section definitions
    related_pages: [string] # Optional: Related page IDs
```

### Project Section Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Project name for display |
| `description` | string | Yes | Brief 1-2 sentence description |
| `repo_base_url` | string | No | Base URL without commit hash |
| `ref_commit_hash` | string | Yes | Current commit hash |
| `updated_at` | string | No | Date in YYYY-MM-DD format |

### Page ID Format

Page IDs must be globally unique across all wiki pages ([toc_schema.md:58-75](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/toc_schema.md#L58-L75)):

```
{repo_name}_{number}_{page-name}
```

Rules:
- Use repository name as prefix
- Include zero-padded number for ordering
- Use kebab-case for page name
- No spaces or special characters

### Section ID Format

Section IDs inherit from page ID ([toc_schema.md:77-93](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/toc_schema.md#L77-L93)):

```
{page_id}_{section-name}
```

For nested sections:
```
{parent_section_id}_{subsection-name}
```

### Source Files Patterns

Both explicit paths and glob patterns are supported ([toc_schema.md:95-106](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/toc_schema.md#L95-L106)):

| Pattern | Description |
|---------|-------------|
| `src/main.py` | Exact file path |
| `src/*.py` | All Python files in src/ |
| `src/**/*.py` | All Python files recursively |
| `src/` | All files in src/ directory |
| `docs/api/*.md` | All markdown in docs/api/ |

### Diagram Types

| Type | Use Case |
|------|----------|
| `flowchart` | Process flows, decision trees, data flow |
| `sequence` | Interaction sequences, API calls |
| `class` | Class relationships, inheritance |
| `state` | State machines, status transitions |
| `er` | Entity relationships, database schema |
| `gantt` | Project timelines (rarely used) |

### Validation Rules

The schema enforces several validation rules ([toc_schema.md:204-211](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/toc_schema.md#L204-L211)):

1. **ID Uniqueness**: All page and section IDs must be unique
2. **Required Fields**: All required fields must be present
3. **File Extension**: Filename must end with `.md`
4. **Diagram Types**: Must be from allowed values when specified
5. **Section Depth**: Recommend max 3 levels of nesting
6. **Source Files**: Each page should have at least 1 source file

### Page Count Guidelines

| Project Size | Recommended Pages |
|--------------|-------------------|
| Small (< 10 files) | 3-5 pages |
| Medium (10-50 files) | 5-8 pages |
| Large (50-200 files) | 8-12 pages |
| Very Large (> 200 files) | 10-15 pages |

Sources: [toc_schema.md:1-238](https://github.com/natsu1211/deepwiki-skill/blob/38f3e4f642cfbc9511d4cc1421b2c1ded9febd97/skills/wiki/references/toc_schema.md#L1-L238)
<!-- END:AUTOGEN deepwiki-skill_05_policies_toc-schema -->

---
