#!/usr/bin/env python3
"""
Collect TOC synchronization context for incremental updates.

This script compares TOC structure with existing documentation to determine
what needs to be synced (new pages, updated sections, deleted sections).

Usage:
    python sync_context.py --repo-path /path/to/repo --toc-file toc.yaml --doc-dir ./docs/wiki/

Options:
    --repo-path PATH       Repository path (required)
    --toc-file PATH        TOC YAML file path (required)
    --doc-dir PATH         Documentation directory (required)
    --output PATH          Output file path (default: stdout)
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional

import yaml


def extract_page_id(content: str) -> Optional[str]:
    """Extract PAGE_ID from markdown content."""
    pattern = r'<!-- PAGE_ID:\s*(\S+)\s*-->'
    match = re.search(pattern, content)
    return match.group(1) if match else None


def extract_autogen_sections(content: str) -> List[str]:
    """Extract all AUTOGEN section IDs from markdown content."""
    pattern = r'<!-- BEGIN:AUTOGEN (\S+) -->'
    return re.findall(pattern, content)


def is_section_content_empty(content: str, section_id: str) -> bool:
    """Check if a section's content is empty."""
    begin_pattern = rf'<!-- BEGIN:AUTOGEN {re.escape(section_id)} -->\n?'
    end_pattern = rf'<!-- END:AUTOGEN {re.escape(section_id)} -->'

    begin_match = re.search(begin_pattern, content)
    if not begin_match:
        return True

    content_start = begin_match.end()
    end_match = re.search(end_pattern, content[content_start:])
    if not end_match:
        return True

    inner_content = content[content_start:content_start + end_match.start()]
    stripped = inner_content.strip()

    if not stripped:
        return True

    # Check if only contains separators
    lines = [line.strip() for line in stripped.split('\n') if line.strip()]
    non_separator = [line for line in lines if line != '---']

    return len(non_separator) == 0


