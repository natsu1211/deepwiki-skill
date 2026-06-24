#!/usr/bin/env python3
"""
Collect project context for wiki generation.

This script scans a repository and collects project structure and README
for use in wiki documentation generation.

Usage:
    python collect_context.py --repo-path /path/to/repo [options]

Options:
    --repo-path PATH       Repository path (required)
    --max-depth INT        Maximum scan depth (default: 10)
    --include PATTERN      Include patterns (repeatable)
    --exclude PATTERN      Exclude patterns (repeatable)
    --output PATH          Output file path (default: stdout)
"""

import argparse
import json
import os
import sys
import fnmatch
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from collections import defaultdict


# max_bytes ≈ max_tokens*3, Claude 200k context: keep a buffer for system/prompt/response
# adjust via env if needed.
DEFAULT_MAX_BYTES = int(os.getenv("DOC_GEN_DEFAULT_MAX_BYTES", "600000"))

# Budget allocation (approximate percentages)
STRUCTURE_BUDGET_PCT = 0.80
README_BUDGET_PCT = 0.20

# Default patterns to exclude
DEFAULT_EXCLUDE_PATTERNS = [
    '.git',
    '.svn',
    '.hg',
    'node_modules',
    '__pycache__',
    '*.pyc',
    '.venv',
    'venv',
    'env',
    '.env',
    'dist',
    'build',
    'target',
    '*.egg-info',
    '.idea',
    '.vscode',
    '.DS_Store',
    '*.log',
    '.pytest_cache',
    '.mypy_cache',
    '.tox',
    'coverage',
    '.coverage',
]

# Language detection by extension
EXTENSION_LANGUAGE_MAP = {
    '.py': 'Python',
    '.js': 'JavaScript',
    '.ts': 'TypeScript',
    '.jsx': 'JavaScript React',
    '.tsx': 'TypeScript React',
    '.java': 'Java',
    '.c': 'C',
    '.cpp': 'C++',
    '.cc': 'C++',
    '.cxx': 'C++',
    '.h': 'C/C++ Header',
    '.hpp': 'C++ Header',
    '.go': 'Go',
    '.rs': 'Rust',
    '.rb': 'Ruby',
    '.php': 'PHP',
    '.swift': 'Swift',
    '.kt': 'Kotlin',
    '.scala': 'Scala',
    '.sh': 'Shell',
    '.bash': 'Bash',
    '.zsh': 'Zsh',
    '.fish': 'Fish',
    '.ps1': 'PowerShell',
    '.r': 'R',
    '.R': 'R',
    '.m': 'MATLAB/Objective-C',
    '.sql': 'SQL',
    '.md': 'Markdown',
    '.rst': 'reStructuredText',
    '.tex': 'LaTeX',
    '.html': 'HTML',
    '.htm': 'HTML',
    '.css': 'CSS',
    '.scss': 'SCSS',
    '.sass': 'Sass',
    '.less': 'Less',
    '.json': 'JSON',
    '.xml': 'XML',
    '.yaml': 'YAML',
    '.yml': 'YAML',
    '.toml': 'TOML',
    '.ini': 'INI',
    '.cfg': 'Config',
    '.conf': 'Config',
    '.vue': 'Vue',
    '.svelte': 'Svelte',
    '.dart': 'Dart',
    '.lua': 'Lua',
    '.vim': 'VimScript',
    '.el': 'Emacs Lisp',
    '.clj': 'Clojure',
    '.ex': 'Elixir',
    '.exs': 'Elixir',
    '.erl': 'Erlang',
    '.hrl': 'Erlang',
    '.hs': 'Haskell',
    '.ml': 'OCaml',
    '.dockerfile': 'Dockerfile',
    '.proto': 'Protocol Buffers',
}


class FileReadError(Exception):
    """Raised when file reading fails."""
    pass


class EncodingDetectionError(Exception):
    """Raised when encoding detection fails."""
    pass


