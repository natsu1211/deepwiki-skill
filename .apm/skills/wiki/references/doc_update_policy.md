# Incremental Update Policy

This document describes the two-phase algorithm for incremental documentation updates.

## Overview

Incremental updates enable efficient documentation maintenance by:
1. Only regenerating sections affected by changes
2. Preserving manual content outside AUTOGEN markers
3. Tracking documentation version via `ref_commit_hash`

## Two-Phase Workflow

```
┌─────────────────────────────────────────┐
│ Phase A: TOC Structure Sync             │
│ - Detect TOC changes vs existing docs   │
│ - Generate new pages                    │
│ - Add/delete sections in existing pages │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│ Phase B: Source Code Update             │
│ - Detect source file changes via git    │
│ - Regenerate affected sections          │
│ - Update TOC metadata                   │
└─────────────────────────────────────────┘
```

## Phase A: TOC Structure Sync

### Purpose

Synchronize documentation with TOC structure changes made manually by users.

### Detection

Use `scripts/collect_sync_context.py` to compare:
- TOC page/section definitions
- Existing markdown files with PAGE_ID markers

### Outputs

```json
{
  "new_pages": [
    {
      "page_id": "project_04_new-feature",
      "title": "New Feature",
      "filename": "04_new-feature.md",
      "sections": [...]
    }
  ],
  "pages_to_update": {
    "project_02_architecture": {
      "file_path": "docs/wiki/02_architecture.md",
      "new_sections": [...],
      "deleted_sections": ["project_02_arch_old-module"],
      "existing_sections": [...]
    }
  },
  "unchanged_pages": ["project_01_overview", "project_03_api"]
}
```

### Actions

#### A1: Generate New Pages

For each page in `new_pages`:
1. Collect source files (run `read_files.py`)
2. Generate complete page following `page_template.md`
3. Include PAGE_ID marker at start
4. Save to `{doc_dir}/{filename}`

#### A2: Update Existing Pages (Section Changes)

For each page in `pages_to_update`:

**Delete removed sections**
Pseudo code:
```
for section_id in deleted_sections:
    # Remove content between markers
    # <!-- BEGIN:AUTOGEN {section_id} --> ... <!-- END:AUTOGEN {section_id} -->
    # Also remove the --- separator
```

**Add new sections**
Pseudo code:
```
for section in new_sections:
    # Generate section content
    # Insert after previous section's END marker
    # Maintain TOC order
```

### Document-TOC Coexistence Rule

Documents without PAGE_ID marker or with PAGE_ID not in TOC are **ignored** (not deleted).
This allows manually written documents to coexist in the same directory.

---

## Phase B: Source Code Update

### Purpose

Regenerate documentation sections affected by source code changes.

### Detection

Use `collect_update_context.py` to analyze:
- Git diff between `ref_commit_hash` and `HEAD`
- Source file patterns in TOC sections

Optional: include line-numbered diffs in `change_details` by running:

```bash
python3 collect_update_context.py --include-diff --diff-context 5 --repo-path /path/to/repo --toc-file toc.yaml --doc-dir ./docs/wiki/
```

### Prerequisites

The TOC must have a valid `ref_commit_hash` in the project section.
If missing, fall back to full generation mode.

### Outputs

```json
{
  "update_mode": "incremental",
  "base_commit": "abc123",
  "target_commit": "def456",
  "commit_range": "abc1234..def4567",
  "toc_file": "toc.yaml",
  "toc_updated_at": "2024-01-15",
  "changed_files": [
    { "path": "src/components/Button.tsx", "status": "M" },
    { "path": "src/old/Legacy.ts", "status": "D" },
    { "path": "src/new/Renamed.ts", "status": "R" }
  ],
  "sections_to_update": [
    {
      "page_id": "project_02_architecture",
      "page_file": "02_architecture.md",
      "section_id": "project_02_arch_components",
      "section_title": "Components",
      "source_patterns": ["src/components/**/*.ts"],
      "matched_files": ["src/components/Button.tsx"],
      "current_content": "...",
      "change_details": [{ "path": "src/components/Button.tsx", "status": "M" }]
    }
  ],
  "new_source_files": [
    {
      "path": "src/features/NewFeature.ts",
      "needs_toc_update": true,
      "status": "A"
    }
  ],
  "deleted_source_files": [
    {
      "path": "src/old/Deprecated.ts",
      "affected_sections": ["project_02_arch_deprecated"],
      "status": "D"
    }
  ],
  "docs_metadata": {
    "02_architecture.md": {
      "file": "02_architecture.md",
      "path": "./docs/wiki/02_architecture.md",
      "autogen_sections": ["project_02_arch_components"],
      "exists": true
    }
  },
  "metadata": {
    "total_changed_files": 3,
    "total_new_files": 1,
    "total_modified_files": 1,
    "total_deleted_files": 1,
    "total_renamed_files": 1,
    "total_sections_to_update": 1,
    "total_new_source_files": 1,
    "total_deleted_source_files": 1,
    "docs_analyzed": 1,
    "requires_full_generation": false
  }
}
```

