#!/usr/bin/env python3
"""
Read multiple files and return contents with line numbers.

This script reads source files and adds line numbers for citation purposes
in wiki documentation generation.

Usage:
    python read_files.py --repo-path /path/to/repo --files '["file1.py", "file2.ts"]'

    # With glob patterns
    python read_files.py --repo-path /path/to/repo --files '["src/**/*.cs", "README.md"]'

Options:
    --repo-path PATH       Repository path (required)
    --files JSON           JSON array of file paths or glob patterns (required)
    --line-numbers         Add line numbers (default: true)
    --max-size BYTES       Maximum file size in bytes (default: 1MB)
    --output PATH          Output file path (default: stdout)
"""

import argparse
import glob as glob_module
import json
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional


def is_glob_pattern(path: str) -> bool:
    """Check if a path contains glob pattern characters."""
    return '*' in path or '?' in path or '[' in path


def expand_glob_patterns(repo_path: str, file_paths: List[str]) -> List[str]:
    """Expand glob patterns in file paths to concrete file paths.

    Args:
        repo_path: Repository root path
        file_paths: List of file paths, may contain glob patterns

    Returns:
        List of concrete file paths (no duplicates, sorted)
    """
    repo = Path(repo_path)
    expanded = set()

    for pattern in file_paths:
        if is_glob_pattern(pattern):
            # Expand glob pattern relative to repo
            full_pattern = str(repo / pattern)
            matches = glob_module.glob(full_pattern, recursive=True)
            for match in matches:
                match_path = Path(match)
                # Only include files, not directories
                if match_path.is_file():
                    # Convert back to repo-relative path
                    try:
                        rel_path = match_path.relative_to(repo)
                        expanded.add(str(rel_path))
                    except ValueError:
                        # Path is not relative to repo, use as-is
                        expanded.add(match)
        else:
            # Not a glob pattern, use as-is
            expanded.add(pattern)

    return sorted(expanded)


# Language detection by extension
EXTENSION_LANGUAGE_MAP = {
    '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript',
    '.jsx': 'JavaScript React', '.tsx': 'TypeScript React',
    '.java': 'Java', '.c': 'C', '.cpp': 'C++', '.cc': 'C++',
    '.h': 'C/C++ Header', '.hpp': 'C++ Header',
    '.go': 'Go', '.rs': 'Rust', '.rb': 'Ruby', '.php': 'PHP',
    '.swift': 'Swift', '.kt': 'Kotlin', '.scala': 'Scala',
    '.sh': 'Shell', '.bash': 'Bash', '.zsh': 'Zsh',
    '.cs': 'C#', '.fs': 'F#', '.vb': 'Visual Basic',
    '.r': 'R', '.R': 'R', '.sql': 'SQL',
    '.md': 'Markdown', '.rst': 'reStructuredText',
    '.html': 'HTML', '.css': 'CSS', '.scss': 'SCSS',
    '.json': 'JSON', '.xml': 'XML', '.yaml': 'YAML', '.yml': 'YAML',
    '.toml': 'TOML', '.ini': 'INI',
    '.vue': 'Vue', '.svelte': 'Svelte', '.dart': 'Dart', '.lua': 'Lua',
}


def detect_language(file_path: str) -> Optional[str]:
    """Detect programming language from file extension."""
    ext = Path(file_path).suffix.lower()
    name = Path(file_path).name.lower()

    if name.startswith('dockerfile'):
        return 'Dockerfile'
    if name in ['makefile', 'gnumakefile']:
        return 'Makefile'

    return EXTENSION_LANGUAGE_MAP.get(ext)


def detect_encoding(file_path: Path) -> str:
    """Detect file encoding by trying multiple encodings."""
    encodings = ['utf-8', 'utf-16', 'iso-8859-1', 'latin-1', 'ascii', 'gb2312', 'gbk']

    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                f.read(1024)
            return encoding
        except (UnicodeDecodeError, UnicodeError):
            continue
        except Exception:
            continue

    return 'utf-8'  # Default fallback


def is_binary_file(file_path: Path, sample_size: int = 8192) -> bool:
    """Check if a file is binary by examining its content."""
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(sample_size)

        if not chunk:
            return False

        # Check for null bytes
        if b'\x00' in chunk:
            return True

        # Try to decode as UTF-8
        try:
            chunk.decode('utf-8')
            return False
        except UnicodeDecodeError:
            pass

        # Try other encodings
        for encoding in ['latin-1', 'iso-8859-1', 'cp1252']:
            try:
                chunk.decode(encoding)
                return False
            except (UnicodeDecodeError, LookupError):
                continue

        return True

    except Exception:
        return False


def format_size(size_bytes: int) -> str:
    """Format byte size to human-readable string."""
    size = float(size_bytes)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