class ProjectScannerError(Exception):
    """Base exception for project scanner operations."""
    pass


class ValidationError(Exception):
    """Raised when input validation fails."""
    pass


@dataclass
class FileInfo:
    """Information about a file."""
    path: str
    size: int
    encoding: str
    language: Optional[str] = None
    is_binary: bool = False
    error: Optional[str] = None


@dataclass
class ScanResult:
    """Results from scanning a project."""
    root_path: str
    total_files: int = 0
    total_directories: int = 0
    total_size: int = 0
    files: List[Dict[str, Any]] = field(default_factory=list)
    language_stats: Dict[str, int] = field(default_factory=dict)
    tree_structure: str = ""
    scan_depth: int = 0


def _calculate_json_size(data: Any) -> int:
    """Calculate the UTF-8 byte size of data when serialized to JSON."""
    return len(json.dumps(data, ensure_ascii=False).encode('utf-8'))


def detect_encoding(file_path: Path) -> str:
    """Detect file encoding by trying multiple encodings."""
    encodings_to_try = ['utf-8', 'utf-16', 'iso-8859-1', 'latin-1', 'ascii', 'gb2312', 'gbk']

    for encoding in encodings_to_try:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                f.read(1024)
            return encoding
        except (UnicodeDecodeError, UnicodeError):
            continue
        except Exception:
            continue

    raise EncodingDetectionError(f"Could not detect encoding for {file_path}")


def is_binary_file(file_path: Path, sample_size: int = 8192) -> bool:
    """Check if a file is binary by examining its content."""
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(sample_size)

        if not chunk:
            return False

        if b'\x00' in chunk:
            return True

        try:
            chunk.decode('utf-8')
            return False
        except UnicodeDecodeError:
            pass

        for encoding in ['latin-1', 'iso-8859-1', 'cp1252', 'gbk', 'gb2312']:
            try:
                chunk.decode(encoding)
                return False
            except (UnicodeDecodeError, LookupError):
                continue

        text_chars = bytes(range(32, 127)) + b'\n\r\t\b\f\v'
        non_text_count = sum(1 for byte in chunk if byte not in text_chars and byte < 128)

        ascii_bytes = [b for b in chunk if b < 128]
        if ascii_bytes:
            return (non_text_count / len(ascii_bytes)) > 0.5

        return True
    except Exception:
        return False


def detect_language(file_path: str) -> Optional[str]:
    """Detect programming language from file extension."""
    path = Path(file_path)
    ext = path.suffix.lower()
    name = path.name.lower()

    if name.startswith('dockerfile'):
        return 'Dockerfile'
    if name in ['makefile', 'gnumakefile']:
        return 'Makefile'

    return EXTENSION_LANGUAGE_MAP.get(ext)


def read_file_content(
    file_path: str,
    max_size: Optional[int] = None,
    encoding: Optional[str] = None
) -> Tuple[str, str]:
    """Read file content with automatic encoding detection."""
    path = Path(file_path)

    if not path.exists():
        raise FileReadError(f"File does not exist: {file_path}")

    if not path.is_file():
        raise FileReadError(f"Path is not a file: {file_path}")

    file_size = path.stat().st_size

    if max_size and file_size > max_size:
        raise FileReadError(f"File too large: {file_size} bytes (max: {max_size})")

    if is_binary_file(path):
        raise FileReadError(f"File appears to be binary: {file_path}")

    if encoding is None:
        try:
            encoding = detect_encoding(path)
        except EncodingDetectionError as e:
            raise FileReadError(f"Failed to detect encoding: {e}") from e

    try:
        with open(path, 'r', encoding=encoding, errors='replace') as f:
            content = f.read()
        return content, encoding
    except Exception as e:
        raise FileReadError(f"Failed to read file {file_path}: {e}") from e


