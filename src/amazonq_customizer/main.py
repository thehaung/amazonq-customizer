import typer
from typing import Optional
from pathlib import Path
from amazonq_customizer.init_cmd import initialize_directories
from amazonq_customizer.check_cmd import check_customizations

app = typer.Typer()

@app.command()
def init(
    root: Optional[Path] = typer.Option(Path("."), "--root", help="Target root directory"),
    is_global: bool = typer.Option(False, "--global", help="Initialize in ~/.aws/amazonq")
):
    """Initialize Amazon Q directories."""
    initialize_directories(root, is_global)

@app.command()
def check(
    root: Optional[Path] = typer.Option(Path("."), "--root", help="Target root directory"),
    is_global: bool = typer.Option(False, "--global", help="Check ~/.aws/amazonq/ rules and prompts")
):
    """Check existing Amazon Q customizations."""
    root_path = Path(".") if root is None else root
    check_customizations(root_path, is_global)

if __name__ == "__main__":
    app()