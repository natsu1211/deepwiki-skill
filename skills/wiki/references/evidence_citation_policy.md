# Evidence Writing Policy

This document defines the rules for evidence-base writing requirements for wiki documentation.

1. **Source Citation**

**Every major claim must be backed by citations from actual source files.**

- Never guess or infer information
- Never make up line numbers
- Only describe functionality present in source code
- If information is missing, state it explicitly

## Citation Format

### URL Structure

```
{repo_base_url}/{ref_commit_hash}/{file_path}#L{start}
{repo_base_url}/{ref_commit_hash}/{file_path}#L{start}-L{end}
```

Components:
- `repo_base_url`: Base URL without commit hash (e.g., `https://github.com/owner/repo/blob`)
- `ref_commit_hash`: Git commit hash for permanent links
- `file_path`: Relative path from repository root
- `start`: Starting line number
- `end`: Ending line number (for ranges)

### Link Format

**Single line**:
```markdown
[filename.ext:42](https://github.com/owner/repo/blob/abc123/path/to/file.ext#L42)
```

**Line range**:
```markdown
[filename.ext:42-50](https://github.com/owner/repo/blob/abc123/path/to/file.ext#L42-L50)
```

### Display Text Rules

| Component | Rule | Example |
|-----------|------|---------|
| Filename | Use only the filename (no directory path) | `Button.tsx` not `src/components/Button.tsx` |
| Line numbers | Use actual numbers from file content | `:42` or `:42-50` |
| Separator | Use colon between filename and lines | `Button.tsx:42` |

## Citation Placement

### Inline Citations

Place citations immediately after the claim, **wrapped in parentheses**:

```markdown
The Button component accepts a `variant` prop that controls its appearance ([Button.tsx:15-20](url)).
```

**IMPORTANT**: 
- The citation MUST come BEFORE the period (as part of the sentence), not after. The period marks the end of the entire statement including its citation.
- Inline citations MUST be wrapped in parentheses `()` to visually separate them from the surrounding text. This improves readability and makes citations clearly identifiable.

Examples:
- Correct: `The function validates input. ([validator.ts:42](url))`
- Wrong: `The function validates input. [validator.ts:42](url)`

### End-of-Section Citations

Summarize all sources at the end of each section:

```markdown
Source: [Button.tsx:15-20](url), [types.ts:5-10](url)
<!-- END:AUTOGEN section_id -->
```

### Citation in Tables

Include citations in table cells, **wrapped in parentheses**:

```markdown
| Component | Purpose |
|-----------|---------|
| Button | Renders clickable buttons ([Button.tsx:1-30](url)) |
| Input | Handles text input ([Input.tsx:1-45](url)) |
```

## Citation Requirements

### Citation Distribution

- Spread citations throughout the section
- Don't cluster all citations at the end
- Each major claim should have a citation nearby

### Extracting Line Numbers

1. The line number appears at the start of each line (before `→`)
2. Use these exact numbers in citations
3. Never guess or estimate line numbers

## What NOT to Cite

- General programming concepts
- Standard library functions
- Well-known patterns
- Your own explanations and summaries

2. **Code Examples**
- Prefer real code from source files over hypothetical ones
- Extract line numbers from the file content (shown at start of each line)
- Include line numbers: `` `file.cs:42` `` where 42 is the **actual line number from the file**
- Copy code exactly as shown (excluding the line number prefix)
- Prefer real examples over hypotheticals

3. **Accuracy**: Only describe functionality present in source code
- ALL information MUST come from source files
- Do NOT infer, invent, or use external knowledge
- Use actual line numbers from file content for all citations
- If information is missing, state it explicitly

4. **Tables (RECOMMENDED)**:
- Summarize API endpoints, configuration, data models, features
- Always include: Name/Endpoint, Type/Method, Description
- Add relevant columns: Parameters, Default Values, Constraints

5. **Code Snippets (OPTIONAL but valuable)**:
- Include short, relevant code from source files
- Well-formatted with language identifiers
- Illustrate key implementations, patterns, configurations

6. **Language**: Generate content in the language specified by locale code
- Default: ja-JP (Japanese)
- Respect locale from TOC `project.language` field