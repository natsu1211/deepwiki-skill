#!/usr/bin/env python3
"""
Generate wiki documentation summary report (SUMMARY.md).

This script analyzes generated documentation and produces a summary report with:
- Generation status (pages/sections completion)
- Citation statistics and coverage
- Diagram validation summary
- Issues and recommendations

Usage:
    python generate_summary.py --doc-dir docs/wiki --toc-file docs/wiki/toc.yaml

    # With validation reports
    python generate_summary.py --doc-dir docs/wiki --toc-file docs/wiki/toc.yaml \
        --structure-report docs/wiki/_reports/structure_validation.json \
        --mermaid-report docs/wiki/_reports/mermaid_invalid.json

Options:
    --doc-dir PATH           Directory containing generated .md docs
    --toc-file PATH          Path to toc.yaml file
    --structure-report PATH  Path to structure_validation.json (optional)
    --mermaid-report PATH    Path to mermaid_invalid.json (optional)
    --output PATH            Output path for SUMMARY.md (default: {doc_dir}/_reports/SUMMARY.md)
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

try:
    import yaml
except ImportError:
    yaml = None


@dataclass
class PageStats:
    """Statistics for a single page."""
    filename: str
    title: str
    expected_sections: int = 0
    found_sections: int = 0
    citations: int = 0
    diagrams: int = 0
    has_page_id: bool = False
    issues: List[str] = field(default_factory=list)

    @property
    def status(self) -> str:
        if self.found_sections == self.expected_sections and self.has_page_id:
            return "✅"
        elif self.found_sections > 0:
            return "⚠️"
        else:
            return "❌"


@dataclass
class SummaryData:
    """Aggregated summary data."""
    repo_name: str = ""
    commit_hash: str = ""
    total_pages: int = 0
    pages_found: int = 0
    total_sections: int = 0
    sections_found: int = 0
    total_citations: int = 0
    total_diagrams: int = 0
    valid_diagrams: int = 0
    invalid_diagrams: int = 0
    page_stats: List[PageStats] = field(default_factory=list)
    covered_files: Dict[str, List[str]] = field(default_factory=dict)
    uncovered_files: List[str] = field(default_factory=list)
    errors: List[Dict[str, Any]] = field(default_factory=list)
    warnings: List[Dict[str, Any]] = field(default_factory=list)


def load_yaml(path: Path) -> Optional[Dict[str, Any]]:
    """Load YAML file."""
    if yaml is None:
        print("Error: PyYAML is required. Install with: pip install pyyaml", file=sys.stderr)
        return None
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading {path}: {e}", file=sys.stderr)
        return None


def load_json(path: Path) -> Optional[Dict[str, Any]]:
    """Load JSON file if exists."""
    if not path.exists():
        return None
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: Could not load {path}: {e}", file=sys.stderr)
        return None


def count_sections_recursive(sections: List[Dict[str, Any]]) -> int:
    """Recursively count autogen sections."""
    count = 0
    for section in sections:
        if section.get("autogen", True) and section.get("id"):
            count += 1
        nested = section.get("sections", [])
        if nested:
            count += count_sections_recursive(nested)
    return count


def collect_source_files_recursive(sections: List[Dict[str, Any]], inherited: List[str]) -> Set[str]:
    """Recursively collect source files from sections."""
    files = set(inherited)
    for section in sections:
        section_files = section.get("source_files", [])
        files.update(section_files)
        nested = section.get("sections", [])
        if nested:
            files.update(collect_source_files_recursive(nested, list(files)))
    return files


def extract_citations(content: str) -> List[Tuple[str, str]]:
    """Extract citations from markdown content.

    Returns list of (filename, url) tuples.
    """
    citations = []
    # Match patterns like [file.ext:N](url) or [file.ext:N-M](url)
    pattern = r'\[([^\]]+?):(\d+(?:-\d+)?)\]\(([^)]+)\)'
    for match in re.finditer(pattern, content):
        filename = match.group(1)
        url = match.group(3)
        citations.append((filename, url))
    return citations


def count_mermaid_diagrams(content: str) -> int:
    """Count mermaid code blocks in content."""
    pattern = r'```mermaid'
    return len(re.findall(pattern, content, re.IGNORECASE))


def extract_autogen_sections(content: str) -> Set[str]:
    """Extract AUTOGEN section IDs from content."""
    sections = set()
    pattern = r'<!--\s*BEGIN:AUTOGEN\s+(\S+)\s*-->'
    for match in re.finditer(pattern, content):
        sections.add(match.group(1))
    return sections


def check_page_id(content: str, expected_id: str) -> bool:
    """Check if PAGE_ID marker exists and matches."""
    pattern = r'<!--\s*PAGE_ID:\s*(\S+)\s*-->'
    match = re.search(pattern, content)
    if match:
        return match.group(1) == expected_id
    return False


def analyze_docs(
    doc_dir: Path,
    toc_data: Dict[str, Any],
    structure_report: Optional[Dict[str, Any]],
    mermaid_report: Optional[Dict[str, Any]],
) -> SummaryData:
    """Analyze documentation and collect statistics."""
    summary = SummaryData()

    # Extract project info
    project = toc_data.get("project", {})
    summary.repo_name = project.get("name", "Unknown")
    summary.commit_hash = project.get("ref_commit_hash", "Unknown")

    pages = toc_data.get("pages", [])
    summary.total_pages = len(pages)

    # Collect all expected source files from TOC
    all_source_files: Set[str] = set()
    cited_files: Dict[str, List[str]] = defaultdict(list)

    for page in pages:
        page_id = page.get("id", "")
        filename = page.get("filename", "")
        title = page.get("title", filename)
        sections = page.get("sections", [])
        page_source_files = page.get("source_files", [])

        # Count expected sections
        expected_sections = count_sections_recursive(sections)
        summary.total_sections += expected_sections

        # Collect source files
        all_source_files.update(page_source_files)
        all_source_files.update(collect_source_files_recursive(sections, page_source_files))

        # Initialize page stats
        stats = PageStats(
            filename=filename,
            title=title,
            expected_sections=expected_sections,
        )

        # Check if file exists and analyze
        filepath = doc_dir / filename
        if filepath.exists():
            summary.pages_found += 1
            content = filepath.read_text(encoding='utf-8')

            # Check PAGE_ID
            stats.has_page_id = check_page_id(content, page_id)

            # Count found sections
            found_section_ids = extract_autogen_sections(content)
            stats.found_sections = len(found_section_ids)
            summary.sections_found += stats.found_sections

            # Count citations
            citations = extract_citations(content)
            stats.citations = len(citations)
            summary.total_citations += stats.citations

            # Track which files are cited
            for cited_file, _ in citations:
                cited_files[cited_file].append(filename)

            # Count diagrams
            stats.diagrams = count_mermaid_diagrams(content)
            summary.total_diagrams += stats.diagrams
        else:
            stats.issues.append("File not found")

        summary.page_stats.append(stats)

    # Analyze source coverage
    # Skip glob patterns (contain * or ?) as they can't be directly matched to citations
    def is_glob_pattern(path: str) -> bool:
        return '*' in path or '?' in path

    for source_file in all_source_files:
        # Skip glob patterns - they're not directly comparable to cited filenames
        if is_glob_pattern(source_file):
            continue

        # Extract just the filename for matching
        source_name = Path(source_file).name
        if source_name in cited_files:
            summary.covered_files[source_file] = cited_files[source_name]
        else:
            # Also check with full path patterns
            found = False
            for cited in cited_files:
                if cited in source_file or source_file.endswith(cited):
                    summary.covered_files[source_file] = cited_files[cited]
                    found = True
                    break
            if not found:
                summary.uncovered_files.append(source_file)

    # Include validation report data
    if structure_report:
        summary.errors = structure_report.get("errors", [])
        summary.warnings = structure_report.get("warnings", [])

    # Include mermaid report data
    if mermaid_report:
        metadata = mermaid_report.get("metadata", {})
        summary.valid_diagrams = metadata.get("valid_count", 0)
        summary.invalid_diagrams = metadata.get("invalid_count", 0)
        # If no metadata, count from blocks
        if not metadata:
            blocks = mermaid_report.get("blocks", [])
            summary.invalid_diagrams = len([b for b in blocks if not b.get("is_valid", True)])

    return summary


def generate_summary_md(summary: SummaryData) -> str:
    """Generate SUMMARY.md content."""
    lines = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Header
    lines.append("# Wiki Documentation Summary")
    lines.append("")
    lines.append(f"Generated: {timestamp}")
    lines.append(f"Repository: {summary.repo_name}")
    lines.append(f"Commit: `{summary.commit_hash}`")
    lines.append("")

    # Overall status
    pages_complete = summary.pages_found == summary.total_pages
    sections_complete = summary.sections_found == summary.total_sections
    no_errors = len(summary.errors) == 0

    if pages_complete and sections_complete and no_errors:
        overall_status = "✅ Complete"
    elif summary.pages_found > 0 and len(summary.errors) == 0:
        overall_status = "⚠️ Incomplete"
    else:
        overall_status = "❌ Has Errors"

    lines.append("## Generation Status")
    lines.append("")
    lines.append(f"**Overall Status**: {overall_status}")
    lines.append("")
    lines.append("| Metric | Expected | Actual | Status |")
    lines.append("|--------|----------|--------|--------|")
    lines.append(f"| Pages | {summary.total_pages} | {summary.pages_found} | {'✅' if pages_complete else '❌'} |")
    lines.append(f"| Sections | {summary.total_sections} | {summary.sections_found} | {'✅' if sections_complete else '⚠️'} |")
    lines.append(f"| Citations | - | {summary.total_citations} | {'✅' if summary.total_citations > 0 else '⚠️'} |")

    if summary.total_diagrams > 0 or summary.invalid_diagrams > 0:
        valid = summary.total_diagrams - summary.invalid_diagrams if summary.valid_diagrams == 0 else summary.valid_diagrams
        diagram_status = '✅' if summary.invalid_diagrams == 0 else '⚠️'
        lines.append(f"| Diagrams | {summary.total_diagrams} | {valid} valid | {diagram_status} |")

    lines.append("")

    # Page details
    lines.append("## Page Details")
    lines.append("")
    lines.append("| Page | Title | Sections | Citations | Diagrams | Status |")
    lines.append("|------|-------|----------|-----------|----------|--------|")

    for stats in summary.page_stats:
        sections_str = f"{stats.found_sections}/{stats.expected_sections}"
        lines.append(f"| {stats.filename} | {stats.title} | {sections_str} | {stats.citations} | {stats.diagrams} | {stats.status} |")

    lines.append("")

    # Source coverage
    lines.append("## Source Coverage")
    lines.append("")

    if summary.covered_files:
        lines.append("### Covered Files")
        lines.append("")
        for source_file, citing_pages in sorted(summary.covered_files.items()):
            pages_str = ", ".join(sorted(set(citing_pages)))
            lines.append(f"- `{source_file}` - cited in {pages_str}")
        lines.append("")

    if summary.uncovered_files:
        lines.append("### Uncovered Files")
        lines.append("")
        lines.append("> Files listed in TOC but not cited in any documentation:")
        lines.append("")
        for source_file in sorted(summary.uncovered_files):
            lines.append(f"- `{source_file}`")
        lines.append("")

    # Issues
    lines.append("## Issues")
    lines.append("")

    if summary.errors:
        lines.append("### Errors (Must Fix)")
        lines.append("")
        for error in summary.errors:
            file = error.get("file", "unknown")
            message = error.get("message", "")
            lines.append(f"- **{file}**: {message}")
        lines.append("")
    else:
        lines.append("### Errors")
        lines.append("")
        lines.append("None")
        lines.append("")

    if summary.warnings:
        lines.append("### Warnings")
        lines.append("")
        for warning in summary.warnings:
            file = warning.get("file", "unknown")
            message = warning.get("message", "")
            lines.append(f"- **{file}**: {message}")
        lines.append("")

    # Recommendations
    lines.append("### Recommendations")
    lines.append("")
    recommendations = []

    if summary.uncovered_files:
        recommendations.append(f"- Add citations for {len(summary.uncovered_files)} uncovered source files")

    low_citation_pages = [s for s in summary.page_stats if s.citations < 3 and s.expected_sections > 0]
    if low_citation_pages:
        recommendations.append(f"- Improve citation coverage in {len(low_citation_pages)} pages with fewer than 3 citations")

    if summary.invalid_diagrams > 0:
        recommendations.append(f"- Fix {summary.invalid_diagrams} invalid Mermaid diagrams")

    if not recommendations:
        recommendations.append("- None - documentation looks good!")

    lines.extend(recommendations)
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate wiki documentation summary report"
    )
    parser.add_argument(
        "--doc-dir",
        required=True,
        help="Directory containing generated .md docs"
    )
    parser.add_argument(
        "--toc-file",
        required=True,
        help="Path to toc.yaml file"
    )
    parser.add_argument(
        "--structure-report",
        help="Path to structure_validation.json (optional)"
    )
    parser.add_argument(
        "--mermaid-report",
        help="Path to mermaid_invalid.json (optional)"
    )
    parser.add_argument(
        "--output",
        help="Output path for SUMMARY.md (default: {doc_dir}/_reports/SUMMARY.md)"
    )

    args = parser.parse_args()

    # Validate inputs
    doc_dir = Path(args.doc_dir)
    if not doc_dir.exists():
        print(f"Error: doc_dir does not exist: {doc_dir}", file=sys.stderr)
        return 1

    toc_path = Path(args.toc_file)
    if not toc_path.exists():
        print(f"Error: toc_file does not exist: {toc_path}", file=sys.stderr)
        return 1

    # Load TOC
    toc_data = load_yaml(toc_path)
    if toc_data is None:
        return 1

    # Load optional reports
    structure_report = None
    if args.structure_report:
        structure_report = load_json(Path(args.structure_report))
    else:
        # Try default location
        default_structure = doc_dir / "_reports" / "structure_validation.json"
        structure_report = load_json(default_structure)

    mermaid_report = None
    if args.mermaid_report:
        mermaid_report = load_json(Path(args.mermaid_report))
    else:
        # Try default location
        default_mermaid = doc_dir / "_reports" / "mermaid_invalid.json"
        mermaid_report = load_json(default_mermaid)

    # Analyze documentation
    summary = analyze_docs(doc_dir, toc_data, structure_report, mermaid_report)

    # Generate summary
    summary_md = generate_summary_md(summary)

    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = doc_dir / "_reports" / "SUMMARY.md"

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write output
    output_path.write_text(summary_md, encoding='utf-8')
    print(f"Summary written to: {output_path}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
