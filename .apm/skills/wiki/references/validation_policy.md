# Document Validation Policy

This document defines the validation rules for wiki documents during Phase 4.

## Overview

After all documents are generated, validate:
1. **Mermaid Diagram Validation** - Ensure all diagrams compile
2. **Document Structure Validation** - Ensure markers are correct

## Document Structure Validation

### PAGE_ID Validation

Every wiki page must have a PAGE_ID marker at the beginning.

**Format**:
```html
<!-- PAGE_ID: {page_id} -->
```

**Validation Rules**:
| Check | Action if Failed |
|-------|------------------|
| PAGE_ID marker exists at file start | Add the marker |
| page_id matches TOC definition | Fix to match TOC |
| Only one PAGE_ID per file | Remove duplicates |

**Example**:
```markdown
<!-- PAGE_ID: myproject_01_overview -->
<details>
<summary>Relevant source files</summary>
...
```

### AUTOGEN Marker Validation

Every auto-generated section must have matching BEGIN and END markers.

**Format**:
```html
<!-- BEGIN:AUTOGEN {section_id} -->
{generated content}
<!-- END:AUTOGEN {section_id} -->
```

**Validation Rules**:

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

#### Orphaned Markers

**Problem**: BEGIN without matching END, or vice versa.

```markdown
<!-- BEGIN:AUTOGEN myproject_01_section1 -->
## Section 1

Content here...

## Section 2  <!-- Missing END marker! -->

<!-- BEGIN:AUTOGEN myproject_01_section2 -->
```

**Fix**: Add missing marker or remove orphan.

#### Duplicate Markers

**Problem**: Same section_id appearing multiple times.

```markdown
<!-- BEGIN:AUTOGEN myproject_01_overview -->
## First Instance
<!-- END:AUTOGEN myproject_01_overview -->

...

<!-- BEGIN:AUTOGEN myproject_01_overview -->  <!-- Duplicate! -->
## Second Instance
<!-- END:AUTOGEN myproject_01_overview -->
```

**Fix**: Remove duplicate or rename section_id.

#### Mismatched IDs

**Problem**: BEGIN and END have different section_ids.

```markdown
<!-- BEGIN:AUTOGEN myproject_01_section1 -->
## Section
<!-- END:AUTOGEN myproject_01_section2 -->  <!-- Mismatch! -->
```

**Fix**: Correct END marker to match BEGIN.

#### Extra Markers

**Problem**: AUTOGEN markers not defined in TOC.

```markdown
<!-- BEGIN:AUTOGEN myproject_01_unknown_section -->  <!-- Not in TOC! -->
## Unknown Section
<!-- END:AUTOGEN myproject_01_unknown_section -->
```

**Fix**: Remove markers or add section to TOC.

## Validation Workflow

Use MCP tools to validate documentation:

### Step 1: Validate Document Structure

Use `validate_docs_structure` MCP tool:

```
validate_docs_structure(
    doc_dir="{doc_dir}",
    toc_file="{doc_dir}/toc.yaml",
    repo_path="{repo_path}"
)
```

**Returns**:
```json
{
  "summary": {
    "pages_validated": 10,
    "pages_missing": 0,
    "sections_validated": 25,
    "sections_missing": 2,
    "total_errors": 3,
    "total_warnings": 1,
    "is_valid": false
  },
  "errors": [
    {
      "file": "02_architecture.md",
      "line": null,
      "severity": "error",
      "category": "autogen",
      "message": "Missing AUTOGEN section 'myproject_02_arch_core' defined in TOC",
      "fix_hint": "Add BEGIN:AUTOGEN and END:AUTOGEN markers around the section"
    }
  ],
  "warnings": [...]
}
```

**Issue Categories**:
- `page_id`: PAGE_ID marker issues
- `autogen`: AUTOGEN BEGIN/END marker issues
- `structure`: Document structure issues (H1 headings, file size)
- `link`: Internal link issues
- `toc`: TOC alignment issues

### Step 2: Validate Mermaid Diagrams

Use `get_invalid_mermaid_blocks` MCP tool:

```
get_invalid_mermaid_blocks(
    doc_dir="{doc_dir}"
)
```

**Returns**:
```json
{
  "invalid_blocks": [
    {
      "file_path": "03_api.md",
      "code": "graph TD\n  A --> B[missing bracket",
      "start_line": 45,
      "end_line": 52,
      "error_message": "Syntax error on line 2",
      "error_type": "syntax_error",
      "fix_hint": "Check bracket matching in node definitions"
    }
  ],
  "total_invalid": 1,
  "total_scanned": 15,
  "files_affected": 1
}
```

### Step 3: Fix Issues

Based on validation results, fix issues:

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

### Step 4: Re-validate

After fixes, run validation again to confirm all issues are resolved:

```
validate_docs_structure(...) -> summary.is_valid == true
get_invalid_mermaid_blocks(...) -> total_invalid == 0
```

## Validation Report

Include in final report:

```
### Document Structure Validation
- **Files checked**: 10
- **PAGE_ID issues**: 0
- **AUTOGEN marker issues**: 2
  - 02_architecture.md: Added missing END marker for section `myproject_02_arch_core`
  - 03_api.md: Fixed mismatched section_id `myproject_03_api_endpoints`

### Mermaid Diagram Validation
- **Diagrams scanned**: 15
- **Invalid diagrams**: 1 (fixed)
  - 03_api.md:45: Fixed syntax error in flowchart
```

## Integration Order

Run validations in order:

```
Phase 4: Validation
├── 4.1 Mermaid Diagram Validation
│   ├── Extract blocks
│   ├── Validate syntax
│   └── Fix invalid diagrams
│
└── 4.2 Document Structure Validation
    ├── Validate PAGE_ID markers
    ├── Validate AUTOGEN markers
    └── Auto-fix issues
```

Both validations contribute to the final validation report.
