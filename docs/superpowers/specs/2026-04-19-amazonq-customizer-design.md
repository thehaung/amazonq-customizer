# Amazon Q Customizer CLI Design Spec

## Overview
The `amazonq-customizer` is a Python-based Command Line Interface (CLI) application designed to automate the setup and conversion of AI assistant "skills" (such as those from Claude Code and Superpowers) into a format compatible with the Amazon Q IDE extension. Specifically, it converts these skills into Amazon Q "Prompts".

## Architecture
- **Language:** Python 3
- **CLI Framework:** Typer
- **Package Management:** `pip` with `setup.py` / `requirements.txt` to allow global installation.
- **File System:** Standard library `pathlib` for cross-platform compatibility.

## Core Commands

### `amazonq-customizer init`
Initializes the necessary directory structure for Amazon Q customizations.
- **Behavior:** Creates the `prompts/` and `rules/` directories.
- **Options:**
  - `--root` (String): The target root directory. Defaults to the current working directory (`.`).
  - `--global` (Flag): If set, initializes the structure in `~/.aws/amazonq` instead of the local directory.

### `amazonq-customizer convert`
Converts external skills (markdown files) into Amazon Q Prompts.
- **Behavior:**
  1. Reads markdown files from a provided source directory (e.g., `/Users/thehaung/Developer/AI`).
  2. Parses the skill content.
  3. Injects a specific instruction header that forces Amazon Q to announce the activated prompt and list its steps before execution.
  4. Writes the resulting `.md` files into the appropriate `prompts/` directory.
- **Options:**
  - `--source` (String, Required): Path to the directory containing the source skills.
  - `--global` (Flag): If set, writes the converted prompts to `~/.aws/amazonq/prompts/` instead of the local `./prompts/` directory.

## Skill Conversion Logic
To satisfy the requirement that Amazon Q must print out the selected prompts and skills during execution, the CLI will inject a header block at the top of every converted skill file.

**Header Template:**
```markdown
# INSTRUCTIONS FOR AMAZON Q
When the user invokes this prompt, you MUST immediately print the following before taking any action or answering any questions:
"ACTIVATED PROMPT: [Skill Name]" 
"Executing the following steps:" 
(Briefly list the core steps or rules you are about to follow based on the instructions below.)

---
[Original Skill Content]
```

## Project Structure
```
amazonq-customizer/
├── amazonq_customizer/
│   ├── __init__.py
│   ├── main.py          # Typer app definition and CLI entry points
│   ├── init_cmd.py      # Logic for the 'init' command
│   ├── convert_cmd.py   # Logic for the 'convert' command
│   └── templates.py     # String templates for Amazon Q prompt headers
├── requirements.txt
└── setup.py             # Packaging configuration
```

## Future Scope
- **Rules Generation:** Currently, all skills are mapped to Prompts. Future iterations will include mapping specific constraints to Project Rules (`.amazonq/rules/`).