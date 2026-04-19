from pathlib import Path
import typer
import os

def initialize_directories(root_dir: Path, is_global: bool):
    if is_global:
        base_dir = Path.home() / ".aws" / "amazonq"
        rules_dir = None # Rules are project specific usually, but prompts go here
        prompts_dir = base_dir / "prompts"
    else:
        base_dir = root_dir.absolute()
        rules_dir = base_dir / ".amazonq" / "rules"
        prompts_dir = None
    
    if prompts_dir:
        prompts_dir.mkdir(parents=True, exist_ok=True)
        typer.echo(f"Created prompts directory at: {prompts_dir}")
        
    if rules_dir:
        rules_dir.mkdir(parents=True, exist_ok=True)
        typer.echo(f"Created rules directory at: {rules_dir}")

    # Symlink prompt files from source to the initialized prompts directory
    source_prompts_dir = Path(__file__).parent.parent.parent / "prompts"
    if source_prompts_dir.exists() and prompts_dir:
        prompt_files = list(source_prompts_dir.glob("*.md"))
        for prompt_file in prompt_files:
            target_link = prompts_dir / prompt_file.name
            if target_link.exists() or target_link.is_symlink():
                target_link.unlink()
            target_link.symlink_to(prompt_file.absolute())
        typer.echo(f"Symlinked {len(prompt_files)} prompts to {prompts_dir}")