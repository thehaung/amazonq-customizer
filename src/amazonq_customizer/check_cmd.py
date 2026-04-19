from pathlib import Path
import typer

def check_customizations(root_dir: Path, is_global: bool):
    found_any = False

    if is_global:
        base_dir = Path.home() / ".aws" / "amazonq"
        rules_dir = base_dir / "rules"
        prompts_dir = base_dir / "prompts"
    else:
        base_dir = root_dir.absolute()
        rules_dir = base_dir / ".amazonq" / "rules"
        prompts_dir = base_dir / ".amazonq" / "prompts"

    if prompts_dir and prompts_dir.exists():
        prompts = list(prompts_dir.glob("*.md"))
        if prompts:
            label = "Global" if is_global else "Project"
            typer.echo(f"{label} Prompts Directory: {prompts_dir}")
            for md_file in prompts:
                typer.echo(f"  - {md_file.name}")
            found_any = True

    if rules_dir and rules_dir.exists():
        rules = list(rules_dir.glob("*.md"))
        if rules:
            label = "Global" if is_global else "Project"
            typer.echo(f"{label} Rules Directory: {rules_dir}")
            for md_file in rules:
                typer.echo(f"  - {md_file.name}")
            found_any = True
            
    if not found_any:
        scope = "global" if is_global else "local project"
        typer.echo(f"No {scope} rules or prompts found.")