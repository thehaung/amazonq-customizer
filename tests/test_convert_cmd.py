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