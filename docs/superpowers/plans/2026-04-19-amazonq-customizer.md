# Amazon Q Customizer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Python CLI (`amazonq-customizer`) using Typer that initializes Amazon Q directories and converts external AI skills into Amazon Q Prompts.

**Architecture:** A modular Python Typer application with separate files for command logic (`init` and `convert`), utilizing `pathlib` for file operations and standard `pytest` for testing. 

**Tech Stack:** Python 3, `typer`, `pytest`

---

### Task 1: Project Setup and Skeleton

**Files:**
- Create: `requirements.txt`
- Create: `setup.py`
- Create: `amazonq_customizer/__init__.py`
- Create: `amazonq_customizer/main.py`
- Create: `tests/__init__.py`
- Create: `tests/test_main.py`

- [ ] **Step 1: Create `requirements.txt` and `setup.py`**
```text
# requirements.txt
typer>=0.9.0
pytest>=7.0.0
```
```python
# setup.py
from setuptools import setup, find_packages

setup(
    name="amazonq-customizer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "typer>=0.9.0",
    ],
    entry_points={
        "console_scripts": [
            "amazonq-customizer=amazonq_customizer.main:app",
        ],
    },
)
```

- [ ] **Step 2: Write failing test for main app**
```python
# tests/test_main.py
from typer.testing import CliRunner
from amazonq_customizer.main import app

runner = CliRunner()

def test_app_exists():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "init" in result.stdout
```

- [ ] **Step 3: Run test to verify it fails**
Run: `python -m pytest tests/test_main.py -v`
Expected: FAIL (app not defined)

- [ ] **Step 4: Write minimal implementation**
```python
# amazonq_customizer/__init__.py
# Empty file
```
```python
# amazonq_customizer/main.py
import typer

app = typer.Typer()

@app.command()
def init():
    """Initialize Amazon Q directories."""
    pass

@app.command()
def convert():
    """Convert skills to Amazon Q Prompts."""
    pass

if __name__ == "__main__":
    app()
```

- [ ] **Step 5: Run test to verify it passes**
Run: `python -m pytest tests/test_main.py -v`
Expected: PASS

- [ ] **Step 6: Commit**
```bash
git add requirements.txt setup.py amazonq_customizer/ tests/
git commit -m "chore: setup project structure and main CLI skeleton"
```

---

### Task 2: Implement `init` Command

**Files:**
- Create: `amazonq_customizer/init_cmd.py`
- Create: `tests/test_init_cmd.py`
- Modify: `amazonq_customizer/main.py`

- [ ] **Step 1: Write the failing test**
```python
# tests/test_init_cmd.py
from pathlib import Path
from amazonq_customizer.init_cmd import initialize_directories

def test_initialize_directories_local(tmp_path):
    target_dir = tmp_path / "myproject"
    target_dir.mkdir()
    
    initialize_directories(root_dir=target_dir, is_global=False)
    
    assert (target_dir / ".amazonq" / "rules").exists()
    assert (target_dir / "prompts").exists()

def test_initialize_directories_global(tmp_path, monkeypatch):
    home_dir = tmp_path / "home"
    home_dir.mkdir()
    monkeypatch.setattr(Path, "home", lambda: home_dir)
    
    initialize_directories(root_dir=None, is_global=True)
    
    assert (home_dir / ".aws" / "amazonq" / "prompts").exists()
```

- [ ] **Step 2: Run test to verify it fails**
Run: `python -m pytest tests/test_init_cmd.py -v`
Expected: FAIL (ModuleNotFoundError)

- [ ] **Step 3: Write minimal implementation**
```python
# amazonq_customizer/init_cmd.py
from pathlib import Path
import typer

def initialize_directories(root_dir: Path, is_global: bool):
    if is_global:
        base_dir = Path.home() / ".aws" / "amazonq"
        rules_dir = None # Rules are project specific usually, but prompts go here
        prompts_dir = base_dir / "prompts"
    else:
        base_dir = root_dir.absolute()
        rules_dir = base_dir / ".amazonq" / "rules"
        prompts_dir = base_dir / "prompts"
    
    if prompts_dir:
        prompts_dir.mkdir(parents=True, exist_ok=True)
        typer.echo(f"Created prompts directory at: {prompts_dir}")
        
    if rules_dir:
        rules_dir.mkdir(parents=True, exist_ok=True)
        typer.echo(f"Created rules directory at: {rules_dir}")
```
Update `amazonq_customizer/main.py` to use it:
```python
# amazonq_customizer/main.py (update init command)
import typer
from typing import Optional
from pathlib import Path
from amazonq_customizer.init_cmd import initialize_directories

app = typer.Typer()

@app.command()
def init(
    root: Optional[Path] = typer.Option(Path("."), "--root", help="Target root directory"),
    is_global: bool = typer.Option(False, "--global", help="Initialize in ~/.aws/amazonq")
):
    """Initialize Amazon Q directories."""
    initialize_directories(root, is_global)

@app.command()
def convert():
    """Convert skills to Amazon Q Prompts."""
    pass

if __name__ == "__main__":
    app()
```

- [ ] **Step 4: Run test to verify it passes**
Run: `python -m pytest tests/test_init_cmd.py -v`
Expected: PASS

- [ ] **Step 5: Commit**
```bash
git add amazonq_customizer/ tests/
git commit -m "feat: implement init command logic"
```

