<!-- PAGE_ID: deepwiki-skill_05_policies -->
<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [evidence_citation_policy.md:1-134](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/evidence_citation_policy.md#L1-L134)
- [mermaid_policy.md:1-428](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/mermaid_policy.md#L1-L428)
- [validation_policy.md:1-262](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/validation_policy.md#L1-L262)
- [doc_update_policy.md:1-389](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/doc_update_policy.md#L1-L389)
- [page_template.md:1-282](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/page_template.md#L1-L282)
- [toc_schema.md:1-238](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/toc_schema.md#L1-L238)

</details>

# Reference Policies

> **Related Pages**: [[Workflow Phases|03_workflow.md]], [[Python Scripts|04_scripts.md]]

---

<!-- BEGIN:AUTOGEN deepwiki-skill_05_policies_evidence-citation -->
## Evidence Citation Policy

This section describes the requirements for source code citations and line references in generated wiki documentation.

The evidence citation policy establishes that every major claim in the documentation must be backed by citations from actual source files ([evidence_citation_policy.md:7-8](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/evidence_citation_policy.md#L7-L8)). The policy emphasizes never guessing or inferring information, never making up line numbers, and only describing functionality present in source code ([evidence_citation_policy.md:9-12](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/evidence_citation_policy.md#L9-L12)).

### Citation URL Structure

Citations follow a specific URL format that includes the repository base URL, commit hash, file path, and line numbers ([evidence_citation_policy.md:18-21](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/evidence_citation_policy.md#L18-L21)):

```
{repo_base_url}/{ref_commit_hash}/{file_path}#L{start}
{repo_base_url}/{ref_commit_hash}/{file_path}#L{start}-L{end}
```

### Link Format

| Format | Syntax | Example |
|--------|--------|---------|
| Single line | `[filename.ext:42](url#L42)` | `[Button.tsx:42](https://...)` ([evidence_citation_policy.md:33-35](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/evidence_citation_policy.md#L33-L35)) |
| Line range | `[filename.ext:42-50](url#L42-L50)` | `[Button.tsx:42-50](https://...)` ([evidence_citation_policy.md:37-40](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/evidence_citation_policy.md#L37-L40)) |

### Display Text Rules

The display text for citations uses only the filename (without directory path), actual line numbers from the file content, and a colon separator between filename and lines ([evidence_citation_policy.md:42-49](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/evidence_citation_policy.md#L42-L49)).

### Citation Placement

Citations can be placed inline (immediately after the claim, wrapped in parentheses) or at the end of each section as a summary ([evidence_citation_policy.md:52-75](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/evidence_citation_policy.md#L52-L75)). Inline citations must come before the period and be wrapped in parentheses for readability ([evidence_citation_policy.md:60-66](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/evidence_citation_policy.md#L60-L66)).

### What NOT to Cite

The policy specifies that general programming concepts, standard library functions, well-known patterns, and the author's own explanations do not need citations ([evidence_citation_policy.md:102-108](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/evidence_citation_policy.md#L102-L108)).

Sources: [evidence_citation_policy.md:1-134](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/evidence_citation_policy.md#L1-L134)
<!-- END:AUTOGEN deepwiki-skill_05_policies_evidence-citation -->

---

<!-- BEGIN:AUTOGEN deepwiki-skill_05_policies_mermaid -->
## Mermaid Diagram Policy

This section covers the guidelines for generating Mermaid diagrams in wiki documentation.

The Mermaid policy defines rules and best practices for creating diagrams that render correctly and communicate technical concepts effectively ([mermaid_policy.md:1-5](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/mermaid_policy.md#L1-L5)).

### Supported Diagram Types

| Type | Use Case | Syntax |
|------|----------|--------|
| `flowchart` | Process flows, data flow, decision trees | `graph TD` |
| `sequence` | Interaction sequences, API calls | `sequenceDiagram` |
| `class` | Class relationships, inheritance | `classDiagram` |
| `state` | State machines, status transitions | `stateDiagram-v2` |
| `er` | Entity relationships, database schema | `erDiagram` |
| `gantt` | Project timelines | `gantt` |

([mermaid_policy.md:7-15](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/mermaid_policy.md#L7-L15))

### Critical Rules

The policy defines six critical rules that must be followed:

1. **Use Vertical Orientation**: Always use `graph TD` (top-down), never `graph LR` (left-right) ([mermaid_policy.md:19-20](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/mermaid_policy.md#L19-L20)).

2. **Quote All Node Text**: All node text must be wrapped in double quotes to prevent parse errors ([mermaid_policy.md:22-48](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/mermaid_policy.md#L22-L48)).

3. **Subgraph Names - No Special Characters**: Subgraph names must not contain parentheses or special characters; use alphanumeric characters and underscores only ([mermaid_policy.md:49-72](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/mermaid_policy.md#L49-L72)).

4. **Sequence Diagram Messages - Never Empty**: The colon in sequence diagrams must be followed by content; use `;` as placeholder when there's no meaningful message ([mermaid_policy.md:74-93](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/mermaid_policy.md#L74-L93)).

5. **No Shorthand Activation**: Do not use shorthand activation syntax (`->>+`, `-->>-`) in sequence diagrams ([mermaid_policy.md:95-115](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/mermaid_policy.md#L95-L115)).

6. **No Source Citations in Diagrams**: Never include source file citations inside Mermaid diagrams; place citations outside the diagram in the documentation text ([mermaid_policy.md:117-133](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/mermaid_policy.md#L117-L133)).

### Validation Process

The policy includes a validation process using `validate_mermaid.py` to extract and validate diagrams ([mermaid_policy.md:249-258](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/mermaid_policy.md#L249-L258)):

```bash
python3 validate_mermaid.py --input {doc_dir} --invalid-only --output _reports/mermaid_invalid.json
```

Error types include `lexical_error`, `syntax_error`, `node_error`, `edge_error`, `graph_structure_error`, and `style_error` ([mermaid_policy.md:276-288](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/mermaid_policy.md#L276-L288)).

Sources: [mermaid_policy.md:1-428](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/mermaid_policy.md#L1-L428)
<!-- END:AUTOGEN deepwiki-skill_05_policies_mermaid -->

---

<!-- BEGIN:AUTOGEN deepwiki-skill_05_policies_validation -->
## Validation Policy

This section describes the document structure validation requirements for wiki documentation.

The validation policy defines the rules that must be checked after all documents are generated, focusing on two main areas: Mermaid diagram validation and document structure validation ([validation_policy.md:6-9](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/validation_policy.md#L6-L9)).

### PAGE_ID Validation

Every wiki page must have a PAGE_ID marker at the beginning of the file ([validation_policy.md:14-15](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/validation_policy.md#L14-L15)):

```html
<!-- PAGE_ID: {page_id} -->
```

| Check | Action if Failed |
|-------|------------------|
| PAGE_ID marker exists at file start | Add the marker |
| page_id matches TOC definition | Fix to match TOC |
| Only one PAGE_ID per file | Remove duplicates |

([validation_policy.md:22-27](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/validation_policy.md#L22-L27))

### AUTOGEN Marker Validation

Every auto-generated section must have matching BEGIN and END markers ([validation_policy.md:37-39](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/validation_policy.md#L37-L39)):

| Check | Action if Failed |
|-------|------------------|
| BEGIN marker exists for each `autogen: true` section | Add before section content |
| END marker exists for each `autogen: true` section | Add after section content |
| BEGIN section_id matches END section_id | Correct the mismatched ID |
| section_id matches TOC definition | Update to match TOC |
| No orphaned markers (BEGIN without END) | Add missing END or remove orphan |
| No duplicate markers (same ID multiple times) | Remove duplicates |
| No extra markers not in TOC | Remove extra markers |

([validation_policy.md:48-58](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/validation_policy.md#L48-L58))

### Validation Workflow

The validation workflow uses MCP tools in a specific order ([validation_policy.md:121-134](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/validation_policy.md#L121-L134)):

1. **Validate Document Structure** using `validate_docs_structure` MCP tool
2. **Validate Mermaid Diagrams** using `get_invalid_mermaid_blocks` MCP tool
3. **Fix Issues** based on validation results
4. **Re-validate** to confirm all issues are resolved

Issue categories include: `page_id`, `autogen`, `structure`, `link`, and `toc` ([validation_policy.md:163-169](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/validation_policy.md#L163-L169)).

Sources: [validation_policy.md:1-262](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/validation_policy.md#L1-L262)
<!-- END:AUTOGEN deepwiki-skill_05_policies_validation -->

---

<!-- BEGIN:AUTOGEN deepwiki-skill_05_policies_doc-update -->
## Document Update Policy

This section describes the guidelines for incremental documentation updates.

The document update policy describes a two-phase algorithm for incremental documentation updates that only regenerates sections affected by changes, preserves manual content outside AUTOGEN markers, and tracks documentation version via `ref_commit_hash` ([doc_update_policy.md:5-10](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/doc_update_policy.md#L5-L10)).

### Phase A: TOC Structure Sync

Phase A synchronizes documentation with TOC structure changes made manually by users ([doc_update_policy.md:30-34](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/doc_update_policy.md#L30-L34)). It uses `collect_sync_context.py` to compare TOC page/section definitions against existing markdown files with PAGE_ID markers ([doc_update_policy.md:36-40](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/doc_update_policy.md#L36-L40)).

Actions include:
- **A1: Generate New Pages** - For each page in `new_pages`, collect source files and generate complete page following `page_template.md` ([doc_update_policy.md:68-74](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/doc_update_policy.md#L68-L74))
- **A2: Update Existing Pages** - Delete removed sections and add new sections while maintaining TOC order ([doc_update_policy.md:76-96](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/doc_update_policy.md#L76-L96))

### Phase B: Source Code Update

Phase B regenerates documentation sections affected by source code changes ([doc_update_policy.md:105-109](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/doc_update_policy.md#L105-L109)). It uses `collect_update_context.py` to analyze the Git diff between `ref_commit_hash` and `HEAD` ([doc_update_policy.md:113-115](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/doc_update_policy.md#L113-L115)).

Actions include:
- **B1: Regenerate Affected Sections** - Update content based on new source files while following evidence citation rules ([doc_update_policy.md:194-218](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/doc_update_policy.md#L194-L218))
- **B2: Handle New Source Files** - Analyze uncovered files and decide placement (new section or page) ([doc_update_policy.md:220-235](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/doc_update_policy.md#L220-L235))
- **B3: Handle Deleted Source Files** - Remove sections with no remaining source files ([doc_update_policy.md:237-247](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/doc_update_policy.md#L237-L247))
- **B4: Update TOC Metadata** - Update `ref_commit_hash` and `updated_at` after all updates ([doc_update_policy.md:249-258](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/doc_update_policy.md#L249-L258))

### AUTOGEN Block Handling

The policy emphasizes safe replacement by only modifying content between AUTOGEN markers and preserving manual content outside the markers ([doc_update_policy.md:262-289](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/doc_update_policy.md#L262-L289)). Nested AUTOGEN blocks are handled correctly to avoid affecting parent section markers ([doc_update_policy.md:291-310](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/doc_update_policy.md#L291-L310)).

Sources: [doc_update_policy.md:1-389](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/doc_update_policy.md#L1-L389)
<!-- END:AUTOGEN deepwiki-skill_05_policies_doc-update -->

---

<!-- BEGIN:AUTOGEN deepwiki-skill_05_policies_page-template -->
## Page Template

This section describes the standard format for generated wiki pages.

The page template defines the structure that every wiki page must follow ([page_template.md:7-8](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/page_template.md#L7-L8)).

### Required Page Structure

Every wiki page must contain the following elements in order ([page_template.md:9-46](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/page_template.md#L9-L46)):

1. **PAGE_ID Marker** - At the very beginning of the file
2. **Source Files List** - Collapsible list of source files used for context
3. **Page Title** - H1 heading
4. **Related Pages** - Links to related wiki pages
5. **Sections** - Content sections with AUTOGEN markers

### Markers

| Marker Type | Purpose | Format |
|-------------|---------|--------|
| PAGE_ID | Uniquely identify the page for incremental updates | `<!-- PAGE_ID: {page_id} -->` |
| AUTOGEN | Mark auto-generated content boundaries for safe updates | `<!-- BEGIN:AUTOGEN {section_id} -->` ... `<!-- END:AUTOGEN {section_id} -->` |

([page_template.md:50-78](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/page_template.md#L50-L78))

### Heading Levels

| Section Depth | Heading | Markdown |
|---------------|---------|----------|
| Page title | H1 | `#` |
| Top-level section | H2 | `##` |
| Nested level 1 | H3 | `###` |
| Nested level 2 | H4 | `####` |
| Nested level 3 | H5 | `#####` |

([page_template.md:130-138](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/page_template.md#L130-L138))

### Section Content Guidelines

Each section should start with the heading and a brief 1-2 sentence introduction ([page_template.md:165-177](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/page_template.md#L165-L177)). The section body should include explanatory text with source citations, code examples (if relevant), tables for structured data, and diagrams (if `diagrams_needed: true`) ([page_template.md:179-186](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/page_template.md#L179-L186)).

Each section should end with source citations summary, the END:AUTOGEN marker, and a horizontal rule ([page_template.md:188-199](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/page_template.md#L188-L199)).

Sources: [page_template.md:1-282](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/page_template.md#L1-L282)
<!-- END:AUTOGEN deepwiki-skill_05_policies_page-template -->

---

<!-- BEGIN:AUTOGEN deepwiki-skill_05_policies_toc-schema -->
## TOC Schema

This section describes the schema specification for toc.yaml files.

The TOC schema defines the structure for `toc.yaml` files used in wiki generation ([toc_schema.md:1-3](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/toc_schema.md#L1-L3)).

### Project Section Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Project name for display |
| `description` | string | Yes | Brief 1-2 sentence description |
| `repo_base_url` | string | No | Base URL without commit hash |
| `ref_commit_hash` | string | Yes | Current commit hash (from `git rev-parse HEAD`) |
| `updated_at` | string | No | Date in YYYY-MM-DD format |

([toc_schema.md:49-57](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/toc_schema.md#L49-L57))

### Page ID Format

Page IDs must be globally unique across all wiki pages and follow the format `{repo_name}_{number}_{page-name}` ([toc_schema.md:59-76](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/toc_schema.md#L59-L76)). Rules include using the repository name as prefix, zero-padded number for ordering, kebab-case for page name, and no spaces or special characters.

### Section ID Format

Section IDs inherit from page ID using the format `{page_id}_{section-name}`, and nested sections use `{parent_section_id}_{subsection-name}` ([toc_schema.md:78-94](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/toc_schema.md#L78-L94)).

### Source Files Patterns

The schema supports both explicit file paths and glob patterns ([toc_schema.md:96-106](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/toc_schema.md#L96-L106)):

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

([toc_schema.md:108-117](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/toc_schema.md#L108-L117))

### Validation Rules

The schema defines six validation rules ([toc_schema.md:206-212](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/toc_schema.md#L206-L212)):

1. **ID Uniqueness** - All page and section IDs must be unique
2. **Required Fields** - All required fields must be present
3. **File Extension** - Filename must end with `.md`
4. **Diagram Types** - Must be from allowed values when specified
5. **Section Depth** - Recommend max 3 levels of nesting
6. **Source Files** - Each page should have at least 1 source file

### Page Count Guidelines

| Project Size | Recommended Pages |
|--------------|-------------------|
| Small (< 10 files) | 3-5 pages |
| Medium (10-50 files) | 5-8 pages |
| Large (50-200 files) | 8-12 pages |
| Very Large (> 200 files) | 10-15 pages |

([toc_schema.md:214-221](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/toc_schema.md#L214-L221))

Sources: [toc_schema.md:1-238](https://github.com/natsu1211/deepwiki-skill/blob/784d30af68157f49d7f829f85d49dafe9fba65cd/skills/wiki/references/toc_schema.md#L1-L238)
<!-- END:AUTOGEN deepwiki-skill_05_policies_toc-schema -->

---