def load_toc(toc_path: str) -> Dict[str, Any]:
    """Load and parse TOC YAML file."""
    path = Path(toc_path)
    if not path.exists():
        raise FileNotFoundError(f"TOC file not found: {toc_path}")

    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def collect_toc_pages(toc: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """Collect all pages and their sections from TOC."""
    pages_map = {}

    for page in toc.get("pages", []):
        page_id = page.get("id", "")
        page_sources = page.get("source_files", [])

        def collect_sections(sections_list: List, inherited_sources: List[str], depth: int = 0) -> List[Dict]:
            result = []
            for section in sections_list:
                section_id = section.get("id", "")
                section_sources = section.get("source_files", [])
                all_sources = inherited_sources + section_sources

                section_info = {
                    "section_id": section_id,
                    "title": section.get("title", ""),
                    "description": section.get("description", ""),
                    "autogen": section.get("autogen", False),
                    "source_files": all_sources,
                    "diagrams_needed": section.get("diagrams_needed", False),
                    "diagram_types": section.get("diagram_types", []),
                    "depth": depth,
                }
                result.append(section_info)

                # Process nested sections
                nested = section.get("sections", [])
                if nested:
                    result.extend(collect_sections(nested, all_sources, depth + 1))

            return result

        sections = collect_sections(page.get("sections", []), page_sources)
        section_ids = [s["section_id"] for s in sections]

        pages_map[page_id] = {
            "page_id": page_id,
            "title": page.get("title", ""),
            "filename": page.get("filename", ""),
            "source_files": page_sources,
            "sections": sections,
            "section_ids": section_ids,
            "related_pages": page.get("related_pages", []),
        }

    return pages_map


def scan_existing_docs(doc_dir: str) -> Dict[str, Dict[str, Any]]:
    """Scan existing documentation files with PAGE_ID markers."""
    doc_path = Path(doc_dir)
    if not doc_path.exists():
        return {}

    docs_by_page_id = {}

    for md_file in doc_path.glob("*.md"):
        try:
            content = md_file.read_text(encoding='utf-8', errors='replace')

            page_id = extract_page_id(content)
            if not page_id:
                continue

            autogen_sections = extract_autogen_sections(content)

            # Find empty sections
            empty_sections = [
                section_id for section_id in autogen_sections
                if is_section_content_empty(content, section_id)
            ]

            docs_by_page_id[page_id] = {
                "page_id": page_id,
                "file_path": str(md_file),
                "filename": md_file.name,
                "autogen_sections": autogen_sections,
                "empty_sections": empty_sections,
            }

        except Exception:
            continue

    return docs_by_page_id


def collect_sync_context(
    repo_path: str,
    toc_file: str,
    doc_dir: str
) -> Dict[str, Any]:
    """
    Collect context for syncing documentation with TOC structure.

    Args:
        repo_path: Repository path
        toc_file: Path to TOC YAML file
        doc_dir: Documentation directory

    Returns:
        Sync context dictionary
    """
    # Resolve paths
    repo = Path(repo_path).resolve()

    toc_path = Path(toc_file)
    if not toc_path.is_absolute():
        toc_path = repo / toc_file

    doc_path = Path(doc_dir)
    if not doc_path.is_absolute():
        doc_path = repo / doc_dir

    # Load TOC
    toc = load_toc(str(toc_path))
    toc_pages = collect_toc_pages(toc)
    toc_page_ids = set(toc_pages.keys())

    # Scan existing docs
    existing_docs = scan_existing_docs(str(doc_path))
    existing_page_ids = set(existing_docs.keys())

    # Compare pages
    new_page_ids = toc_page_ids - existing_page_ids
    common_page_ids = toc_page_ids & existing_page_ids

    # Build new_pages list
    new_pages = [toc_pages[page_id] for page_id in new_page_ids]

    # Compare sections for common pages
    pages_to_update = {}
    unchanged_pages = []

    for page_id in common_page_ids:
        toc_page = toc_pages[page_id]
        doc_info = existing_docs[page_id]

        toc_section_ids = set(toc_page["section_ids"])
        existing_section_ids = set(doc_info["autogen_sections"])
        empty_section_ids = set(doc_info.get("empty_sections", []))

        # Sections missing or empty
        missing_section_ids = toc_section_ids - existing_section_ids
        empty_existing = toc_section_ids & empty_section_ids
        new_section_ids = missing_section_ids | empty_existing

        deleted_section_ids = existing_section_ids - toc_section_ids
        existing_with_content = (toc_section_ids & existing_section_ids) - empty_section_ids

        if new_section_ids or deleted_section_ids:
            new_sections = [
                s for s in toc_page["sections"]
                if s["section_id"] in new_section_ids
            ]

            pages_to_update[page_id] = {
                "page_id": page_id,
                "file_path": doc_info["file_path"],
                "filename": doc_info["filename"],
                "new_sections": new_sections,
                "deleted_sections": list(deleted_section_ids),
                "existing_sections": list(existing_with_content),
            }
        else:
            unchanged_pages.append(page_id)

    # Statistics
    total_new_sections = sum(len(p["new_sections"]) for p in pages_to_update.values())
    total_deleted_sections = sum(len(p["deleted_sections"]) for p in pages_to_update.values())
    total_empty_sections = sum(len(d.get("empty_sections", [])) for d in existing_docs.values())

    return {
        "new_pages": new_pages,
        "pages_to_update": pages_to_update,
        "unchanged_pages": unchanged_pages,
        "toc_project": toc.get("project", {}),
        "metadata": {
            "toc_file": str(toc_path),
            "doc_dir": str(doc_path),
            "total_toc_pages": len(toc_page_ids),
            "total_existing_docs": len(existing_page_ids),
            "total_new_pages": len(new_pages),
            "total_pages_to_update": len(pages_to_update),
            "total_unchanged_pages": len(unchanged_pages),
            "total_new_sections": total_new_sections,
            "total_deleted_sections": total_deleted_sections,
            "total_empty_sections_detected": total_empty_sections,
        }
    }


def main():
    parser = argparse.ArgumentParser(
        description="Collect TOC sync context for incremental updates"
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
        "--output",
        help="Output file path (default: stdout)"
    )

    args = parser.parse_args()

    try:
        result = collect_sync_context(
            repo_path=args.repo_path,
            toc_file=args.toc_file,
            doc_dir=args.doc_dir
        )

        output = json.dumps(result, ensure_ascii=False, indent=2)

        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(output, encoding='utf-8')
            print(f"Sync context saved to: {args.output}", file=sys.stderr)
        else:
            print(output)

        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
