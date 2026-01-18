#!/usr/bin/env python3
"""
Extract and validate Mermaid diagram syntax.

This script extracts Mermaid blocks from Markdown files and validates them
using mermaid-cli (mmdc), providing structured error details for fixing.

Usage:
    # Validate all diagrams in a directory
    python mermaid_validate.py --input ./docs/wiki/ --invalid-only

    # Validate a single Mermaid file
    python mermaid_validate.py --input diagram.mmd

    # Validate code string directly
    python mermaid_validate.py --code "graph TD\\n    A-->B"

    # Validate from pre-extracted blocks JSON
    python mermaid_validate.py --blocks blocks.json

Options:
    --input PATH           Input file (.mmd) or directory (scans .md files)
    --code CODE            Mermaid code string
    --blocks PATH          JSON file with extracted blocks
    --output PATH          Output JSON report (default: stdout)
    --patterns PATTERNS    Glob patterns for .md files (default: *.md)
    --invalid-only         Only output invalid blocks
    --extract-only         Only extract blocks, don't validate
"""

import argparse
import functools
import json
import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, List, Optional


@dataclass
class MermaidBlock:
    """Represents a mermaid code block extracted from Markdown."""
    code: str
    start_line: int
    end_line: int
    start_pos: int
    end_pos: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "code": self.code,
            "start_line": self.start_line,
            "end_line": self.end_line,
            "start_pos": self.start_pos,
            "end_pos": self.end_pos,
        }


@dataclass
class ValidationResult:
    """Result of mermaid syntax validation."""
    is_valid: bool
    error_message: Optional[str] = None
    error_type: Optional[str] = None
    error_line: Optional[int] = None
    fix_hint: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "error_message": self.error_message,
            "error_type": self.error_type,
            "error_line": self.error_line,
            "fix_hint": self.fix_hint,
        }


# =============================================================================
# Extraction Functions
# =============================================================================

def extract_mermaid_blocks(content: str) -> List[MermaidBlock]:
    """
    Extract mermaid code blocks from Markdown content.

    Args:
        content: Markdown content string

    Returns:
        List of MermaidBlock objects with position and content info
    """
    blocks = []
    lines = content.split('\n')

    i = 0
    current_pos = 0

    while i < len(lines):
        line = lines[i]
        line_stripped = line.strip()

        # Check for mermaid code block start
        if line_stripped == '```mermaid':
            start_line = i + 1  # 1-indexed
            start_pos = current_pos
            mermaid_lines = []
            i += 1
            current_pos += len(line) + 1  # Move past the opening line

            # Collect mermaid code until closing ```
            while i < len(lines):
                current_line = lines[i]
                if current_line.strip() == '```':
                    end_line = i + 1  # 1-indexed
                    # Calculate end position (include the closing ```)
                    end_pos = current_pos + len(current_line)

                    mermaid_code = '\n'.join(mermaid_lines)
                    blocks.append(MermaidBlock(
                        code=mermaid_code,
                        start_line=start_line,
                        end_line=end_line,
                        start_pos=start_pos,
                        end_pos=end_pos,
                    ))
                    current_pos += len(current_line) + 1
                    i += 1
                    break

                mermaid_lines.append(current_line)
                current_pos += len(current_line) + 1  # +1 for newline
                i += 1
        else:
            current_pos += len(line) + 1  # +1 for newline
            i += 1

    return blocks


def detect_diagram_type(code: str) -> str:
    """Detect the type of Mermaid diagram."""
    first_line = code.split('\n')[0].strip().lower()

    if first_line.startswith('graph') or first_line.startswith('flowchart'):
        return 'flowchart'
    elif first_line.startswith('sequencediagram'):
        return 'sequence'
    elif first_line.startswith('classdiagram'):
        return 'class'
    elif first_line.startswith('statediagram'):
        return 'state'
    elif first_line.startswith('erdiagram'):
        return 'er'
    elif first_line.startswith('gantt'):
        return 'gantt'
    elif first_line.startswith('pie'):
        return 'pie'
    elif first_line.startswith('journey'):
        return 'journey'
    elif first_line.startswith('gitgraph'):
        return 'gitgraph'
    else:
        return 'unknown'


