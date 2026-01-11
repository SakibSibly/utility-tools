# utility-tools

Useful tools for day-to-day life hacks.

## Overview

This repository contains various day-to-day useful tools and utility scripts that make things go smoother and better. Each tool is designed to be self-contained and easy to use.

## Available Tools

### Index Generator

The `index_generator.py` script scans the current directory and subdirectories to create an organized `index.md` file for easy navigation.

**Features:**
- Automatically discovers Python scripts, documentation, and configuration files
- Extracts descriptions from Python docstrings
- Generates organized navigation with categories
- Ignores common directories (.git, __pycache__, venv, etc.)

**Usage:**

```bash
# Generate index in current directory
python index_generator.py

# Generate index for a specific directory
python index_generator.py -d /path/to/directory

# Specify custom output file
python index_generator.py -o custom_index.md
```

## Getting Started

1. Clone this repository
2. Run any tool directly with Python:
   ```bash
   python index_generator.py
   ```

## Contributing

Feel free to add more utility tools to this repository! Each tool should:
- Be self-contained and easy to use
- Include clear documentation
- Follow Python best practices
- Have descriptive docstrings

## License

This project is licensed under the CC0 1.0 Universal license - see the LICENSE file for details.
