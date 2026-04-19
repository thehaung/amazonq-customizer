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
        if md_file.name.upper() == "SKILL.MD":
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