def scan_document_mermaid(file_path: str) -> Dict[str, Any]:
    """
    Scan a Markdown document for mermaid blocks.

    Args:
        file_path: Path to the Markdown file

    Returns:
        Dictionary with file info and blocks
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    content = path.read_text(encoding='utf-8', errors='replace')
    blocks = extract_mermaid_blocks(content)

    block_results = []
    for i, block in enumerate(blocks):
        block_info = block.to_dict()
        block_info["id"] = f"{path.stem}_mermaid_{i+1}"
        block_info["type"] = detect_diagram_type(block.code)
        block_results.append(block_info)

    return {
        "file_path": str(path),
        "total_blocks": len(blocks),
        "blocks": block_results,
    }


def scan_directory_mermaid(
    doc_dir: str,
    file_patterns: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Scan a directory for Markdown files and their mermaid blocks.

    Args:
        doc_dir: Path to the documentation directory
        file_patterns: Optional list of glob patterns (default: ["*.md"])

    Returns:
        Dictionary containing:
        - files: List of file scan results
        - summary: Aggregate statistics
    """
    doc_path = Path(doc_dir)

    if not doc_path.exists():
        raise FileNotFoundError(f"Directory not found: {doc_dir}")

    if file_patterns is None:
        file_patterns = ["*.md"]

    # Collect all matching files
    md_files = set()
    for pattern in file_patterns:
        md_files.update(doc_path.glob(pattern))

    file_results = []
    total_blocks = 0
    type_counts: Dict[str, int] = {}
    errors = []

    for md_file in sorted(md_files):
        try:
            result = scan_document_mermaid(str(md_file))

            if result["total_blocks"] > 0:
                file_results.append(result)
                total_blocks += result["total_blocks"]

                # Count by type
                for block in result["blocks"]:
                    diagram_type = block.get("type", "unknown")
                    type_counts[diagram_type] = type_counts.get(diagram_type, 0) + 1

        except Exception as e:
            errors.append({
                "file_path": str(md_file),
                "error": str(e),
            })

    return {
        "files": file_results,
        "errors": errors,
        "summary": {
            "total_files_scanned": len(md_files),
            "files_with_mermaid": len(file_results),
            "total_blocks": total_blocks,
            "total_errors": len(errors),
            "type_counts": type_counts,
        },
        "metadata": {
            "doc_dir": str(doc_path),
            "file_patterns": file_patterns,
        },
    }