def get_file_info(file_path: str) -> FileInfo:
    """Get comprehensive information about a file."""
    path = Path(file_path)

    try:
        if not path.exists():
            return FileInfo(
                path=file_path,
                size=0,
                encoding="unknown",
                error="File does not exist"
            )

        size = path.stat().st_size
        is_binary = is_binary_file(path)

        if is_binary:
            return FileInfo(
                path=file_path,
                size=size,
                encoding="binary",
                is_binary=True
            )

        try:
            encoding = detect_encoding(path)
        except EncodingDetectionError:
            encoding = "unknown"

        language = detect_language(file_path)

        return FileInfo(
            path=file_path,
            size=size,
            encoding=encoding,
            language=language,
            is_binary=False
        )

    except Exception as e:
        return FileInfo(
            path=file_path,
            size=0,
            encoding="unknown",
            error=str(e)
        )


def matches_pattern(path: str, pattern: str) -> bool:
    """Check if a path matches a pattern."""
    path = path.replace('\\', '/')
    pattern = pattern.replace('\\', '/')

    path_obj = Path(path)
    path_name = path_obj.name

    if pattern.endswith('/') or (not any(c in pattern for c in '*?[')):
        folder_pattern = pattern.rstrip('/')
        if path.startswith(folder_pattern + '/'):
            return True
        if '/' + folder_pattern + '/' in path or path == folder_pattern:
            return True

    if pattern.startswith('**/') and pattern.endswith('/**'):
        dir_name = pattern[3:-3]
        parts = path.split('/')
        return dir_name in parts

    if pattern.startswith('**/'):
        suffix = pattern[3:]
        return path.endswith(suffix) or ('/' + suffix) in path

    if pattern.endswith('/**'):
        prefix = pattern[:-3]
        return path.startswith(prefix + '/') or ('/' + prefix + '/') in path

    if fnmatch.fnmatch(path_name, pattern):
        return True
    if fnmatch.fnmatch(path, pattern):
        return True

    if '**' in pattern:
        try:
            if path_obj.match(pattern):
                return True
        except ValueError:
            pass

    return False


def should_exclude(path: str, exclude_patterns: List[str]) -> bool:
    """Check if a path should be excluded based on patterns."""
    for pattern in exclude_patterns:
        if matches_pattern(path, pattern):
            return True

    return False


def should_include(path: str, include_patterns: Optional[List[str]]) -> bool:
    """Check if a path should be included based on patterns."""
    if include_patterns is None or len(include_patterns) == 0:
        return True

    for pattern in include_patterns:
        if matches_pattern(path, pattern):
            return True

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
    """Find the git repository root by searching for .git directory."""
    current = Path(start_path).resolve()

    while current != current.parent:
        if (current / ".git").exists():
            return str(current)
        current = current.parent

    if (current / ".git").exists():
        return str(current)

    return str(Path(start_path).resolve())


def generate_tree_structure(
    root_path: str,
    files: List[Dict[str, Any]],
    max_depth: Optional[int] = None
) -> str:
    """Generate a tree-like string representation of the project structure."""
    root = Path(root_path)
    tree_lines = [root.name + "/"]
    dir_tree: Dict[str, List[str]] = defaultdict(list)

    for file_info in files:
        file_path = Path(file_info["path"])
        try:
            rel_path = file_path.relative_to(root)
            parts = rel_path.parts

            if max_depth and len(parts) > max_depth:
                continue

            current = ""
            for part in parts[:-1]:
                parent = current
                current = str(Path(current) / part) if current else part
                if current not in dir_tree[parent]:
                    dir_tree[parent].append(current)

            parent = str(Path(*parts[:-1])) if len(parts) > 1 else ""
            file_entry = str(rel_path)
            if file_entry not in dir_tree[parent]:
                dir_tree[parent].append(file_entry)
        except ValueError:
            continue

    for key in dir_tree:
        dir_tree[key].sort()

    def add_tree_lines(parent: str, prefix: str, depth: int):
        if max_depth and depth >= max_depth:
            return

        entries = dir_tree.get(parent, [])
        for i, entry in enumerate(entries):
            is_last = (i == len(entries) - 1)
            entry_path = Path(entry)
            is_dir = entry in dir_tree

            if is_last:
                tree_char = "└── "
                next_prefix = prefix + "    "
            else:
                tree_char = "├── "
                next_prefix = prefix + "│   "

            name = entry_path.name
            if is_dir:
                name += "/"

            tree_lines.append(prefix + tree_char + name)

            if is_dir:
                add_tree_lines(entry, next_prefix, depth + 1)

    add_tree_lines("", "", 1)
    return "\n".join(tree_lines)


