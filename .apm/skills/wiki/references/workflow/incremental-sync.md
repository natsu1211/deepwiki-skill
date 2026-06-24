# Phase: incremental-sync (Phase 6)

## Goal

Collect the context needed to update existing docs safely after changes:
- Phase A: detect TOC structure changes
- Phase B: detect source code changes relevant to the TOC mappings

This step does not rewrite docs; it produces change context that `doc-write` uses to regenerate only affected pages/sections.

## Inputs

| Name | Required | Default | Description |
|------|----------|---------|-------------|
| `repo_path` | Yes | - | Absolute repository path |
| `output_dir` | No | `docs/wiki` | Documentation output directory |
| `doc_dir` | No | `{output_dir}` | Documentation directory containing existing `.md` |
| `toc_file` | No | `{output_dir}/toc.yaml` | Existing TOC |
| `target_commit` | No | `HEAD` | Target commit for change detection |
| `include_diff` | No | `false` | Whether to include patch data in update context |
| `diff_context` | No | `0` | Diff context lines when `include_diff=true` |

## Outputs

| Path | Description |
|------|-------------|
| `{output_dir}/_context/sync_context.json` | TOC sync result (Phase A) |
| `{output_dir}/_context/update_context.json` | Source update context (Phase B) |

## References 

- `../references/doc_update_policy.md`

## Scripts

### Phase A: `collect_sync_context.py`

Detects structural differences between `toc.yaml` and existing documentation files.

**Usage**:
```bash
python3 /scripts/collect_sync_context.py \
  --repo-path "{repo_path}" \
  --toc-file "{toc_file}" \
  --doc-dir "{doc_dir}" \
  --output "{output_dir}/_context/sync_context.json"
```

**Parameters**:

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--repo-path` | Yes | - | Absolute repository root path |
| `--toc-file` | Yes | - | Path to toc.yaml |
| `--doc-dir` | Yes | - | Directory containing existing .md docs |
| `--output` | No | stdout | Output JSON path |

**Output JSON Structure**:
```json
{
  "status": "sync_needed|up_to_date|full_rebuild_needed",
  "changes": {
    "added_pages": ["04_new_page"],
    "removed_pages": ["03_old_page"],
    "modified_pages": ["01_overview"],
    "added_sections": [{"page": "01_overview", "section": "new_section"}],
    "removed_sections": []
  },
  "recommendation": "Regenerate modified pages and added pages"
}
```

### Phase B: `collect_update_context.py`

Detects source code changes and maps them to affected wiki pages/sections.

**Usage**:
```bash
python3 /scripts/collect_update_context.py \
  --repo-path "{repo_path}" \
  --toc-file "{toc_file}" \
  --doc-dir "{doc_dir}" \
  --target-commit "{target_commit}" \
  --output "{output_dir}/_context/update_context.json"
```

**Parameters**:

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--repo-path` | Yes | - | Absolute repository root path |
| `--toc-file` | Yes | - | Path to toc.yaml |
| `--doc-dir` | Yes | - | Directory containing existing .md docs |
| `--target-commit` | No | `HEAD` | Target commit for change detection |
| `--include-diff` | No | `false` | Include line-numbered patch data (flag) |
| `--diff-context` | No | `0` | Context lines for patches |
| `--no-line-numbers` | No | `false` | Omit line numbers in patches (flag) |
| `--output` | No | stdout | Output JSON path |

**Output JSON Structure**:
```json
{
  "base_commit": "abc123",
  "target_commit": "def456",
  "affected_pages": [
    {
      "page_id": "myapp_01_overview",
      "filename": "01_overview.md",
      "affected_sections": ["myapp_01_overview_intro"],
      "changed_files": ["src/main.ts"],
      "change_details": {
        "src/main.ts": {
          "status": "modified",
          "diff": "..."
        }
      }
    }
  ],
  "unaffected_pages": ["myapp_02_architecture"]
}
```

### Optional: `get_section_update_diff.py`

Get focused diffs for a specific set of files (useful for detailed section updates).

**Usage**:
```bash
python3 /scripts/get_section_update_diff.py \
  --repo-path "{repo_path}" \
  --base-commit "{base_commit}" \
  --target-commit "{target_commit}" \
  --file-paths '["path/to/a", "path/to/b"]'
```

**Parameters**:

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--repo-path` | Yes | - | Absolute repository root path |
| `--base-commit` | Yes | - | Base commit hash (ref_commit_hash from TOC) |
| `--target-commit` | No | `HEAD` | Target commit hash |
| `--file-paths` | Yes | - | JSON array of file paths to diff |
| `--context` | No | `3` | Diff context lines |
| `--line-numbers` | No | `true` | Include line numbers in output |
| `--output` | No | stdout | Output JSON path |

## Workflow

0. Read `/references/doc_update_policy.md` to understand document update requirement.
1. Run Phase A (`collect_sync_context.py`):
   - if it indicates TOC drift that requires a full rebuild, stop and recommend rerunning full generation.
2. Run Phase B (`collect_update_context.py`) to map code changes to pages/sections.
3. Hand off to `doc-write`:
   - regenerate only affected pages/sections
   - do not touch manual sections or content outside AUTOGEN markers

## Validation

- `{output_dir}/_context/sync_context.json` exists and is valid JSON
- `{output_dir}/_context/update_context.json` exists and is valid JSON
- Each output explicitly lists changes or states “no changes”