def extract_mermaid(
    input_path: str,
    file_patterns: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Extract Mermaid blocks from file or directory.

    Args:
        input_path: Path to file or directory
        file_patterns: Optional glob patterns for directory scan

    Returns:
        Dictionary with extracted blocks and metadata
    """
    path = Path(input_path)

    if not path.exists():
        raise FileNotFoundError(f"Path not found: {input_path}")

    if path.is_file():
        result = scan_document_mermaid(str(path))
        # Flatten to match expected output format
        return {
            "blocks": result["blocks"],
            "errors": [],
            "metadata": {
                "input_path": str(path),
                "files_processed": 1,
                "total_blocks": result["total_blocks"],
                "total_errors": 0,
                "type_counts": {
                    block.get("type", "unknown"): 1
                    for block in result["blocks"]
                },
            },
        }
    else:
        result = scan_directory_mermaid(str(path), file_patterns)
        # Flatten blocks from all files
        all_blocks = []
        for file_info in result["files"]:
            for block in file_info["blocks"]:
                block["file_path"] = file_info["file_path"]
                all_blocks.append(block)

        return {
            "blocks": all_blocks,
            "errors": result["errors"],
            "metadata": {
                "input_path": str(path),
                "files_processed": result["summary"]["files_with_mermaid"],
                "total_blocks": result["summary"]["total_blocks"],
                "total_errors": result["summary"]["total_errors"],
                "type_counts": result["summary"]["type_counts"],
            },
        }


# =============================================================================
# Validation Functions
# =============================================================================


@functools.cache
def check_mermaid_cli_available() -> bool:
    """Check if mermaid CLI (mmdc) is available. Result is cached."""
    try:
        result = subprocess.run(
            ['mmdc', '--version'],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def find_mmdc() -> Optional[str]:
    """Find mermaid-cli (mmdc) executable."""
    # Try common locations
    paths_to_try = [
        "mmdc",
        "npx mmdc",
        "./node_modules/.bin/mmdc",
        "../node_modules/.bin/mmdc",
    ]

    for path in paths_to_try:
        try:
            result = subprocess.run(
                path.split() + ["--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                return path
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            continue

    return None


def _classify_error(error_message: str) -> str:
    """Classify mermaid error type based on error message."""
    error_lower = error_message.lower()

    # More specific patterns first
    if 'lexical error' in error_lower or 'unrecognized text' in error_lower:
        return 'lexical_error'
    elif 'syntax' in error_lower or 'parse' in error_lower:
        return 'syntax_error'
    elif 'node' in error_lower or 'vertex' in error_lower:
        return 'node_error'
    elif 'edge' in error_lower or 'arrow' in error_lower or 'link' in error_lower:
        return 'edge_error'
    elif 'graph' in error_lower or 'diagram' in error_lower:
        return 'graph_structure_error'
    elif 'style' in error_lower or 'class' in error_lower:
        return 'style_error'
    else:
        return 'unknown'


def _generate_fix_hint(error_message: str, error_type: str) -> Optional[str]:
    """Generate a fix hint based on error patterns."""
    error_lower = error_message.lower()

    # Check for common patterns and provide specific hints
    if '\\' in error_message or 'unrecognized text' in error_lower:
        if '\\"]' in error_message or '\\"' in error_message:
            return (
                "Remove backslash escapes before quotes. "
                "In mermaid, use regular quotes without escaping: "
                'A["text"] not A[\\"text\\"]'
            )

    if 'lexical error' in error_lower:
        return (
            "Check for special characters that need quoting. "
            "Node labels with special chars should use quotes: "
            'A["Label (with parens)"]'
        )

    if error_type == 'syntax_error':
        return (
            "Check diagram structure: ensure valid diagram type declaration "
            "(graph TD, flowchart LR, etc.) and proper arrow syntax (-->, ---, -.->)"
        )

    if error_type == 'node_error':
        return (
            "Check node definitions: ensure brackets are balanced [], "
            "node IDs use only alphanumeric and underscore, "
            "and special characters in labels are quoted"
        )

    if error_type == 'edge_error':
        return (
            "Check arrow/edge syntax: use valid arrows (-->, ---, -.->), "
            'quote edge labels with special characters: A -- "label" --> B'
        )

    # Check for common error patterns
    if 'empty' in error_lower or 'expected' in error_lower:
        return "Check for empty messages in sequence diagrams: use A->>B: message instead of A->>B:"

    if 'shorthand' in error_lower:
        return "Avoid shorthand activation: use explicit activate/deactivate instead of ->>+ or -->>-"

    return None


def _parse_error(raw_error: str) -> tuple:
    """
    Parse raw mmdc error output into structured components.

    Returns:
        Tuple of (clean_message, error_type, error_line, fix_hint)
    """
    # Extract first meaningful line (before stack trace)
    lines = raw_error.strip().split('\n')
    first_line = lines[0] if lines else raw_error

    # Extract line number from patterns like "on line 6" or "at line 6"
    error_line = None
    line_match = re.search(r'(?:on|at)\s+line\s+(\d+)', raw_error, re.IGNORECASE)
    if line_match:
        error_line = int(line_match.group(1))

    # Clean the error message - remove stack traces and keep core info
    clean_message = first_line
    if 'Error:' in first_line:
        clean_message = first_line.split('Error:', 1)[1].strip()

    # Classify error type
    error_type = _classify_error(raw_error)

    # Generate fix hint based on error patterns
    fix_hint = _generate_fix_hint(raw_error, error_type)

    return clean_message, error_type, error_line, fix_hint


def validate_mermaid_code(
    code: str,
    mmdc_path: str = "mmdc",
) -> ValidationResult:
    """
    Validate Mermaid code using mermaid-cli.

    Args:
        code: Mermaid diagram code
        mmdc_path: Path to mmdc executable

    Returns:
        ValidationResult with validation status and error info
    """
    input_file = None
    output_file = None

    try:
        # Create temp file for input
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.mmd',
            delete=False,
            encoding='utf-8'
        ) as f:
            f.write(code)
            input_file = f.name

        # Create temp file for output (mmdc requires .svg/.png/.pdf extension)
        with tempfile.NamedTemporaryFile(
            suffix='.svg',
            delete=False,
        ) as f:
            output_file = f.name

        # Run mmdc
        cmd = mmdc_path.split() + ['-i', input_file, '-o', output_file]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode == 0:
            return ValidationResult(is_valid=True)
        else:
            raw_error = result.stderr or result.stdout or "Unknown error"
            clean_msg, error_type, error_line, fix_hint = _parse_error(raw_error)
            return ValidationResult(
                is_valid=False,
                error_message=clean_msg,
                error_type=error_type,
                error_line=error_line,
                fix_hint=fix_hint,
            )

    except subprocess.TimeoutExpired:
        return ValidationResult(
            is_valid=False,
            error_message="Validation timeout",
            error_type="timeout",
            fix_hint="Check for infinite loops in diagram",
        )

    except FileNotFoundError:
        return ValidationResult(
            is_valid=False,
            error_message=f"mmdc not found: {mmdc_path}",
            error_type="cli_unavailable",
            fix_hint="Install mermaid-cli: npm install -g @mermaid-js/mermaid-cli",
        )

    except Exception as e:
        return ValidationResult(
            is_valid=False,
            error_message=str(e),
            error_type="unknown",
        )

    finally:
        # Cleanup temp files
        if input_file and os.path.exists(input_file):
            os.unlink(input_file)
        if output_file and os.path.exists(output_file):
            os.unlink(output_file)


def validate_mermaid(code: str) -> ValidationResult:
    """
    Validate mermaid diagram syntax using mermaid CLI.

    Args:
        code: Mermaid diagram code

    Returns:
        ValidationResult with validation status and error info.
        If mmdc is not available, returns an error result with error_type="cli_unavailable".
    """
    if not check_mermaid_cli_available():
        return ValidationResult(
            is_valid=False,
            error_message=(
                "Mermaid CLI (mmdc) is not available. "
                "Install it with: npm install -g @mermaid-js/mermaid-cli"
            ),
            error_type="cli_unavailable",
        )

    return validate_mermaid_code(code)


def validate_blocks(
    blocks: List[Dict[str, Any]],
    mmdc_path: str = "mmdc",
) -> Dict[str, Any]:
    """
    Validate multiple Mermaid blocks.

    Args:
        blocks: List of block dictionaries from mermaid_extract.py
        mmdc_path: Path to mmdc executable

    Returns:
        Validation report dictionary
    """
    results = []
    passed = 0
    failed = 0

    for block in blocks:
        if "error" in block:
            results.append({
                "id": block.get("id", "unknown"),
                "file_path": block.get("file_path", block.get("file", "unknown")),
                "is_valid": False,
                "error_message": block["error"],
                "error_type": "extraction_error",
                "error_line": None,
                "fix_hint": None,
            })
            failed += 1
            continue

        code = block.get("code", "")
        if not code:
            continue

        validation = validate_mermaid_code(code, mmdc_path)

        result = {
            "id": block.get("id", "unknown"),
            "file_path": block.get("file_path", block.get("file", "unknown")),
            "start_line": block.get("start_line", block.get("line", 0)),
            "end_line": block.get("end_line", 0),
            "type": block.get("type", "unknown"),
            "code": code,
            **validation.to_dict(),
        }

        results.append(result)

        if validation.is_valid:
            passed += 1
        else:
            failed += 1

    return {
        "results": results,
        "summary": {
            "total": len(results),
            "passed": passed,
            "failed": failed,
            "pass_rate": f"{passed / len(results) * 100:.1f}%" if results else "N/A"
        }
    }


def get_invalid_blocks(validation_result: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Extract only invalid mermaid blocks from a validation result.

    Args:
        validation_result: Result from validate_blocks

    Returns:
        List of invalid block info
    """
    invalid_blocks = []

    for result in validation_result.get("results", []):
        if not result.get("is_valid", True):
            invalid_blocks.append({
                "file_path": result.get("file_path", ""),
                "code": result.get("code", ""),
                "start_line": result.get("start_line", 0),
                "end_line": result.get("end_line", 0),
                "error_message": result.get("error_message"),
                "error_type": result.get("error_type"),
                "error_line": result.get("error_line"),
                "fix_hint": result.get("fix_hint"),
            })

    return invalid_blocks


def main():
    parser = argparse.ArgumentParser(
        description="Extract and validate Mermaid diagram syntax"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--input",
        help="Input file (.mmd) or directory (scans .md files)"
    )
    group.add_argument(
        "--code",
        help="Mermaid code string"
    )
    group.add_argument(
        "--blocks",
        help="JSON file with extracted blocks"
    )
    parser.add_argument(
        "--output",
        help="Output JSON file (default: stdout)"
    )
    parser.add_argument(
        "--patterns",
        nargs="+",
        help="Glob patterns for .md files (default: *.md)"
    )
    parser.add_argument(
        "--mmdc",
        default="mmdc",
        help="Path to mmdc executable (default: mmdc)"
    )
    parser.add_argument(
        "--invalid-only",
        action="store_true",
        help="Only output invalid blocks"
    )
    parser.add_argument(
        "--extract-only",
        action="store_true",
        help="Only extract blocks, don't validate"
    )

    args = parser.parse_args()

    # Find mmdc (only needed if validating)
    mmdc_path = args.mmdc
    if not args.extract_only and mmdc_path == "mmdc":
        found = find_mmdc()
        if found:
            mmdc_path = found
        else:
            print("Warning: mmdc not found, validation may fail", file=sys.stderr)

    try:
        if args.input:
            input_path = Path(args.input)

            # Check if it's a directory or .md file (extract from markdown)
            if input_path.is_dir() or input_path.suffix.lower() == '.md':
                # Extract blocks from markdown file(s)
                extracted = extract_mermaid(str(input_path), args.patterns)
                blocks = extracted["blocks"]

                if args.extract_only:
                    # Just return extracted blocks
                    result = extracted
                else:
                    # Validate extracted blocks
                    result = validate_blocks(blocks, mmdc_path)

                    if args.invalid_only:
                        invalid = get_invalid_blocks(result)
                        files_affected = len(set(b["file_path"] for b in invalid if b.get("file_path")))
                        result = {
                            "invalid_blocks": invalid,
                            "total_invalid": len(invalid),
                            "total_scanned": result["summary"]["total"],
                            "files_affected": files_affected,
                        }
            else:
                # Single .mmd file - validate directly
                code = input_path.read_text(encoding='utf-8')
                validation = validate_mermaid_code(code, mmdc_path)
                result = validation.to_dict()

        elif args.code:
            # Validate code string
            validation = validate_mermaid_code(args.code, mmdc_path)
            result = validation.to_dict()

        elif args.blocks:
            # Validate blocks from JSON
            blocks_data = json.loads(Path(args.blocks).read_text(encoding='utf-8'))
            blocks = blocks_data.get("blocks", blocks_data)
            if isinstance(blocks, dict):
                blocks = blocks.get("blocks", [])
            result = validate_blocks(blocks, mmdc_path)

            if args.invalid_only:
                invalid = get_invalid_blocks(result)
                files_affected = len(set(b["file_path"] for b in invalid if b.get("file_path")))
                result = {
                    "invalid_blocks": invalid,
                    "total_invalid": len(invalid),
                    "total_scanned": result["summary"]["total"],
                    "files_affected": files_affected,
                }

        output = json.dumps(result, ensure_ascii=False, indent=2)

        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(output, encoding='utf-8')
            print(f"Output saved to: {args.output}", file=sys.stderr)
        else:
            print(output)

        # Exit with error code if validation failed
        if isinstance(result, dict):
            if "is_valid" in result and not result["is_valid"]:
                return 1
            if "summary" in result and result["summary"]["failed"] > 0:
                return 1
            if "total_invalid" in result and result["total_invalid"] > 0:
                return 1

        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
