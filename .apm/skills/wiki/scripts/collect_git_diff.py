#!/usr/bin/env python3
"""
Collect git diff data for analysis.

This script collects git changes between commits with optional line numbers
and context extension.

Usage:
    python collect_git_diff.py --repo-path /path/to/repo [options]

Options:
    --repo-path PATH           Repository path (required)
    --base-ref REF             Base reference (default: origin/main)
    --head-ref REF             Head reference (default: HEAD)
    --include-uncommitted      Include staged/unstaged changes
    --context INT              Context lines for diff (default: 3)
    --no-line-numbers          Don't add line numbers
    --output PATH              Output file path (default: stdout)
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional


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
            status = parts[0][0]
            path = parts[-1]
            files.append({"status": status, "path": path})

    return files


def get_file_patch(
    repo_path: str,
    base: str,
    target: str,
    file_path: str,
    context_lines: int = 3
) -> str:
    """Get a unified diff patch for a single file."""
    return run_git_command(
        repo_path,
        ["diff", "--patch", f"--unified={context_lines}", f"{base}..{target}", "--", file_path]
    )


def get_file_content_at_commit(repo_path: str, commit: str, file_path: str) -> Optional[str]:
    """Get file content at a specific commit."""
    try:
        return run_git_command(repo_path, ["show", f"{commit}:{file_path}"])
    except Exception:
        return None


def get_staged_diff(repo_path: str, file_path: str, context_lines: int = 0) -> str:
    """Get staged diff for a file."""
    try:
        return run_git_command(
            repo_path,
            ["diff", "--cached", f"--unified={context_lines}", "--", file_path]
        )
    except Exception:
        return ""


def get_unstaged_diff(repo_path: str, file_path: str, context_lines: int = 0) -> str:
    """Get unstaged diff for a file."""
    try:
        return run_git_command(
            repo_path,
            ["diff", f"--unified={context_lines}", "--", file_path]
        )
    except Exception:
        return ""


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


def collect_git_diff(
    repo_path: str,
    base_ref: str = "origin/main",
    head_ref: Optional[str] = None,
    include_uncommitted: bool = False,
    context_lines: int = 3,
    add_line_numbers: bool = True
) -> Dict[str, Any]:
    """
    Collect git diff data for analysis.

    Args:
        repo_path: Repository path
        base_ref: Base reference (default: origin/main)
        head_ref: Head reference (default: HEAD)
        include_uncommitted: Include staged/unstaged changes
        context_lines: Number of context lines for diff
        add_line_numbers: Whether to add line numbers

    Returns:
        Dictionary containing diff data and metadata
    """
    repo = Path(repo_path).resolve()
    repo_str = str(repo)

    # Resolve commits
    head = head_ref or "HEAD"
    head_hash = resolve_commit(repo_str, head)
    base_hash = resolve_commit(repo_str, base_ref)

    # Get merge base
    try:
        merge_base_hash = get_merge_base(repo_str, base_hash, head_hash)
    except RuntimeError:
        merge_base_hash = base_hash

    # Get changed files
    changed_files = get_changed_files(repo_str, merge_base_hash, head_hash)

    # Process each file
    files = []
    total_size = 0

    for file_info in changed_files:
        filepath = file_info["path"]
        status = file_info["status"]

        try:
            # Get patch
            patch = get_file_patch(repo_str, merge_base_hash, head_hash, filepath, context_lines)

            # Add uncommitted changes if requested
            if include_uncommitted:
                staged = get_staged_diff(repo_str, filepath, context_lines)
                unstaged = get_unstaged_diff(repo_str, filepath, context_lines)
                if staged.strip():
                    patch = patch + "\n" + staged if patch.strip() else staged
                if unstaged.strip():
                    patch = patch + "\n" + unstaged if patch.strip() else unstaged

            if not patch.strip() and not status.startswith("D"):
                continue

            # Get file sizes
            original_content = get_file_content_at_commit(repo_str, merge_base_hash, filepath)
            new_content = get_file_content_at_commit(repo_str, head_hash, filepath)

            original_size = len(original_content.encode("utf-8")) if original_content else 0
            new_size = len(new_content.encode("utf-8")) if new_content else 0

            if status.startswith("D"):
                new_size = 0

            # Format patch
            formatted_patch = patch
            if add_line_numbers:
                formatted_patch = convert_to_hunks_with_line_numbers(patch, filepath, status)

            file_data = {
                "filename": filepath,
                "status": status,
                "formatted_patch": formatted_patch,
                "original_size": original_size,
                "new_size": new_size,
                "is_deleted": status.startswith("D")
            }

            files.append(file_data)
            total_size += len(formatted_patch.encode("utf-8"))

        except Exception as e:
            files.append({
                "filename": filepath,
                "status": status,
                "formatted_patch": f"## File: '{filepath}'\n[Error: {e}]",
                "original_size": 0,
                "new_size": 0,
                "is_deleted": False,
                "error": str(e)
            })

    files_processed = sum(1 for f in files if not f.get("error"))
    files_with_errors = sum(1 for f in files if f.get("error"))

    return {
        "repo": repo_str,
        "base_ref": base_ref,
        "head_ref": head or "HEAD",
        "range": f"{merge_base_hash[:7]}..{head_hash[:7]}",
        "merge_base": merge_base_hash,
        "changed_files": changed_files,
        "files": files,
        "files_processed": files_processed,
        "files_with_errors": files_with_errors,
        "total_size": total_size,
        "context_lines": context_lines,
        "add_line_numbers": add_line_numbers,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Collect git diff data for analysis"
    )
    parser.add_argument(
        "--repo-path",
        required=True,
        help="Repository path"
    )
    parser.add_argument(
        "--base-ref",
        default="origin/main",
        help="Base reference (default: origin/main)"
    )
    parser.add_argument(
        "--head-ref",
        default=None,
        help="Head reference (default: HEAD)"
    )
    parser.add_argument(
        "--include-uncommitted",
        action="store_true",
        help="Include staged/unstaged changes"
    )
    parser.add_argument(
        "--context",
        type=int,
        default=3,
        help="Context lines for diff (default: 3)"
    )
    parser.add_argument(
        "--no-line-numbers",
        action="store_false",
        dest="add_line_numbers",
        help="Don't add line numbers to patches"
    )
    parser.add_argument(
        "--output",
        help="Output file path (default: stdout)"
    )

    args = parser.parse_args()

    try:
        result = collect_git_diff(
            repo_path=args.repo_path,
            base_ref=args.base_ref,
            head_ref=args.head_ref,
            include_uncommitted=args.include_uncommitted,
            context_lines=args.context,
            add_line_numbers=args.add_line_numbers
        )

        output = json.dumps(result, ensure_ascii=False, indent=2)

        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(output, encoding="utf-8")
            print(f"Diff saved to: {args.output}", file=sys.stderr)
        else:
            print(output)

        return 0

    except RuntimeError as e:
        print(f"Git error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
