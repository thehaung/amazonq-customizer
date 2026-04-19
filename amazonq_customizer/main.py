import typer
from typing import Optional
from pathlib import Path
from amazonq_customizer.init_cmd import initialize_directories
from amazonq_customizer.convert_cmd import convert_skills

app = typer.Typer()

@app.command()
def init(
    root: Optional[Path] = typer.Option(Path("."), "--root", help="Target root directory"),
    is_global: bool = typer.Option(False, "--global", help="Initialize in ~/.aws/amazonq")
):
    """Initialize Amazon Q directories."""
    initialize_directories(root, is_global)

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