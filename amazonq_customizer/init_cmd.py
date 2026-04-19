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