<!-- PAGE_ID: deepwiki-skill_04_scripts -->
<details>
<summary>📚 Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [collect_context.py:1-768](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/collect_context.py#L1-L768)
- [collect_sync_context.py:1-325](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/collect_sync_context.py#L1-L325)
- [collect_update_context.py:1-594](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/collect_update_context.py#L1-L594)
- [read_files.py:1-390](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/read_files.py#L1-L390)
- [collect_git_diff.py:1-369](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/collect_git_diff.py#L1-L369)
- [get_section_update_diff.py:1-262](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/get_section_update_diff.py#L1-L262)
- [validate_docs_structure.py:1-596](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/validate_docs_structure.py#L1-L596)
- [validate_mermaid.py:1-825](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/validate_mermaid.py#L1-L825)
- [generate_summary.py:1-501](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/generate_summary.py#L1-L501)
- [requirements.txt:1-2](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/requirements.txt#L1-L2)

</details>

# Python Helper Scripts

> **Related Pages**: [[Workflow Phases and Execution Modes|03_workflow.md]], [[Policies, Schema, and Templates|05_policies.md]]

The `scripts/` directory contains the deterministic Python utilities that back each documentation phase. The agent delegates all repository I/O — directory scanning, line-numbered file reads, git diffing, structure/diagram validation, and summary reporting — to these scripts so that citations and change detection are reproducible rather than inferred. Each script is a standalone CLI that accepts arguments, prints JSON (or writes Markdown), and exits non-zero on failure. The only third-party dependency is PyYAML ([requirements.txt:1-2](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/requirements.txt#L1-L2)).

---

<!-- BEGIN:AUTOGEN deepwiki-skill_04_scripts_context-collection -->
## Context Collection Scripts

These scripts gather the raw material the agent reasons over: the project structure and README (`collect_context.py`), the sync state between a TOC and existing docs (`collect_sync_context.py`), the git-driven update plan (`collect_update_context.py`), and line-numbered file contents for citations (`read_files.py`).

### collect_context.py

`collect_context.py` scans a repository and produces a JSON context pack containing the directory tree, file/language statistics, and README content. The top-level entry point is `collect_context`, which validates inputs (rejecting empty paths and `max_depth` outside the 1–20 range), resolves the git root, and assembles a result dictionary with `structure`, `readme`, and `metadata` keys ([collect_context.py:584-614](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/collect_context.py#L584-L614)).

The script applies a token-aware byte budget so the context pack stays within an LLM context window. `DEFAULT_MAX_BYTES` defaults to 600000 bytes (overridable via the `DOC_GEN_DEFAULT_MAX_BYTES` environment variable), split roughly 80% to structure and 20% to the README ([collect_context.py:30-36](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/collect_context.py#L30-L36)). To honor the structure budget it performs adaptive depth reduction: it scans at the requested depth and, if the serialized structure exceeds the budget, decrements the depth down to a floor of 3, marking `structure_truncated` when it had to shrink ([collect_context.py:616-655](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/collect_context.py#L616-L655)).

File handling is defensive. `detect_encoding` tries a sequence of encodings (`utf-8`, `utf-16`, several Latin and Chinese codecs) before giving up ([collect_context.py:179-193](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/collect_context.py#L179-L193)), `is_binary_file` inspects a byte sample for null bytes and decode failures to filter binaries ([collect_context.py:196-230](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/collect_context.py#L196-L230)), and `detect_language` maps extensions (and special names like `Dockerfile`/`Makefile`) to language labels using `EXTENSION_LANGUAGE_MAP` ([collect_context.py:233-244](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/collect_context.py#L233-L244)). A large `DEFAULT_EXCLUDE_PATTERNS` list filters out noise such as `.git`, `node_modules`, and `__pycache__` during the walk ([collect_context.py:38-63](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/collect_context.py#L38-L63)).

| Argument | Default | Description |
|----------|---------|-------------|
| `--repo-path` | required | Repository path to scan ([collect_context.py:713-717](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/collect_context.py#L713-L717)) |
| `--max-depth` | `10` | Maximum scan depth ([collect_context.py:718-723](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/collect_context.py#L718-L723)) |
| `--include` | none | Include patterns, repeatable ([collect_context.py:724-729](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/collect_context.py#L724-L729)) |
| `--exclude` | none | Exclude patterns, repeatable ([collect_context.py:730-735](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/collect_context.py#L730-L735)) |
| `--output` | stdout | Output file path ([collect_context.py:736-739](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/collect_context.py#L736-L739)) |

### read_files.py

`read_files.py` is the citation backbone: it reads the source files referenced by a TOC and returns their contents annotated with line numbers, so the agent can cite exact ranges. The `read_files` function resolves each path against the git root, reads it, and aggregates per-file results plus `files_read`/`files_failed` counters ([read_files.py:251-309](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/read_files.py#L251-L309)).

When line numbers are requested, each line is prefixed using a fixed-width number and a `→` delimiter, producing the `{spaces}{line_num}→{content}` format consumed elsewhere in the pipeline ([read_files.py:238-243](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/read_files.py#L238-L243)). Before reading, the script enforces a `max_size` cap (default 1 MB) and skips binary files, recording an `error` string instead of raising ([read_files.py:204-222](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/read_files.py#L204-L222)).

The `--files` argument accepts a JSON array that may contain glob patterns. `expand_glob_patterns` detects pattern characters via `is_glob_pattern` and expands them with `glob.glob(..., recursive=True)` relative to the repo, returning a sorted, de-duplicated list of concrete file paths ([read_files.py:30-68](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/read_files.py#L30-L68)). The CLI parses the JSON, expands globs, and warns when nothing matches ([read_files.py:351-360](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/read_files.py#L351-L360)).

```python
if include_line_numbers:
    numbered_lines = [f"{i+1:6}→{line}" for i, line in enumerate(lines)]
    result["content"] = "\n".join(numbered_lines)
```
The numbering loop that every citation depends on ([read_files.py:237-241](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/read_files.py#L237-L241)).

### collect_sync_context.py

`collect_sync_context.py` compares a TOC against the Markdown files already on disk to decide what must be (re)generated when the TOC structure changes. `collect_sync_context` loads the TOC, flattens its pages/sections, scans existing docs, and partitions pages into new, to-update, and unchanged sets ([collect_sync_context.py:166-268](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/collect_sync_context.py#L166-L268)).

It reads the page and section state directly from the Markdown markers: `extract_page_id` and `extract_autogen_sections` parse the `PAGE_ID` and `BEGIN:AUTOGEN` comments ([collect_sync_context.py:28-38](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/collect_sync_context.py#L28-L38)), while `is_section_content_empty` checks whether an AUTOGEN block contains only whitespace or `---` separators, so empty stubs are treated as needing generation ([collect_sync_context.py:41-65](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/collect_sync_context.py#L41-L65)). `collect_toc_pages` walks nested sections recursively, merging inherited page-level `source_files` into each section ([collect_sync_context.py:78-125](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/collect_sync_context.py#L78-L125)).

For each page present in both the TOC and on disk, it computes section-level deltas: sections that are missing or empty become `new_sections`, and sections present on disk but absent from the TOC become `deleted_sections` ([collect_sync_context.py:213-244](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/collect_sync_context.py#L213-L244)). All three CLI arguments — `--repo-path`, `--toc-file`, and `--doc-dir` — are required ([collect_sync_context.py:275-289](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/collect_sync_context.py#L275-L289)).

### collect_update_context.py

`collect_update_context.py` is the code-change counterpart to the sync script: it analyzes git changes between the TOC's recorded commit and a target commit to decide which sections need regeneration. `collect_update_context` reads `ref_commit_hash` from the TOC's `project` block as the base commit; if it is absent, the script returns an `update_mode` of `"full"` to signal that a complete regeneration is required ([collect_update_context.py:320-352](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/collect_update_context.py#L320-L352)).

In incremental mode it computes a merge base between the base and target commits and lists changed files via `git diff --name-status`, categorizing them into added, modified, deleted, and renamed sets ([collect_update_context.py:354-367](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/collect_update_context.py#L354-L367)). It then maps each changed file back to the sections whose `source_patterns` match it — using `collect_section_sources` to flatten the TOC and `match_file_to_patterns` for folder, glob, and filename matching — and attaches the affected section's `current_content` extracted from the existing doc ([collect_update_context.py:407-449](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/collect_update_context.py#L407-L449)). Added files not covered by any pattern are surfaced as `new_source_files` needing a TOC update, and deleted files list the sections they affect ([collect_update_context.py:451-480](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/collect_update_context.py#L451-L480)).

When `--include-diff` is set, the script enriches each changed file with a line-numbered patch produced by `convert_to_hunks_with_line_numbers`, which rewrites unified-diff hunks so that added (`+`), removed (`-`), and context lines carry their actual line numbers ([collect_update_context.py:103-155](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/collect_update_context.py#L103-L155)).

Sources: [collect_context.py:584-768](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/collect_context.py#L584-L768), [read_files.py:30-309](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/read_files.py#L30-L309), [collect_sync_context.py:166-268](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/collect_sync_context.py#L166-L268), [collect_update_context.py:284-506](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/collect_update_context.py#L284-L506)
<!-- END:AUTOGEN deepwiki-skill_04_scripts_context-collection -->

---

<!-- BEGIN:AUTOGEN deepwiki-skill_04_scripts_diff -->
## Git Diff Scripts

Two scripts produce line-numbered diffs across commits. `collect_git_diff.py` collects all changed files in a range for broad change analysis, while `get_section_update_diff.py` targets a specific list of files for section-level updates. Both share the same git-interaction helpers and the same line-numbering algorithm.

### Shared git helpers

Both scripts wrap git through `run_git_command`, which runs `git` as a subprocess in the repo directory and raises `RuntimeError` on a non-zero return code ([collect_git_diff.py:30-40](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/collect_git_diff.py#L30-L40)). They reuse `resolve_commit` (`git rev-parse`), `get_file_patch` (a `git diff --patch --unified=N` for one file), and `convert_to_hunks_with_line_numbers` for formatting ([get_section_update_diff.py:20-61](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/get_section_update_diff.py#L20-L61)). The line-numbering helper skips diff metadata lines (`diff --git`, `index`, `---`, `+++`) and emits deletion markers for files with a `D` status ([get_section_update_diff.py:73-125](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/get_section_update_diff.py#L73-L125)).

### collect_git_diff.py

`collect_git_diff` resolves the head and base refs, computes their merge base, and walks every changed file, building a per-file record with a formatted patch and the original/new byte sizes ([collect_git_diff.py:175-292](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/collect_git_diff.py#L175-L292)). The base reference defaults to `origin/main` and the head to `HEAD` ([collect_git_diff.py:175-201](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/collect_git_diff.py#L175-L201)). With `--include-uncommitted`, it appends staged and unstaged diffs (via `get_staged_diff` and `get_unstaged_diff`) onto the committed patch so work-in-progress changes are visible ([collect_git_diff.py:226-233](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/collect_git_diff.py#L226-L233)). Errors for individual files are captured into the per-file record rather than aborting the whole run ([collect_git_diff.py:265-274](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/collect_git_diff.py#L265-L274)).

| Argument | Default | Description |
|----------|---------|-------------|
| `--base-ref` | `origin/main` | Base reference for the diff ([collect_git_diff.py:304-308](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/collect_git_diff.py#L304-L308)) |
| `--head-ref` | `HEAD` | Head reference ([collect_git_diff.py:309-313](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/collect_git_diff.py#L309-L313)) |
| `--include-uncommitted` | off | Include staged/unstaged changes ([collect_git_diff.py:314-318](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/collect_git_diff.py#L314-L318)) |
| `--context` | `3` | Context lines per hunk ([collect_git_diff.py:319-324](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/collect_git_diff.py#L319-L324)) |
| `--no-line-numbers` | off | Disable line numbering ([collect_git_diff.py:325-330](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/collect_git_diff.py#L325-L330)) |

### get_section_update_diff.py

`get_section_update_diff` takes explicit `--base-commit` and `--target-commit` hashes plus a JSON `--file-paths` array, and returns diffs only for those files ([get_section_update_diff.py:128-184](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/get_section_update_diff.py#L128-L184)). For each file it queries the status with `get_file_status`, skips files with no status, and skips files whose patch is empty unless they were deleted ([get_section_update_diff.py:146-157](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/get_section_update_diff.py#L146-L157)). Unlike `collect_git_diff.py`, its context window defaults to `0` lines, producing tight, change-only patches suited to updating a single section ([get_section_update_diff.py:211-216](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/get_section_update_diff.py#L211-L216)).

Sources: [collect_git_diff.py:30-292](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/collect_git_diff.py#L30-L292), [get_section_update_diff.py:73-184](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/get_section_update_diff.py#L73-L184)
<!-- END:AUTOGEN deepwiki-skill_04_scripts_diff -->

---

<!-- BEGIN:AUTOGEN deepwiki-skill_04_scripts_validation-summary -->
## Validation and Summary Scripts

The final three scripts form the quality gate and reporting layer: `validate_docs_structure.py` checks each page against the TOC, `validate_mermaid.py` validates diagram syntax, and `generate_summary.py` aggregates everything into a `SUMMARY.md` report.

### validate_docs_structure.py

`validate_docs` loads the TOC, then for every page validates the matching Markdown file and accumulates issues and statistics into a `ValidationResult` ([validate_docs_structure.py:433-524](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/validate_docs_structure.py#L433-L524)). Each issue is an `Issue` dataclass carrying a file, optional line, severity (`error`/`warning`), category, message, and a `fix_hint` ([validate_docs_structure.py:45-63](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/validate_docs_structure.py#L45-L63)).

The core checks are:

| Check | Behavior |
|-------|----------|
| PAGE_ID | Flags a missing or mismatched `PAGE_ID` marker against the TOC's page id ([validate_docs_structure.py:373-394](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/validate_docs_structure.py#L373-L394)) |
| AUTOGEN pairing | Uses a stack to detect nested, orphaned, unclosed, and mismatched `BEGIN`/`END` markers ([validate_docs_structure.py:155-222](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/validate_docs_structure.py#L155-L222)) |
| Section coverage | Reports TOC sections with no AUTOGEN block as errors, and extra on-disk sections as warnings ([validate_docs_structure.py:224-246](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/validate_docs_structure.py#L224-L246)) |
| Internal links | Warns on links to files not in the TOC and errors on links whose target file is missing on disk ([validate_docs_structure.py:251-296](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/validate_docs_structure.py#L251-L296)) |
| Structure | Requires exactly one H1 heading and warns on very small files ([validate_docs_structure.py:299-342](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/validate_docs_structure.py#L299-L342)) |

Expected sections are collected recursively, so nested subsections are validated too ([validate_docs_structure.py:396-411](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/validate_docs_structure.py#L396-L411)). The serialized result marks `is_valid` as true only when there are zero errors, and `main` exits non-zero in that case so the phase can fail a pipeline ([validate_docs_structure.py:75-90](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/validate_docs_structure.py#L75-L90)). A `--fix` flag is accepted but explicitly not yet implemented ([validate_docs_structure.py:558-559](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/validate_docs_structure.py#L558-L559)).

### validate_mermaid.py

`validate_mermaid.py` extracts Mermaid code blocks from Markdown and validates them with the Mermaid CLI (`mmdc`). `extract_mermaid_blocks` scans line by line for ` ```mermaid ` fences and records each block's code along with its start/end line and character positions ([validate_mermaid.py:86-141](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/validate_mermaid.py#L86-L141)). It can accept a single file, a directory of `.md` files, a raw `--code` string, or a pre-extracted `--blocks` JSON ([validate_mermaid.py:737-790](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/validate_mermaid.py#L737-L790)).

Validation runs `mmdc` against a temporary `.mmd` file, rendering to a throwaway SVG; a zero return code means valid, otherwise the stderr is parsed ([validate_mermaid.py:477-533](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/validate_mermaid.py#L477-L533)). `_parse_error` extracts a line number, `_classify_error` maps the message to a type such as `lexical_error`, `syntax_error`, `node_error`, or `edge_error`, and `_generate_fix_hint` returns a targeted remediation string ([validate_mermaid.py:376-474](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/validate_mermaid.py#L376-L474)). If `mmdc` is not installed, `check_mermaid_cli_available` causes validation to return a `cli_unavailable` result rather than crashing ([validate_mermaid.py:335-347](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/validate_mermaid.py#L335-L347)).

The `--invalid-only` flag reduces the report to just the failing blocks plus counts of total scanned and files affected, which is the form consumed by the summary step ([validate_mermaid.py:754-762](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/validate_mermaid.py#L754-L762)). Like the structure validator, `main` returns a non-zero exit code when any block is invalid ([validate_mermaid.py:802-811](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/validate_mermaid.py#L802-L811)).

### generate_summary.py

`generate_summary.py` produces the human-readable `SUMMARY.md`. `analyze_docs` reads the TOC and each generated page, counting expected versus found AUTOGEN sections, citations, and Mermaid diagrams into a `SummaryData` aggregate ([generate_summary.py:173-287](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/generate_summary.py#L173-L287)). Citations are detected with a regex matching the `[file.ext:N](url)` / `[file.ext:N-M](url)` citation format, and diagrams are counted by ` ```mermaid ` fences ([generate_summary.py:134-152](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/generate_summary.py#L134-L152)).

It also computes source coverage by comparing the TOC's declared `source_files` (skipping glob patterns) against the filenames actually cited, splitting them into covered and uncovered lists ([generate_summary.py:247-270](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/generate_summary.py#L247-L270)). When available, it folds in the structure and Mermaid validation reports — by default reading them from `_reports/structure_validation.json` and `_reports/mermaid_invalid.json` under the doc directory ([generate_summary.py:461-476](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/generate_summary.py#L461-L476)). `generate_summary_md` then renders the overall status, per-page table, coverage sections, and a recommendations block, writing by default to `{doc_dir}/_reports/SUMMARY.md` ([generate_summary.py:290-413](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/generate_summary.py#L290-L413)).

Sources: [validate_docs_structure.py:155-524](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/validate_docs_structure.py#L155-L524), [validate_mermaid.py:86-811](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/validate_mermaid.py#L86-L811), [generate_summary.py:134-413](https://github.com/natsu1211/deepwiki-skill/blob/5623db8cf158176a7d55791d6fb9bcb992834262/.apm/skills/wiki/scripts/generate_summary.py#L134-L413)
<!-- END:AUTOGEN deepwiki-skill_04_scripts_validation-summary -->

---
