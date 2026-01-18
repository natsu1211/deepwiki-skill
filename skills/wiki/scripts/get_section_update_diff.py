#!/usr/bin/env python3
"""
Get line-numbered diffs for specific files in a commit range.

Usage:
    python get_section_update_diff.py --repo-path /path/to/repo \
      --base-commit abc123 --target-commit def456 \
      --file-paths '["src/foo.py", "src/bar.py"]'
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any, List


def run_git_command(repo_path: str, args: List[str]) -> str:
    """Run a git command and return stdout."""
    result = subprocess.run(
        ["git"] + args,
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git command failed")
    return result.stdout.strip()


def resolve_commit(repo_path: str, ref: str) -> str:
    """Resolve a git reference to a commit hash."""
    return run_git_command(repo_path, ["rev-parse", ref])


def get_file_status(repo_path: str, base: str, target: str, file_path: str) -> str:
    """Get git status for a single file between two commits."""
    output = run_git_command(
        repo_path,
        ["diff", "--name-status", f"{base}..{target}", "--", file_path]
    )
    if not output:
        return ""
    parts = output.split("\t")
    return parts[0] if parts else ""


def get_file_patch(
    repo_path: str,
    base: str,
    target: str,
    file_path: str,
    context_lines: int
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


def get_section_update_diff(
    repo_path: str,
    base_commit: str,
    target_commit: str,
    file_paths: List[str],
    context_lines: int = 0,
    add_line_numbers: bool = True
) -> Dict[str, Any]:
    """Get line-numbered diffs for specific files."""
    repo = Path(repo_path).resolve()
    repo_str = str(repo)

    base_hash = resolve_commit(repo_str, base_commit)
    target_hash = resolve_commit(repo_str, target_commit)

    files = []
    total_size = 0

    for file_path in file_paths:
        status = get_file_status(repo_str, base_hash, target_hash, file_path)
        if not status:
            continue

        try:
            patch = get_file_patch(repo_str, base_hash, target_hash, file_path, context_lines)
        except Exception:
            patch = ""

        if not patch.strip() and not status.startswith("D"):
            continue

        formatted_patch = patch
        if add_line_numbers:
            formatted_patch = convert_to_hunks_with_line_numbers(patch, file_path, status)

        original_size = get_file_size_at_commit(repo_str, base_hash, file_path)
        new_size = get_file_size_at_commit(repo_str, target_hash, file_path)
        if status.startswith("D"):
            new_size = 0

        file_info = {
            "filename": file_path,
            "status": status,
            "formatted_patch": formatted_patch,
            "original_size": original_size,
            "new_size": new_size,
            "is_deleted": status.startswith("D"),
        }
        files.append(file_info)
        total_size += len(formatted_patch.encode("utf-8"))

    return {
        "files": files,
        "total_size": total_size,
        "files_processed": len(files),
        "commit_range": f"{base_hash[:7]}..{target_hash[:7]}",
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Get line-numbered diffs for specific files"
    )
    parser.add_argument(
        "--repo-path",
        required=True,
        help="Repository path"
    )
    parser.add_argument(
        "--base-commit",
        required=True,
        help="Base commit hash"
    )
    parser.add_argument(
        "--target-commit",
        required=True,
        help="Target commit hash"
    )
    parser.add_argument(
        "--file-paths",
        required=True,
        help="JSON array of file paths"
    )
    parser.add_argument(
        "--context",
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
        file_paths = json.loads(args.file_paths)
        if not isinstance(file_paths, list):
            raise ValueError("--file-paths must be a JSON array")

        result = get_section_update_diff(
            repo_path=args.repo_path,
            base_commit=args.base_commit,
            target_commit=args.target_commit,
            file_paths=file_paths,
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
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
