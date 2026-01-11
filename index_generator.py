#!/usr/bin/env python3
"""
Index Generator - A utility tool to generate index.md for easy navigation.

This script scans the current directory and subdirectories for Python scripts
and other files, then creates an index.md file with organized navigation links.
"""

import os
import sys
from pathlib import Path
from datetime import datetime


def should_ignore(path, ignore_patterns=None):
    """
    Check if a path should be ignored based on common patterns.
    
    Args:
        path: Path to check
        ignore_patterns: Additional patterns to ignore
    
    Returns:
        bool: True if path should be ignored
    """
    if ignore_patterns is None:
        ignore_patterns = []
    
    default_ignores = [
        '.git', '__pycache__', '.pytest_cache', 'venv', 'env',
        '.vscode', '.idea', 'node_modules', '.DS_Store', 'index.md'
    ]
    
    all_ignores = default_ignores + ignore_patterns
    
    # Check if any part of the path matches ignore patterns
    parts = Path(path).parts
    for part in parts:
        if part in all_ignores or part.startswith('.'):
            return True
    
    return False


def scan_directory(root_dir='.'):
    """
    Scan directory and subdirectories for files.
    
    Args:
        root_dir: Root directory to scan (default: current directory)
    
    Returns:
        dict: Dictionary with categorized files
    """
    root_path = Path(root_dir).resolve()
    
    files_by_type = {
        'python_scripts': [],
        'markdown_files': [],
        'other_files': []
    }
    
    for item in root_path.rglob('*'):
        if item.is_file():
            rel_path = item.relative_to(root_path)
            
            # Skip ignored files
            if should_ignore(rel_path):
                continue
            
            # Categorize files
            if item.suffix == '.py':
                files_by_type['python_scripts'].append(rel_path)
            elif item.suffix == '.md':
                files_by_type['markdown_files'].append(rel_path)
            else:
                # Only include configuration and text files
                if item.suffix in ['.txt', '.json', '.yaml', '.yml', '.toml', '.cfg', '.ini']:
                    files_by_type['other_files'].append(rel_path)
    
    # Sort all lists
    for key in files_by_type:
        files_by_type[key].sort()
    
    return files_by_type


def get_file_description(file_path):
    """
    Try to extract description from file (first line of docstring for Python files).
    
    Args:
        file_path: Path to the file
    
    Returns:
        str: Description or empty string
    """
    try:
        if file_path.suffix == '.py':
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                in_docstring = False
                for line in lines:
                    stripped = line.strip()
                    if '"""' in stripped or "'''" in stripped:
                        if not in_docstring:
                            in_docstring = True
                            # Check if docstring is on same line
                            content = stripped.strip('"""').strip("'''").strip()
                            if content:
                                return content
                        else:
                            # End of docstring
                            break
                    elif in_docstring:
                        if stripped:
                            return stripped
    except Exception:
        pass
    
    return ""


def generate_index(root_dir='.', output_file='index.md'):
    """
    Generate index.md file with navigation links.
    
    Args:
        root_dir: Root directory to scan
        output_file: Output file name
    """
    root_path = Path(root_dir).resolve()
    output_path = root_path / output_file
    
    print(f"Scanning directory: {root_path}")
    files_by_type = scan_directory(root_dir)
    
    # Generate markdown content
    content = []
    content.append("# Utility Tools Index")
    content.append("")
    content.append(f"*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    content.append("")
    content.append("This index provides easy navigation to all utility tools in this repository.")
    content.append("")
    
    # Python Scripts section
    if files_by_type['python_scripts']:
        content.append("## Python Scripts")
        content.append("")
        for script in files_by_type['python_scripts']:
            description = get_file_description(root_path / script)
            if description:
                content.append(f"- [{script}]({script}) - {description}")
            else:
                content.append(f"- [{script}]({script})")
        content.append("")
    
    # Markdown Files section
    if files_by_type['markdown_files']:
        content.append("## Documentation")
        content.append("")
        for md_file in files_by_type['markdown_files']:
            content.append(f"- [{md_file}]({md_file})")
        content.append("")
    
    # Other Files section
    if files_by_type['other_files']:
        content.append("## Configuration Files")
        content.append("")
        for other_file in files_by_type['other_files']:
            content.append(f"- [{other_file}]({other_file})")
        content.append("")
    
    # Usage section
    content.append("---")
    content.append("")
    content.append("## How to Use")
    content.append("")
    content.append("Each tool in this repository is designed to be self-contained and easy to use.")
    content.append("Check individual tool documentation for specific usage instructions.")
    content.append("")
    content.append("### Regenerating This Index")
    content.append("")
    content.append("To regenerate this index after adding new tools:")
    content.append("")
    content.append("```bash")
    content.append("python index_generator.py")
    content.append("```")
    content.append("")
    
    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content))
    
    print(f"✓ Index generated successfully: {output_path}")
    print(f"  - {len(files_by_type['python_scripts'])} Python scripts")
    print(f"  - {len(files_by_type['markdown_files'])} Markdown files")
    print(f"  - {len(files_by_type['other_files'])} Configuration files")


def main():
    """Main entry point for the script."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Generate an index.md file for easy navigation of utility tools.'
    )
    parser.add_argument(
        '-d', '--directory',
        default='.',
        help='Directory to scan (default: current directory)'
    )
    parser.add_argument(
        '-o', '--output',
        default='index.md',
        help='Output file name (default: index.md)'
    )
    
    args = parser.parse_args()
    
    try:
        generate_index(args.directory, args.output)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
