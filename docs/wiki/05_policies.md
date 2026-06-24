<!-- PAGE_ID: deepwiki-skill_05_policies -->
<details>
<summary>📚 Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [toc_schema.md:1-238](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/toc_schema.md#L1-L238)
- [page_template.md:1-281](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/page_template.md#L1-L281)
- [evidence_citation_policy.md:1-133](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/evidence_citation_policy.md#L1-L133)
- [mermaid_policy.md:1-427](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/mermaid_policy.md#L1-L427)
- [validation_policy.md:1-262](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/validation_policy.md#L1-L262)
- [doc_update_policy.md:1-389](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/doc_update_policy.md#L1-L389)
- [toc.yaml.template:1-255](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/templates/toc.yaml.template#L1-L255)

</details>

# Policies, Schema, and Templates

> **Related Pages**: [[Workflow Phases and Execution Modes|03_workflow.md]], [[Python Helper Scripts|04_scripts.md]]

The reference documents under `.apm/skills/wiki/references/` and the starter template under `.apm/skills/wiki/templates/` are the contracts that govern every generated wiki. They define the shape of the `toc.yaml` structure, the markers and citation rules that shape page content, the validation gates that documents must pass, and the algorithm for incremental updates. The workflow phases (see [[Workflow Phases and Execution Modes|03_workflow.md]]) load these files on demand and treat them as the source of truth.

---

<!-- BEGIN:AUTOGEN deepwiki-skill_05_policies_toc-schema -->
## TOC Schema and Template

This section describes the schema that defines a `toc.yaml` file and the starter template that seeds a new one. The schema document specifies the contract for wiki structure, while the template provides a ready-to-customize example.

### The toc.yaml Schema

`toc_schema.md` defines the schema for `toc.yaml` files used in wiki generation ([toc_schema.md:1-3](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/toc_schema.md#L1-L3)). A TOC has three top-level keys: a required `project` block, a required `pages` array, and an optional `notes` array ([toc_schema.md:9-44](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/toc_schema.md#L9-L44)).

The `project` block carries metadata used for citations and incremental tracking. The fields and their requirements are defined in the schema ([toc_schema.md:50-56](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/toc_schema.md#L50-L56)):

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Project name for display ([toc_schema.md:52](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/toc_schema.md#L52)) |
| `description` | Yes | Brief 1-2 sentence description ([toc_schema.md:53](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/toc_schema.md#L53)) |
| `repo_base_url` | No | Base URL without commit hash ([toc_schema.md:54](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/toc_schema.md#L54)) |
| `ref_commit_hash` | Yes | Current commit hash, from `git rev-parse HEAD` ([toc_schema.md:55](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/toc_schema.md#L55)) |
| `updated_at` | No | Date in YYYY-MM-DD format ([toc_schema.md:56](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/toc_schema.md#L56)) |

Each entry in `pages` defines an output document. A page requires an `id`, `title`, and `filename`, requires a `source_files` array shared by all its sections, and requires a `sections` array; it may optionally carry a `description` and a `related_pages` list for cross-linking ([toc_schema.md:18-41](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/toc_schema.md#L18-L41)). Each section requires an `id`, `title`, an `autogen` boolean, and a `diagrams_needed` boolean; sections may add their own `source_files`, a `diagram_types` list (required when `diagrams_needed` is true), and nested `sections` of the same structure ([toc_schema.md:27-37](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/toc_schema.md#L27-L37)).

### ID Conventions

IDs are hierarchical and must be globally unique. A page ID follows the pattern `{repo_name}_{number}_{page-name}`, using the repository name as prefix, a zero-padded number for ordering, and kebab-case for the page name with no spaces or special characters ([toc_schema.md:60-75](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/toc_schema.md#L60-L75)). Section IDs inherit from the page ID as `{page_id}_{section-name}`, and nested sections extend the parent section ID as `{parent_section_id}_{subsection-name}` ([toc_schema.md:79-93](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/toc_schema.md#L79-L93)).

### Source File Patterns and Diagram Types

`source_files` entries accept both explicit paths and glob patterns, where `src/*.py` matches one level and `src/**/*.py` matches recursively ([toc_schema.md:95-105](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/toc_schema.md#L95-L105)). When `diagrams_needed` is true, `diagram_types` must contain values from the allowed set ([toc_schema.md:107-116](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/toc_schema.md#L107-L116)):

| Type | Use Case |
|------|----------|
| `flowchart` | Process flows, decision trees, data flow ([toc_schema.md:111](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/toc_schema.md#L111)) |
| `sequence` | Interaction sequences, API calls ([toc_schema.md:112](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/toc_schema.md#L112)) |
| `class` | Class relationships, inheritance ([toc_schema.md:113](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/toc_schema.md#L113)) |
| `state` | State machines, status transitions ([toc_schema.md:114](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/toc_schema.md#L114)) |
| `er` | Entity relationships, database schema ([toc_schema.md:115](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/toc_schema.md#L115)) |
| `gantt` | Project timelines, rarely used ([toc_schema.md:116](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/toc_schema.md#L116)) |

### Validation Rules and Sizing Guidance

The schema enforces six validation rules: all page and section IDs must be unique, all required fields must be present, filenames must end with `.md`, diagram types must come from the allowed values, nesting is recommended to a maximum of three levels, and each page should have at least one source file ([toc_schema.md:204-211](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/toc_schema.md#L204-L211)). It also provides page-count guidance scaled to project size, recommending 3-5 pages for small projects under 10 files up to 10-15 pages for very large projects over 200 files ([toc_schema.md:213-220](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/toc_schema.md#L213-L220)).

### The Starter Template

`toc.yaml.template` is a fully worked example meant to be copied and customized, with placeholders such as `{PROJECT_NAME}`, `{REPO_BASE_URL}`, and `{COMMIT_HASH}` ([toc.yaml.template:1-9](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/templates/toc.yaml.template#L1-L9)). It ships six common pages — Overview, Architecture, Getting Started, API Reference, Configuration, and Development Guide — with the latter ones marked optional ([toc.yaml.template:13-247](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/templates/toc.yaml.template#L13-L247)). Its `notes` instruct the user to remove pages that don't apply, replace `{repo}` with the repository name, and replace `{ext}` with the project's primary file extension ([toc.yaml.template:249-255](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/templates/toc.yaml.template#L249-L255)).

Sources: [toc_schema.md:1-220](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/toc_schema.md#L1-L220), [toc.yaml.template:1-255](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/templates/toc.yaml.template#L1-L255)
<!-- END:AUTOGEN deepwiki-skill_05_policies_toc-schema -->

---

<!-- BEGIN:AUTOGEN deepwiki-skill_05_policies_content -->
## Content Policies

This section covers the three reference documents that govern what generated page content looks like: the page template and its markers, the evidence citation rules, and the Mermaid diagram conventions.

### Page Template and Markers

`page_template.md` defines the page structure and marker conventions every wiki page must follow ([page_template.md:1-7](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/page_template.md#L1-L7)). A page opens with a `PAGE_ID` marker, followed by a collapsible source-file list, the H1 title, a related-pages line, and one or more autogen-wrapped sections separated by horizontal rules ([page_template.md:9-46](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/page_template.md#L9-L46)).

Two marker types anchor the page for safe incremental updates:

| Marker | Format | Rules |
|--------|--------|-------|
| `PAGE_ID` | `<!-- PAGE_ID: {page_id} -->` | Must be at the very beginning of the file, must match the TOC ID, and only one per file ([page_template.md:50-63](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/page_template.md#L50-L63)) |
| `AUTOGEN` | `<!-- BEGIN:AUTOGEN {id} -->` / `<!-- END:AUTOGEN {id} -->` | Every autogen section needs both markers, the ID must match the TOC, content outside markers is preserved on update, and a `---` separator follows each section ([page_template.md:69-97](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/page_template.md#L69-L97)) |

Heading depth maps directly to section nesting: the page title is H1, top-level sections are H2, and each nested level adds one heading level down to H5 ([page_template.md:130-138](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/page_template.md#L130-L138)). Sections where `autogen: false` are left as a placeholder with a manual-maintenance comment and must NOT receive AUTOGEN markers, so that hand-written content survives regeneration ([page_template.md:201-215](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/page_template.md#L201-L215)).

### Evidence Citation Policy

`evidence_citation_policy.md` makes evidence-based writing mandatory: every major claim must be backed by citations from actual source files, and the generator must never guess, never invent line numbers, only describe functionality present in the source, and explicitly state when information is missing ([evidence_citation_policy.md:1-12](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/evidence_citation_policy.md#L1-L12)).

Citations are links whose URL is built from `repo_base_url`, `ref_commit_hash`, the repo-relative file path, and an anchor of the form `#L{start}` or `#L{start}-L{end}` ([evidence_citation_policy.md:18-28](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/evidence_citation_policy.md#L18-L28)). The display text uses only the filename with no directory path, a colon separator, and the actual line numbers — for example `Button.tsx:42` rather than the full path ([evidence_citation_policy.md:42-49](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/evidence_citation_policy.md#L42-L49)).

Placement rules are strict. Inline citations must be wrapped in parentheses and must come BEFORE the closing period, so the period ends the whole statement including its citation ([evidence_citation_policy.md:53-66](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/evidence_citation_policy.md#L53-L66)). Citations should be spread throughout a section rather than clustered at the end, with each major claim carrying a nearby citation ([evidence_citation_policy.md:91-94](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/evidence_citation_policy.md#L91-L94)). Line numbers are read from the start of each line before the `→` delimiter and must never be guessed ([evidence_citation_policy.md:96-100](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/evidence_citation_policy.md#L96-L100)).

The policy also scopes what should NOT be cited — general programming concepts, standard library functions, well-known patterns, and the author's own summaries ([evidence_citation_policy.md:102-107](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/evidence_citation_policy.md#L102-L107)). It prefers real code over hypotheticals, recommends tables for summarizing endpoints and configuration, and selects output language from the locale code, defaulting to Japanese ([evidence_citation_policy.md:109-133](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/evidence_citation_policy.md#L109-L133)).

### Mermaid Diagram Policy

`mermaid_policy.md` defines rules and best practices for Mermaid diagrams and maps each diagram type to its syntax keyword, such as `graph TD` for flowcharts and `sequenceDiagram` for sequences ([mermaid_policy.md:1-14](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/mermaid_policy.md#L1-L14)). Six critical rules constrain diagram generation:

| Rule | Requirement |
|------|-------------|
| Vertical orientation | Always use `graph TD` (top-down), never `graph LR` ([mermaid_policy.md:18-20](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/mermaid_policy.md#L18-L20)) |
| Quote node text | All node text must be wrapped in double quotes across every node type ([mermaid_policy.md:22-47](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/mermaid_policy.md#L22-L47)) |
| Clean subgraph names | Subgraph names must use only alphanumerics and underscores, no parentheses or special characters ([mermaid_policy.md:49-72](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/mermaid_policy.md#L49-L72)) |
| Non-empty messages | A sequence-diagram colon must be followed by content, using `;` as a placeholder when there is none ([mermaid_policy.md:74-92](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/mermaid_policy.md#L74-L92)) |
| No shorthand activation | Do not use `->>+` / `-->>-`; use explicit `activate` / `deactivate` ([mermaid_policy.md:94-115](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/mermaid_policy.md#L94-L115)) |
| No citations in diagrams | Never place source citations inside a diagram; keep them in the surrounding text ([mermaid_policy.md:117-133](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/mermaid_policy.md#L117-L133)) |

Node labels should be written in the target language, defaulting to Japanese ([mermaid_policy.md:135-146](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/mermaid_policy.md#L135-L146)). The policy recommends keeping flowcharts to 10-15 nodes with 3-4 word labels for readability ([mermaid_policy.md:168-172](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/mermaid_policy.md#L168-L172)). Diagrams are validated with `validate_mermaid.py`, whose output reports an `error_type`, `error_line`, and `fix_hint` per block ([mermaid_policy.md:249-288](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/mermaid_policy.md#L249-L288)). When a diagram still fails after three fix attempts, the policy directs the generator to comment it out, add a TODO marker, and record it in the report ([mermaid_policy.md:300-305](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/mermaid_policy.md#L300-L305)).

Sources: [page_template.md:1-215](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/page_template.md#L1-L215), [evidence_citation_policy.md:1-133](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/evidence_citation_policy.md#L1-L133), [mermaid_policy.md:1-305](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/mermaid_policy.md#L1-L305)
<!-- END:AUTOGEN deepwiki-skill_05_policies_content -->

---

<!-- BEGIN:AUTOGEN deepwiki-skill_05_policies_validation-update -->
## Validation and Update Policies

This section covers the two reference documents that govern quality gates after generation and the algorithm for keeping documentation in sync with code: the validation policy and the incremental update policy.

### Document Validation Policy

`validation_policy.md` defines the rules applied during the validation phase, which checks two things after all documents are generated: that every Mermaid diagram compiles and that document markers are correct ([validation_policy.md:1-9](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/validation_policy.md#L1-L9)).

Structure validation has two parts. Every page must carry a `PAGE_ID` marker at the file start; if it is missing it is added, if it mismatches the TOC it is fixed, and duplicates are removed ([validation_policy.md:13-35](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/validation_policy.md#L13-L35)). Every `autogen: true` section must have matching BEGIN and END markers whose IDs agree with each other and with the TOC, and the policy enumerates the integrity failures to detect ([validation_policy.md:37-119](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/validation_policy.md#L37-L119)):

| Failure | Description |
|---------|-------------|
| Orphaned marker | A BEGIN without a matching END, or vice versa ([validation_policy.md:62-77](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/validation_policy.md#L62-L77)) |
| Duplicate marker | The same section ID appearing multiple times ([validation_policy.md:79-95](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/validation_policy.md#L79-L95)) |
| Mismatched IDs | BEGIN and END carrying different section IDs ([validation_policy.md:97-107](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/validation_policy.md#L97-L107)) |
| Extra marker | An AUTOGEN block not defined in the TOC ([validation_policy.md:109-119](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/validation_policy.md#L109-L119)) |

The workflow runs `validate_docs_structure` and `get_invalid_mermaid_blocks`, both of which return structured JSON with per-issue categories, fix hints, and an `is_valid` summary ([validation_policy.md:121-198](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/validation_policy.md#L121-L198)). Issues are categorized as `page_id`, `autogen`, `structure`, `link`, or `toc`, each with a prescribed auto-fix action ([validation_policy.md:163-215](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/validation_policy.md#L163-L215)). After fixing, validation is re-run until `summary.is_valid` is true and `total_invalid` is zero ([validation_policy.md:217-223](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/validation_policy.md#L217-L223)). The integration order runs Mermaid validation first, then structure validation, with both feeding the final report ([validation_policy.md:244-261](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/validation_policy.md#L244-L261)).

### Incremental Update Policy

`doc_update_policy.md` describes the two-phase algorithm for incremental documentation updates, whose goal is to only regenerate affected sections, preserve manual content outside AUTOGEN markers, and track the documentation version via `ref_commit_hash` ([doc_update_policy.md:1-11](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/doc_update_policy.md#L1-L11)).

**Phase A — TOC Structure Sync** synchronizes documentation with manual TOC edits. It uses `collect_sync_context.py` to compare TOC page and section definitions against the existing markdown files that carry PAGE_ID markers, producing lists of new pages, pages to update, and unchanged pages ([doc_update_policy.md:30-64](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/doc_update_policy.md#L30-L64)). New pages are generated in full, and existing pages have removed sections deleted and new sections inserted in TOC order ([doc_update_policy.md:66-96](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/doc_update_policy.md#L66-L96)). A coexistence rule keeps the system safe: documents without a PAGE_ID marker, or with a PAGE_ID not in the TOC, are ignored rather than deleted, so hand-written documents can share the directory ([doc_update_policy.md:98-102](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/doc_update_policy.md#L98-L102)).

**Phase B — Source Code Update** regenerates sections affected by code changes. It uses `collect_update_context.py` to analyze the git diff between `ref_commit_hash` and `HEAD` against the source patterns in each TOC section, and it requires a valid `ref_commit_hash`, otherwise it falls back to full generation ([doc_update_policy.md:105-127](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/doc_update_policy.md#L105-L127)). The phase has four actions: regenerate affected sections, handle new source files, handle deleted source files, and update TOC metadata ([doc_update_policy.md:192-258](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/doc_update_policy.md#L192-L258)). Notably, new CI/CD files, build scripts, config files, or docs do not trigger new pages or sections ([doc_update_policy.md:220-228](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/doc_update_policy.md#L220-L228)), and after all updates the TOC's `ref_commit_hash` and `updated_at` are advanced ([doc_update_policy.md:249-258](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/doc_update_policy.md#L249-L258)).

The safety guarantee underlying both phases is that only content between AUTOGEN markers is ever replaced, never the manual content outside them, and nested blocks are updated without disturbing their parent markers ([doc_update_policy.md:262-310](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/doc_update_policy.md#L262-L310)). The policy also defines error handling for a missing `ref_commit_hash`, an invalid base commit, and conflicting TOC-versus-source changes, where TOC structure changes take priority before source content updates are applied ([doc_update_policy.md:314-333](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/doc_update_policy.md#L314-L333)).

Sources: [validation_policy.md:1-261](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/validation_policy.md#L1-L261), [doc_update_policy.md:1-389](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/references/doc_update_policy.md#L1-L389)
<!-- END:AUTOGEN deepwiki-skill_05_policies_validation-update -->

---