---

### Task 3: Implement Templates and Skill Parsing

**Files:**
- Create: `amazonq_customizer/templates.py`
- Create: `tests/test_templates.py`

- [ ] **Step 1: Write failing test**
```python
# tests/test_templates.py
from amazonq_customizer.templates import inject_header

def test_inject_header():
    skill_name = "brainstorming"
    original_content = "# Brainstorming\nContent here."
    result = inject_header(skill_name, original_content)
    
    assert "# INSTRUCTIONS FOR AMAZON Q" in result
    assert "ACTIVATED PROMPT: brainstorming" in result
    assert original_content in result
```

- [ ] **Step 2: Run test to verify it fails**
Run: `python -m pytest tests/test_templates.py -v`
Expected: FAIL

- [ ] **Step 3: Write minimal implementation**
```python
# amazonq_customizer/templates.py

AMAZON_Q_HEADER_TEMPLATE = """# INSTRUCTIONS FOR AMAZON Q
When the user invokes this prompt, you MUST immediately print the following before taking any action or answering any questions:
"ACTIVATED PROMPT: {skill_name}" 
"Executing the following steps:" 
(Briefly list the core steps or rules you are about to follow based on the instructions below.)

---
{original_content}"""

def inject_header(skill_name: str, original_content: str) -> str:
    return AMAZON_Q_HEADER_TEMPLATE.format(
        skill_name=skill_name,
        original_content=original_content
    )
```

- [ ] **Step 4: Run test to verify it passes**
Run: `python -m pytest tests/test_templates.py -v`
Expected: PASS

- [ ] **Step 5: Commit**
```bash
git add amazonq_customizer/templates.py tests/test_templates.py
git commit -m "feat: add amazon q header templates"
```

---

### Task 4: Implement `convert` Command

**Files:**
- Create: `amazonq_customizer/convert_cmd.py`
- Create: `tests/test_convert_cmd.py`
- Modify: `amazonq_customizer/main.py`

- [ ] **Step 1: Write failing test**
```python
# tests/test_convert_cmd.py
from pathlib import Path
from amazonq_customizer.convert_cmd import convert_skills

def test_convert_skills(tmp_path):
    source_dir = tmp_path / "skills"
    source_dir.mkdir()
    
    # Create a mock skill
    skill_dir = source_dir / "my-skill"
    skill_dir.mkdir()
    skill_file = skill_dir / "SKILL.md"
    skill_file.write_text("# My Skill\nDoes things.")
    
    # Target directory
    target_prompts_dir = tmp_path / "prompts"
    target_prompts_dir.mkdir()
    
    convert_skills(source_dir=source_dir, prompts_dir=target_prompts_dir)
    
    output_file = target_prompts_dir / "my-skill.md"
    assert output_file.exists()
    content = output_file.read_text()
    assert "ACTIVATED PROMPT: my-skill" in content
    assert "# My Skill\nDoes things." in content
```

- [ ] **Step 2: Run test to verify it fails**
Run: `python -m pytest tests/test_convert_cmd.py -v`
Expected: FAIL

- [ ] **Step 3: Write minimal implementation**
```python
# amazonq_customizer/convert_cmd.py
from pathlib import Path
import typer
from amazonq_customizer.templates import inject_header

def convert_skills(source_dir: Path, prompts_dir: Path):
    if not source_dir.exists() or not source_dir.is_dir():
        typer.echo(f"Error: Source directory {source_dir} does not exist.", err=True)
        raise typer.Exit(code=1)
        
    if not prompts_dir.exists():
        prompts_dir.mkdir(parents=True, exist_ok=True)
        
    count = 0
    # Assuming skills are in subdirectories like `skill-name/SKILL.md` or just `.md` files
    for md_file in source_dir.rglob("*.md"):
        # Determine skill name
        if md_file.name.upper() == "SKILL.md":
            skill_name = md_file.parent.name
        else:
            skill_name = md_file.stem
            
        original_content = md_file.read_text(encoding="utf-8")
        converted_content = inject_header(skill_name, original_content)
        
        output_file = prompts_dir / f"{skill_name}.md"
        output_file.write_text(converted_content, encoding="utf-8")
        typer.echo(f"Converted {skill_name} -> {output_file}")
        count += 1
        
    typer.echo(f"Successfully converted {count} skills.")
```
Update `amazonq_customizer/main.py` to use it:
```python
# amazonq_customizer/main.py (update convert command)
# ... [keep existing imports] ...
from amazonq_customizer.convert_cmd import convert_skills

# ... [keep existing init command] ...

@app.command()
def convert(
    source: Path = typer.Option(..., "--source", help="Source directory containing skills"),
    is_global: bool = typer.Option(False, "--global", help="Write to ~/.aws/amazonq/prompts/")
):
    """Convert skills to Amazon Q Prompts."""
    if is_global:
        prompts_dir = Path.home() / ".aws" / "amazonq" / "prompts"
    else:
        prompts_dir = Path.cwd() / "prompts"
        
    convert_skills(source, prompts_dir)

if __name__ == "__main__":
    app()
```

- [ ] **Step 4: Run test to verify it passes**
Run: `python -m pytest tests/test_convert_cmd.py -v`
Expected: PASS

- [ ] **Step 5: Commit**
```bash
git add amazonq_customizer/ tests/
git commit -m "feat: implement convert command to generate Q prompts"
```
