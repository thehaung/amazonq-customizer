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