def scan_project(
    repo_path: str,
    max_depth: int = 10,
    include_patterns: Optional[List[str]] = None,
    exclude_patterns: Optional[List[str]] = None,
    include_file_stats: bool = True,
    include_git_status: bool = False
) -> ScanResult:
    """Scan a project directory and collect structure information."""
    root = Path(repo_path)

    if not root.exists():
        raise ProjectScannerError(f"Path does not exist: {repo_path}")

    if not root.is_dir():
        raise ProjectScannerError(f"Path is not a directory: {repo_path}")

    if exclude_patterns is None:
        exclude_patterns = DEFAULT_EXCLUDE_PATTERNS

    result = ScanResult(
        root_path=str(root.absolute()),
        scan_depth=max_depth
    )

    language_counts: Dict[str, int] = defaultdict(int)
    scanned_depth = 0

    try:
        for root_dir, dirs, files in os.walk(root):
            current_path = Path(root_dir)

            try:
                rel_path = current_path.relative_to(root)
                current_depth = len(rel_path.parts) if str(rel_path) != "." else 0
            except ValueError:
                continue

            if current_depth >= max_depth:
                dirs.clear()
                continue

            scanned_depth = max(scanned_depth, current_depth)

            dirs[:] = [
                d for d in dirs
                if not should_exclude(str(current_path / d), exclude_patterns)
            ]
            dirs.sort()

            result.total_directories += len(dirs)

            for filename in sorted(files):
                file_path = current_path / filename
                file_path_str = str(file_path)

                if should_exclude(file_path_str, exclude_patterns):
                    continue

                if not should_include(file_path_str, include_patterns):
                    continue

                result.total_files += 1

                if include_file_stats:
                    info = get_file_info(file_path_str)

                    file_data = {
                        "path": file_path_str,
                        "relative_path": str(file_path.relative_to(root)),
                        "size": info.size,
                        "language": info.language,
                        "is_binary": info.is_binary,
                    }

                    if include_git_status:
                        file_data["git_status"] = None

                    result.files.append(file_data)
                    result.total_size += info.size

                    if info.language:
                        language_counts[info.language] += 1

        result.language_stats = dict(language_counts)
        result.scan_depth = scanned_depth
        result.tree_structure = generate_tree_structure(
            str(root),
            result.files,
            max_depth=max_depth
        )

        return result

    except Exception as e:
        raise ProjectScannerError(f"Failed to scan project: {e}") from e


