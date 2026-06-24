#!/usr/bin/env python3
"""
Collect update context for incremental documentation updates.

This script analyzes git changes and TOC structure to determine which
documentation sections need to be regenerated.

Usage:
    python update_context.py --repo-path /path/to/repo --toc-file toc.yaml --doc-dir ./docs/wiki/

Options:
    --repo-path PATH       Repository path (required)
    --toc-file PATH        TOC YAML file path (required)
    --doc-dir PATH         Documentation directory (required)
    --target-commit REF    Target commit (default: HEAD)
    --include-diff         Include line-numbered patch data in change_details
    --diff-context INT     Diff context lines (default: 0)
    --no-line-numbers      Don't add line numbers to diff patches
    --output PATH          Output file path (default: stdout)
"""

import argparse
import fnmatch
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional

import yaml


def run_git_command(repo_path: str, args: List[str]) -> str:
    """Run a git command and return output."""
    result = subprocess.run(
        ["git"] + args,
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"Git command failed: {result.stderr}")
    return result.stdout.strip()


def resolve_commit(repo_path: str, ref: str) -> str:
    """Resolve a git reference to a commit hash."""
    return run_git_command(repo_path, ["rev-parse", ref])


def get_merge_base(repo_path: str, ref1: str, ref2: str) -> str:
    """Get merge base between two commits."""
    return run_git_command(repo_path, ["merge-base", ref1, ref2])


def get_changed_files(repo_path: str, base: str, target: str) -> List[Dict[str, str]]:
    """Get list of changed files between commits."""
    output = run_git_command(
        repo_path,
        ["diff", "--name-status", f"{base}..{target}"]
    )

    if not output:
        return []

    files = []
    for line in output.split('\n'):
        if not line:
            continue
        parts = line.split('\t')
        if len(parts) >= 2:
            status = parts[0][0]  # First char: A, M, D, R, etc.
            path = parts[-1]  # Last part is the path (handles renames)
            files.append({"status": status, "path": path})

    return files


def get_file_patch(
    repo_path: str,
    base: str,
    target: str,
    file_path: str,
    context_lines: int = 0
) -> str:
    """Get a unified diff patch for a single file."""
    return run_git_command(
        repo_path,
        ["diff", "--patch", f"--unified={context_lines}", f"{base}..{target}", "--", file_path]
    )


def get_file_size_at_commit(repo_path: str, commit: str, file_path: str) -> int:
    """Get file size in bytes at a specific commit."""
    try:
        content = run_git_command(repo_path, ["show", f"{commit}:{file_path}"])
        return len(content.encode("utf-8"))
    except Exception:
        return 0


def convert_to_hunks_with_line_numbers(
    patch: str,
    filename: str = "",
    status: str = ""
) -> str:
    """Convert patch to unified format with line numbers."""
    if status and status.startswith("D"):
        return f"\n\n## File '{filename}' was deleted\n"

    output_lines = []
    if filename:
        output_lines.append(f"\n\n## File: '{filename}'\n")

    patch_lines = patch.splitlines()
    re_hunk_header = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@[ ]?(.*)")

    old_line_num = 0
    new_line_num = 0

    for line in patch_lines:
        if "no newline at end of file" in line.lower():
            continue

        if (
            line.startswith("diff --git")
            or line.startswith("index ")
            or line.startswith("---")
            or line.startswith("+++")
        ):
            continue

        if line.startswith("@@"):
            match = re_hunk_header.match(line)
            if match:
                old_start = int(match.group(1))
                new_start = int(match.group(3))
                old_line_num = old_start
                new_line_num = new_start
                output_lines.append(f"\n{line}\n")
            continue

        if line.startswith("-"):
            output_lines.append(f"-{old_line_num} {line[1:]}\n")
            old_line_num += 1
        elif line.startswith("+"):
            output_lines.append(f"+{new_line_num} {line[1:]}\n")
            new_line_num += 1
        else:
            output_lines.append(f"{new_line_num} {line}\n")
            old_line_num += 1
            new_line_num += 1

    return "".join(output_lines).rstrip()


