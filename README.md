# utility-tools
Useful tools for day-to-day life hacks.

## Tools

### Obsidian Index Generator

A Python script that scans directories for markdown files and creates a comprehensive index.md file for easy navigation in Obsidian.

#### Features

- Scans current directory and all subdirectories for `.md` files
- Automatically excludes the generated `index.md` from the listing
- Organizes files by directory structure
- Generates statistics (total files and directories)
- Creates Obsidian-compatible wiki-links for easy navigation
- Provides a table of contents with directory anchors

#### Usage

**Run in a specific directory:**
```bash
python create_obsidian_index.py /path/to/your/obsidian/vault
```

**Run in the current directory:**
```bash
cd /path/to/your/obsidian/vault
python create_obsidian_index.py
```

#### Output

The script generates an `index.md` file with:
- Generation timestamp
- Statistics (total files and directories)
- Table of contents with clickable directory links
- Organized file listings by directory
- Obsidian wiki-links for each file

#### Example Output

```markdown
# Obsidian Notes Index

*Generated on: 2026-01-10 13:13:28*

## Statistics

- **Total Files**: 5
- **Total Directories**: 3

## Table of Contents

- [📁 Root Directory](#root)
- [📁 personal](#personal)
- [📁 programming](#programming)

---

## Root Directory

*1 file(s)*

- [[welcome|welcome]]

## personal

*2 file(s)*

- [[personal/daily-journal|daily-journal]]
- [[personal/goals|goals]]
```

#### Requirements

- Python 3.6 or higher
- No external dependencies (uses only standard library)
