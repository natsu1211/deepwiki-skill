# Phase: repo-scan (Phase 1)

## Goal

Collect project context needed for TOC design and documentation generation.

## Inputs

| Name | Required | Default | Description |
|------|----------|---------|-------------|
| `repo_path` | Yes | - | Absolute path to the target repository (git repo root preferred) |
| `output_dir` | No | `docs/wiki` | Documentation output directory |
| `include` | No | - | Include patterns (repeatable; forwarded to script) |
| `exclude` | No | - | Exclude patterns (repeatable; forwarded to script) |
| `max_depth` | No | `10` | Max scan depth |

## Outputs

| Path | Description |
|------|-------------|
| `{output_dir}/_context/context_pack.json` | Project context JSON for `toc-design` |

## Scripts

Use `collect_context.py` to collect project context. DO NOT use any other ad-hoc script.

**Usage**:
```bash
python3 /scripts/collect_context.py \
  --repo-path "{repo_path}" \
  --max-depth 10 \
  --output "{output_dir}/_context/context_pack.json"
```

**Parameters**:

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--repo-path` | Yes | - | Absolute repository root path |
| `--max-depth` | No | `10` | Scan depth |
| `--include` | No | - | Include patterns (folder or glob, repeatable) |
| `--exclude` | No | - | Exclude patterns (folder or glob, repeatable) |
| `--output` | No | stdout | Output JSON path |

**Output JSON Structure**:
```json
{
  "structure": {
    "tree": "...",
    "file_count": 42,
    "directory_count": 8,
    "total_size": 156300,
    "total_size_formatted": "152.6 KB",
    "languages": {"Python": 25, "JavaScript": 10}
  },
  "readme": {
    "content": "...",
    "path": "README.md",
    "encoding": "utf-8"
  },
  "metadata": {
    "repo_path": "/path/to/repo",
    "has_readme": true,
    "structure_truncated": false,
    "readme_truncated": false
  }
}
```

## Workflow

1. **Validate repository**:
   - Verify `repo_path` exists and is a directory
   - Check if it's a git repository (has `.git` folder)

2. **Collect git metadata**:
   ```bash
   git rev-parse --show-toplevel  # Repo root
   git remote get-url origin       # Repo URL (if available)
   git rev-parse HEAD              # Commit hash
   ```

3. **Run context collection**:
   ```bash
   python3 /scripts/collect_context.py \
     --repo-path "{repo_path}" \
     --max-depth 10 \
     --output "{output_dir}/_context/context_pack.json"
   ```

## Validation

- [ ] `{output_dir}/_context/` directory exists
- [ ] `{output_dir}/_context/context_pack.json` is valid JSON