def load_toc(toc_path: str) -> Dict[str, Any]:
    """Load and parse TOC YAML file."""
    path = Path(toc_path)
    if not path.exists():
        raise FileNotFoundError(f"TOC file not found: {toc_path}")

    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def match_file_to_patterns(filepath: str, patterns: List[str]) -> bool:
    """Check if a file path matches any pattern."""
    for pattern in patterns:
        normalized_path = filepath.replace('\\', '/')
        normalized_pattern = pattern.replace('\\', '/')

        # Folder path matching
        if normalized_pattern.endswith('/'):
            folder = normalized_pattern.rstrip('/')
            if normalized_path.startswith(folder + '/') or normalized_path.startswith(folder):
                return True
            continue

        # Glob matching
        if fnmatch.fnmatch(normalized_path, normalized_pattern):
            return True

        # Filename matching
        if '/' not in normalized_pattern and '*' not in normalized_pattern:
            if Path(normalized_path).name == normalized_pattern:
                return True

    return False


def collect_section_sources(toc: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """Collect source file patterns for all sections in TOC."""
    sections_map = {}

    for page in toc.get("pages", []):
        page_id = page.get("id", "")
        page_file = page.get("filename", "")
        page_sources = page.get("source_files", [])

        def process_section(section: Dict, inherited_sources: List[str], depth: int = 0):
            section_id = section.get("id", "")
            section_sources = section.get("source_files", [])
            all_sources = inherited_sources + section_sources

            sections_map[section_id] = {
                "page_id": page_id,
                "page_file": page_file,
                "section_id": section_id,
                "section_title": section.get("title", ""),
                "source_patterns": all_sources,
                "autogen": section.get("autogen", False),
                "depth": depth,
            }

            for subsection in section.get("sections", []):
                process_section(subsection, all_sources, depth + 1)

        for section in page.get("sections", []):
            process_section(section, page_sources)

    return sections_map


def extract_autogen_content(content: str, section_id: str) -> str:
    """Extract content of an AUTOGEN section."""
    begin_pattern = rf'<!-- BEGIN:AUTOGEN {re.escape(section_id)} -->\n?'
    end_pattern = rf'<!-- END:AUTOGEN {re.escape(section_id)} -->'

    begin_match = re.search(begin_pattern, content)
    if not begin_match:
        return ""

    content_start = begin_match.end()
    end_match = re.search(end_pattern, content[content_start:])
    if not end_match:
        return ""

    return content[content_start:content_start + end_match.start()]


def extract_autogen_section_content(content: str) -> Dict[str, str]:
    """Extract content inside all AUTOGEN blocks (without markers)."""
    result = {}
    begin_pattern = r'<!-- BEGIN:AUTOGEN (\S+) -->\n?'
    begin_matches = list(re.finditer(begin_pattern, content))

    for begin_match in begin_matches:
        section_id = begin_match.group(1)
        content_start = begin_match.end()
        end_pattern = rf'<!-- END:AUTOGEN {re.escape(section_id)} -->'
        end_match = re.search(end_pattern, content[content_start:])
        if end_match:
            content_end = content_start + end_match.start()
            result[section_id] = content[content_start:content_end]

    return result


def collect_doc_metadata(doc_dir: str) -> Dict[str, Dict[str, Any]]:
    """Collect metadata from markdown files in the documentation directory."""
    doc_path = Path(doc_dir)
    if not doc_path.exists():
        return {}

    docs_metadata = {}
    for md_file in doc_path.glob("*.md"):
        try:
            content = md_file.read_text(encoding='utf-8', errors='replace')
            autogen_contents = extract_autogen_section_content(content)
            docs_metadata[md_file.name] = {
                "file": md_file.name,
                "path": str(md_file),
                "autogen_sections": list(autogen_contents.keys()),
                "exists": True,
            }
        except Exception:
            continue

    return docs_metadata


def collect_update_context(
    repo_path: str,
    toc_file: str,
    doc_dir: str,
    target_commit: str = "HEAD",
    include_diff: bool = False,
    diff_context: int = 0,
    add_line_numbers: bool = True
) -> Dict[str, Any]:
    """
    Collect context for incremental documentation update.

    Args:
        repo_path: Repository path
        toc_file: TOC YAML file path
        doc_dir: Documentation directory
        target_commit: Target commit to update to
        include_diff: Whether to include line-numbered patch data
        diff_context: Number of context lines for diff patches
        add_line_numbers: Whether to add line numbers to patches

    Returns:
        Update context dictionary
    """
    # Resolve paths
    repo = Path(repo_path).resolve()
    repo_str = str(repo)

    toc_path = Path(toc_file)
    if not toc_path.is_absolute():
        toc_path = repo / toc_file

    doc_path = Path(doc_dir)
    if not doc_path.is_absolute():
        doc_path = repo / doc_dir

    # Load TOC
    toc = load_toc(str(toc_path))
    project = toc.get("project", {})

    # Get version tracking from TOC
    base_commit = project.get("ref_commit_hash")
    toc_updated_at = project.get("updated_at")

    # Resolve target commit
    target_hash = resolve_commit(repo_str, target_commit)

    # Collect document metadata
    docs_metadata = collect_doc_metadata(str(doc_path))

    # If no base commit, need full generation
    if not base_commit:
        return {
            "update_mode": "full",
            "base_commit": None,
            "target_commit": target_hash,
            "commit_range": None,
            "changed_files": [],
            "sections_to_update": [],
            "new_source_files": [],
            "deleted_source_files": [],
            "docs_metadata": docs_metadata,
            "metadata": {
                "total_changed_files": 0,
                "total_sections_to_update": 0,
                "docs_analyzed": len(docs_metadata),
                "requires_full_generation": True
            }
        }

    # Get merge base for proper diff
    try:
        merge_base = get_merge_base(repo_str, base_commit, target_hash)
    except RuntimeError:
        merge_base = base_commit

    # Get changed files
    changed_files = get_changed_files(repo_str, merge_base, target_hash)

    # Categorize changes
    new_files = [f for f in changed_files if f["status"] == "A"]
    modified_files = [f for f in changed_files if f["status"] == "M"]
    deleted_files = [f for f in changed_files if f["status"] == "D"]
    renamed_files = [f for f in changed_files if f["status"] == "R"]

    # Collect section sources
    sections_map = collect_section_sources(toc)

    # Find sections to update
    sections_to_update = []
    changed_paths = [f["path"] for f in changed_files]

    diff_cache: Dict[str, Dict[str, Any]] = {}
    if include_diff:
        for file_info in changed_files:
            path = file_info["path"]
            status = file_info["status"]
            try:
                patch = get_file_patch(repo_str, merge_base, target_hash, path, diff_context)
            except Exception:
                patch = ""

            if not patch.strip() and not status.startswith("D"):
                continue

            formatted_patch = patch
            if add_line_numbers:
                formatted_patch = convert_to_hunks_with_line_numbers(patch, path, status)

            original_size = get_file_size_at_commit(repo_str, merge_base, path)
            new_size = get_file_size_at_commit(repo_str, target_hash, path)
            if status.startswith("D"):
                new_size = 0

            diff_cache[path] = {
                "formatted_patch": formatted_patch,
                "original_size": original_size,
                "new_size": new_size,
                "is_deleted": status.startswith("D"),
            }

    doc_contents_cache: Dict[str, Dict[str, str]] = {}

    for section_id, section_info in sections_map.items():
        if not section_info.get("autogen", False):
            continue

        patterns = section_info.get("source_patterns", [])
        if not patterns:
            continue

        # Find matched files
        matched = [p for p in changed_paths if match_file_to_patterns(p, patterns)]
        if matched:
            # Get current content from doc
            current_content = ""
            page_file = section_info["page_file"]
            doc_file = None
            if page_file in docs_metadata:
                doc_file = Path(docs_metadata[page_file].get("path", ""))

            if doc_file and doc_file.exists():
                try:
                    cache_key = str(doc_file)
                    if cache_key not in doc_contents_cache:
                        content = doc_file.read_text(encoding='utf-8', errors='replace')
                        doc_contents_cache[cache_key] = extract_autogen_section_content(content)
                    current_content = doc_contents_cache[cache_key].get(section_id, "")
                except Exception:
                    pass

            change_details = []
            for file_info in changed_files:
                if file_info["path"] not in matched:
                    continue
                detail = dict(file_info)
                if include_diff and file_info["path"] in diff_cache:
                    detail.update(diff_cache[file_info["path"]])
                change_details.append(detail)

            sections_to_update.append({
                **section_info,
                "matched_files": matched,
                "current_content": current_content,
                "change_details": change_details
            })

    # Find uncovered new files
    covered_patterns = set()
    for info in sections_map.values():
        covered_patterns.update(info.get("source_patterns", []))

    new_source_files = []
    for f in new_files:
        is_covered = any(match_file_to_patterns(f["path"], [p]) for p in covered_patterns)
        if not is_covered:
            new_source_files.append({
                "path": f["path"],
                "status": "A",
                "needs_toc_update": True
            })

    # Find deleted files affecting docs
    deleted_source_files = []
    for f in deleted_files:
        affected = []
        for section_id, info in sections_map.items():
            patterns = info.get("source_patterns", [])
            if match_file_to_patterns(f["path"], patterns):
                affected.append(section_id)

        if affected:
            deleted_source_files.append({
                "path": f["path"],
                "status": "D",
                "affected_sections": affected
            })

    return {
        "update_mode": "incremental",
        "base_commit": base_commit,
        "target_commit": target_hash,
        "commit_range": f"{merge_base[:7]}..{target_hash[:7]}",
        "toc_file": str(toc_path),
        "toc_updated_at": toc_updated_at,
        "changed_files": changed_files,
        "sections_to_update": sections_to_update,
        "new_source_files": new_source_files,
        "deleted_source_files": deleted_source_files,
        "docs_metadata": docs_metadata,
        "metadata": {
            "total_changed_files": len(changed_files),
            "total_new_files": len(new_files),
            "total_modified_files": len(modified_files),
            "total_deleted_files": len(deleted_files),
            "total_renamed_files": len(renamed_files),
            "total_sections_to_update": len(sections_to_update),
            "total_new_source_files": len(new_source_files),
            "total_deleted_source_files": len(deleted_source_files),
            "docs_analyzed": len(docs_metadata),
            "requires_full_generation": False
        }
    }


def main():
    parser = argparse.ArgumentParser(
        description="Collect update context for incremental documentation"
    )
    parser.add_argument(
        "--repo-path",
        required=True,
        help="Repository path"
    )
    parser.add_argument(
        "--toc-file",
        required=True,
        help="TOC YAML file path"
    )
    parser.add_argument(
        "--doc-dir",
        required=True,
        help="Documentation directory"
    )
    parser.add_argument(
        "--target-commit",
        default="HEAD",
        help="Target commit (default: HEAD)"
    )
    parser.add_argument(
        "--include-diff",
        action="store_true",
        help="Include line-numbered patch data in change_details"
    )
    parser.add_argument(
        "--diff-context",
        type=int,
        default=0,
        help="Number of context lines for diff patches (default: 0)"
    )
    parser.add_argument(
        "--no-line-numbers",
        action="store_false",
        dest="add_line_numbers",
        help="Don't add line numbers to diff patches"
    )
    parser.add_argument(
        "--output",
        help="Output file path (default: stdout)"
    )

    args = parser.parse_args()
    if args.add_line_numbers is None:
        args.add_line_numbers = True

    try:
        result = collect_update_context(
            repo_path=args.repo_path,
            toc_file=args.toc_file,
            doc_dir=args.doc_dir,
            target_commit=args.target_commit,
            include_diff=args.include_diff,
            diff_context=args.diff_context,
            add_line_numbers=args.add_line_numbers
        )

        output = json.dumps(result, ensure_ascii=False, indent=2)

        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(output, encoding='utf-8')
            print(f"Update context saved to: {args.output}", file=sys.stderr)
        else:
            print(output)

        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except RuntimeError as e:
        print(f"Git error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
