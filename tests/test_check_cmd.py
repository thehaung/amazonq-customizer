from pathlib import Path
from amazonq_customizer.check_cmd import check_customizations

def test_check_customizations_local(tmp_path, capsys):
    target_dir = tmp_path / "myproject"
    rules_dir = target_dir / ".amazonq" / "rules"
    rules_dir.mkdir(parents=True)
    (rules_dir / "my_rule.md").write_text("Content")
    
    check_customizations(root_dir=target_dir, is_global=False)
    captured = capsys.readouterr()
    assert "Project Rules Directory:" in captured.out
    assert "my_rule.md" in captured.out

def test_check_customizations_global(tmp_path, monkeypatch, capsys):
    home_dir = tmp_path / "home"
    home_dir.mkdir()
    monkeypatch.setattr(Path, "home", lambda: home_dir)
    
    prompts_dir = home_dir / ".aws" / "amazonq" / "prompts"
    prompts_dir.mkdir(parents=True)
    (prompts_dir / "my_prompt.md").write_text("Content")
    
    check_customizations(root_dir=None, is_global=True)
    captured = capsys.readouterr()
    assert "Global Prompts Directory:" in captured.out
    assert "my_prompt.md" in captured.out

def test_check_customizations_empty_local(tmp_path, capsys):
    check_customizations(root_dir=tmp_path, is_global=False)
    captured = capsys.readouterr()
    assert "No local project rules or prompts found." in captured.out
