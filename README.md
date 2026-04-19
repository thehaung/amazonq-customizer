# Amazon Q Customizer

A Command Line Interface (CLI) tool designed to manage and streamline Amazon Q customizations, specifically focusing on agent skills, rules, and prompts.

This tool helps you convert your agent skills into Amazon Q prompt formats and symlink them directly into your Amazon Q Developer configuration folders, both locally per-project and globally across your system.

## Project Structure

- `src/amazonq_customizer/`: Contains the core CLI application logic.
- `prompts/`: Stores the generated Markdown files that serve as Amazon Q prompts. These are prefixed by their source domain (e.g., `java:clean-code.md`, `superpowers:brainstorming.md`).
- `sources/`: The raw agent skill definitions (e.g., `claude-code-java` and `obra/superpowers`) which are compiled into the `prompts/` directory.

## Installation

This project is built using standard Python packaging (`pyproject.toml` and `setuptools`). You can install it using `pip`.

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Install the CLI Package
Install the package in editable mode for development:
```bash
pip install -e .
```

This will expose the `amazonq-customizer` command globally in your Python environment.

## Usage

The CLI provides two primary commands: `init` and `check`.

### `init` Command

Initializes the required Amazon Q directories and symlinks the customized prompts.

- **Local Initialization (Default):**
  Creates the `.amazonq/rules` directory in your current project root.
  *(Note: Local initialization purposely skips creating or symlinking the `prompts` directory, keeping prompts centralized or global).*
  ```bash
  amazonq-customizer init
  ```
  You can also specify a specific root directory:
  ```bash
  amazonq-customizer init --root /path/to/project
  ```

- **Global Initialization (`--global`):**
  Creates the `~/.aws/amazonq/prompts` directory and automatically symlinks all the `.md` prompt files from this project's `prompts/` folder into your global Amazon Q configuration.
  ```bash
  amazonq-customizer init --global
  ```

### `check` Command

Checks and lists existing Amazon Q customizations (rules and prompts) to verify your setup.

- **Local Check (Default):**
  Looks for `.amazonq/rules` and `.amazonq/prompts` in your current directory and lists the active files.
  ```bash
  amazonq-customizer check
  ```

- **Global Check (`--global`):**
  Looks in your global `~/.aws/amazonq/` directory and lists the globally active rules and prompts.
  ```bash
  amazonq-customizer check --global
  ```

## Development & Testing

To run the test suite, ensure you have installed the development dependencies (`pytest`) and run:

```bash
PYTHONPATH=src pytest tests/
```