def collect_context(
    repo_path: str,
    max_depth: int = 10,
    include_patterns: Optional[List[str]] = None,
    exclude_patterns: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Collect comprehensive project context."""
    if not repo_path or not repo_path.strip():
        raise ValidationError("Repository path cannot be empty")
    if max_depth < 1:
        raise ValidationError(f"max_depth must be at least 1, got {max_depth}")
    if max_depth > 20:
        raise ValidationError(f"max_depth cannot exceed 20, got {max_depth}")
    repo_path = find_git_root(repo_path)
    repo_path_obj = Path(repo_path)

    max_bytes = DEFAULT_MAX_BYTES
    budget_used = True
    structure_truncated = False
    readme_truncated = False
    actual_max_depth = max_depth

    result: Dict[str, Any] = {
        "structure": {},
        "readme": {},
        "metadata": {
            "repo_path": str(repo_path),
            "has_readme": False,
            "budget_used": budget_used,
        }
    }

    # 1. Collect directory structure with adaptive depth reduction
    try:
        structure_budget = int(max_bytes * STRUCTURE_BUDGET_PCT) if budget_used else float('inf')
        current_depth = max_depth
        min_depth = 3
        temp_structure: Dict[str, Any] = {}
        structure_size = 0

        while current_depth >= min_depth:
            scan_result = scan_project(
                repo_path=repo_path,
                max_depth=current_depth,
                include_patterns=include_patterns,
                exclude_patterns=exclude_patterns,
                include_file_stats=True,
                include_git_status=False,
            )

            temp_structure = {
                "tree": scan_result.tree_structure,
                "file_count": scan_result.total_files,
                "directory_count": scan_result.total_directories,
                "total_size": scan_result.total_size,
                "total_size_formatted": format_size(scan_result.total_size),
                "languages": scan_result.language_stats,
            }

            structure_size = _calculate_json_size(temp_structure)

            if structure_size <= structure_budget:
                result["structure"] = temp_structure
                actual_max_depth = current_depth
                if current_depth < max_depth:
                    structure_truncated = True
                break
            current_depth -= 1
        else:
            result["structure"] = temp_structure
            actual_max_depth = min_depth
            structure_truncated = True
    except Exception as e:
        result["structure"]["error"] = str(e)

    # 2. Collect README with budget control
    readme_names = ["README.md", "README.MD", "README", "Readme.md", "readme.md"]
    for readme_name in readme_names:
        readme_path = repo_path_obj / readme_name
        if readme_path.exists() and readme_path.is_file():
            try:
                content, encoding = read_file_content(str(readme_path))

                if budget_used:
                    current_size = _calculate_json_size(result)
                    remaining_budget = max_bytes - current_size
                    readme_budget = int(max_bytes * README_BUDGET_PCT)
                    effective_readme_budget = min(readme_budget, remaining_budget)

                    if effective_readme_budget > 0:
                        content_bytes = content.encode('utf-8')
                        if len(content_bytes) > effective_readme_budget:
                            truncated_bytes = content_bytes[:effective_readme_budget]
                            content = truncated_bytes.decode('utf-8', errors='ignore')
                            readme_truncated = True
                    else:
                        content = "[README content omitted due to budget constraints]"
                        readme_truncated = True

                result["readme"] = {
                    "content": content,
                    "path": str(readme_path),
                    "encoding": encoding
                }
                result["metadata"]["has_readme"] = True
                break
            except FileReadError as e:
                result["readme"]["error"] = str(e)

    if not result["metadata"]["has_readme"]:
        result["readme"]["error"] = "No README file found"

    total_size = _calculate_json_size(result)

    result["metadata"].update({
        "total_size": total_size,
        "total_size_formatted": format_size(total_size),
        "structure_truncated": structure_truncated,
        "structure_depth_used": actual_max_depth,
        "readme_truncated": readme_truncated,
    })

    return result


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Collect project context for wiki generation"
    )
    parser.add_argument(
        "--repo-path",
        required=True,
        help="Repository path"
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        default=10,
        help="Maximum scan depth (default: 10)"
    )
    parser.add_argument(
        "--include",
        action="append",
        dest="include_patterns",
        help="Include patterns (can be repeated)"
    )
    parser.add_argument(
        "--exclude",
        action="append",
        dest="exclude_patterns",
        help="Exclude patterns (can be repeated)"
    )
    parser.add_argument(
        "--output",
        help="Output file path (default: stdout)"
    )

    args = parser.parse_args()

    try:
        result = collect_context(
            repo_path=args.repo_path,
            max_depth=args.max_depth,
            include_patterns=args.include_patterns,
            exclude_patterns=args.exclude_patterns
        )

        output = json.dumps(result, ensure_ascii=False, indent=2)

        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(output, encoding='utf-8')
            print(f"Context saved to: {args.output}", file=sys.stderr)
        else:
            print(output)

        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
