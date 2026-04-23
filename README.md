# Amazon Q Customizer

A CLI tool to manage and deploy Amazon Q customizations (skills, rules, and prompts).

## Overview

Amazon Q Customizer bridges the gap between agent skill definitions and Amazon Q Developer. It converts structured skill files into Amazon Q-compatible prompt formats and manages their deployment through symlinks.

The tool supports two modes of operation:

- **Local mode**: Creates project-specific directories (`.amazonq/rules`) for per-project rules
- **Global mode**: Manages system-wide Amazon Q configuration in `~/.aws/amazonq/`, symlinking prompts for use across all projects

## Architecture

The tool uses a three-layer architecture:

```
┌─────────────────────────────────────────────────────────────────┐
│                    DEPLOYMENT LAYER                              │
│  (Symlinks created by amazonq-customizer init --global)         │
│                                                                  │
│   ~/.aws/amazonq/prompts/  <-- symlinks -->  prompts/*.md       │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │ compiles from
┌─────────────────────────────────────────────────────────────────┐
│                     COMPILED LAYER                              │
│         (Tracked in git, Amazon Q prompt format)                │
│                                                                  │
│   prompts/java:clean-code.md           (YAML frontmatter)       │
│   prompts/java:solid-principles.md     name: clean-code         │
│   prompts/superpowers:brainstorming.md description: ...         │
│   ...                                                           │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │ sourced from external repos
┌─────────────────────────────────────────────────────────────────┐
│                      SOURCE LAYER                               │
│              (Gitignored, external skill definitions)           │
│                                                                  │
│   sources/claude-code-java/skills/...                           │
│   sources/obra/superpowers/skills/...                           │
└─────────────────────────────────────────────────────────────────┘
```

**Key flows:**

1. **Source to Compiled**: Raw skill definitions from external repositories are converted to Amazon Q prompt format with YAML frontmatter
2. **Compiled to Deployment**: `init --global` creates symlinks from `prompts/*.md` to `~/.aws/amazonq/prompts/`
3. **Local only**: `init` (without `--global`) only creates `.amazonq/rules` for project-level rules

## Installation

This project requires Python 3.9 or higher.

```bash
# Install dependencies
pip install -r requirements.txt

# Install the CLI package in editable mode
pip install -e .
```

This exposes the `amazonq-customizer` command globally in your Python environment.

## Usage

The CLI provides two primary commands: `init` and `check`.

### `init` Command

Initializes Amazon Q directories. Behavior differs between local and global modes.

**Local initialization (default):**

Creates the `.amazonq/rules` directory in your project root for project-specific rules. Note: Local mode intentionally does NOT create or symlink the prompts directory. Prompts are designed to be global and shared across projects.

```bash
# Initialize in current directory
amazonq-customizer init

# Initialize in specific directory
amazonq-customizer init --root /path/to/project
```

**Global initialization (`--global`):**

Creates `~/.aws/amazonq/prompts/` and symlinks all markdown files from the project's `prompts/` directory. This makes prompts available system-wide to Amazon Q Developer.

```bash
amazonq-customizer init --global
```

After running `init --global`, Amazon Q Developer will have access to all prompts in its prompt selector.

### `check` Command

Lists existing Amazon Q customizations to verify your setup.

**Local check (default):**

Scans the current project for `.amazonq/rules` and `.amazonq/prompts` directories, listing all active files.

```bash
amazonq-customizer check
```

**Global check (`--global`):**

Scans `~/.aws/amazonq/` for globally configured rules and prompts.

```bash
amazonq-customizer check --global
```

## Prompt System

Prompts are the core customization mechanism for Amazon Q Developer.

### Naming Convention

Prompt files follow the pattern `domain:name.md`:

- `java:clean-code.md` — Java-specific clean code guidelines
- `superpowers:brainstorming.md` — Brainstorming skill from obra/superpowers
- `java:test-quality.md` — Java testing best practices

The domain prefix helps organize prompts by category and source.

### Frontmatter Format

Every prompt file includes YAML frontmatter with two required fields:

```yaml
---
name: clean-code
description: Clean Code principles (DRY, KISS, YAGNI), naming conventions, function design, and refactoring. Use when user says "clean this code", "refactor", "improve readability", or when reviewing code quality.
---
```

- `name`: Short identifier for the prompt (used by Amazon Q)
- `description`: Explains when to use this prompt (shown in Amazon Q's prompt selector)

### Where Prompts Live

- **Source files**: External repositories cloned into `sources/` (gitignored)
- **Compiled prompts**: Markdown files in `prompts/` (tracked in git)
- **Deployed prompts**: Symlinks in `~/.aws/amazonq/prompts/` (created by `init --global`)

### Available Prompts

See the `prompts/` directory for the complete list of available prompts. The collection includes:

- Java skills (clean code, SOLID principles, design patterns, security audits, etc.)
- Superpowers skills (brainstorming, TDD, debugging, code review workflows, etc.)

## Project Structure

```
amazonq-customizer/
├── src/amazonq_customizer/     # Core CLI logic
│   ├── __init__.py
│   ├── main.py                 # CLI entry point (Typer app)
│   ├── init_cmd.py             # init command implementation
│   └── check_cmd.py            # check command implementation
├── prompts/                    # Compiled prompt files (tracked in git)
│   ├── java:*.md               # Java-specific prompts
│   └── superpowers:*.md        # Superpowers workflow prompts
├── tests/                      # Test suite
│   ├── test_main.py
│   ├── test_init_cmd.py
│   └── test_check_cmd.py
├── sources/                    # Raw skill definitions (gitignored)
│   ├── claude-code-java/       # Java skills source
│   └── obra/superpowers/       # Superpowers skills source
├── rules/                      # Placeholder for project-level Amazon Q rules
├── .agent/                     # Tool-managed agent skills (gitignored)
├── .gemini/                    # Tool-managed Gemini commands (gitignored)
├── pyproject.toml              # Package metadata and dependencies
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Development and Testing

This project requires Python 3.9 or higher.

To run the test suite:

```bash
PYTHONPATH=src pytest tests/
```

This runs all tests in the `tests/` directory using the source code from `src/`.

## Contributing

Contributions are welcome. To add new prompts:

1. Add the source skill definition to the appropriate `sources/` subdirectory
2. Compile it to the `prompts/` directory following the frontmatter format
3. Run the test suite to ensure nothing breaks
4. Submit a pull request

There is no formal contribution process yet. For major changes, open an issue first to discuss what you would like to change.
