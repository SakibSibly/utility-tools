#!/usr/bin/env python3
"""
Obsidian Index Generator

This script scans the current directory and all subdirectories for markdown (.md) files
and creates a comprehensive index.md file for easy navigation in Obsidian.

Usage:
    python create_obsidian_index.py [directory]
    
If no directory is specified, it uses the current directory.
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict


def scan_markdown_files(root_dir):
    """
    Scan the directory tree for markdown files.
    
    Args:
        root_dir: Root directory to start scanning from
        
    Returns:
        Dictionary with directory paths as keys and lists of markdown files as values
    """
    md_files = defaultdict(list)
    root_path = Path(root_dir).resolve()
    
    for md_file in root_path.rglob("*.md"):
        # Skip the index.md file itself
        if md_file.name.lower() == "index.md":
            continue
            
        # Get relative path from root
        try:
            rel_path = md_file.relative_to(root_path)
            parent_dir = str(rel_path.parent) if str(rel_path.parent) != "." else "Root"
            md_files[parent_dir].append(md_file)
        except ValueError:
            # Skip files outside root directory
            continue
    
    return md_files


def create_obsidian_link(file_path, root_path):
    """
    Create an Obsidian-compatible link for a markdown file.
    
    Args:
        file_path: Path object of the markdown file
        root_path: Root directory path
        
    Returns:
        String with Obsidian link format
    """
    # Get relative path from root
    rel_path = file_path.relative_to(root_path)
    
    # File name without extension for display
    display_name = file_path.stem
    
    # Create Obsidian wiki-link format: [[file_path|display_name]]
    # For better compatibility, use the relative path without extension
    link_path = str(rel_path.with_suffix(''))
    
    return f"[[{link_path}|{display_name}]]"


def generate_index_content(md_files, root_path):
    """
    Generate the content for the index.md file.
    
    Args:
        md_files: Dictionary of directories and their markdown files
        root_path: Root directory path
        
    Returns:
        String with the complete index content
    """
    content = []
    
    # Header
    content.append("# Obsidian Notes Index")
    content.append("")
    content.append(f"*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    content.append("")
    
    # Statistics
    total_files = sum(len(files) for files in md_files.values())
    total_dirs = len(md_files)
    content.append("## Statistics")
    content.append("")
    content.append(f"- **Total Files**: {total_files}")
    content.append(f"- **Total Directories**: {total_dirs}")
    content.append("")
    
    # Table of Contents
    content.append("## Table of Contents")
    content.append("")
    
    # Sort directories (Root first, then alphabetically)
    sorted_dirs = sorted(md_files.keys(), key=lambda x: (x != "Root", x.lower()))
    
    for directory in sorted_dirs:
        files = md_files[directory]
        dir_display = "📁 Root Directory" if directory == "Root" else f"📁 {directory}"
        content.append(f"- [{dir_display}](#{directory.lower().replace(' ', '-').replace('/', '-').replace('.', '')})")
    
    content.append("")
    content.append("---")
    content.append("")
    
    # File listings by directory
    for directory in sorted_dirs:
        files = md_files[directory]
        
        # Directory header
        dir_display = "Root Directory" if directory == "Root" else directory
        content.append(f"## {dir_display}")
        content.append("")
        content.append(f"*{len(files)} file(s)*")
        content.append("")
        
        # Sort files alphabetically
        sorted_files = sorted(files, key=lambda x: x.name.lower())
        
        # List files
        for file_path in sorted_files:
            link = create_obsidian_link(file_path, root_path)
            content.append(f"- {link}")
        
        content.append("")
    
    # Footer
    content.append("---")
    content.append("")
    content.append("*This index was automatically generated. To regenerate, run `python create_obsidian_index.py`*")
    content.append("")
    
    return "\n".join(content)


def main():
    """Main function to generate the index."""
    # Determine root directory
    if len(sys.argv) > 1:
        root_dir = sys.argv[1]
    else:
        root_dir = os.getcwd()
    
    root_path = Path(root_dir).resolve()
    
    # Check if directory exists
    if not root_path.exists() or not root_path.is_dir():
        print(f"Error: Directory '{root_dir}' does not exist.")
        sys.exit(1)
    
    print(f"Scanning for markdown files in: {root_path}")
    
    # Scan for markdown files
    md_files = scan_markdown_files(root_path)
    
    if not md_files:
        print("No markdown files found (excluding index.md).")
        sys.exit(0)
    
    # Generate index content
    print(f"Found {sum(len(files) for files in md_files.values())} markdown file(s) in {len(md_files)} director(y/ies).")
    index_content = generate_index_content(md_files, root_path)
    
    # Write to index.md
    index_path = root_path / "index.md"
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_content)
    
    print(f"✓ Index created successfully: {index_path}")


if __name__ == "__main__":
    main()