def find_git_root(start_path: str) -> str:
    """Find git repository root by searching for .git directory."""
    current = Path(start_path).resolve()

    while current != current.parent:
        if (current / ".git").exists():
            return str(current)
        current = current.parent

    if (current / ".git").exists():
        return str(current)

    return str(Path(start_path).resolve())


def read_file_with_line_numbers(
    file_path: Path,
    include_line_numbers: bool = True,
    max_size: int = 1024 * 1024
) -> Dict[str, Any]:
    """
    Read a file and return its content with metadata.

    Args:
        file_path: Path to the file
        include_line_numbers: Whether to add line numbers
        max_size: Maximum file size in bytes

    Returns:
        Dictionary with file content and metadata
    """
    result = {
        "path": str(file_path),
        "content": None,
        "size": 0,
        "encoding": "unknown",
        "language": None,
        "error": None
    }

    if not file_path.exists():
        result["error"] = "File does not exist"
        return result

    if not file_path.is_file():
        result["error"] = "Path is not a file"
        return result

    try:
        size = file_path.stat().st_size
        result["size"] = size

        if size > max_size:
            result["error"] = f"File too large: {format_size(size)} (max: {format_size(max_size)})"
            return result

        if is_binary_file(file_path):
            result["error"] = "Binary file"
            return result

        # Detect encoding
        encoding = detect_encoding(file_path)
        result["encoding"] = encoding

        # Detect language
        result["language"] = detect_language(str(file_path))

        # Read content
        with open(file_path, 'r', encoding=encoding, errors='replace') as f:
            content = f.read()

        lines = content.splitlines()

        # Add line numbers if requested
        if include_line_numbers:
            # Use arrow format for clear line number separation
            numbered_lines = [f"{i+1:6}→{line}" for i, line in enumerate(lines)]
            result["content"] = "\n".join(numbered_lines)
        else:
            result["content"] = content

    except Exception as e:
        result["error"] = str(e)

    return result


def read_files(
    repo_path: str,
    file_paths: List[str],
    include_line_numbers: bool = True,
    max_size: int = 1024 * 1024
) -> Dict[str, Any]:
    """
    Read multiple files from a repository.

    Args:
        repo_path: Repository root path
        file_paths: List of file paths (relative or absolute)
        include_line_numbers: Whether to add line numbers
        max_size: Maximum file size in bytes

    Returns:
        Dictionary with file contents and metadata
    """
    # Find git root
    git_root = find_git_root(repo_path)
    root = Path(git_root)

    results = []
    total_size = 0
    files_read = 0
    files_failed = 0

    for file_path in file_paths:
        # Resolve path
        path = Path(file_path)
        original_path = file_path  # Keep original for relative path storage
        if not path.is_absolute():
            path = root / file_path

        # Read file
        result = read_file_with_line_numbers(
            path,
            include_line_numbers=include_line_numbers,
            max_size=max_size
        )

        # Store relative path (original) instead of absolute path
        result["path"] = original_path

        if result["error"]:
            files_failed += 1
        else:
            files_read += 1
            total_size += result["size"]

        results.append(result)

    return {
        "files": results,
        "total_size": total_size,
        "total_size_formatted": format_size(total_size),
        "files_read": files_read,
        "files_failed": files_failed
    }


def main():
    parser = argparse.ArgumentParser(
        description="Read files with line numbers for wiki generation"
    )
    parser.add_argument(
        "--repo-path",
        required=True,
        help="Repository path"
    )
    parser.add_argument(
        "--files",
        required=True,
        help="JSON array of file paths"
    )
    parser.add_argument(
        "--line-numbers",
        action="store_true",
        default=True,
        help="Add line numbers (default: true)"
    )
    parser.add_argument(
        "--no-line-numbers",
        action="store_false",
        dest="line_numbers",
        help="Don't add line numbers"
    )
    parser.add_argument(
        "--max-size",
        type=int,
        default=1024 * 1024,
        help="Maximum file size in bytes (default: 1MB)"
    )
    parser.add_argument(
        "--output",
        help="Output file path (default: stdout)"
    )

    args = parser.parse_args()

    try:
        # Parse file paths
        file_paths = json.loads(args.files)
        if not isinstance(file_paths, list):
            raise ValueError("--files must be a JSON array")

        # Expand glob patterns to concrete file paths
        expanded_paths = expand_glob_patterns(args.repo_path, file_paths)
        if not expanded_paths:
            print(f"Warning: No files matched the patterns: {file_paths}", file=sys.stderr)

        result = read_files(
            repo_path=args.repo_path,
            file_paths=expanded_paths,
            include_line_numbers=args.line_numbers,
            max_size=args.max_size
        )

        output = json.dumps(result, ensure_ascii=False, indent=2)

        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(output, encoding='utf-8')
            print(f"Output saved to: {args.output}", file=sys.stderr)
        else:
            print(output)

        return 0

    except json.JSONDecodeError as e:
        print(f"Error parsing --files JSON: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
