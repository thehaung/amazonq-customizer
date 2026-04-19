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