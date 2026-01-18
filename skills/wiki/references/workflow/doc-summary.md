# Step: doc-summary (Phase 5)

## Goal

Generate documentation summary report (`SUMMARY.md`) with:
- Generation status (pages/sections completion)
- Citation statistics and source coverage
- Diagram count summary
- Issues from validation reports (if available)

## Scripts

### `generate_summary.py`

Generates the SUMMARY.md report by analyzing documentation and validation results.

**Usage**:
```bash
python3 /scripts/generate_summary.py \
  --doc-dir "{doc_dir}" \
  --toc-file "{toc_file}" \
  --output "{output_dir}/_reports/SUMMARY.md"
```

**Parameters**:

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--doc-dir` | Yes | - | Directory containing generated .md docs |
| `--toc-file` | Yes | - | Path to toc.yaml file |
| `--structure-report` | No | `{doc_dir}/_reports/structure_validation.json` | Structure validation report (auto-detected) |
| `--mermaid-report` | No | `{doc_dir}/_reports/mermaid_invalid.json` | Mermaid validation report (auto-detected) |
| `--output` | No | `{doc_dir}/_reports/SUMMARY.md` | Output path for SUMMARY.md |

**Output Format**:

The script generates a markdown report with the following sections:

```markdown
# Wiki Documentation Summary

Generated: {timestamp}
Repository: {repo_name}
Commit: `{ref_commit_hash}`

## Generation Status

**Overall Status**: ✅ Complete / ⚠️ Incomplete / ❌ Has Errors

| Metric | Expected | Actual | Status |
|--------|----------|--------|--------|
| Pages | {n} | {n} | ✅/❌ |
| Sections | {n} | {n} | ✅/⚠️ |
| Citations | - | {n} | ✅/⚠️ |
| Diagrams | {n} | {valid} valid | ✅/⚠️ |

## Page Details

| Page | Title | Sections | Citations | Diagrams | Status |
|------|-------|----------|-----------|----------|--------|
| 01_overview.md | Overview | 4/4 | 49 | 2 | ✅ |
| ... | ... | ... | ... | ... | ... |

## Source Coverage

### Covered Files
- `src/main.ts` - cited in 01_overview.md, 02_architecture.md

### Uncovered Files
- `src/utils/helper.ts` - in TOC but never cited

## Issues

### Errors (Must Fix)
- **{file}**: {error_message}

### Warnings
- **{file}**: {warning_message}

### Recommendations
- {recommendation}
```

## Workflow

### 1. Run Summary Generation

Execute the script to generate the summary report:

```bash
python3 /scripts/generate_summary.py \
  --doc-dir "{doc_dir}" \
  --toc-file "{toc_file}" \
  --output "{output_dir}/_reports/SUMMARY.md"
```

The script automatically:
1. Parses `{toc_file}` to enumerate expected pages and sections
2. Scans generated docs to check completion status
3. Extracts and counts citations from each page
4. Counts Mermaid diagrams in each page
5. Analyzes source file coverage (cited vs uncited)
6. Reads validation reports (if present) to include errors/warnings
7. Generates the SUMMARY.md report

### 2. Review Summary

Check the generated `SUMMARY.md` for:
- **Overall Status**: Should be "✅ Complete" for successful generation
- **Page Details**: All pages should show expected sections count
- **Source Coverage**: Review uncovered files for potential gaps
- **Issues**: Address any errors before considering documentation complete

## Status Indicators

| Status | Meaning |
|--------|---------|
| ✅ Complete | All pages/sections generated, no errors |
| ⚠️ Incomplete | Some sections missing or has warnings |
| ❌ Has Errors | Validation errors present |

## Error Handling

- **Missing toc_file**: Script exits with error
- **Missing doc_dir**: Script exits with error
- **Missing validation reports**: Script continues without error/warning data
- **Missing pages**: Reported in Page Details with ❌ status
