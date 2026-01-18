#!/usr/bin/env python3
"""
Validate wiki documentation structure against TOC specification.

This script validates:
- PAGE_ID markers (presence and correctness)
- AUTOGEN markers (BEGIN/END pairs, no overlaps)
- TOC alignment (all pages/sections exist)
- Internal links (valid targets)
- Basic structure (H1 headings, file existence)

Usage:
    # Validate all docs in a directory
    python validate_docs_structure.py --doc-dir docs/wiki --toc-file docs/wiki/toc.yaml

    # Output JSON report
    python validate_docs_structure.py --doc-dir docs/wiki --toc-file docs/wiki/toc.yaml --output report.json

    # Show only errors (no warnings)
    python validate_docs_structure.py --doc-dir docs/wiki --toc-file docs/wiki/toc.yaml --errors-only

Options:
    --doc-dir PATH       Directory containing generated .md docs
    --toc-file PATH      Path to toc.yaml file
    --output PATH        Output JSON report (default: stdout)
    --errors-only        Only report errors, not warnings
    --fix                Auto-fix issues where possible (PAGE_ID, missing markers)
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

try:
    import yaml
except ImportError:
    yaml = None


@dataclass
class Issue:
    """Represents a validation issue."""
    file: str
    line: Optional[int]
    severity: str  # "error" or "warning"
    category: str  # "page_id", "autogen", "structure", "link", "toc"
    message: str
    fix_hint: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "file": self.file,
            "line": self.line,
            "severity": self.severity,
            "category": self.category,
            "message": self.message,
            "fix_hint": self.fix_hint,
        }


@dataclass
class ValidationResult:
    """Result of document structure validation."""
    issues: List[Issue] = field(default_factory=list)
    pages_validated: int = 0
    pages_missing: int = 0
    sections_validated: int = 0
    sections_missing: int = 0

    def to_dict(self) -> Dict[str, Any]:
        errors = [i for i in self.issues if i.severity == "error"]
        warnings = [i for i in self.issues if i.severity == "warning"]
        return {
            "summary": {
                "pages_validated": self.pages_validated,
                "pages_missing": self.pages_missing,
                "sections_validated": self.sections_validated,
                "sections_missing": self.sections_missing,
                "total_errors": len(errors),
                "total_warnings": len(warnings),
                "is_valid": len(errors) == 0,
            },
            "errors": [i.to_dict() for i in errors],
            "warnings": [i.to_dict() for i in warnings],
        }


def load_toc(toc_path: str) -> Dict[str, Any]:
    """Load and parse TOC YAML file."""
    if yaml is None:
        raise ImportError("PyYAML is required. Install with: pip install pyyaml")

    path = Path(toc_path)
    if not path.exists():
        raise FileNotFoundError(f"TOC file not found: {toc_path}")

    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def extract_page_id(content: str) -> Tuple[Optional[str], Optional[int]]:
    """
    Extract PAGE_ID from document content.

    Returns:
        Tuple of (page_id, line_number) or (None, None) if not found
    """
    lines = content.split("\n")
    for i, line in enumerate(lines[:5]):  # Check first 5 lines
        match = re.match(r"<!--\s*PAGE_ID:\s*(\S+)\s*-->", line.strip())
        if match:
            return match.group(1), i + 1
    return None, None


def extract_autogen_markers(content: str) -> List[Dict[str, Any]]:
    """
    Extract all AUTOGEN markers from content.

    Returns:
        List of marker info dicts with keys: type, section_id, line, position
    """
    markers = []
    lines = content.split("\n")

    for i, line in enumerate(lines):
        # Check for BEGIN marker
        begin_match = re.match(r"<!--\s*BEGIN:AUTOGEN\s+(\S+)\s*-->", line.strip())
        if begin_match:
            markers.append({
                "type": "BEGIN",
                "section_id": begin_match.group(1),
                "line": i + 1,
                "position": content.find(line),
            })

        # Check for END marker
        end_match = re.match(r"<!--\s*END:AUTOGEN\s+(\S+)\s*-->", line.strip())
        if end_match:
            markers.append({
                "type": "END",
                "section_id": end_match.group(1),
                "line": i + 1,
                "position": content.find(line),
            })

    return markers


def validate_autogen_markers(
    markers: List[Dict[str, Any]],
    expected_sections: List[str],
    filename: str,
) -> List[Issue]:
    """
    Validate AUTOGEN marker pairs and coverage.

    Checks:
    - Every BEGIN has matching END
    - No overlapping markers
    - All expected sections are present
    """
    issues = []

    # Track open markers (stack)
    open_markers: List[Dict[str, Any]] = []
    found_sections: Set[str] = set()

    for marker in markers:
        if marker["type"] == "BEGIN":
            # Check for overlap (BEGIN inside another BEGIN without END)
            if open_markers:
                outer = open_markers[-1]
                issues.append(Issue(
                    file=filename,
                    line=marker["line"],
                    severity="error",
                    category="autogen",
                    message=f"Nested AUTOGEN marker '{marker['section_id']}' inside '{outer['section_id']}' (opened at line {outer['line']})",
                    fix_hint="Close the outer AUTOGEN section before starting a new one, or remove nested markers",
                ))
            open_markers.append(marker)

        elif marker["type"] == "END":
            if not open_markers:
                issues.append(Issue(
                    file=filename,
                    line=marker["line"],
                    severity="error",
                    category="autogen",
                    message=f"END:AUTOGEN '{marker['section_id']}' without matching BEGIN",
                    fix_hint="Add BEGIN:AUTOGEN marker before content, or remove orphaned END marker",
                ))
            else:
                begin_marker = open_markers.pop()
                if begin_marker["section_id"] != marker["section_id"]:
                    issues.append(Issue(
                        file=filename,
                        line=marker["line"],
                        severity="error",
                        category="autogen",
                        message=f"Mismatched AUTOGEN markers: BEGIN '{begin_marker['section_id']}' (line {begin_marker['line']}) vs END '{marker['section_id']}'",
                        fix_hint=f"Change END marker to match BEGIN: END:AUTOGEN {begin_marker['section_id']}",
                    ))
                else:
                    found_sections.add(marker["section_id"])

    # Check for unclosed BEGIN markers
    for marker in open_markers:
        issues.append(Issue(
            file=filename,
            line=marker["line"],
            severity="error",
            category="autogen",
            message=f"BEGIN:AUTOGEN '{marker['section_id']}' without matching END",
            fix_hint=f"Add END:AUTOGEN {marker['section_id']} after section content",
        ))

    # Check for missing expected sections
    for section_id in expected_sections:
        if section_id not in found_sections:
            issues.append(Issue(
                file=filename,
                line=None,
                severity="error",
                category="autogen",
                message=f"Missing AUTOGEN section '{section_id}' defined in TOC",
                fix_hint=f"Add BEGIN:AUTOGEN {section_id} and END:AUTOGEN {section_id} markers around the section",
            ))

    # Check for extra sections not in TOC
    extra_sections = found_sections - set(expected_sections)
    for section_id in extra_sections:
        issues.append(Issue(
            file=filename,
            line=None,
            severity="warning",
            category="autogen",
            message=f"AUTOGEN section '{section_id}' not defined in TOC",
            fix_hint="Remove extra AUTOGEN markers or add section to TOC",
        ))

    return issues


def validate_internal_links(
    content: str,
    filename: str,
    valid_files: Set[str],
    doc_dir: Path,
) -> List[Issue]:
    """Validate internal markdown links."""
    issues = []
    lines = content.split("\n")

    for i, line in enumerate(lines):
        # Find markdown links to .md files
        links = re.findall(r'\[([^\]]+)\]\(([^\)]+\.md[^\)]*)\)', line)

        for link_text, link_target in links:
            # Skip external links
            if link_target.startswith(("http://", "https://")):
                continue

            # Extract filename (remove anchors)
            target_file = link_target.split("#")[0]

            # Check if target is in TOC
            if target_file not in valid_files:
                issues.append(Issue(
                    file=filename,
                    line=i + 1,
                    severity="warning",
                    category="link",
                    message=f"Link to '{target_file}' not defined in TOC",
                    fix_hint="Verify the target file exists or update the link",
                ))
            else:
                # Check if file exists on disk
                target_path = doc_dir / target_file
                if not target_path.exists():
                    issues.append(Issue(
                        file=filename,
                        line=i + 1,
                        severity="error",
                        category="link",
                        message=f"Broken link: '{target_file}' does not exist",
                        fix_hint="Generate the missing page or remove the link",
                    ))

    return issues


def validate_document_structure(
    content: str,
    filename: str,
) -> List[Issue]:
    """Validate basic document structure."""
    issues = []
    lines = content.split("\n")

    # Check for H1 heading (not H2)
    h1_lines = [(i, line) for i, line in enumerate(lines)
                if line.startswith("# ") and not line.startswith("## ")]

    if not h1_lines:
        issues.append(Issue(
            file=filename,
            line=None,
            severity="error",
            category="structure",
            message="Missing H1 heading",
            fix_hint="Add a single H1 heading (# Title) at the start of the page",
        ))
    elif len(h1_lines) > 1:
        for i, _ in h1_lines[1:]:
            issues.append(Issue(
                file=filename,
                line=i + 1,
                severity="warning",
                category="structure",
                message="Multiple H1 headings found",
                fix_hint="Use H2 (##) for section headings, reserve H1 for page title only",
            ))

    # Check file size (warn if very small)
    if len(content) < 500:
        issues.append(Issue(
            file=filename,
            line=None,
            severity="warning",
            category="structure",
            message=f"Very small file ({len(content)} chars)",
            fix_hint="Consider adding more content or verifying generation completed",
        ))

    return issues


def validate_page(
    filepath: Path,
    page_info: Dict[str, Any],
    valid_files: Set[str],
    doc_dir: Path,
) -> Tuple[List[Issue], int]:
    """
    Validate a single page against TOC specification.

    Returns:
        Tuple of (issues, sections_found_count)
    """
    issues = []
    filename = filepath.name

    # Read file content
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception as e:
        issues.append(Issue(
            file=filename,
            line=None,
            severity="error",
            category="structure",
            message=f"Cannot read file: {e}",
        ))
        return issues, 0

    # Validate PAGE_ID
    expected_page_id = page_info.get("id")
    found_page_id, page_id_line = extract_page_id(content)

    if not found_page_id:
        issues.append(Issue(
            file=filename,
            line=1,
            severity="error",
            category="page_id",
            message="Missing PAGE_ID marker",
            fix_hint=f"Add <!-- PAGE_ID: {expected_page_id} --> at the start of the file",
        ))
    elif found_page_id != expected_page_id:
        issues.append(Issue(
            file=filename,
            line=page_id_line,
            severity="error",
            category="page_id",
            message=f"PAGE_ID mismatch: found '{found_page_id}', expected '{expected_page_id}'",
            fix_hint=f"Change PAGE_ID to: <!-- PAGE_ID: {expected_page_id} -->",
        ))

    # Collect expected autogen sections (recursively including nested sections)
    def collect_section_ids(sections: List[Dict[str, Any]]) -> List[str]:
        """Recursively collect section IDs from sections and their nested sections."""
        result = []
        for section in sections:
            if section.get("autogen", True):  # Default to autogen=true
                section_id = section.get("id")
                if section_id:
                    result.append(section_id)
            # Recursively collect from nested sections
            nested = section.get("sections", [])
            if nested:
                result.extend(collect_section_ids(nested))
        return result

    expected_sections = collect_section_ids(page_info.get("sections", []))

    # Validate AUTOGEN markers
    markers = extract_autogen_markers(content)
    autogen_issues = validate_autogen_markers(markers, expected_sections, filename)
    issues.extend(autogen_issues)

    # Count sections found
    found_section_ids = {m["section_id"] for m in markers if m["type"] == "END"}
    sections_found = len(found_section_ids & set(expected_sections))

    # Validate internal links
    link_issues = validate_internal_links(content, filename, valid_files, doc_dir)
    issues.extend(link_issues)

    # Validate basic structure
    structure_issues = validate_document_structure(content, filename)
    issues.extend(structure_issues)

    return issues, sections_found


def validate_docs(
    doc_dir: str,
    toc_file: str,
    errors_only: bool = False,
) -> ValidationResult:
    """
    Validate all documentation against TOC specification.

    Args:
        doc_dir: Directory containing generated .md docs
        toc_file: Path to toc.yaml file
        errors_only: If True, only include errors (not warnings)

    Returns:
        ValidationResult with all issues and statistics
    """
    result = ValidationResult()
    doc_path = Path(doc_dir)
    toc = load_toc(toc_file)

    # Build set of valid filenames from TOC
    valid_files: Set[str] = set()
    pages = toc.get("pages", [])

    for page in pages:
        filename = page.get("filename")
        if filename:
            valid_files.add(filename)

    # Validate each page in TOC
    for page in pages:
        filename = page.get("filename")
        if not filename:
            continue

        filepath = doc_path / filename

        if not filepath.exists():
            result.pages_missing += 1
            result.issues.append(Issue(
                file=filename,
                line=None,
                severity="error",
                category="toc",
                message=f"Page defined in TOC but file not found",
                fix_hint="Generate the missing page or remove from TOC",
            ))
            continue

        result.pages_validated += 1

        # Count expected sections (recursively including nested sections)
        def count_autogen_sections(sections: List[Dict[str, Any]]) -> int:
            count = 0
            for s in sections:
                if s.get("autogen", True) and s.get("id"):
                    count += 1
                # Recursively count nested sections
                nested = s.get("sections", [])
                if nested:
                    count += count_autogen_sections(nested)
            return count

        expected_section_count = count_autogen_sections(page.get("sections", []))

        # Validate page
        issues, sections_found = validate_page(filepath, page, valid_files, doc_path)
        result.sections_validated += sections_found
        result.sections_missing += expected_section_count - sections_found

        result.issues.extend(issues)

    # Check for extra files not in TOC
    # Note: SUMMARY.md is now in _reports/, so no need to exclude it from doc_dir
    existing_files = set(f.name for f in doc_path.glob("*.md"))
    extra_files = existing_files - valid_files

    for extra_file in extra_files:
        result.issues.append(Issue(
            file=extra_file,
            line=None,
            severity="warning",
            category="toc",
            message="File exists but not defined in TOC",
            fix_hint="Add to TOC or remove the file",
        ))

    # Filter to errors only if requested
    if errors_only:
        result.issues = [i for i in result.issues if i.severity == "error"]

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Validate wiki documentation structure against TOC specification"
    )
    parser.add_argument(
        "--doc-dir",
        required=True,
        help="Directory containing generated .md docs",
    )
    parser.add_argument(
        "--toc-file",
        required=True,
        help="Path to toc.yaml file",
    )
    parser.add_argument(
        "--output",
        help="Output JSON report (default: stdout)",
    )
    parser.add_argument(
        "--errors-only",
        action="store_true",
        help="Only report errors, not warnings",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Auto-fix issues where possible (not yet implemented)",
    )

    args = parser.parse_args()

    if args.fix:
        print("Warning: --fix is not yet implemented", file=sys.stderr)

    try:
        result = validate_docs(
            doc_dir=args.doc_dir,
            toc_file=args.toc_file,
            errors_only=args.errors_only,
        )

        output = json.dumps(result.to_dict(), ensure_ascii=False, indent=2)

        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(output, encoding="utf-8")
            print(f"Report saved to: {args.output}", file=sys.stderr)
        else:
            print(output)

        # Exit with error code if validation failed
        if not result.to_dict()["summary"]["is_valid"]:
            return 1

        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ImportError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