### Actions

#### B1: Regenerate Affected Sections

For each section in `sections_to_update`:

1. **Get current source files**:
    ```bash
    read_files.py --files {matched_files} --line-numbers
    ```

2. **Get diff context** (optional, for understanding changes):
    ```bash
    python3 get_section_update_diff.py --repo-path /path/to/repo \
      --base-commit {base_commit} --target-commit {target_commit} \
      --file-paths '["path/to/file.ext"]'
    ```

3. **Regenerate content**:
   - Keep section structure and heading level
   - Update content based on new source files
   - Follow `references/evidence_citation_policy.md` rules
   - Update diagrams if needed

4. **Update document**:
   - Replace content between AUTOGEN markers ONLY
   - Never modify content outside markers

#### B2: Handle New Source Files

For uncovered source files (`new_source_files`):

1. Analyze file content and purpose
2. Decide placement:
   - Similar to existing page → Add section to that page
   - New functionality → Create new page (add to TOC)
   - **Do NOT add new pages or sections for CI/CD files, build scripts, config files, or docs**

3. Update TOC:
   - New sections: Insert before last section (last section is reserved for engineer-guide)
   - New pages: Add at end of pages array
   - Use glob patterns when possible

4. Generate documentation for new content

#### B3: Handle Deleted Source Files

For deleted files (`deleted_source_files`):

1. Check `affected_sections`
2. If section has no remaining source files:
   - Remove section from TOC
   - Remove AUTOGEN block from markdown
3. If page has no remaining sections:
   - Remove page from TOC
   - Optionally delete markdown file

#### B4: Update TOC Metadata

After all updates:

```yaml
project:
  # ... other fields ...
  ref_commit_hash: "{new_target_commit}"
  updated_at: "{current_date}"
```

---

## AUTOGEN Block Handling

### Safe Replacement

Only modify content between markers:

```markdown
<!-- BEGIN:AUTOGEN section_id -->
{THIS CONTENT CAN BE REPLACED}
<!-- END:AUTOGEN section_id -->
```

### Preserve Manual Content

Never modify content outside AUTOGEN markers:

```markdown
## Manual Notes

This section is manually maintained.
<!-- BEGIN:AUTOGEN next_section -->
{auto-generated content}
<!-- END:AUTOGEN next_section -->

## More Manual Content

Additional notes here.
```

### Nested AUTOGEN Blocks

Handle nested blocks correctly:

```markdown
<!-- BEGIN:AUTOGEN parent_section -->
## Parent Section

Overview text...

<!-- BEGIN:AUTOGEN child_section -->
### Child Section

Details...
<!-- END:AUTOGEN child_section -->

<!-- END:AUTOGEN parent_section -->
```

When updating `child_section`, don't affect `parent_section` markers.

---

## Error Handling

### Missing ref_commit_hash

If TOC doesn't have `ref_commit_hash`:
- Log warning
- Fall back to full generation mode
- Add `ref_commit_hash` after generation

### Invalid Base Commit

If base commit doesn't exist in git history:
- Try to find merge base
- If all fails, use full generation mode

### Conflicting Changes

If both TOC and source changed for same section:
- Prioritize TOC structure changes
- Then apply source content updates

---

## Update Report Format

```markdown
## Incremental Update Complete

- **Mode**: Incremental Update
- **Commit Range**: abc1234 → def5678

### Phase A: TOC Structure Sync
- **New Pages Generated**: 1
  - `project_04_auth` → 04_auth.md (3 sections)
- **Existing Pages Updated**: 1
  - 02_architecture.md
    - Added: `project_02_arch_cache`
    - Deleted: `project_02_arch_deprecated`

### Phase B: Source Code Update

#### Sections Regenerated
- **Sections Updated**: 3
  - 02_architecture.md (2 sections)
  - 03_api.md (1 section)

#### Auto TOC Updates
- **New Sections Added**: 2
- **Sections Removed**: 1
- **Files Now Covered**: 3

### Output
- Documents updated in: ./docs/wiki/
- TOC updated: ./toc.yaml
```

---

## Best Practices

1. **Commit TOC changes separately**
   - Makes Phase A changes clear
   - Easier to track documentation structure evolution

2. **Use glob patterns in TOC**
   - `src/components/**/*.tsx` covers new files automatically
   - Reduces need for TOC updates

3. **Regular updates**
   - Run updates frequently (e.g., after each PR)
   - Smaller diffs = faster updates

4. **Review `_reports/SUMMARY.md`**
   - Check coverage after updates
   - Identify gaps in documentation
